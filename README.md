# parametric-plasma-source

![Python package](https://github.com/DanShort12/parametric-plasma-source/workflows/Python%20package/badge.svg)

Python package, C++ source and build files for parametric plasma source for use in fusion neutron transport calculations with OpenMC.

The plasma source is based on a paper by [C. Fausser et al](https://www.sciencedirect.com/science/article/pii/S0920379612000853)

## Installation

### Installing from PyPI

```pip install parametric_plasma_source```

### Installing from source

Installation of the parametric plasma source from source requires cmake to build the underlying C++ code. This can be obtained from
your OS's package manager by e.g. `sudo apt-get install cmake` or from cmake source.

If you intend to develop the code then it is recommended to work in a virtual environment.

The requirements for developing the code can be installed by running:

```pip install -r requirements-develop.txt```

The package can be built and installed in editable mode by:

```pip install -e .```

## Usage

The parametric plasma source can be sampled either directly in Python 3 or sampled in an OpenMC simulation.

For a better understanding of the varibles take a look at the [C. Fausser et al](https://www.sciencedirect.com/science/article/pii/S0920379612000853) paper.

### Sampling in Python

The parametric plasma source can be imported an used in Python 3 in the following manner:

```[python]
from parametric_plasma_source import PlasmaSource
from random import random

plasma_params = {
    "elongation": 1.557,
    "ion_density_origin": 1.09e20,
    "ion_density_peaking_factor": 1,
    "ion_density_pedestal": 1.09e20,
    "ion_density_separatrix": 3e19,
    "ion_temperature_origin": 45.9,
    "ion_temperature_peaking_factor": 8.06,
    "ion_temperature_pedestal": 6.09,
    "ion_temperature_separatrix": 0.1,
    "major_radius": 9.06,
    "minor_radius": 2.92258,
    "pedestal_radius": 0.8 * 2.92258,
    "plasma_id": 1,
    "shafranov_shift": 0.44789,
    "triangularity": 0.270,
    "ion_temperature_beta": 6,
}

my_plasma = PlasmaSource(**plasma_params)
sample = my_plasma.sample([random(), random(), random(), random(), random(), random(), random(), random()])
particle_x, particle_y, particle_z = sample[0], sample[1], sample[2]
particle_x_dir, particle_y_dir, particle_z_dir = sample[3], sample[4], sample[5]
particle_energy_mev = sample[6]
```

### Sampling in OpenMC

The parametric plasma source also contains a plugin library for OpenMC to allow the source to be sampled in an OpenMC simulation.

When using the OpenMC sampling the inputs must be provided in meters where applicable (the sampling will convert to cm).

```[python]
from parametric_plasma_source import PlasmaSource, SOURCE_SAMPLING_PATH
import openmc

plasma_params = {
    "elongation": 1.557,
    "ion_density_origin": 1.09e20,
    "ion_density_peaking_factor": 1,
    "ion_density_pedestal": 1.09e20,
    "ion_density_separatrix": 3e19,
    "ion_temperature_origin": 45.9,
    "ion_temperature_peaking_factor": 8.06,
    "ion_temperature_pedestal": 6.09,
    "ion_temperature_separatrix": 0.1,
    "major_radius": 9.06,
    "minor_radius": 2.92258,
    "pedestal_radius": 0.8 * 2.92258,
    "plasma_id": 1,
    "shafranov_shift": 0.44789,
    "triangularity": 0.270,
    "ion_temperature_beta": 6,
}

my_plasma = PlasmaSource(**plasma_params)
settings = openmc.Settings()
settings.run_mode = "fixed source"
settings.batches = 10
settings.particles = 1000
source = openmc.Source()
source.library = SOURCE_SAMPLING_PATH
source.parameters = str(my_plasma)
settings.source = source
settings.export_to_xml()
```

## Running Tests

The tests are run by executing `pytest tests` from within your virtual environment.

## C API for use with Fortran

A C API is provided for linking of the plasma source routine to Fortran. This is particularly useful for compilation with MCNP. To compile a static library and a test program a build script is provided in the ```parametric-plasma-source/fortran_api``` folder. This can be run in the following manner:

```[bash]
cd parametric-plasma-source/parametric_plasma_source/fortran_api
./build_lib.sh intel
```
for use with intel ifort and icpc compilers or
```[bash]
cd parametric-plasma-source/parametric_plasma_source/fortran_api
./build_lib.sh gnu
```
for use with the gnu gfortran and g++ compilers.

### Use with MCNP

In order to use the library with MCNPv6.2 the ```plasma_source_module.F90``` and ```mcnp_pp.F90``` should be placed in the MCNP ```src``` folder. The ```source.F90``` provided with MCNP should then be modified to:

```[fortran]
subroutine source

  ! .. Use Statements ..
  use mcnp_interfaces_mod, only : expirx
  use mcnp_debug
  use pp_source_mk2_mod

  implicit none

  call parametric_plasma_2

  return
end subroutine source
```
The MCNP Makefile should also be updated to point to the library during linking. This can be done by adding the first line and modifying the second line in the Makefile:
```
PPLIB = -lplasmasource -L$(PLASMA_SOURCE)
COMPILE_LINE=$(LD) $(OUT_EXE)$(EXEC) $(F_OBJS) $(C_OBJS) $(ALL_LDFLAGS) $(PLOTLIBS) $(LIB_DMMP) $(EXTRALIBS) \
             $(PPLIB)
```
When compiling MCNP the PLASMA_SOURCE variable then needs to be set to the folder containing ```libplasmasource.a```. An example of the compliation line would be:

```
make build CONFIG='intel openmpi omp plot' PLASMA_SOURCE=/plasma/source/dir/
```

The source parameters are passed using the rdum and idum cards in the mcnp input file

```[fortran]
ion_density_pedistal           = rdum(1)
ion_density_seperatrix         = rdum(2)
ion_density_origin             = rdum(3)
ion_temperature_pedistal       = rdum(4)
ion_temperature_seperatrix     = rdum(5)
ion_temperature_origin         = rdum(6)
ion_density_peaking_factor     = rdum(7)
ion_temperature_peaking_factor = rdum(8)
ion_temperature_beta           = rdum(9)
minor_radius                   = rdum(10)
major_radius                   = rdum(11)
pedistal_radius                = rdum(12)
elongation                     = rdum(13)
triangularity                  = rdum(14)
min_toroidal_angle             = rdum(15)
max_toroidal_angle             = rdum(16)
        
number_of_bins                 = idum(2)
plasma_id                      = idum(3)
```
Note that idum(1) is intentionally left unused. This can be used for source selection if multiple user defined sources are to be compiled in the same executable. 
