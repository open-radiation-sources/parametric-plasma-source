"""
Auto-generated file. To edit, run `python build_python.py`.
This will need to be run whenever a new C++ version is made available.
"""

source_sampling_cpp = (
"""#include <iostream>
#include "openmc/random_lcg.h"
#include "openmc/source.h"
#include "openmc/particle.h"
#include "plasma_source.hpp"


// Spherical tokamak SOURCE 
// units are in SI units
const double ion_density_pedistal = 1.09e+20; // ions per m^3
const double ion_density_seperatrix = 3e+19;
const double ion_density_origin = 1.09e+20;
const double ion_temperature_pedistal = 6.09;
const double ion_temperature_seperatrix = 0.1;
const double ion_temperature_origin = 45.9;
const double ion_density_peaking_factor = 1;
const double ion_temperature_peaking_factor = 8.06; // check alpha or beta value from paper
const double ion_temperature_beta = 6.0;
const double minor_radius = 1.56; // metres
const double major_radius = 2.5; // metres
const double pedistal_radius = 0.8 * minor_radius; // pedistal minor rad in metres
const double elongation = 2.0;
const double triangularity = 0.55;
const double shafranov_shift = 0.0; //metres
const std::string name = "parametric_plasma_source";
const int number_of_bins  = 100;
const int plasma_type = 1; // 1 is default; //0 = L mode anything else H/A mode


plasma_source::PlasmaSource source = plasma_source::PlasmaSource(ion_density_pedistal,
       ion_density_seperatrix,
       ion_density_origin,
       ion_temperature_pedistal,
       ion_temperature_seperatrix,
       ion_temperature_origin,
       pedistal_radius,
       ion_density_peaking_factor,
       ion_temperature_peaking_factor,
       ion_temperature_beta,
       minor_radius,
       major_radius,
       elongation,
       triangularity,
       shafranov_shift,
       name,
       plasma_type,
       number_of_bins,
       0.0,
       360.0);
  
// you must have external C linkage here otherwise 
// dlopen will not find the file
extern "C" openmc::Particle::Bank sample_source(uint64_t* seed) {
    openmc::Particle::Bank particle;
    // wgt
    particle.particle = openmc::Particle::Type::neutron;
    particle.wgt = 1.0;
    // position 

    std::array<double,8> randoms = {openmc::prn(seed),
                            openmc::prn(seed),
                            openmc::prn(seed),
                            openmc::prn(seed),
                            openmc::prn(seed),
                            openmc::prn(seed),
                            openmc::prn(seed),
                            openmc::prn(seed)};

    double u,v,w,E;
    source.SampleSource(randoms,particle.r.x,particle.r.y,particle.r.z,
                        u,v,w,E); 

    particle.r.x *= 100.;
    particle.r.y *= 100.;
    particle.r.z *= 100.;    
   
    // particle.E = 14.08e6;
    particle.E = E*1e6; // convert from MeV -> eV

    particle.u = {u,
                  v,
                  w};

    
    particle.delayed_group = 0;
    return particle;    
}


"""
)

plasma_source_cpp = (
"""#include <iostream>
#include <vector>
#include <cmath>
#include "plasma_source.hpp"
#include <stdlib.h>     
#include "openmc/random_lcg.h"

#define RANDOM openmc::prn()

namespace plasma_source {

// default constructor
PlasmaSource::PlasmaSource() {}

// large constructor
PlasmaSource::PlasmaSource(const double ion_density_ped, const double ion_density_sep,
	    const double ion_density_origin, const double ion_temp_ped,
	    const double ion_temp_sep, const double ion_temp_origin, 
	    const double pedistal_rad, const double ion_density_peak,
	    const double ion_temp_peak, const double ion_temp_beta,
      const double minor_radius, const double major_radius,
      const double elongation, const double triangularity,
      const double shafranov, const std::string plasma_type,
      const int plasma_id, const int number_of_bins,
      const double min_toroidal_angle,
      const double max_toroidal_angle ) {

  // set params
  ionDensityPedistal = ion_density_ped;
  ionDensitySeperatrix = ion_density_sep;
  ionDensityOrigin = ion_density_origin;
  ionTemperaturePedistal = ion_temp_ped;
  ionTemperatureSeperatrix = ion_temp_sep;
  ionTemperatureOrigin = ion_temp_origin;
  pedistalRadius = pedistal_rad;
  ionDensityPeaking = ion_density_peak;
  ionTemperaturePeaking = ion_temp_peak;
  ionTemperatureBeta = ion_temp_beta;
  minorRadius = minor_radius;
  majorRadius = major_radius;
  this->elongation = elongation;
  this->triangularity = triangularity;
  this->shafranov = shafranov;
  plasmaType = plasma_type;
  plasmaId = plasma_id;
  numberOfBins = number_of_bins;
  minToroidalAngle = min_toroidal_angle/180.*M_PI;
  maxToroidalAngle = max_toroidal_angle/180.*M_PI;

  setup_plasma_source();
}

// destructor
PlasmaSource::~PlasmaSource(){}

// main master sample function
void PlasmaSource::SampleSource(std::array<double,8> random_numbers,
                                double &x,
                                double &y,
                                double &z,
                                double &u,
                                double &v,
                                double &w,
                                double &E) {
  double radius = 0.;
  int bin = 0;
  sample_source_radial(random_numbers[0],random_numbers[1],radius,bin);
  double r = 0.;
  convert_rad_to_rz(radius,random_numbers[2],r,z);
  convert_r_to_xy(r,random_numbers[3],x,y);
  sample_energy(bin,random_numbers[4],random_numbers[5],E);
  isotropic_direction(random_numbers[6],random_numbers[7],
                      u,v,w);

}

/*
 * sample the pdf src_profile, to generate the sampled minor radius
 */
void PlasmaSource::sample_source_radial(double rn_store1, double rn_store2, 
                          double &sampled_radius, int &sampled_bin) {
  
  for ( int i = 0 ; i < numberOfBins ; i++ ) {
    if ( rn_store1 <= source_profile[i] ) {
      if ( i > 0 ) {
	      sampled_radius = (float(i-1)*(binWidth)) + (binWidth*(rn_store2));
	      sampled_bin = i;
	      return;
      } else {
	      sampled_radius = binWidth*(rn_store2);
	      sampled_bin = i;
	      return;
      }
    }
  }

  std::cerr << "error" << std::endl;
  std::cerr << "Sample position greater than plasma radius" << std::endl;
  exit(1);
  return;
}

/*
 * sample the energy of the neutrons, updates energy neutron in mev
 */
void PlasmaSource::sample_energy(const int bin_number, double random_number1, double random_number2,
		      double &energy_neutron) {
  // generate the normally distributed number
  const double twopi = 6.28318530718;
  double sample1 = std::sqrt(-2.0*std::log(random_number1));
  double sample2 = cos(twopi*(random_number2));
  energy_neutron = (5.59/2.35)*(ion_kt[bin_number])*sample1*sample2;
  energy_neutron += 14.08;
  // test energy limit
  // if (energy_neutron < 15.5){energy_neutron = 15.5} else {}
  return;
}

/*
 * convert the sampled radius to an rz coordinate by using plasma parameters
 */
void PlasmaSource::convert_rad_to_rz( const double minor_sampled,
			                  const double rn_store, 
                        double &radius, double &height)
{
  const double twopi = 6.28318530718;
  
  double alpha = twopi*(rn_store);
  
  double shift = shafranov*(1.0-std::pow(minor_sampled/(minorRadius),2));
  
  radius = majorRadius + minor_sampled*cos(alpha+(triangularity*sin(alpha))) + shift;
  height = elongation*minor_sampled*sin(alpha);
  
 
  return;
}
  

/*
 * convert rz_to_xyz
 */
void PlasmaSource::convert_r_to_xy(const double r, const double rn_store, 
                     double &x, double &y) 
                    
{
  double toroidal_extent = maxToroidalAngle - minToroidalAngle;
  double toroidal_angle = toroidal_extent*rn_store + minToroidalAngle;
  x = r*sin(toroidal_angle);
  y = r*cos(toroidal_angle);
  return;
}

/*
 * sets up the cumulatitive probability profile
 * on the basis of the ion temp and ion density
 * this portion is deterministic
 */
void PlasmaSource::setup_plasma_source()
{
  double ion_d; // ion density
  double ion_t; // ion temp

  std::vector<double> src_strength; // the source strength, n/m3
  double r;

  binWidth = minorRadius/float(numberOfBins);
  double total = 0.0; // total source strength

  for (int i = 0 ; i < numberOfBins ; i++) {
    r = binWidth * float(i);
    ion_d = ion_density(r);
    ion_t = ion_temperature(r);
    src_strength.push_back(std::pow(ion_d,2)*dt_xs(ion_t));
    ion_kt.push_back(sqrt(ion_t/1000.0)); // convert to sqrt(MeV)
    total += src_strength[i];
  }

  // normalise the source profile
  double sum = 0 ;
  for ( int i = 0 ; i < numberOfBins ; i++) {
	sum += src_strength[i];
    source_profile.push_back(sum/total);
  }
  return;
}

/*
 * function that returns the ion density given the 
 * given the critical plasma parameters
 */
double PlasmaSource::ion_density(const double sample_radius)
{
  double ion_dens = 0.0;

  if( plasmaId == 0 ) {
    ion_dens = ionDensityOrigin*
      (1.0-std::pow(sample_radius/minorRadius,2));
  } else {
    if(sample_radius <= pedistalRadius) {
      ion_dens += ionDensityPedistal;
      double product;
      product = 1.0-std::pow(sample_radius/pedistalRadius,2);
      product = std::pow(product,ionDensityPeaking);
      ion_dens += (ionDensityOrigin-ionDensityPedistal)*
            	  (product);
    } else {
      ion_dens += ionDensitySeperatrix;
      double product;
      product = ionDensityPedistal - ionDensitySeperatrix;
      ion_dens += product*(minorRadius-sample_radius)/(minorRadius-pedistalRadius);
    }
  }

  return ion_dens;
}
		   
/*
 * function that returns the ion density given the 
 * given the critical plasma parameters
 */
double PlasmaSource::ion_temperature(const double sample_radius)
{
  double ion_temp = 0.0;

  if( plasmaId == 0 ) {
    ion_temp = ionTemperatureOrigin*
      (1.0-std::pow(sample_radius/minorRadius,
		    ionTemperaturePeaking));
  } else {
    if(sample_radius <= pedistalRadius) {
      ion_temp += ionTemperaturePedistal;
      double product;
      product = 1.0-std::pow(sample_radius/pedistalRadius,ionTemperatureBeta);
      product = std::pow(product,ionTemperaturePeaking);
      ion_temp += (ionTemperatureOrigin-
		   ionTemperaturePedistal)*(product);
    } else {
      ion_temp += ionTemperatureSeperatrix;
      double product;
      product = ionTemperaturePedistal - ionTemperatureSeperatrix;
      ion_temp += product*(minorRadius-sample_radius)/(minorRadius-pedistalRadius);
    }
  }

  return ion_temp;
}

/*
 * returns the dt cross section for a given ion temp
 */
double PlasmaSource::dt_xs(double ion_temp)
{
  double dt;
  double c[7]={2.5663271e-18,19.983026,2.5077133e-2,
	       2.5773408e-3,6.1880463e-5,6.6024089e-2,
	       8.1215505e-3};
  
  double u = 1.0-ion_temp*(c[2]+ion_temp*(c[3]-c[4]*ion_temp))
    /(1.0+ion_temp*(c[5]+c[6]*ion_temp));

  dt = c[0]/(std::pow(u,5./6.)*std::pow(ion_temp,2./3.0));
  dt *= exp(-1.*c[1]*std::pow(u/ion_temp,1./3.));

  return dt;
}

/*
 * returns the dt cross section for a given ion temp
 */
void PlasmaSource::isotropic_direction(const double random1, 
                                         const double random2,
                                         double &u, double &v,
                                         double &w) {
  double t = 2*M_PI*random1;
  double p = acos(1. - 2.*random2);

  u = sin(p)*cos(t);
  v = sin(p)*sin(t);
  w = cos(p);
  
  return;
}

} // end of namespace
"""
)

plasma_source_hpp = (
"""#include <iostream>
#include <array>
namespace plasma_source {

struct xs_params {
  double c[7];
};

class PlasmaSource {
public:
// constructor
PlasmaSource();
// destructor
~PlasmaSource();
// large constructor
PlasmaSource(const double ion_density_ped, const double ion_density_sep,
	    const double ion_density_origin, const double ion_temp_ped,
	    const double ion_temp_sep, const double ion_temp_origin, 
	    const double pedistal_rad, const double ion_density_peak,
	    const double ion_temp_peak, const double ion_temp_beta,
      const double minor_radius, const double major_radius,
      const double elongation, const double triangularity,
      const double shafranov, const std::string plasma_type,
      const int plasma_id, const int number_of_bins,
		const double min_toroidal_angle = 0.0,
		const double max_toridal_angle = 360.);

// main sample fucnction
void SampleSource(std::array<double,8> randoms,
			 double &x,
			 double &y,
			 double &z,
			 double &u,
			 double &v,
			 double &w,
			 double &E);

/*
 * Function to setup the plasma source in the first case.
 */
void setup_plasma_source();

/*
 * function to calculate the ion density at a specific minor 
 * radius
 */
double ion_density(const double sample_radius);

/*
 * function to calculate the ion temperature at a specific minor 
 * radius
 */
double ion_temperature(const double sample_radius);

/*
 * function to determine the value of the dt xs cross sections at 
 * a specific ion temp
 */
double dt_xs(double ion_temp);

/*
 * sample the source, returns the minor radius sampled
 * expects new rn_store every call
 */
void sample_source_radial(double rn_store1, double rn_store2, 
						  double &sampled_radius,
						  int &sampled_bin);

/*
 * sample the neutron energy  in MeV
 */
void sample_energy(const int bin_number, double random_number1, double random_number2,
		    	   double &energy_neutron);

/*
 * take the sampled minor radius and convert to cylindrical coordinates
 */ 
void convert_rad_to_rz(const double minor_sampled,
					   const double rn_store, 
					   double &radius, 
					   double &height);

/*
 * convert partial cylindrical coords to xyz
 */
void convert_r_to_xy(const double r, const double rn_store, 
                     double &x, double &y);
/*
 * get an isotropically direction vector
 */
void isotropic_direction(const double random1, const double random2,
						double &u, double &v, double &w);

private:
  std::vector<double> source_profile;
  std::vector<double> ion_kt;

  double ionDensityPedistal;
  double ionDensitySeperatrix;
  double ionDensityOrigin;
  double ionTemperaturePedistal;
  double ionTemperatureSeperatrix;
  double ionTemperatureOrigin;
  double pedistalRadius;
  double ionDensityPeaking;
  double ionTemperaturePeaking;
  double ionTemperatureBeta;
  double minorRadius;
  double majorRadius;
  double elongation;
  double triangularity;
  double shafranov;
  double minToroidalAngle;
  double maxToroidalAngle;

  std::string plasmaType;
  int plasmaId;
  double binWidth;
  int numberOfBins;

};
}// end of namespace"""
)

make_file = (
"""
# Makefile to build dynamic sources for OpenMC
# this assumes that your source sampling filename is
# source_sampling.cpp 
#
# you can add fortran, c and cpp dependencies to this source
# adding them in FC_DEPS, C_DEPS, and CXX_DEPS accordingly

ifeq ($(FC), f77)
FC = gfortran 
endif 

default: all 

ALL = source_sampling
# add your fortran depencies here
FC_DEPS =
# add your c dependencies here
C_DEPS = 
# add your cpp dependencies here 
CPP_DEPS = plasma_source.cpp
DEPS = $(FC_DEPS) $(C_DEPS) $(CPP_DEPS)
OPT_LEVEL = -O3
FFLAGS = $(OPT_LEVEL) -fPIC
C_FLAGS = -fPIC
CXX_FLAGS = -fPIC

 #this directory will need changing if your openmc path is different
OPENMC_DIR = /opt/openmc
OPENMC_INC_DIR = $(OPENMC_DIR)/include
OPENMC_LIB_DIR = $(OPENMC_DIR)/lib
# setting the so name is important
LINK_FLAGS = $(OPT_LEVEL) -Wall -Wl,-soname,source_sampling.so 
# setting shared is important
LINK_FLAGS += -L$(OPENMC_LIB_DIR) -lopenmc -lgfortran -fPIC -shared
OPENMC_INCLUDES = -I$(OPENMC_INC_DIR) -I$(OPENMC_DIR)/vendor/pugixml

all: $(ALL) 

source_sampling: $(DEPS)
	$(CXX) source_sampling.cpp $(DEPS) $(OPENMC_INCLUDES) $(LINK_FLAGS) -o $@.so 
# make any fortran objects
%.o : %.F90 
	$(FC) -c $(FFLAGS) $*.F90 -o $@
# make any c objects
%.o : %.c
	$(CC) -c $(FFLAGS) $*.c -o $@
#make any cpp objects
%.o : %.cpp
	$(CXX) -c $(FFLAGS) $*.cpp -o $@
clean: 
	rm -rf *.o *.mod
"""
)
