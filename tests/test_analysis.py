#!/usr/bin/env python3
"""
Unit tests for Scottish Mansion Tax Analysis - Analysis module.

Tests validate weight calculations, data integrity, and output correctness.
"""

import pytest

from scotland_mansion_tax.analysis import (
    BAND_I_RATIO,
    BAND_I_SURCHARGE,
    BAND_J_RATIO,
    BAND_J_SURCHARGE,
    CONSTITUENCY_COUNCIL_MAPPING,
    COUNCIL_DATA,
    ESTIMATED_STOCK,
    analyze_constituencies,
    calculate_wealth_adjusted_weights,
)


class TestWeightCalculations:
    """Tests for weight calculation correctness."""

    def test_edinburgh_weights_sum_to_one(self):
        """Edinburgh constituency weights should sum to 1.0."""
        df = analyze_constituencies(verbose=False)
        edin = df[df["council"] == "City of Edinburgh"]
        assert abs(edin["weight"].sum() - 1.0) < 0.001

    def test_all_council_weights_sum_to_one(self):
        """Weights within each council should sum to 1.0."""
        df = analyze_constituencies(verbose=False)
        for council in df["council"].unique():
            council_df = df[df["council"] == council]
            weight_sum = council_df["weight"].sum()
            assert abs(weight_sum - 1.0) < 0.001, (
                f"{council} weights sum to {weight_sum}, expected 1.0"
            )

    def test_weights_are_positive(self):
        """All weights should be positive."""
        df = analyze_constituencies(verbose=False)
        assert (df["weight"] > 0).all(), "All weights should be positive"

    def test_weights_not_exceed_one(self):
        """No individual weight should exceed 1.0."""
        df = analyze_constituencies(verbose=False)
        assert (df["weight"] <= 1.0).all(), "No weight should exceed 1.0"


class TestConstituencyMapping:
    """Tests for constituency mapping completeness."""

    def test_all_73_constituencies_mapped(self):
        """All 73 Scottish Parliament constituencies should be mapped."""
        assert len(CONSTITUENCY_COUNCIL_MAPPING) == 73

    def test_all_constituencies_in_output(self):
        """Output should contain all 73 constituencies."""
        df = analyze_constituencies(verbose=False)
        assert len(df) == 73

    def test_no_duplicate_constituencies(self):
        """No duplicate constituency entries in output."""
        df = analyze_constituencies(verbose=False)
        assert df["constituency"].nunique() == len(df)


class TestRevenueCalculations:
    """Tests for revenue calculation correctness."""

    def test_total_revenue_approximately_18_5m(self):
        """Total allocated revenue should be approximately £18.5m."""
        df = analyze_constituencies(verbose=False)
        total_revenue = df["allocated_revenue"].sum()
        expected = ESTIMATED_STOCK * (
            BAND_I_RATIO * BAND_I_SURCHARGE + BAND_J_RATIO * BAND_J_SURCHARGE
        )
        # Allow 1% tolerance for rounding
        assert abs(total_revenue - expected) / expected < 0.01

    def test_share_percentages_sum_to_100(self):
        """Share percentages should sum to approximately 100%."""
        df = analyze_constituencies(verbose=False)
        # Only count constituencies with sales
        df_with_sales = df[df["estimated_sales"] > 0]
        share_sum = df_with_sales["share_pct"].sum()
        assert abs(share_sum - 100.0) < 0.1, (
            f"Shares sum to {share_sum}%, expected ~100%"
        )

    def test_band_split_matches_ratios(self):
        """Band I/J sales should match expected ratios."""
        df = analyze_constituencies(verbose=False)
        total_band_i = df["band_i_sales"].sum()
        total_band_j = df["band_j_sales"].sum()
        total_sales = total_band_i + total_band_j

        actual_i_ratio = total_band_i / total_sales
        actual_j_ratio = total_band_j / total_sales

        assert abs(actual_i_ratio - BAND_I_RATIO) < 0.001
        assert abs(actual_j_ratio - BAND_J_RATIO) < 0.001


class TestWealthFactors:
    """Tests for wealth factor loading and application."""

    def test_wealth_data_source_column_present(self):
        """Output should include wealth_data_source column."""
        df = analyze_constituencies(verbose=False)
        assert "wealth_data_source" in df.columns

    def test_wealth_data_source_valid_values(self):
        """wealth_data_source should be 'band_fh' or 'fallback_population_only'."""
        df = analyze_constituencies(verbose=False)
        valid_sources = {"band_fh", "fallback_population_only"}
        assert df["wealth_data_source"].isin(valid_sources).all()

    def test_edinburgh_central_higher_factor_than_pentlands(self):
        """Edinburgh Central should have higher wealth factor than Pentlands."""
        df = analyze_constituencies(verbose=False)
        central = df[df["constituency"] == "Edinburgh Central"]["wealth_factor"].values[0]
        pentlands = df[df["constituency"] == "Edinburgh Pentlands"]["wealth_factor"].values[0]
        # Edinburgh Central (New Town, Stockbridge) should be wealthier
        assert central > pentlands, (
            f"Expected Edinburgh Central ({central}) > Edinburgh Pentlands ({pentlands})"
        )


class TestDataIntegrity:
    """Tests for data integrity and consistency."""

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
        df = analyze_constituencies(verbose=False)
        required_columns = [
            "constituency",
            "council",
            "population",
            "wealth_factor",
            "wealth_data_source",
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
        df = analyze_constituencies(verbose=False)
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
