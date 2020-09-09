"""Tests for the methods in plasma_source."""

import math
import os
import pytest
from random import random

from parametric_plasma_source import PlasmaSource


class TestPlasmaSource:
    """A class to run tests against the plasma source."""

    def test_ion_density_magnetic_origin(self, plasma_source):
        """Test the ion density at the magnetic origin."""
        ion_density = plasma_source.ion_density(0.0)

        assert ion_density == pytest.approx(1.09e20)

    def test_ion_density_inside_pedestal(self, plasma_source):
        """Test the ion density inside the pedestal."""
        ion_density = plasma_source.ion_density(20.0)

        assert ion_density == pytest.approx(1.09e20)

    def test_ion_density_outside_pedestal(self, plasma_source):
        """Test the ion density outside the pedestal."""
        ion_density = plasma_source.ion_density(240.0)

        assert ion_density == pytest.approx(1.00629067e20)

    def test_ion_density_boundary(self, plasma_source):
        """Test the ion density at the boundary."""
        ion_density = plasma_source.ion_density(plasma_source.minor_radius)

        assert ion_density == pytest.approx(plasma_source.ion_density_seperatrix)

    def test_ion_temperature_magnetic_origin(self, plasma_source):
        """Test the ion temperature at the magnetic origin."""
        ion_temperature = plasma_source.ion_temperature(0.0)

        assert ion_temperature == pytest.approx(plasma_source.ion_temperature_origin)

    def test_ion_temperature_inside_pedestal(self, plasma_source):
        """Test the ion temperature inside the pedestal."""
        ion_temperature = plasma_source.ion_temperature(20.0)

        assert ion_temperature == pytest.approx(45.89987429)

    def test_ion_temperature_outside_pedestal(self, plasma_source):
        """Test the ion temperature outside the pedestal."""
        ion_temperature = plasma_source.ion_temperature(240.0)

        assert ion_temperature == pytest.approx(5.45529258)

    def test_ion_temperature_boundary(self, plasma_source):
        """Test the ion temperature at the boundary."""
        ion_temperature = plasma_source.ion_temperature(plasma_source.minor_radius)

        assert ion_temperature == pytest.approx(
            plasma_source.ion_temperature_seperatrix
        )

    def test_dt_cross_section(self, plasma_source):
        """Test the dt cross section at a specific temperature."""
        dt_cross_section = plasma_source.dt_xs(4.25e7)

        assert dt_cross_section == pytest.approx(0.0)

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
        sample = plasma_source.sample(randoms)

        assert len(sample) == 7

        # The 4th, 5th and 6th elements together define a unit vector
        direction_length = math.sqrt(sample[3] ** 2 + sample[4] ** 2 + sample[5] ** 2)
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

        sample = plasma_source.sample(randoms)

        assert sample == expected
