from distutils import dir_util
import os
import subprocess
import sys

from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext


with open("parametric_plasma_source/__init__.py", "r") as f:
    for line in f.readlines():
        if "__version__" in line:
            version = line.split()[-1].strip('"')


class CMakeExtention(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pybind11==2.6.0"])
        try:
            subprocess.check_output(["cmake", "--version"])
        except FileNotFoundError:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "cmake==3.18.2"])
            except OSError:
                raise RuntimeError(
                    "CMake must be installed to build the "
                    "following extentions: "
                    ", ".join(e.name for e in self.extensions)
                )

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        import pybind11

        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + extdir,
            "-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY=" + extdir,
            "-DPYTHON_EXECUTABLE=" + sys.executable,
            "-DPYBIND11_PATH=" + os.path.abspath(os.path.dirname(pybind11.__file__))
        ]

        cfg = "Debug" if self.debug else "Release"
        build_args = ["--config", cfg]

        cmake_args += ["-DCMAKE_BUILD_TYPE=" + cfg]
        build_args += ["--", "-j2"]

        env = os.environ.copy()
        env["CXXFLAGS"] = '{} -DVERSION_INFO=\\"{}\\"'.format(
            env.get("CXXFLAGS", ""), self.distribution.get_version()
        )

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(
            ["cmake", extdir] + cmake_args, cwd=self.build_temp, env=env
        )
        subprocess.check_call(
            ["cmake", "--build", "."] + build_args, cwd=self.build_temp
        )


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="parametric_plasma_source",
    version=version,
    author="Andrew Davis",
    author_email="jonathan.shimwell@ukaea.uk",
    description="Parametric plasma source for fusion simulations in OpenMC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/makeclean/parametric-plasma-source/",
    packages=["parametric_plasma_source"],
    ext_modules=[CMakeExtention("parametric_plasma_source/plasma_source")],
    package_data={
        "parametric_plasma_source": [
            "src/plasma_source*",
            "src/source_sampling*",
            "CMakeLists.txt",
        ]
    },
    cmdclass=dict(build_ext=CMakeBuild),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
