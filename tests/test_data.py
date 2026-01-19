#!/usr/bin/env python3
"""
Unit tests for Scottish Mansion Tax Analysis - Data module.

Tests validate data loading and downloading functionality.
"""

import pytest

from scotland_mansion_tax.data import (
    load_population_data,
    load_wealth_factors,
)


class TestPopulationData:
    """Tests for population data loading."""

    def test_population_data_loads(self):
        """Population data should load successfully."""
        df = load_population_data(verbose=False)
        assert len(df) > 0
        assert "constituency" in df.columns
        assert "population" in df.columns

    def test_population_data_has_73_constituencies(self):
        """Population data should have 73 constituencies."""
        df = load_population_data(verbose=False)
        assert len(df) == 73

    def test_population_values_reasonable(self):
        """Population values should be reasonable (>10k, <200k)."""
        df = load_population_data(verbose=False)
        assert (df["population"] > 10000).all()
        assert (df["population"] < 200000).all()


class TestWealthFactors:
    """Tests for wealth factor loading."""

    def test_wealth_factors_load(self):
        """Wealth factors should load successfully."""
        factors, _ = load_wealth_factors(verbose=False)
        assert len(factors) > 0

    def test_wealth_factors_non_negative(self):
        """All wealth factors should be non-negative (0 is valid for areas with no Band H)."""
        factors, _ = load_wealth_factors(verbose=False)
        assert all(f >= 0 for f in factors.values())


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
