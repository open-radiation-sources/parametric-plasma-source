
import os
from pathlib import Path
import tempfile
import shutil


class Plasma():

    def __init__(self,
                 elongation=2.,
                 major_radius=450,
                 minor_radius=150,
                 single_null=True,
                 triangularity=0.55,
                 ion_density_pedistal=1.09e20,
                 ion_density_seperatrix=3e19,
                 ion_density_origin=1.09e20,
                 ion_temperature_pedistal=6.09,
                 ion_temperature_seperatrix=0.1,
                 ion_temperature_origin=45.9,
                 pedistal_radius=0.8,
                 ion_density_peaking_factor=1,
                 ion_temperature_peaking_factor=8.06,
                 shafranov_shift=0.0,
                 number_of_bins=100,
                 plasma_type=1,
                 openmc_install_directory = '/opt/openmc/'
                 ):

        # properties needed for plasma shapes
        self.elongation = elongation
        self.major_radius = major_radius
        self.minor_radius = minor_radius
        self.single_null = single_null
        self.triangularity = triangularity
        self.ion_density_pedistal = ion_density_pedistal  # ions per m^3
        self.ion_density_seperatrix = ion_density_seperatrix
        self.ion_density_origin = ion_density_origin
        self.ion_temperature_pedistal = ion_temperature_pedistal
        self.ion_temperature_seperatrix = ion_temperature_seperatrix
        self.ion_temperature_origin = ion_temperature_origin
        self.pedistal_radius = pedistal_radius  # pedistal major rad
        self.ion_density_peaking_factor = ion_density_peaking_factor
        self.ion_temperature_peaking_factor = ion_temperature_peaking_factor
        self.shafranov_shift = shafranov_shift
        self.number_of_bins = number_of_bins
        self.plasma_type = plasma_type  # 0 = L mode anything else H/A mode
        self.openmc_install_directory = openmc_install_directory

        self.plasma_source_cpp_file = '\n'.join(['#include <iostream>',
            '#include <vector>',
            '#include <cmath>',
            '#include "plasma_source.hpp"',
            '#include <stdlib.h>     ',
            '#include "openmc/random_lcg.h"',

            '#define RANDOM openmc::prn()',

            'namespace plasma_source {',

            '// default constructor',
            'PlasmaSource::PlasmaSource() {}',

            '// large constructor',
            'PlasmaSource::PlasmaSource(const double ion_density_ped, const double ion_density_sep,',
            '	    const double ion_density_origin, const double ion_temp_ped,',
            '	    const double ion_temp_sep, const double ion_temp_origin, ',
            '	    const double pedistal_rad, const double ion_density_peak,',
            '	    const double ion_temp_peak, const double minor_radius, ',
            '	    const double major_radius, const double elongation, ',
            '	    const double triangularity, const double shafranov, ',
            '	    const std::string plasma_type, const int plasma_id,',
            '	    const int number_of_bins,',
            '      const double min_toroidal_angle,',
            '      const double max_toroidal_angle ) {',

            '  // set params',
            '  ionDensityPedistal = ion_density_ped;',
            '  ionDensitySeperatrix = ion_density_sep;',
            '  ionDensityOrigin = ion_density_origin;',
            '  ionTemperaturePedistal = ion_temp_ped;',
            '  ionTemperatureSeperatrix = ion_temp_sep;',
            '  ionTemperatureOrigin = ion_temp_origin;',
            '  pedistalRadius = pedistal_rad;',
            '  ionDensityPeaking = ion_density_peak;',
            '  ionTemperaturePeaking = ion_temp_peak;',
            '  minorRadius = minor_radius;',
            '  majorRadius = major_radius;',
            '  this->elongation = elongation;',
            '  this->triangularity = triangularity;',
            '  this->shafranov = shafranov;',
            '  plasmaType = plasma_type;',
            '  plasmaId = plasma_id;',
            '  numberOfBins = number_of_bins;',
            '  minToroidalAngle = min_toroidal_angle/180.*M_PI;',
            '  maxToroidalAngle = max_toroidal_angle/180.*M_PI;',

            '  setup_plasma_source();',
            '}',

            '// destructor',
            'PlasmaSource::~PlasmaSource(){}',

            '// main master sample function',
            'void PlasmaSource::SampleSource(std::array<double,8> random_numbers,',
            '                                double &x,',
            '                                double &y,',
            '                                double &z,',
            '                                double &u,',
            '                                double &v,',
            '                                double &w,',
            '                                double &E) {',
            '  double radius = 0.;',
            '  int bin = 0;',
            '  sample_source_radial(random_numbers[0],random_numbers[1],radius,bin);',
            '  double r = 0.;',
            '  convert_rad_to_rz(radius,random_numbers[2],r,z);',
            '  convert_r_to_xy(r,random_numbers[3],x,y);',
            '  sample_energy(bin,random_numbers[4],random_numbers[5],E);',
            '  isotropic_direction(random_numbers[6],random_numbers[7],',
            '                      u,v,w);',
            '}',

            '/*',
            ' * sample the pdf src_profile, to generate the sampled minor radius',
            ' */',
            'void PlasmaSource::sample_source_radial(double rn_store1, double rn_store2, ',
            '                          double &sampled_radius, int &sampled_bin) {',
            
            '  for ( int i = 0 ; i < numberOfBins ; i++ ) {',
            '    if ( rn_store1 <= source_profile[i] ) {',
            '      if ( i > 0 ) {',
            '	      sampled_radius = (float(i-1)*(binWidth)) + (binWidth*(rn_store2));',
            '	      sampled_bin = i;',
            '	      return;',
            '      } else {',
            '	      sampled_radius = binWidth*(rn_store2);',
            '	      sampled_bin = i;',
            '	      return;',
            '      }',
            '    }',
            '  }',

            '  std::cerr << "error" << std::endl;',
            '  std::cerr << "Sample position greater than plasma radius" << std::endl;',
            '  exit(1);',
            '  return;',
            '}',

            '/*',
            ' * sample the energy of the neutrons, updates energy neutron in mev',
            ' */',
            'void PlasmaSource::sample_energy(const int bin_number, double random_number1, double random_number2,',
            '		      double &energy_neutron) {',
            '  // generate the normally distributed number',
            '  const double twopi = 6.28318530718;',
            '  double sample1 = std::sqrt(-2.0*std::log(random_number1));',
            '  double sample2 = cos(twopi*(random_number2));',
            '  energy_neutron = (5.59/2.35)*(ion_kt[bin_number])*sample1*sample2;',
            '  energy_neutron += 14.08;',
            '  // test energy limit',
            '  // if (energy_neutron < 15.5){energy_neutron = 15.5} else {}',
            '  return;',
            '}',

            '/*',
            ' * convert the sampled radius to an rz coordinate by using plasma parameters',
            ' */',
            'void PlasmaSource::convert_rad_to_rz( const double minor_sampled,',
            '			                  const double rn_store, ',
            '                        double &radius, double &height)',
            '{',
            '  const double twopi = 6.28318530718;',
            
            '  double alpha = twopi*(rn_store);',
            
            '  double shift = shafranov*(1.0-std::pow(minor_sampled/(minorRadius),2));',
            
            '  radius = majorRadius + minor_sampled*cos(alpha+(triangularity*sin(alpha))) + shift;',
            '  height = elongation*minor_sampled*sin(alpha);',
            
            
            '  return;',
            '}',
            

            '/*',
            ' * convert rz_to_xyz',
            ' */',
            'void PlasmaSource::convert_r_to_xy(const double r, const double rn_store, ',
            '                     double &x, double &y) ',
                                
            '{',
            '  double toroidal_extent = maxToroidalAngle - minToroidalAngle;',
            '  double toroidal_angle = toroidal_extent*rn_store + minToroidalAngle;',
            '  x = r*sin(toroidal_angle);',
            '  y = r*cos(toroidal_angle);',
            '  return;',
            '}',

            '/*',
            ' * sets up the cumulatitive probability profile',
            ' * on the basis of the ion temp and ion density',
            ' * this portion is deterministic',
            ' */',
            'void PlasmaSource::setup_plasma_source()',
            '{',
            '  double ion_d; // ion density',
            '  double ion_t; // ion temp',
            
            '  std::vector<double> src_strength; // the source strength, n/m3',
            '  double r;',

            '  binWidth = minorRadius/float(numberOfBins);',
            '  double total = 0.0; // total source strength',

            '  for (int i = 0 ; i < numberOfBins ; i++) {',
            '    r = binWidth * float(i);',
            '    ion_d = ion_density(r);',
            '    ion_t = ion_temperature(r);',
            '    src_strength.push_back(std::pow(ion_d,2)*dt_xs(ion_t));',
            '    ion_kt.push_back(sqrt(ion_t/1000.0)); // convert to sqrt(MeV)',
            '    total += src_strength[i];',
            '  }',

            '  // normalise the source profile',
            '  double sum = 0 ;',
            '  for ( int i = 0 ; i < numberOfBins ; i++) {',
            '	sum += src_strength[i];',
            '    source_profile.push_back(sum/total);',
            '  }',
            '  return;',
            '}',

            '/*',
            ' * function that returns the ion density given the ',
            ' * given the critical plasma parameters',
            ' */',
            'double PlasmaSource::ion_density(const double sample_radius)',
            '{',
            '  double ion_dens = 0.0;',
            '',
            '  if( plasmaId == 0 ) {',
            '    ion_dens = ionDensityOrigin*',
            '      (1.0-std::pow(sample_radius/minorRadius,2));',
            '  } else {',
            '    if(sample_radius <= pedistalRadius) {',
            '      ion_dens += ionDensityPedistal;',
            '      double product;',
            '      product = 1.0-std::pow(sample_radius/pedistalRadius,2);',
            '      product = std::pow(product,ionDensityPeaking);',
            '      ion_dens += (ionDensityOrigin-ionDensityPedistal)*',
            '            	  (product);',
            '    } else {',
            '      ion_dens += ionDensitySeperatrix;',
            '      double product;',
            '      product = ionDensityPedistal - ionDensitySeperatrix;',
            '      ion_dens += product*(minorRadius-sample_radius)/(minorRadius-pedistalRadius);',
            '    }',
            '  }',

            '  return ion_dens;',
            '}',
                    
            '/*',
            ' * function that returns the ion density given the ',
            ' * given the critical plasma parameters',
            ' */',
            'double PlasmaSource::ion_temperature(const double sample_radius)',
            '{',
            '  double ion_temp = 0.0;',

            '  if( plasmaId == 0 ) {',
            '    ion_temp = ionTemperatureOrigin*',
            '      (1.0-std::pow(sample_radius/minorRadius,',
            '		    ionTemperaturePeaking));',
            '  } else {',
            '    if(sample_radius <= pedistalRadius) {',
            '      ion_temp += ionTemperaturePedistal;',
            '      double product;',
            '      product = 1.0-std::pow(sample_radius/pedistalRadius,2);',
            '      product = std::pow(product,ionTemperaturePeaking);',
            '      ion_temp += (ionTemperatureOrigin-',
            '		   ionTemperaturePedistal)*(product);',
            '    } else {',
            '      ion_temp += ionTemperatureSeperatrix;',
            '      double product;',
            '      product = ionTemperaturePedistal - ionTemperatureSeperatrix;',
            '      ion_temp += product*(minorRadius-sample_radius)/(minorRadius-pedistalRadius);',
            '    }',
            '  }',

            '  return ion_temp;',
            '}',

            '/*',
            ' * returns the dt cross section for a given ion temp',
            ' */',
            'double PlasmaSource::dt_xs(double ion_temp)',
            '{',
            '  double dt;',
            '  double c[7]={2.5663271e-18,19.983026,2.5077133e-2,',
            '	       2.5773408e-3,6.1880463e-5,6.6024089e-2,',
            '	       8.1215505e-3};',
            
            '  double u = 1.0-ion_temp*(c[2]+ion_temp*(c[3]-c[4]*ion_temp))',
            '    /(1.0+ion_temp*(c[5]+c[6]*ion_temp));',

            '  dt = c[0]/(std::pow(u,5./6.)*std::pow(ion_temp,2./3.0));',
            '  dt *= exp(-1.*c[1]*std::pow(u/ion_temp,1./3.));',

            '  return dt;',
            '}',

            '/*',
            ' * returns the dt cross section for a given ion temp',
            ' */',
            'void PlasmaSource::isotropic_direction(const double random1, ',
            '                                         const double random2,',
            '                                         double &u, double &v,',
            '                                         double &w) {',
            '  double t = 2*M_PI*random1;',
            '  double p = acos(1. - 2.*random2);',

            '  u = sin(p)*cos(t);',
            '  v = sin(p)*sin(t);',
            '  w = cos(p);',
            
            '  return;',
            '}',

            '} // end of namespace'
        ])

        self.plasma_source_hpp_file = '\n'.join([
            '#include <iostream>',
            '#include <array>',
            'namespace plasma_source {',

            'struct xs_params {',
            '  double c[7];',
            '};',

            'class PlasmaSource {',
            'public:',
            '// constructor',
            'PlasmaSource();',
            '// destructor',
            '~PlasmaSource();',
            '// large constructor',
            'PlasmaSource(const double ion_density_ped, const double ion_density_sep,',
            '	    const double ion_density_origin, const double ion_temp_ped,',
            '	    const double ion_temp_sep, const double ion_temp_origin, ',
            '	    const double pedistal_rad, const double ion_density_peak,',
            '	    const double ion_temp_peak, const double minor_radius, ',
            '	    const double major_radius, const double elongation, ',
            '	    const double triangularity, const double shafranov, ',
            '	    const std::string plasma_type, const int plasma_id,',
            '	    const int number_of_bins,',
            '		const double min_toroidal_angle = 0.0,',
            '		const double max_toridal_angle = 360.);',

            '// main sample fucnction',
            'void SampleSource(std::array<double,8> randoms,',
            '			 double &x,',
            '			 double &y,',
            '			 double &z,',
            '			 double &u,',
            '			 double &v,',
            '			 double &w,',
            '			 double &E);',

            '/*',
            ' * Function to setup the plasma source in the first case.',
            ' */',
            'void setup_plasma_source();',

            '/*',
            ' * function to calculate the ion density at a specific minor ',
            ' * radius',
            ' */',
            'double ion_density(const double sample_radius);',

            '/*',
            ' * function to calculate the ion temperature at a specific minor ',
            ' * radius',
            ' */',
            'double ion_temperature(const double sample_radius);',

            '/*',
            ' * function to determine the value of the dt xs cross sections at ',
            ' * a specific ion temp',
            ' */',
            'double dt_xs(double ion_temp);',

            '/*',
            ' * sample the source, returns the minor radius sampled',
            ' * expects new rn_store every call',
            ' */',
            'void sample_source_radial(double rn_store1, double rn_store2, ',
            '						  double &sampled_radius,',
            '						  int &sampled_bin);',

            '/*',
            ' * sample the neutron energy  in MeV',
            ' */',
            'void sample_energy(const int bin_number, double random_number1, double random_number2,',
            '		    	   double &energy_neutron);',

            '/*',
            ' * take the sampled minor radius and convert to cylindrical coordinates',
            ' */ ',
            'void convert_rad_to_rz(const double minor_sampled,',
            '					   const double rn_store, ',
            '					   double &radius, ',
            '					   double &height);',

            '/*',
            ' * convert partial cylindrical coords to xyz',
            ' */',
            'void convert_r_to_xy(const double r, const double rn_store, ',
            '         double &x, double &y);',
            '/*',
            ' * get an isotropically direction vector',
            ' */',
            'void isotropic_direction(const double random1, const double random2,',
            '						double &u, double &v, double &w);',

            'private:',
            '  std::vector<double> source_profile;',
            '  std::vector<double> ion_kt;',

            '  double ionDensityPedistal;',
            '  double ionDensitySeperatrix;',
            '  double ionDensityOrigin;',
            '  double ionTemperaturePedistal;',
            '  double ionTemperatureSeperatrix;',
            '  double ionTemperatureOrigin;',
            '  double pedistalRadius;',
            '  double ionDensityPeaking;',
            '  double ionTemperaturePeaking;',
            '  double minorRadius;',
            '  double majorRadius;',
            '  double elongation;',
            '  double triangularity;',
            '  double shafranov;',
            '  double minToroidalAngle;',
            '  double maxToroidalAngle;',

            '  std::string plasmaType;',
            '  int plasmaId;',
            '  double binWidth;',
            '  int numberOfBins;',

            '};',
            '}// end of namespace'
        ])

        self.source_sampling_cpp_file = '\n'.join(['#include <iostream>',
            '#include "openmc/random_lcg.h"',
            '#include "openmc/source.h"',
            '#include "openmc/particle.h"',
            '#include "plasma_source.hpp"',
            '',
            '',
            '// Spherical tokamak SOURCE', 
            '// units are in SI units',
            'const double ion_density_pedistal = 1.09e+20; // ions per m^3',
            'const double ion_density_seperatrix = 3e+19;',
            'const double ion_density_origin = 1.09e+20;',
            'const double ion_temperature_pedistal = 6.09;',
            'const double ion_temperature_seperatrix = 0.1;',
            'const double ion_temperature_origin = 45.9;',
            'const double pedistal_radius = 0.8; // pedistal major rad',
            'const double ion_density_peaking_factor = 1;',
            'const double ion_temperature_peaking_factor = 8.06; // check alpha or beta value from paper',
            'const double minor_radius = 1.56; // metres',
            'const double major_radius = 2.5; // metres',
            'const double elongation = 2.0;',
            'const double triangularity = 0.55;',
            'const double shafranov_shift = 0.0; //metres',
            'const std::string name = "parametric_plasma_source";',
            'const int number_of_bins  = 100;',
            'const int plasma_type = 1; // 1 is default; //0 = L mode anything else H/A mode',
            '',
            '',
            'plasma_source::PlasmaSource source = plasma_source::PlasmaSource(ion_density_pedistal,',
            '       ion_density_seperatrix,',
            '       ion_density_origin,',
            '       ion_temperature_pedistal,',
            '       ion_temperature_seperatrix,',
            '       ion_temperature_origin,',
            '       pedistal_radius,',
            '       ion_density_peaking_factor,',
            '       ion_temperature_peaking_factor,',
            '       minor_radius,',
            '       major_radius,',
            '       elongation,',
            '       triangularity,',
            '       shafranov_shift,',
            '       name,',
            '       plasma_type,',
            '       number_of_bins,',
            '       0.0,',
            '       360.0);',

            '// you must have external C linkage here otherwise',
            '// dlopen will not find the file',
            'extern "C" openmc::Particle::Bank sample_source(uint64_t* seed) {',
            '    openmc::Particle::Bank particle;',
            '    // wgt',
            '    particle.particle = openmc::Particle::Type::neutron;',
            '    particle.wgt = 1.0;',
            '    // position',
            '',
            '    std::array<double,8> randoms = {openmc::prn(seed),',
            '                            openmc::prn(seed),',
            '                            openmc::prn(seed),',
            '                            openmc::prn(seed),',
            '                            openmc::prn(seed),',
            '                            openmc::prn(seed),',
            '                            openmc::prn(seed),',
            '                            openmc::prn(seed)};',
            '',
            '    double u,v,w,E;',
            '    source.SampleSource(randoms,particle.r.x,particle.r.y,particle.r.z,',
            '                        u,v,w,E);',
            '',
            '    particle.r.x *= 100.;',
            '    particle.r.y *= 100.;',
            '    particle.r.z *= 100.;',  
            '',
            '    // particle.E = 14.08e6;',
            '    particle.E = E*1e6; // convert from MeV -> eV',
            '',
            '    particle.u = {u,',
            '                  v,',
            '                  w};',
            '',
            '',
            '    particle.delayed_group = 0;',
            '    return particle;',
            '}',
            ''
        ])

        self.plasma_make_file = '\n'.join(['# Makefile to build dynamic sources for OpenMC',
            '# this assumes that your source sampling filename is',
            '# source_sampling.cpp',
            '#',
            '# you can add fortran, c and cpp dependencies to this source',
            '# adding them in FC_DEPS, C_DEPS, and CXX_DEPS accordingly',
            '',
            'ifeq ($(FC), f77)',
            'FC = gfortran',
            'endif',
            '',
            'default: all',
            '',
            'ALL = source_sampling',
            '# add your fortran depencies here',
            'FC_DEPS =',
            '# add your c dependencies here',
            'C_DEPS =',
            '# add your cpp dependencies here',
            'CPP_DEPS = plasma_source.cpp',
            'DEPS = $(FC_DEPS) $(C_DEPS) $(CPP_DEPS)',
            'OPT_LEVEL = -O3',
            'FFLAGS = $(OPT_LEVEL) -fPIC',
            'C_FLAGS = -fPIC',
            'CXX_FLAGS = -fPIC',
            '',
            '#this directory will need changing if your openmc path is different',
            'OPENMC_DIR = /opt/openmc',
            'OPENMC_INC_DIR = $(OPENMC_DIR)/include',
            'OPENMC_LIB_DIR = $(OPENMC_DIR)/lib',
            '# setting the so name is important',
            'LINK_FLAGS = $(OPT_LEVEL) -Wall -Wl,-soname,source_sampling.so',
            '# setting shared is important',
            'LINK_FLAGS += -L$(OPENMC_LIB_DIR) -lopenmc -lgfortran -fPIC -shared',
            'OPENMC_INCLUDES = -I$(OPENMC_INC_DIR) -I$(OPENMC_DIR)/vendor/pugixml',
            '',
            'all: $(ALL)',
            '',
            'source_sampling: $(DEPS)',
            '	$(CXX) source_sampling.cpp $(DEPS) $(OPENMC_INCLUDES) $(LINK_FLAGS) -o $@.so',
            '# make any fortran objects',
            '%.o : %.F90',
            '	$(FC) -c $(FFLAGS) $*.F90 -o $@',
            '# make any c objects',
            '%.o : %.c',
            '	$(CC) -c $(FFLAGS) $*.c -o $@',
            '#make any cpp objects',
            '%.o : %.cpp',
            '	$(CXX) -c $(FFLAGS) $*.cpp -o $@',
            'clean:',
            '	rm -rf *.o *.mod'
        ])


    @property
    def openmc_install_directory(self):
        return self._openmc_install_directory

    @openmc_install_directory.setter
    def openmc_install_directory(self, value):
        if Path(value).exists() == False:
            raise ValueError('openmc_install_directory is out of range')
        else:
            self._openmc_install_directory = value

    @property
    def plasma_type(self):
        return self._plasma_type

    @plasma_type.setter
    def plasma_type(self, plasma_type):
        if plasma_type < 0:
            raise ValueError('plasma_type is out of range')
        else:
            self._plasma_type = plasma_type

    @property
    def number_of_bins(self):
        return self._number_of_bins

    @number_of_bins.setter
    def number_of_bins(self, number_of_bins):
        if number_of_bins < 0:
            raise ValueError('number_of_bins is out of range')
        else:
            self._number_of_bins = number_of_bins

    @property
    def shafranov_shift(self):
        return self._shafranov_shift

    @shafranov_shift.setter
    def shafranov_shift(self, shafranov_shift):
        if shafranov_shift < 0:
            raise ValueError('shafranov_shift is out of range')
        else:
            self._shafranov_shift = shafranov_shift

    @property
    def ion_temperature_peaking_factor(self):
        return self._ion_temperature_peaking_factor

    @ion_temperature_peaking_factor.setter
    def ion_temperature_peaking_factor(self, ion_temperature_peaking_factor):
        if ion_temperature_peaking_factor < 0:
            raise ValueError('ion_temperature_peaking_factor is out of range')
        else:
            self._ion_temperature_peaking_factor = ion_temperature_peaking_factor

    @property
    def ion_density_peaking_factor(self):
        return self._ion_density_peaking_factor

    @ion_density_peaking_factor.setter
    def ion_density_peaking_factor(self, ion_density_peaking_factor):
        if ion_density_peaking_factor < 0:
            raise ValueError('ion_density_peaking_factor is out of range')
        else:
            self._ion_density_peaking_factor = ion_density_peaking_factor

    @property
    def pedistal_radius(self):
        return self._pedistal_radius

    @pedistal_radius.setter
    def pedistal_radius(self, pedistal_radius):
        if pedistal_radius < 0:
            raise ValueError('pedistal_radius is out of range')
        else:
            self._pedistal_radius = pedistal_radius

    @property
    def ion_temperature_origin(self):
        return self._ion_temperature_origin

    @ion_temperature_origin.setter
    def ion_temperature_origin(self, ion_temperature_origin):
        if ion_temperature_origin < 0:
            raise ValueError('ion_temperature_origin is out of range')
        else:
            self._ion_temperature_origin = ion_temperature_origin

    @property
    def ion_temperature_seperatrix(self):
        return self._ion_temperature_seperatrix

    @ion_temperature_seperatrix.setter
    def ion_temperature_seperatrix(self, ion_temperature_seperatrix):
        if ion_temperature_seperatrix < 0:
            raise ValueError('ion_temperature_seperatrix is out of range')
        else:
            self._ion_temperature_seperatrix = ion_temperature_seperatrix

    @property
    def ion_temperature_pedistal(self):
        return self._ion_temperature_pedistal

    @ion_temperature_pedistal.setter
    def ion_temperature_pedistal(self, ion_temperature_pedistal):
        if ion_temperature_pedistal < 0:
            raise ValueError('ion_temperature_pedistal is out of range')
        else:
            self._ion_temperature_pedistal = ion_temperature_pedistal

    @property
    def ion_density_origin(self):
        return self._ion_density_origin

    @ion_density_origin.setter
    def ion_density_origin(self, ion_density_origin):
        if ion_density_origin < 0:
            raise ValueError('ion_density_origin is out of range')
        else:
            self._ion_density_origin = ion_density_origin

    @property
    def ion_density_seperatrix(self):
        return self._ion_density_seperatrix

    @ion_density_seperatrix.setter
    def ion_density_seperatrix(self, ion_density_seperatrix):
        if ion_density_seperatrix < 0:
            raise ValueError('ion_density_seperatrix is out of range')
        else:
            self._ion_density_seperatrix = ion_density_seperatrix

    @property
    def triangularity(self):
        return self._triangularity

    @triangularity.setter
    def triangularity(self, triangularity):
        if triangularity > 2000 or triangularity < -2000:
            raise ValueError('triangularity is out of range')
        else:
            self._triangularity = triangularity

    @property
    def single_null(self):
        return self._single_null

    @single_null.setter
    def single_null(self, single_null):
        if type(single_null) != bool :
            raise ValueError('single_null must be True or False')
        else:
            self._single_null = single_null

    @property
    def minor_radius(self):
        return self._minor_radius

    @minor_radius.setter
    def minor_radius(self, minor_radius):
        if minor_radius > 2000 or minor_radius < 1:
            raise ValueError('minor_radius is out of range')
        else:
            self._minor_radius = minor_radius

    @property
    def major_radius(self):
        return self._major_radius

    @major_radius.setter
    def major_radius(self, major_radius):
        if major_radius > 2000 or major_radius < 1:
            raise ValueError('major_radius is out of range')
        else:
            self._major_radius = major_radius

    @property
    def elongation(self):
        return self._elongation

    @elongation.setter
    def elongation(self, elongation):
        if elongation > 4 or elongation < 0:
            raise ValueError('elongation is out of range')
        else:
            self._elongation = elongation

    @property
    def ion_density_pedistal(self):
        return self._ion_density_pedistal

    @ion_density_pedistal.setter
    def ion_density_pedistal(self, ion_density_pedistal):
        if ion_density_pedistal > 10e22 or ion_density_pedistal < 1e4:
            raise ValueError('ion_density_pedistal is out of range')
        else:
            self._ion_density_pedistal = ion_density_pedistal



    def export_plasma_source(self, output_filename):
        """Writes and compiles custom plasma source for the reactor
        :param output_folder: the output folder where the .so complied plasma source will be created
        :type output_folder: str
        ...
        :return: filename of the compiled source
        :rtype: str
        """

        if self.openmc_install_directory is None:
            raise ValueError('directory must be set to create .so file')

        temp_folder = Path(tempfile.mkdtemp())

        print('temp_folder', temp_folder)

        Path(output_filename).parent.mkdir(parents=True, exist_ok=True)

        editted_plasma_make_file = self.plasma_make_file.replace('OPENMC_DIR = /opt/openmc', 'OPENMC_DIR = '+self.openmc_install_directory)
        with open(temp_folder/'Makefile', "w") as text_file:
            text_file.write(editted_plasma_make_file)

        with open(temp_folder/'plasma_source.cpp', "w") as text_file:
            text_file.write(self.plasma_source_cpp_file)

        with open(temp_folder/'plasma_source.hpp', "w") as text_file:
            text_file.write(self.plasma_source_hpp_file)

        plasma_varibles = [
            ('const double ion_density_pedistal = 1.09e+20', 'const double ion_density_pedistal = ' + str(self.ion_density_pedistal)),
            ('const double ion_density_seperatrix = 3e+19', 'const double ion_density_seperatrix = ' + str(self.ion_density_seperatrix)),
            ('const double ion_density_origin = 1.09e+20', 'const double ion_density_origin = ' + str(self.ion_density_origin)),
            ('const double ion_temperature_pedistal = 6.09', 'const double ion_temperature_pedistal = ' + str(self.ion_temperature_pedistal)),
            ('const double ion_temperature_seperatrix = 0.1','const double ion_temperature_seperatrix = ' + str(self.ion_temperature_seperatrix)),
            ('const double ion_temperature_origin = 45.9', 'const double ion_temperature_origin = ' + str(self.ion_temperature_origin)),
            ('const double pedistal_radius = 0.8', 'const double pedistal_radius = ' + str(self.pedistal_radius)),
            ('const double ion_density_peaking_factor = 1', 'const double ion_density_peaking_factor = ' + str(self.ion_density_peaking_factor)),
            ('const double ion_temperature_peaking_factor = 8.06', 'const double ion_temperature_peaking_factor = ' + str(self.ion_temperature_peaking_factor)),
            ('const double minor_radius = 1.56', 'const double minor_radius = ' + str(self.minor_radius / 100.)),
            ('const double major_radius = 2.5', 'const double major_radius = ' + str(self.major_radius / 100.)),
            ('const double elongation = 2.0', 'const double elongation = ' + str(self.elongation)),
            ('const double triangularity = 0.55', 'const double triangularity = ' + str(self.triangularity)),
            ('const double shafranov_shift = 0.0', 'const double shafranov_shift = ' + str(self.shafranov_shift / 100.)),
            ('const int number_of_bins  = 100', 'const int number_of_bins = ' + str(self.number_of_bins)),
            ('const int plasma_type = 1', 'const int plasma_type = ' + str(self.plasma_type))
        ]

        editted_source_sampling_cpp_file = self.source_sampling_cpp_file
        for entry in plasma_varibles:
            if entry[0] in self.source_sampling_cpp_file:
                editted_source_sampling_cpp_file = editted_source_sampling_cpp_file.replace(entry[0], entry[1])
            else:
                raise ValueError(entry[0],' string not found in ', self.source_sampling_cpp_file)


        with open(temp_folder/'source_sampling.cpp', "w") as text_file:
            text_file.write(editted_source_sampling_cpp_file)

        cwd = os.getcwd()
        os.chdir(Path(temp_folder))

        os.system('make clean')
        os.system('make')

        os.chdir(cwd)
        shutil.move(temp_folder/'source_sampling.so', output_filename)
        print('parametric plasma source compiled and saved to ',  output_filename)
        shutil.rmtree(temp_folder)

        return output_filename
