#!/bin/bash
# Complete analysis pipeline for UK Mansion Tax analysis

set -e  # Exit on error

echo "=========================================="
echo "UK MANSION TAX ANALYSIS - FULL PIPELINE"
echo "=========================================="
echo ""

# Check if data files exist
echo "Checking for required data files..."

if [ ! -f "pp-2024.csv" ]; then
    echo "ERROR: pp-2024.csv not found"
    echo "Run: python download_data.py"
    exit 1
fi

if [ ! -d "Data/multi_csv" ]; then
    echo "ERROR: NSPL postcode data not found"
    echo "Run: python download_data.py"
    exit 1
fi

if [ ! -f "TS003_household_composition_p19wpc.xlsx" ]; then
    echo "ERROR: Census TS003 household data not found"
    echo "Download from: https://statistics.ukdataservice.ac.uk/dataset/ons_2021_ts003_demography_household_composition"
    exit 1
fi

echo "✓ All required data files present"
echo ""

# Run main analysis
echo "=========================================="
echo "Step 1: Running constituency analysis..."
echo "=========================================="
python3 analyze_2024_complete.py

echo ""
echo "=========================================="
echo "Step 2: Generating household impact..."
echo "=========================================="
python3 generate_household_impact.py

echo ""
echo "=========================================="
echo "ANALYSIS COMPLETE!"
echo "=========================================="
echo ""
echo "Generated files:"
echo "  - constituency_impact_2024_1m_COMPLETE.csv"
echo "  - constituency_impact_2024_2m_COMPLETE.csv"
echo "  - mansion_tax_household_impact.csv"
echo "  - mansion_tax_household_impact_2m.csv"
echo ""
echo "See 2024_ANALYSIS_SUMMARY.md for full results."
