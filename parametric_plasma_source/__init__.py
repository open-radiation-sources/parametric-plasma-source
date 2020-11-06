import os

__version__ = "0.0.9.dev2"

PLASMA_SOURCE_PATH = os.path.dirname(__file__)
SOURCE_SAMPLING_PATH = os.sep.join([PLASMA_SOURCE_PATH, "source_sampling.so"])

try:
    from .plasma_source import *
except ImportError:
    print("The plasma_source module could not be found. Please compile before using.")
