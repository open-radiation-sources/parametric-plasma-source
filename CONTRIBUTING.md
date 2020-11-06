# Contributing to parametric-plasma-source

Welcome to parametric-plasma-source - we hope you find the code useful. This guide lays out
a few pointers for how to contribute your own issues or changes to the project.

## Code of Conduct

Participants in the development of the parametric-plasma-source project are governed by the
[Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.
Please report unacceptable behavior to the open-radiation-sources team.

## Raising an Issue

Please report any bugs in the parametric-plasma-source, or suggest any feature enhancements,
via the [Issues](https://github.com/open-radiation-sources/parametric-plasma-source) listed
in GitHub. Before submitting, we ask that you check the currently open issues in case someone
has beaten you to it!

## Submitting Changes

If you would like to actively develop a fix for a bug, or implementation of a feature, then
please indicate so when you raise your Issue. All changes are reviewed via pull requests,
so please create your own fork of the parametric-plasma-source project and create a PR when
your changes are ready.

## Releasing New Versions

New versions of parametric-plasma-source will be released from time to time. This is currently
a semi-manual process, to control the generation of new releases and tags. A release is
initiated by incrementing the `__version__` value in the module's `__init__.py` in the `develop`
branch. When this change is then merged into the `main` branch, a new pre-release build will be
uploaded to [Test PyPI](https://test.pypi.org/project/parametric-plasma-source). The release is
then created in GitHub, which tags the repository with the same version and uploads the release
build to [PyPI](https://pypi.org/project/parametric-plasma-source).
