#define CATCH_CONFIG_MAIN  // This tells Catch to provide a main() - only do this in one cpp file
#include "catch.hpp"
#include "plasma_source.hpp"

double ion_density_ped = 1.09e+20;
double ion_density_sep = 3e+19;
double ion_density_origin = 1.09e+20;
double ion_temp_ped = 6.09;
double ion_temp_sep = 0.1;
double ion_temp_origin = 45.9;
double pedestal_rad = 2.33806;
double ion_density_peak = 1.0;
double ion_temp_peak = 8.06;
double ion_temp_beta = 6.0;
double minor_radius = 2.92258;
double major_radius = 9.06;
double elongation = 1.557;
double triangularity = 0.27;
double shafranov = 0.44789;
std::string plasma_type = "plasma";
int plasma_id = 1;
int number_of_bins = 100;
double min_toroidal_angle = 0.0;
double max_toridal_angle = 360.0;

plasma_source::PlasmaSource source = plasma_source::PlasmaSource(
    ion_density_ped,
    ion_density_sep,
    ion_density_origin,
    ion_temp_ped,
    ion_temp_sep,
    ion_temp_origin, 
    pedestal_rad,
    ion_density_peak,
    ion_temp_peak,
    ion_temp_beta,
    minor_radius,
    major_radius,
    elongation,
    triangularity,
    shafranov,
    plasma_type,
    plasma_id,
    number_of_bins,
    min_toroidal_angle = 0.0,
    max_toridal_angle = 360.
);

TEST_CASE( "Ion density is computed", "[source]" ) {
    REQUIRE( source.ion_density(0.0) == Approx(ion_density_origin) );
    REQUIRE( source.ion_density(0.2) == Approx(ion_density_ped) );
    REQUIRE( source.ion_density(2.4) == Approx(1.00629067e20) );
    REQUIRE( source.ion_density(minor_radius) == Approx(ion_density_sep) );
}

TEST_CASE( "Ion temperature is computed", "[source]" ) {
    REQUIRE( source.ion_temperature(0.0) == Approx(ion_temp_origin) );
    REQUIRE( source.ion_temperature(0.2) == Approx(45.89987429) );
    REQUIRE( source.ion_temperature(2.4) == Approx(5.45529258) );
    REQUIRE( source.ion_temperature(minor_radius) == Approx(ion_temp_sep) );
}

TEST_CASE( "D-T cross section is computed", "[source]" ) {
    REQUIRE( source.dt_xs(ion_temp_origin) == Approx(8.14659e-22) );
    REQUIRE( source.dt_xs(45.89987429) == Approx(8.14658e-22) );
    REQUIRE( source.dt_xs(5.45529258) == Approx(1.80129e-23) );
    REQUIRE( source.dt_xs(ion_temp_sep) == Approx(2.48478e-36) );
}

TEST_CASE( "Source sampling", "[source]" ) {
    double x, y, z;
    double u, v, w;
    double e;
    std::array<double, 8> rands = {0.2, 0.3, 0.1, 0.2, 0.3, 0.1, 0.2, 0.3};
    source.sample(rands, x, y, z, u, v, w, e);
    REQUIRE( x == Approx(9.2401323) );
    REQUIRE( y == Approx(3.0023) );
    REQUIRE( z == Approx(0.275493) );
    REQUIRE( u == Approx(0.283219) );
    REQUIRE( v == Approx(0.871658) );
    REQUIRE( w == Approx(0.4) );
    REQUIRE( e == Approx(14.7198) );
}
