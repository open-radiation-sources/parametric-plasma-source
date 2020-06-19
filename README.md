# parametric-plasma-source

Python package, C++ source and build files for parametric plasma source for use in fusion neutron transport calculations with OpenMC.

The plasma source is based on a paper by [C. Fausser et al](https://www.sciencedirect.com/science/article/pii/S0920379612000853)

# Installation

```pip install parametric_plasma_source```

# Usage

The parametric plasma source can be imported an used in Python 3 in the following manner.

```
from parametric_plasma_source import Plasma
my_plasma = Plasma(major_radius=6,
                   minor_radius=1.5,
                   elongation = 2.0
                   triangularity = 0.55)
my_plasma.export_plasma_source('custom_openmc_plasma_source.so')
```

In the above example the major_radius, minor_radius, elongation and triangularity while the other varibles are kept as the default values.

There are a number of additional arguments that can be passed to the Plasma class on construction. Units are in SI (e.g. meters not cm)

```
ion_density_pedistal = 1.09e+20
ion_density_seperatrix = 3e+19
ion_density_origin = 1.09e+20
ion_temperature_pedistal = 6.09
ion_temperature_seperatrix = 0.1
ion_temperature_origin = 45.9
pedistal_radius = 0.8
ion_density_peaking_factor = 1
ion_temperature_peaking_factor = 8.06
minor_radius = 1.56
major_radius = 2.5
elongation = 2.0
triangularity = 0.55
shafranov_shift = 0.0
number_of_bins = 100
plasma_type = 1
```

For a better understanding of the varibles take a look at the [C. Fausser et al](https://www.sciencedirect.com/science/article/pii/S0920379612000853) paper.

## Building and Running

Note: When building using the `Makefile` you may need to update the `OPENMC_DIR` parameter to select a relevant directory to obtain the OpenMC libraries and includes from.

The OpenMC plugin that samples the plasma source is built by running `make` or `make source_sampling` from within the parametric-plasma-source directory. This will generate the `source_sampling.so` shared object library, which can be referenced by the `library` attribute in the `source` element within the settings.xml being used for the run.

It is also possible to generate a source outside of OpenMC by creating the `source_generator` executable by running `make` or `make source_generator` from within the parameteric-plasma-source directory. The `source_generator` can then be run as below:

```bash
Usage:
source_generator [OPTIONS]

Options:
 -l,--library      Source library, mandatory
 -n,--particles    Number of particles, default 1000
 -o,--output       Output directory, default {current directory}
 -v,--verbosity    Verbosity, default 5
 ```

This will use OpenMC commands to sample the source generated using the specified library with the specified number of particles and output the resulting `initial_source.h5` file in the requested output directory. The `initial_source.h5` can then be analysed to check the properties of the source being generated.
