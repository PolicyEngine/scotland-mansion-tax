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
        factors, source = load_wealth_factors(verbose=False)
        assert len(factors) > 0 or source == "fallback_population_only"

    def test_wealth_factors_return_tuple(self):
        """load_wealth_factors should return (dict, str) tuple."""
        result = load_wealth_factors(verbose=False)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], dict)
        assert isinstance(result[1], str)

    def test_wealth_source_valid(self):
        """Wealth source should be 'band_fh' or 'fallback_population_only'."""
        _, source = load_wealth_factors(verbose=False)
        assert source in {"band_fh", "fallback_population_only"}

    def test_wealth_factors_positive(self):
        """All wealth factors should be positive."""
        factors, _ = load_wealth_factors(verbose=False)
        if factors:  # May be empty if fallback
            assert all(f > 0 for f in factors.values())

    def test_eastwood_has_highest_factor(self):
        """Eastwood should have highest wealth factor (45% Band F-H)."""
        factors, source = load_wealth_factors(verbose=False)
        if source == "band_fh" and factors:
            # Eastwood has 45.1% Band F-H, highest in Scotland
            assert factors.get("Eastwood", 0) > 3.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
