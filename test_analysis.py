#!/usr/bin/env python3
"""
Unit tests for Scottish Mansion Tax Analysis

Tests validate weight calculations, data integrity, and output correctness.
"""

import pytest
import pandas as pd
from analyze_scottish_parliament_constituencies import (
    analyze_constituencies,
    calculate_wealth_adjusted_weights,
    load_population_data,
    load_wealth_factors,
    CONSTITUENCY_COUNCIL_MAPPING,
    COUNCIL_DATA,
    ESTIMATED_STOCK,
    BAND_I_RATIO,
    BAND_J_RATIO,
    BAND_I_SURCHARGE,
    BAND_J_SURCHARGE,
)


class TestWeightCalculations:
    """Tests for weight calculation correctness."""

    def test_edinburgh_weights_sum_to_one(self):
        """Edinburgh constituency weights should sum to 1.0."""
        df = analyze_constituencies()
        edin = df[df["council"] == "City of Edinburgh"]
        assert abs(edin["weight"].sum() - 1.0) < 0.001

    def test_all_council_weights_sum_to_one(self):
        """Weights within each council should sum to 1.0."""
        df = analyze_constituencies()
        for council in df["council"].unique():
            council_df = df[df["council"] == council]
            weight_sum = council_df["weight"].sum()
            assert abs(weight_sum - 1.0) < 0.001, (
                f"{council} weights sum to {weight_sum}, expected 1.0"
            )

    def test_weights_are_non_negative(self):
        """All weights should be non-negative (0 is valid for areas with no Band H)."""
        df = analyze_constituencies()
        assert (df["weight"] >= 0).all(), "All weights should be non-negative"

    def test_weights_not_exceed_one(self):
        """No individual weight should exceed 1.0."""
        df = analyze_constituencies()
        assert (df["weight"] <= 1.0).all(), "No weight should exceed 1.0"


class TestConstituencyMapping:
    """Tests for constituency mapping completeness."""

    def test_all_73_constituencies_mapped(self):
        """All 73 Scottish Parliament constituencies should be mapped."""
        assert len(CONSTITUENCY_COUNCIL_MAPPING) == 73

    def test_all_constituencies_in_output(self):
        """Output should contain all 73 constituencies."""
        df = analyze_constituencies()
        assert len(df) == 73

    def test_no_duplicate_constituencies(self):
        """No duplicate constituency entries in output."""
        df = analyze_constituencies()
        assert df["constituency"].nunique() == len(df)


class TestRevenueCalculations:
    """Tests for revenue calculation correctness."""

    def test_total_revenue_approximately_18_5m(self):
        """Total allocated revenue should be approximately £18.5m."""
        df = analyze_constituencies()
        total_revenue = df["allocated_revenue"].sum()
        # Allow 1% tolerance for rounding
        expected = ESTIMATED_STOCK * (
            BAND_I_RATIO * BAND_I_SURCHARGE + BAND_J_RATIO * BAND_J_SURCHARGE
        )
        assert abs(total_revenue - expected) / expected < 0.01

    def test_share_percentages_sum_to_100(self):
        """Share percentages should sum to approximately 100%."""
        df = analyze_constituencies()
        # Only count constituencies with sales
        df_with_sales = df[df["estimated_sales"] > 0]
        share_sum = df_with_sales["share_pct"].sum()
        assert abs(share_sum - 100.0) < 0.1, (
            f"Shares sum to {share_sum}%, expected ~100%"
        )

    def test_band_split_matches_ratios(self):
        """Band I/J sales should match expected ratios."""
        df = analyze_constituencies()
        total_band_i = df["band_i_sales"].sum()
        total_band_j = df["band_j_sales"].sum()
        total_sales = total_band_i + total_band_j

        actual_i_ratio = total_band_i / total_sales
        actual_j_ratio = total_band_j / total_sales

        assert abs(actual_i_ratio - BAND_I_RATIO) < 0.001
        assert abs(actual_j_ratio - BAND_J_RATIO) < 0.001


class TestWealthFactors:
    """Tests for wealth factor loading and application."""

    def test_wealth_factors_load(self):
        """Wealth factors should load successfully."""
        factors, _ = load_wealth_factors()
        assert len(factors) > 0

    def test_wealth_factors_non_negative(self):
        """All wealth factors should be non-negative."""
        factors, _ = load_wealth_factors()
        assert all(f >= 0 for f in factors.values())


class TestDataIntegrity:
    """Tests for data integrity and consistency."""

    def test_population_data_loads(self):
        """Population data should load successfully."""
        df = load_population_data()
        assert len(df) > 0
        assert "constituency" in df.columns
        assert "population" in df.columns

    def test_council_data_not_empty(self):
        """Council sales data should not be empty."""
        assert sum(COUNCIL_DATA.values()) > 0

    def test_all_councils_mapped(self):
        """All councils in COUNCIL_DATA should have at least one constituency."""
        councils_in_mapping = set(CONSTITUENCY_COUNCIL_MAPPING.values())
        councils_in_data = set(COUNCIL_DATA.keys())
        # All councils with data should be in mapping
        assert councils_in_data.issubset(councils_in_mapping), (
            f"Unmapped councils: {councils_in_data - councils_in_mapping}"
        )


class TestOutputFormat:
    """Tests for output format correctness."""

    def test_required_columns_present(self):
        """All required columns should be present in output."""
        df = analyze_constituencies()
        required_columns = [
            "constituency",
            "council",
            "population",
            "wealth_factor",
            "weight",
            "estimated_sales",
            "band_i_sales",
            "band_j_sales",
            "share_pct",
            "implied_from_sales",
            "allocated_revenue",
        ]
        for col in required_columns:
            assert col in df.columns, f"Missing column: {col}"

    def test_no_negative_values(self):
        """Numeric columns should not have negative values."""
        df = analyze_constituencies()
        numeric_cols = [
            "population",
            "weight",
            "estimated_sales",
            "band_i_sales",
            "band_j_sales",
            "share_pct",
            "allocated_revenue",
        ]
        for col in numeric_cols:
            assert (df[col] >= 0).all(), f"Negative values in {col}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
