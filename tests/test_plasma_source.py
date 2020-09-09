"""Tests for the methods in plasma_source."""

import math
import os
import pytest
from random import random

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

        assert pytest.approx(ion_density, plasma_params["ion_density_seperatrix"])

    def test_ion_temperature_magnetic_origin(self, plasma_source):
        """Test the ion temperature at the magnetic origin."""
        ion_temperature = plasma_source.ion_temperature(0.0)

        assert pytest.approx(ion_temperature, plasma_params["ion_temperature_origin"])

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

    def test_source_to_from_string(self, plasma_source):
        """Test the source can be converted to and from a string."""
        the_str = str(plasma_source)
        new_source = PlasmaSource.from_string(the_str)

        assert id(plasma_source) != id(new_source)
        assert str(new_source) == the_str

    def test_source_string_regression(self, plasma_source):
        """Test the source string representation matches the baseline."""
        baseline_file = os.sep.join(
            [os.path.dirname(__file__), "test_data", "baseline_source.txt"]
        )
        with open(baseline_file, "r") as f:
            baseline_str = f.read().strip()

        the_str = str(plasma_source)
        assert baseline_str == the_str

    def test_sampling(self, plasma_source):
        """Test the sampling function."""
        randoms = [r() for r in [random] * 8]
        sample = plasma_source.sample_source(randoms)

        assert len(sample) == 7

        # The 4th, 5th and 6th elements together define a unit vector
        direction_length = math.sqrt(sample[3]**2 + sample[4]**2 + sample[5]**2)
        assert direction_length == pytest.approx(1.0)

    def test_sampling_regression(self, plasma_source):
        """Test the sampling function returns matching results."""
        randoms = [
            0.17213994440390412,
            0.9186868218670968,
            0.5789738834800362,
            0.08876642179434446,
            0.9556278780110383,
            0.8967227763309567,
            0.5187262083328932,
            0.09064281320718603,
        ]

        expected = (
            490.1585757452634,
            785.7624748651705,
            -19.32184336005464,
            -0.5702309715680232,
            -0.06740484811110535,
            0.8187143735856279,
            14.202333312096737,
        )

        sample = plasma_source.sample_source(randoms)

        assert sample == expected
