"""Tests for the methods in plasma_source."""

import pytest

from parametric_plasma_source.plasma_source import PlasmaSource

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


class TestPlasmaSource:
    """A class to run tests against the plasma source."""

    def test_ion_density_magnetic_origin(self, plasma_source):
        """Test the ion density at the magnetic origin."""
        ion_density = plasma_source.ion_density(0.0)

        assert pytest.approx(ion_density, 1.09e20)

    def test_ion_density_inside_pedestal(self, plasma_source):
        """Test the ion density inside the pedestal."""
        ion_density = plasma_source.ion_density(0.2)

        assert pytest.approx(ion_density, 1.09e20)

    def test_ion_density_outside_pedestal(self, plasma_source):
        """Test the ion density outside the pedestal."""
        ion_density = plasma_source.ion_density(2.4)

        assert pytest.approx(ion_density, 1.00628584e20)

    def test_ion_density_boundary(self, plasma_source):
        """Test the ion density at the boundary."""
        boundary = plasma_params["minor_radius"] / 100.0
        ion_density = plasma_source.ion_density(boundary)

        assert pytest.approx(
            ion_density, plasma_params["ion_density_seperatrix"]
        )

    def test_ion_temperature_magnetic_origin(self, plasma_source):
        """Test the ion temperature at the magnetic origin."""
        ion_temperature = plasma_source.ion_temperature(0.0)

        assert pytest.approx(
            ion_temperature, plasma_params["ion_temperature_origin"]
        )

    def test_ion_temperature_inside_pedestal(self, plasma_source):
        """Test the ion temperature inside the pedestal."""
        ion_temperature = plasma_source.ion_temperature(0.2)

        assert pytest.approx(ion_temperature, 45.89987429)

    def test_ion_temperature_outside_pedestal(self, plasma_source):
        """Test the ion temperature outside the pedestal."""
        ion_temperature = plasma_source.ion_temperature(2.4)

        assert pytest.approx(ion_temperature, 5.45525594)

    def test_ion_temperature_boundary(self, plasma_source):
        """Test the ion temperature at the boundary."""
        boundary = plasma_params["minor_radius"] / 100.0
        ion_temperature = plasma_source.ion_temperature(boundary)

        assert pytest.approx(
            ion_temperature, plasma_params["ion_temperature_seperatrix"]
        )

    def test_dt_cross_section(self, plasma_source):
        """Test the dt cross section at a specific temperature."""
        dt_cross_section = plasma_source.dt_xs(4.25e7)

        assert pytest.approx(dt_cross_section, 0.0)
