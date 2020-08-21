#include <memory>

#include "openmc/random_lcg.h"
#include "openmc/source.h"
#include "openmc/particle.h"
#include "plasma_source.hpp"

// defines a class that wraps our PlasmaSource and exposes it to OpenMC.
class SampledSource : public openmc::CustomSource {
  private:
    // the source that we will sample from
    plasma_source::PlasmaSource source;

  public:
    // create a SampledSource as a wrapper for the source that we will sample from
    SampledSource(plasma_source::PlasmaSource source) : source(source) { }

    // the function that will be exposed in the openmc::CustomSource parent class
    // so that the source can be sampled from.
    // essentially wraps the sample_source method on the source and populates the
    // relevant values in the openmc::Particle::Bank.
    openmc::Particle::Bank sample_source(uint64_t* seed) {
      openmc::Particle::Bank particle;
    
      // random numbers sampled from openmc::prn
      std::array<double,8> randoms = {openmc::prn(seed),
                                      openmc::prn(seed),
                                      openmc::prn(seed),
                                      openmc::prn(seed),
                                      openmc::prn(seed),
                                      openmc::prn(seed),
                                      openmc::prn(seed),
                                      openmc::prn(seed)};

      double u, v, w, E;

      // sample from the source
      this->source.sample_source(randoms,particle.r.x,particle.r.y,particle.r.z,
                                 u,v,w,E);

      // wgt
      particle.particle = openmc::Particle::Type::neutron;
      particle.wgt = 1.0;
      particle.delayed_group = 0;

      // position
      particle.r.x *= 100.; // convert from m -> cm
      particle.r.y *= 100.; // convert from m -> cm
      particle.r.z *= 100.; // convert from m -> cm

      // energy      
      particle.E = E * 1e6; // convert from MeV -> eV

      // direction
      particle.u = { u, v, w };

      return particle;    
    }
};

// A function to create a unique pointer to an instance of this class when generated
// via a plugin call using dlopen/dlsym.
// You must have external C linkage here otherwise dlopen will not find the file
extern "C" unique_ptr<SampledSource> openmc_create_source(const char* parameters) {
  plasma_source::PlasmaSource source = plasma_source::PlasmaSource::from_string(parameters);
  return unique_ptr<SampledSource> (new SampledSource(source));
}
