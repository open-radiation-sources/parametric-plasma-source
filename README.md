# parametric-plasma-source

![Python package](https://github.com/open-radiation-sources/parametric-plasma-source/workflows/Python%20package/badge.svg)
[![ActionsCI](https://github.com/open-radiation-sources/parametric-plasma-source/workflows/python_package/badge.svg)](https://github.com/open-radiation-sources/parametric-plasma-source/actions?query=workflow%3Apython_package)

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
