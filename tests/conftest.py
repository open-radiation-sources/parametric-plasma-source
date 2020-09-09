import pytest

from parametric_plasma_source import PlasmaSource

plasma_params = {
    "elongation": 1.557,
    "ion_density_origin": 1.09e20,
    "ion_density_peaking_factor": 1,
    "ion_density_pedistal": 1.09e20,
    "ion_density_seperatrix": 3e19,
    "ion_temperature_origin": 45.9,
    "ion_temperature_peaking_factor": 8.06,
    "ion_temperature_pedistal": 6.09,
    "ion_temperature_seperatrix": 0.1,
    "major_radius": 906.0,
    "minor_radius": 292.258,
    "pedistal_radius": 0.8 * 292.258,
    "plasma_id": 1,
    "shafranov_shift": 44.789,
    "triangularity": 0.270,
    "ion_temperature_beta": 6,
}


@pytest.fixture(scope="session")
def plasma_source():
    """Make a plasma source to use as a test fixture."""
    return PlasmaSource(**plasma_params)
