#ifdef __cplusplus // Are we compiling this with a C++ compiler ?
extern "C" {
    namespace plasma_source{
        class PlasmaSource;
    }
    using namespace plasma_source;
    typedef PlasmaSource PLASMASOURCE;
#else
    // From the C side, we use an opaque pointer.
    typedef struct PLASMASOURCE PLASMASOURCE;
#endif

//
// PLASMASOURCE* create_emptyplasmasource();

// Large Constructor
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
                                  const double max_toroidal_angle );
                                  
// Destructor
void delete_plasmasource(PLASMASOURCE* source);

// Sample Function
void Sample_Plasma_Source(PLASMASOURCE* source, 
                          double (&random_numbers_c)[8],
                          double &x,
                          double &y,
                          double &z,
                          double &u,
                          double &v,
                          double &w,
                          double &E);
                          
#ifdef __cplusplus
}
#endif 