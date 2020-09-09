#include <iostream>
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
    PlasmaSource(const double ion_density_ped,
                 const double ion_density_sep,
	               const double ion_density_origin,
                 const double ion_temp_ped,
	               const double ion_temp_sep,
                 const double ion_temp_origin, 
	               const double pedistal_rad,
                 const double ion_density_peak,
	               const double ion_temp_peak,
                 const double ion_temp_beta,
                 const double minor_radius,
                 const double major_radius,
                 const double elongation,
                 const double triangularity,
                 const double shafranov,
                 const std::string plasma_type,
                 const int plasma_id,
                 const int number_of_bins,
		             const double min_toroidal_angle = 0.0,
		             const double max_toridal_angle = 360.);

    // main sample fucnction
    void sample(std::array<double,8> randoms,
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
    void sample_radial(double rn_store1,
                       double rn_store2,
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
    void convert_r_to_xy(const double r, const double rn_store, double &x, double &y);

    /*
     * get an isotropically direction vector
     */
    void isotropic_direction(const double random1,
                             const double random2,
		                         double &u,
                             double &v,
                             double &w);

    /*
     * get a key-value pair string representation of this instance of the source
     */
    std::string to_string();

    /*
     * create a new source from the provided key-value pair string representation
     * of the source
     */
    static PlasmaSource from_string(std::string parameters);

    /*
     * Getter for pedestal ion density
     */
    const double &getIonDensityPedestal() const { return ionDensityPedistal; }

    /*
     * Getter for separatrix ion density
     */
    const double &getIonDensitySeparatrix() const { return ionDensitySeperatrix; }

    /*
     * Getter for origin ion density
     */
    const double &getIonDensityOrigin() const { return ionDensityOrigin; }

    /*
     * Getter for pedestal ion temperature
     */
    const double &getIonTemperaturePedestal() const { return ionTemperaturePedistal; }

    /*
     * Getter for separatrix ion temperature
     */
    const double &getIonTemperatureSeperatrix() const { return ionTemperatureSeperatrix; }

    /*
     * Getter for origin ion temperature
     */
    const double &getIonTemperatureOrigin() const { return ionTemperatureOrigin; }

    /*
     * Getter for pedestal radius
     */
    const double &getPedestalRadius() const { return pedistalRadius; }

    /*
     * Getter for ion density peaking factor
     */
    const double &getIonDensityPeaking() const { return ionDensityPeaking; }

    /*
     * Getter for ion temperature peaking factor
     */
    const double &getIonTemperaturePeaking() const { return ionTemperaturePeaking; }

    /*
     * Getter for ion temperature beta factor
     */
    const double &getIonTemperatureBeta() const { return ionTemperatureBeta; }

    /*
     * Getter for minor radius
     */
    const double &getMinorRadius() const { return minorRadius; }

    /*
     * Getter for major radius
     */
    const double &getMajorRadius() const { return majorRadius; }

    /*
     * Getter for elongation
     */
    const double &getElongation() const { return elongation; }

    /*
     * Getter for triangularity
     */
    const double &getTriangularity() const { return triangularity; }

    /*
     * Getter for shafranov shift
     */
    const double &getShafranov() const { return shafranov; }

    /*
     * Getter for minimum toroidal angle
     */
    const double &getMinToroidalAngle() const { return minToroidalAngle; }

    /*
     * Getter for maximum toroidal angle
     */
    const double &getMaxToroidalAngle() const { return maxToroidalAngle; }

    /*
     * Getter for plasma type
     */
    const std::string &getPlasmaType() const { return plasmaType; }

    /*
     * Getter for plasma identifier
     */
    const int &getPlasmaId() const { return plasmaId; }

    /*
     * Getter for number of bins
     */
    const int &getNumberOfBins() const { return numberOfBins; }

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

}// end of namespace
