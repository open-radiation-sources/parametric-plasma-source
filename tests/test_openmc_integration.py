"""Test sampling via OpenMC."""

import pytest

from parametric_plasma_source import sample_source_openmc

pytest.importorskip("openmc")


class TestOpenMCIntegration:
    def test_openmc_integration(self, plasma_source):
        out = sample_source_openmc(plasma_source)
        assert out.stderr is None
        assert "Source sampling completed." in out.stdout.decode("utf-8")
