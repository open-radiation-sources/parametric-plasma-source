# parametric-plasma-source
Source and build files for parametric plasma source for use in fusion neutron transport calculations.

The plasma source is based on a paper by [C. Fausser et al](https://www.sciencedirect.com/science/article/pii/S0920379612000853)

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
