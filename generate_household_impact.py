#!/usr/bin/env python3
"""
Generate household impact analysis for UK mansion tax.

Calculates the percentage of households affected by the proposed mansion tax
in each constituency by merging:
- 2024 property sales above thresholds (from analyze_2024_complete.py)
- Census 2021 household counts (from TS003 data)

Outputs:
- mansion_tax_household_impact.csv (£1.5m threshold)
- mansion_tax_household_impact_2m.csv (£2m threshold)
"""

import pandas as pd
import glob

def load_household_data():
    """Load Census 2021 household composition data."""
    print("Loading Census 2021 household data...")

    # Load TS003 Excel file
    df = pd.read_excel('TS003_household_composition_p19wpc.xlsx', sheet_name='Dataset')

    # Filter out "Does not apply" category
    df = df[df['Household composition (15 categories)'] != 'Does not apply']

    # Sum observations by constituency to get total households
    households = df.groupby([
        'Post-2019 Westminster Parliamentary constituencies Code',
        'Post-2019 Westminster Parliamentary constituencies'
    ])['Observation'].sum().reset_index()

    households.columns = ['constituency_code', 'constituency_name', 'total_households']

    print(f"Loaded household data for {len(households)} constituencies")
    return households

def generate_impact_csv(threshold_label, threshold_value):
    """Generate household impact CSV for a given threshold."""
    print(f"\n{'='*80}")
    print(f"Generating household impact analysis: £{threshold_value:,} threshold")
    print(f"{'='*80}\n")

    # Load data
    households = load_household_data()
    impact = pd.read_csv(f'constituency_impact_2024_{threshold_label}_COMPLETE.csv')

    # Merge
    merged = impact.merge(households, on='constituency_name', how='left')

    # Calculate percentages
    merged['pct_households_affected'] = (
        merged['num_sales'] / merged['total_households'] * 100
    ).round(3)
    merged['avg_loss_per_household'] = 2000  # Fixed surcharge

    # Create output
    output = merged[[
        'constituency_name',
        'pct_households_affected',
        'avg_loss_per_household'
    ]].copy()
    output = output.sort_values('pct_households_affected', ascending=False)

    # Save
    output_file = f'mansion_tax_household_impact_{threshold_label}.csv' if threshold_label == '2m' else 'mansion_tax_household_impact.csv'
    output.to_csv(output_file, index=False)

    # Display summary
    print(f"✓ Generated {output_file}")
    print(f"\nTop 10 constituencies:")
    print(output.head(10).to_string(index=False))
    print(f"\nSummary Statistics:")
    print(f"  Constituencies: {len(output)}")
    print(f"  Avg % affected: {output['pct_households_affected'].mean():.3f}%")
    print(f"  Median % affected: {output['pct_households_affected'].median():.3f}%")
    print(f"  Max % affected: {output['pct_households_affected'].max():.3f}%")

    return output

if __name__ == '__main__':
    print("="*80)
    print("UK MANSION TAX - HOUSEHOLD IMPACT ANALYSIS")
    print("="*80)

    # Check required files exist
    required_files = [
        'TS003_household_composition_p19wpc.xlsx',
        'constituency_impact_2024_1m_COMPLETE.csv',
        'constituency_impact_2024_2m_COMPLETE.csv'
    ]

    missing = [f for f in required_files if not pd.io.common.file_exists(f)]
    if missing:
        print("\nERROR: Missing required files:")
        for f in missing:
            print(f"  - {f}")
        print("\nRun analyze_2024_complete.py first to generate constituency impact files.")
        print("Download TS003 household data from UK Data Service (see README.md).")
        exit(1)

    # Generate both threshold analyses
    impact_1_5m = generate_impact_csv('1m', 1_500_000)
    impact_2m = generate_impact_csv('2m', 2_000_000)

    print("\n" + "="*80)
    print("HOUSEHOLD IMPACT ANALYSIS COMPLETE!")
    print("="*80)
    print("\nGenerated files:")
    print("  - mansion_tax_household_impact.csv (£1.5m threshold)")
    print("  - mansion_tax_household_impact_2m.csv (£2m threshold)")
