#!/usr/bin/env python3
"""
Complete 2024 mansion tax analysis with full NSPL constituency mapping.
"""

import pandas as pd
import glob

def load_constituency_lookup():
    """Load constituency code to name mapping."""
    lookup_path = "Documents/Westminster Parliamentary Constituency names and codes UK as at 12_24.csv"
    df = pd.read_csv(lookup_path)
    lookup = dict(zip(df['PCON24CD'], df['PCON24NM']))
    print(f"Loaded {len(lookup)} constituency names")
    return lookup

def load_postcode_mapping():
    """Load full NSPL postcode to constituency mapping."""
    print("\nLoading NSPL postcode data...")
    csv_files = glob.glob("Data/multi_csv/NSPL_FEB_2025_UK_*.csv")
    print(f"Found {len(csv_files)} postcode area files")

    dfs = []
    for i, csv_file in enumerate(csv_files):
        if i % 20 == 0:
            print(f"  Loading file {i+1}/{len(csv_files)}...")
        df = pd.read_csv(csv_file, usecols=['pcds', 'pcon'])
        dfs.append(df)

    postcode_lookup = pd.concat(dfs, ignore_index=True)
    postcode_lookup = postcode_lookup.dropna(subset=['pcon'])
    print(f"Loaded {len(postcode_lookup):,} active postcodes")

    return postcode_lookup

def analyze_2024_by_constituency(threshold=1_500_000):
    """Analyze 2024 data by constituency."""
    print(f"\n{'='*80}")
    print(f"2024 CONSTITUENCY ANALYSIS - £{threshold:,} Threshold")
    print(f"{'='*80}\n")

    # Load lookups
    const_names = load_constituency_lookup()
    postcode_to_const = load_postcode_mapping()

    # Load 2024 high-value properties
    threshold_label = f'{threshold//1_000_000}m'
    input_file = f'mansion_tax_2024_{threshold_label}_threshold.csv'
    print(f"\nLoading {input_file}...")
    df = pd.read_csv(input_file)
    print(f"Loaded {len(df):,} high-value properties")

    # Match to constituencies
    print("\nMatching properties to constituencies...")
    df['pcds'] = df['postcode']
    df = df.merge(postcode_to_const, on='pcds', how='left')
    df['constituency_name'] = df['pcon'].map(const_names)

    matched = df['pcon'].notna().sum()
    print(f"Successfully matched {matched:,} properties ({matched/len(df)*100:.1f}%)")

    # Calculate constituency statistics
    print("\nCalculating statistics by constituency...")
    const_stats = df[df['pcon'].notna()].groupby('constituency_name').agg({
        'price': ['count', 'mean', 'median', 'sum']
    }).round(0)
    const_stats.columns = ['num_sales', 'mean_price', 'median_price', 'total_value']
    const_stats['estimated_annual_revenue'] = const_stats['num_sales'] * 2000
    const_stats = const_stats.sort_values('num_sales', ascending=False)

    # Display top 30
    print(f"\n{'='*80}")
    print(f"TOP 30 CONSTITUENCIES")
    print(f"{'='*80}\n")
    top_30 = const_stats.head(30).copy()
    top_30['mean_price'] = top_30['mean_price'].apply(lambda x: f"£{x:,.0f}")
    top_30['median_price'] = top_30['median_price'].apply(lambda x: f"£{x:,.0f}")
    top_30['estimated_annual_revenue'] = top_30['estimated_annual_revenue'].apply(lambda x: f"£{x:,.0f}")
    print(top_30[['num_sales', 'mean_price', 'median_price', 'estimated_annual_revenue']].to_string())

    # Summary
    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}\n")
    print(f"Total constituencies with high-value sales: {len(const_stats)}")
    print(f"Total high-value sales: {const_stats['num_sales'].sum():,.0f}")
    print(f"Estimated annual revenue: £{const_stats['estimated_annual_revenue'].sum():,.0f}")
    print(f"Average sales per constituency: {const_stats['num_sales'].mean():.1f}")

    # Geographic concentration
    top_10pct = const_stats.head(int(len(const_stats) * 0.1))
    print(f"\nTop 10% of constituencies account for {top_10pct['num_sales'].sum()/const_stats['num_sales'].sum()*100:.1f}% of sales")

    # Save
    output_file = f'constituency_impact_2024_{threshold_label}_COMPLETE.csv'
    const_stats.to_csv(output_file)

    detail_file = f'properties_with_constituencies_2024_{threshold_label}_COMPLETE.csv'
    df.to_csv(detail_file, index=False)

    print(f"\n✓ Saved constituency stats to {output_file}")
    print(f"✓ Saved property details to {detail_file}")

    return const_stats, df

if __name__ == '__main__':
    print("="*80)
    print("2024 MANSION TAX ANALYSIS - COMPLETE WITH FULL NSPL DATA")
    print("="*80)

    # Analyze both thresholds
    stats_1_5m, props_1_5m = analyze_2024_by_constituency(threshold=1_500_000)
    stats_2m, props_2m = analyze_2024_by_constituency(threshold=2_000_000)

    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
