#include <iostream>
#include "openmc/random_lcg.h"
#include "openmc/source.h"
#include "openmc/particle.h"
#include "plasma_source.hpp"

// you must have external C linkage here otherwise 
// dlopen will not find the file
extern "C" openmc::Particle::Bank sample_source(uint64_t* seed, char* serialization) {
    plasma_source::PlasmaSource source = plasma_source::PlasmaSource::from_xml(serialization);

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
    source.sample_source(randoms,particle.r.x,particle.r.y,particle.r.z,
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


