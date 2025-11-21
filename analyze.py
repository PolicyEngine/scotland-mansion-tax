#!/usr/bin/env python3
"""
UK Mansion Tax Analysis - 2024

Analyzes property sales above £1.5m and £2m thresholds by Westminster constituency.
Generates constituency-level statistics and household impact percentages.
"""

import pandas as pd
import glob

def load_constituency_lookup():
    """Load constituency code to name mapping."""
    lookup_path = "data/Westminster_Parliamentary_Constituency_names_and_codes_UK_as_at_12_24.csv"
    df = pd.read_csv(lookup_path)
    return dict(zip(df['PCON24CD'], df['PCON24NM']))

def load_postcode_mapping():
    """Load NSPL postcode to constituency mapping."""
    csv_files = glob.glob("data/NSPL/NSPL_FEB_2025_UK_*.csv")
    dfs = [pd.read_csv(f, usecols=['pcds', 'pcon']) for f in csv_files]
    postcode_lookup = pd.concat(dfs, ignore_index=True)
    return postcode_lookup.dropna(subset=['pcon'])

def load_household_data():
    """Load Census 2021 household counts."""
    df = pd.read_excel('data/TS003_household_composition_p19wpc.xlsx', sheet_name='Dataset')
    df = df[df['Household composition (15 categories)'] != 'Does not apply']
    households = df.groupby([
        'Post-2019 Westminster Parliamentary constituencies Code',
        'Post-2019 Westminster Parliamentary constituencies'
    ])['Observation'].sum().reset_index()
    households.columns = ['constituency_code', 'constituency_name', 'total_households']
    return households

def analyze_threshold(threshold, const_names, postcode_to_const, households):
    """Analyze properties above threshold by constituency."""
    threshold_label = f'{threshold//1_000_000}m'

    # Load and filter property data
    df = pd.read_csv('data/pp-2024.csv', header=None, names=[
        'transaction_id', 'price', 'date', 'postcode', 'property_type',
        'old_new', 'duration', 'paon', 'saon', 'street', 'locality',
        'town', 'district', 'county', 'ppd_category', 'record_status'
    ])
    df = df[df['price'] >= threshold]

    # Match to constituencies
    df['pcds'] = df['postcode'].str.strip().str.upper()
    df = df.merge(postcode_to_const, on='pcds', how='left')
    df['constituency_name'] = df['pcon'].map(const_names)

    # Calculate constituency stats
    const_stats = df[df['pcon'].notna()].groupby('constituency_name').agg({
        'price': ['count', 'mean', 'median', 'sum']
    }).round(0)
    const_stats.columns = ['num_sales', 'mean_price', 'median_price', 'total_value']
    const_stats['estimated_annual_revenue'] = const_stats['num_sales'] * 2000
    const_stats = const_stats.sort_values('num_sales', ascending=False)

    # Add household percentages
    const_stats = const_stats.merge(households[['constituency_name', 'total_households']],
                                     left_index=True, right_on='constituency_name', how='left')
    const_stats['pct_households_affected'] = (
        const_stats['num_sales'] / const_stats['total_households'] * 100
    ).round(3)

    # Save outputs
    const_stats.to_csv(f'constituency_impact_{threshold_label}.csv')

    # Save household impact file
    household_impact = const_stats[['constituency_name', 'pct_households_affected']].copy()
    household_impact['avg_loss_per_household'] = 2000
    household_impact = household_impact.sort_values('pct_households_affected', ascending=False)
    household_impact.to_csv(f'household_impact_{threshold_label}.csv', index=False)

    return const_stats

if __name__ == '__main__':
    print("Loading reference data...")
    const_names = load_constituency_lookup()
    postcode_to_const = load_postcode_mapping()
    households = load_household_data()

    print("\nAnalyzing £1.5m threshold...")
    stats_1_5m = analyze_threshold(1_500_000, const_names, postcode_to_const, households)
    print(f"  {len(stats_1_5m)} constituencies affected")
    print(f"  {stats_1_5m['num_sales'].sum():.0f} total sales")

    print("\nAnalyzing £2m threshold...")
    stats_2m = analyze_threshold(2_000_000, const_names, postcode_to_const, households)
    print(f"  {len(stats_2m)} constituencies affected")
    print(f"  {stats_2m['num_sales'].sum():.0f} total sales")

    print("\nDone. Generated:")
    print("  constituency_impact_1m.csv")
    print("  constituency_impact_2m.csv")
    print("  household_impact_1m.csv")
    print("  household_impact_2m.csv")
