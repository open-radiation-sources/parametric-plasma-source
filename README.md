# parametric-plasma-source

![Python package](https://github.com/DanShort12/parametric-plasma-source/workflows/Python%20package/badge.svg)

Python package, C++ source and build files for parametric plasma source for use in fusion neutron transport calculations with OpenMC.

The plasma source is based on a paper by [C. Fausser et al](https://www.sciencedirect.com/science/article/pii/S0920379612000853)

## Installation

```pip install parametric_plasma_source```

## Usage

The parametric plasma source can be imported an used in Python 3 in the following manner.

```[python]
from parametric_plasma_source import Plasma
my_plasma = Plasma(major_radius=6,
                   minor_radius=1.5,
                   elongation = 2.0
                   triangularity = 0.55)
my_plasma.export_plasma_source('custom_openmc_plasma_source.so')
```

In the above example the major_radius, minor_radius, elongation and triangularity while the other varibles are kept as the default values.

There are a number of additional arguments that can be passed to the Plasma class on construction. Units are in SI (e.g. meters not cm)

```[python]
ion_density_pedestal = 1.09e+20
ion_density_separatrix = 3e+19
ion_density_origin = 1.09e+20
ion_temperature_pedestal = 6.09
ion_temperature_separatrix = 0.1
ion_temperature_origin = 45.9
pedestal_radius = 0.8
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
