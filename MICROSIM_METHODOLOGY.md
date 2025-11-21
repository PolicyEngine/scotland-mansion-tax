# Mansion Tax Microsimulation Methodology

## Task Clarification
"Use the Land Registry data (census of all property sales) to microsim analyse at the constituency level the mansion tax policy"

## Current Approach vs. Proper Microsimulation

### What We Currently Have
- **2025 sales data only** (446,867 transactions, ~2% of housing stock)
- Geographic distribution analysis
- Sales-based revenue estimates
- **This is NOT a microsimulation** - it's a descriptive analysis of market transactions

### What a True Microsimulation Requires

A microsimulation models policy impacts on a **representative population** of all properties, not just those sold.

## Recommended Microsimulation Approach

### Step 1: Build the Property Universe
**Data Source:** Council Tax Stock of Properties 2024 (CTSOP 2.0)
- Download: https://assets.publishing.service.gov.uk/media/66854999ab5fc5929851b92c/CTSOP2.0_time_series.xlsx
- Contains: All ~25 million properties by council tax band and constituency
- Focus on: Band F, G, H properties (mansion tax targets)

**Result:** Complete population of properties to simulate

### Step 2: Impute 2025 Market Values
Since council tax bands use 1991 valuations, estimate current values using:

**Option A: Recent Sales Method**
- Use Land Registry **2018-2025 data** (all years, not just 2025)
- For each postcode/area, calculate price appreciation since last sale
- Apply local House Price Index trends to properties without recent sales

**Option B: Hedonic Price Model**
- Use historical sales (2018-2025) to build a price prediction model
- Independent variables: council tax band, property type, location, age
- Predict 2025 values for all properties

**Option C: Area-Based Imputation**
- For each small area (LSOA/MSOA), use recent sales to estimate:
  - Average price per band F/G/H property
  - Distribution of values within each band
- Apply to all properties in that area/band combination

### Step 3: Apply Policy Rules
For each property with estimated value > threshold (£1.5m or £2m):

```
if property_value >= threshold:
    if council_tax_band in ['F', 'G', 'H']:
        # Calculate surcharge based on amount above threshold
        # FT article suggests avg £2,000, but actual formula would be:
        excess_value = property_value - threshold
        annual_surcharge = calculate_surcharge(excess_value, band)
    else:
        # Property escapes tax (wrong band despite high value)
        annual_surcharge = 0
```

### Step 4: Model Behavioral Responses (Optional Advanced Step)
- **Deferral take-up:** What % of owners defer vs. pay annually?
- **Property market response:** Do sales/prices change?
- **Avoidance:** Do people restructure ownership?

### Step 5: Aggregate to Constituency Level
Sum across all properties in each constituency:
- Number of properties affected
- Total annual revenue
- Revenue by property type/band
- Distribution effects

## Datasets Required

### Essential
1. **Council Tax Stock (CTSOP 2.0)** - Housing stock by band & constituency
   - https://www.gov.uk/government/statistics/council-tax-stock-of-properties-2024

2. **Land Registry Price Paid Data (2018-2025)** - For value imputation
   - 2025: Already have ✓
   - 2024: https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads
   - 2023-2018: Same source

3. **UK House Price Index** - Regional price trends
   - https://www.gov.uk/government/statistical-data-sets/uk-house-price-index-data-downloads-september-2025

### Helpful Additions
4. **CTSOP 3.0** - Property type characteristics
5. **CTSOP 4.0** - Property age/build period
6. **ONS NSPL** - Postcode to small area mapping (already have ✓)

## Implementation Steps

### Phase 1: Data Assembly (2-3 days)
```bash
# 1. Download Council Tax data
curl -L "https://assets.publishing.service.gov.uk/.../CTSOP2.0_time_series.xlsx" -o council_tax_stock.xlsx

# 2. Download historical price paid data (2018-2024)
# Available at: https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads

# 3. Download UK HPI data
curl -L "https://www.gov.uk/.../uk-hpi-full-file.csv" -o uk_hpi.csv
```

### Phase 2: Value Imputation (3-5 days)
```python
# Pseudocode
1. Load all Land Registry sales 2018-2025
2. Calculate price appreciation by postcode/LSOA
3. For each council tax band F/G/H property:
   - If sold recently (2023-2025): use actual sale price
   - If sold 2018-2022: inflate by local HPI
   - If never sold (or pre-2018): impute using area averages
4. Create property-level dataset with estimated 2025 values
```

### Phase 3: Policy Simulation (1-2 days)
```python
# Apply mansion tax rules
for each property:
    if estimated_value >= threshold and band in ['F','G','H']:
        calculate tax liability
        assign to constituency
```

### Phase 4: Aggregation & Analysis (1-2 days)
- Sum by constituency
- Calculate distribution statistics
- Compare to FT article estimates (£600m from 145k-300k properties)
- Validate results

## Key Differences from Current Analysis

| Aspect | Current Analysis | Microsimulation |
|--------|-----------------|-----------------|
| **Sample** | 2025 sales only (~447k) | All properties (~25m) |
| **Coverage** | 1-2% of housing stock | 100% of housing stock |
| **Values** | Actual sale prices | Imputed 2025 values |
| **Time period** | 1 year (2025) | Multi-year (2018-2025) |
| **Method** | Descriptive statistics | Property-level modeling |
| **Revenue estimate** | £4.7m-£9m (from sales) | £600m (from stock) |
| **Properties affected** | 2,400-4,600 | 145,000-300,000 |

## Validation Checks

Your microsim should produce results close to the FT article:
- ✓ 145,000-300,000 properties affected (depending on threshold)
- ✓ ~£600 million annual revenue
- ✓ Concentrated in London and South East
- ✓ Top affected constituency: Cities of London & Westminster

## Questions to Clarify with Task Assigner

1. **Scope:** Do they want full microsimulation or just sales-based analysis?
2. **Value imputation:** What method should be used for properties without recent sales?
3. **Validation:** What are the target outputs/metrics?
4. **Behavioral modeling:** Should you model deferral, market response, etc.?
5. **Time constraints:** Full microsim is 1-2 weeks of work vs. current approach (done)

## Recommendation

Given the vague instructions, I suggest:

**Option A: Quick Clarification**
- Present current sales-based analysis as "Phase 1"
- Explain that true microsim requires council tax data + multi-year sales
- Get approval before proceeding

**Option B: Full Microsimulation**
- Download council tax stock data
- Download 2018-2024 price paid data
- Build property-level valuation model
- Simulate policy on entire housing stock
- Aggregate to constituencies

The current analysis is valuable but answers "where are high-value sales happening?" not "what is the total policy impact on all existing properties?" - which is what microsim should answer.
