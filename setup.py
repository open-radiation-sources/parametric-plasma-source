import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="parametric_plasma_source",
    version="0.0.6",
    author="Jonathan Shimwell",
    author_email="jonathan.shimwell@ukaea.uk",
    description="Parametric plasma source for fusion simulations in OpenMC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shimwell/parametric_plasma_source",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)