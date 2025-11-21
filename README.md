# UK Mansion Tax Analysis (2024)

Analysis of the proposed UK "mansion tax" using 2024 property transaction data at the Westminster Parliamentary constituency level.

## Overview

This repository contains a complete, reproducible analysis of how a proposed mansion tax would affect different UK constituencies. The analysis uses actual 2024 property sales data from the UK Land Registry, mapped to Westminster Parliamentary constituencies using ONS postcode lookups.

### What is the Mansion Tax?

The proposed mansion tax is a council tax surcharge on high-value properties:
- **Target**: Properties in council tax bands F, G, and H
- **Threshold options**: £1.5 million or £2 million (under debate)
- **Surcharge**: ~£2,000 per property per year
- **Estimated impact**: 145,000-300,000 properties, £600m annual revenue

**Key limitation**: This analysis uses property *sales* in 2024 (1-2% of housing stock), not total properties. See [2024_ANALYSIS_SUMMARY.md](2024_ANALYSIS_SUMMARY.md) for details.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download Data

```bash
python download_data.py
```

**Note**: The Census 2021 TS003 household data must be downloaded manually from:
- [UK Data Service - TS003 Household Composition](https://statistics.ukdataservice.ac.uk/dataset/ons_2021_ts003_demography_household_composition)
- Download: `TS003-Household-Composition-2021-p19wpc-ONS.xlsx`
- Save as: `TS003_household_composition_p19wpc.xlsx`

### 3. Run Analysis

```bash
# Main constituency analysis (generates top-level results)
python analyze_2024_complete.py

# Generate household impact percentages
python generate_household_impact.py
```

## Output Files

### Primary Outputs

| File | Description |
|------|-------------|
| `constituency_impact_2024_1m_COMPLETE.csv` | £1.5m threshold: sales, prices, revenue by constituency |
| `constituency_impact_2024_2m_COMPLETE.csv` | £2m threshold: sales, prices, revenue by constituency |
| `mansion_tax_household_impact.csv` | £1.5m threshold: % of households affected |
| `mansion_tax_household_impact_2m.csv` | £2m threshold: % of households affected |
| `2024_ANALYSIS_SUMMARY.md` | Full analysis report with methodology |

### Key Findings

**£1.5m Threshold:**
- 14,581 properties sold above threshold (1.65% of all sales)
- 567 constituencies affected
- Cities of London & Westminster: 1.628% of households affected
- Top 10% of constituencies account for 58% of high-value sales

**£2m Threshold:**
- 8,328 properties sold above threshold (0.94% of all sales)
- 555 constituencies affected
- Cities of London & Westminster: 1.297% of households affected

## Data Sources

All data is publicly available from UK government sources:

| Dataset | Source | Size | License |
|---------|--------|------|---------|
| Land Registry Price Paid Data 2024 | [gov.uk](https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads) | 147 MB | Open Government Licence |
| ONS National Statistics Postcode Lookup | [geoportal.statistics.gov.uk](https://geoportal.statistics.gov.uk/) | 192 MB | Open Government Licence |
| Westminster Constituency Names/Codes | [geoportal.statistics.gov.uk](https://geoportal.statistics.gov.uk/) | <1 MB | Open Government Licence |
| Census 2021 TS003 Household Composition | [UK Data Service](https://statistics.ukdataservice.ac.uk/) | 200 KB | Open Government Licence |

## Analysis Scripts

| Script | Purpose |
|--------|---------|
| `download_data.py` | Download all required data files |
| `analyze_2024_complete.py` | Main analysis: map properties to constituencies |
| `generate_household_impact.py` | Calculate % of households affected per constituency |

## Methodology

### 1. Data Loading
- Load all 881,757 property transactions from 2024 Land Registry data
- Filter for properties above £1.5m and £2m thresholds

### 2. Geographic Matching
- Map property postcodes to constituencies using ONS NSPL (2.7M postcodes)
- Link constituency codes to names using ONS lookup table
- **Match rate**: 98.3% of high-value properties successfully matched

### 3. Constituency Aggregation
- Count sales per constituency
- Calculate price statistics (mean, median)
- Estimate annual revenue at £2,000 per property

### 4. Household Impact Analysis
- Merge with Census 2021 household counts (by 2024 constituency boundaries)
- Calculate % of households affected = (high-value sales / total households) × 100

## Important Limitations

### Sales vs. Stock
This analysis uses property **sales in 2024**, not total housing **stock**:
- 2024 sales: 14,581 above £1.5m
- FT estimate: 145,000-300,000 total properties affected
- **Sales represent ~5-10% of total stock**

**Implication**: True policy impact would be 10-20x larger than shown in this analysis.

### Geographic Coverage
- England and Wales: Full coverage (575 constituencies)
- Scotland: Property data only, no household counts from Census
- Northern Ireland: Not included

### Revenue Model
- Uses simplified flat £2,000 surcharge
- Actual surcharge would vary by property value
- Does not model deferral option or behavioral responses

## Repository Structure

```
uk-mansion-tax/
├── README.md                                    # This file
├── requirements.txt                             # Python dependencies
├── download_data.py                             # Data download script
├── .gitignore                                   # Excludes large data files
│
├── analyze_2024_complete.py                     # Main analysis script
├── generate_household_impact.py                 # Household % calculations
│
├── 2024_ANALYSIS_SUMMARY.md                     # Full analysis report
├── MICROSIM_METHODOLOGY.md                      # Microsimulation notes
│
├── constituency_impact_2024_1m_COMPLETE.csv     # Results: £1.5m threshold
├── constituency_impact_2024_2m_COMPLETE.csv     # Results: £2m threshold
├── mansion_tax_household_impact.csv             # Household %: £1.5m
├── mansion_tax_household_impact_2m.csv          # Household %: £2m
├── constituency_households_2024.csv             # Census household counts
└── TS003_household_composition_p19wpc.xlsx      # Census source data
```

## Citation

If you use this analysis, please cite:

```
UK Mansion Tax Analysis (2024)
Data sources:
- UK Land Registry Price Paid Data (2024)
- ONS National Statistics Postcode Lookup (February 2025)
- ONS Census 2021 TS003 Household Composition
```

## License

This analysis is released under the MIT License. All data is from UK government sources under the Open Government Licence v3.0.

## Related Resources

- [Financial Times: Labour MPs raise concerns over mansion tax](https://www.ft.com/)
- [House of Commons Library: Constituency Dashboard](https://commonslibrary.parliament.uk/constituency-dashboard/)
- [ONS: Westminster Parliamentary Constituencies](https://www.ons.gov.uk/methodology/geography/ukgeographies/electoralgeography/parliamentaryconstituencies)

## Contact

For questions or issues, please open a GitHub issue.
