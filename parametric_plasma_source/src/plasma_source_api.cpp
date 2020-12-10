#include <algorithm>
#include <array>
#include <iterator>
#include <string>
#include <iostream>
#include <vector>

#include "Plasma_source.h"
#include "plasma_source.hpp"

using namespace std;

PLASMASOURCE* create_plasmasource(const double ion_density_ped, const double ion_density_sep,
                                  const double ion_density_origin, const double ion_temp_ped,
                                  const double ion_temp_sep, const double ion_temp_origin, 
                                  const double pedistal_rad, const double ion_density_peak,
                                  const double ion_temp_peak, const double ion_temp_beta,
                                  const double minor_radius, const double major_radius,
                                  const double elongation, const double triangularity,
                                  const double shafranov, char* plasma_type_c,
                                  const int plasma_id, const int number_of_bins,
                                  const double min_toroidal_angle,
                                  const double max_toroidal_angle){                               
     
    std::string plasma_type;
    plasma_type = plasma_type_c;                                   

    return new plasma_source::PlasmaSource(ion_density_ped, ion_density_sep,
                            ion_density_origin, ion_temp_ped,
                            ion_temp_sep, ion_temp_origin, 
                            pedistal_rad, ion_density_peak,
                            ion_temp_peak, ion_temp_beta,
                            minor_radius, major_radius,
                            elongation, triangularity,
                            shafranov, plasma_type,
                            plasma_id, number_of_bins,
                            min_toroidal_angle,
                            max_toroidal_angle);
           
}

void delete_plasmasource(PLASMASOURCE* source){
    
    // delete source;
    
}

void Sample_Plasma_Source(PLASMASOURCE* source, 
                          double (&random_numbers_c)[8],
                          double &x,
                          double &y,
                          double &z,
                          double &u,
                          double &v,
                          double &w,
                          double &E){
  
    std::array<double, 8> random_numbers;
    std::copy_n(std::begin(random_numbers_c),8,std::begin(random_numbers));
    
    
    source->sample(random_numbers,x,y,z,u,v,w,E);
    
}
