import os
import subprocess
import warnings

__version__ = "0.0.9.dev3"

PLASMA_SOURCE_PATH = os.path.dirname(__file__)
SOURCE_SAMPLING_PATH = os.sep.join([PLASMA_SOURCE_PATH, "source_sampling.so"])
SOURCE_GENERATOR_PATH = os.sep.join([PLASMA_SOURCE_PATH, "source_generator"])

HAS_OPENMC = True
try:
    from .plasma_source import *
except ImportError:
    HAS_OPENMC = False
    warnings.warn("The plasma_source module could not be found. Please compile before using.")


def sample_source_openmc(
    source,
    source_sampling_path=SOURCE_SAMPLING_PATH,
    num_particles=1000,
    output_dir=".",
    verbosity=5
):
    """
    Sample a source using OpenMC

    Parameters
    ----------
    source: PlasmaSource
        The source to sample.
    source_sampling_path: str
        Optional path to the OpenMC source plugin to use for the sampling, by default the
        packaged source sampling shared object.
    num_particles: int
        Optional number of particles to sample, by default 1000.
    output_dir: str
        Optional path to directory that the output h5 file will be written to, by default
        the current directory.
    verbosity: int
        Optional verbosity level, by default 5.

    Returns
    -------
    output: CompletedProcess
        The output from the source sampling process.
    """
    if HAS_OPENMC:
        source_generator_args = [
            SOURCE_GENERATOR_PATH,
            "-l",
            SOURCE_SAMPLING_PATH,
            "-i",
            str(source),
            "-n",
            str(num_particles),
            "-o",
            output_dir,
            "-v",
            str(verbosity)
        ]
        return subprocess.run(source_generator_args, check=True, stdout=subprocess.PIPE)
    else:
        raise RuntimeError("Unable to sample using OpenMC as OpenMC is not installed.")
