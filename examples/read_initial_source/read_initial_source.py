"""
An example of how to read an initial_source.h5 file, as generated from source_generator

In order to create the initial source, first build the source_generator and then run
the below, which will create an example source and sample it 1000 times.

../../build/source_generator -l ../../build/source_sampling.so -i "major_radius=9.06, \
minor_radius=2.92258, elongation=1.557, triangularity=0.27, shafranov_shift=0.44789, \
pedestal_radius=2.33806, ion_density_pedestal=1.09e+20, ion_density_separatrix=3e+19, \
ion_density_origin=1.09e+20, ion_density_alpha=1, ion_temperature_pedestal=6.09, \
ion_temperature_separatrix=0.1, ion_temperature_origin=45.9, \
ion_temperature_alpha=8.06, ion_temperature_beta=6, plasma_type=plasma, plasma_id=1, \
number_of_bins=100, minimum_toroidal_angle=0, maximum_toroidal_angle=360" \
-v 10 -n 1000
"""

import h5py
import matplotlib.pyplot as plt
import numpy as np

path_to_initial_source = "initial_source.h5"

with h5py.File(path_to_initial_source, "r") as f:
    r = np.sqrt(
        np.square(f["source_bank"][...]["r"]["x"])
        + np.square(f["source_bank"][...]["r"]["y"])
    )
    z = f["source_bank"][...]["r"]["z"]

plt.scatter(r, z)

plt.ion()
plt.show()
plt.gca().set_aspect("equal")
