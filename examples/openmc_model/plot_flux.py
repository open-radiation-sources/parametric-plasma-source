import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import openmc

mpl.use("TkAgg")

# Get the flux from the statepoint
with openmc.StatePoint("statepoint.10.h5") as sp:
    flux = np.log(sp.get_tally(scores=["flux"]).mean)
    flux.shape = (50, 50)

# Plot the flux
fig, ax = plt.subplots()
ax.imshow(flux, origin="lower", extent=(-2000.0, 2000.0, -2000.0, 2000.0))
ax.set_xlabel("x [cm]")
ax.set_ylabel("y [cm]")
plt.show()
