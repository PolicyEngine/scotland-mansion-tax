# Scottish Mansion Tax Analysis

Analysis of Scotland's proposed council tax reform for £1m+ properties ([Scottish Budget 2026-27](https://www.gov.scot/publications/scottish-budget-2026-27/)), estimated by Scottish Parliament constituency.

**Live map**: [policyengine.github.io/scotland-mansion-tax](https://policyengine.github.io/scotland-mansion-tax/scottish_mansion_tax_map.html)

## Policy Summary

| Detail | Value |
|--------|-------|
| **Effective date** | 1 April 2028 |
| **Threshold** | £1 million |
| **Band I** | £1m - £2m (89% of properties) |
| **Band J** | £2m+ (11% of properties) |
| **Affected households** | <1% of Scottish households |
| **Rates announced?** | No - rates not yet confirmed |

## Results

| Metric | Value | Source |
|--------|-------|--------|
| £1m+ property stock | [11,481](https://www.savills.com/insight-and-opinion/savills-news/339380/1-in-40-homes-now-valued-£1-million-or-more--according-to-savills) | Savills (2022) |
| £1m+ sales/year | [391](https://www.ros.gov.uk/data-and-statistics/property-market-statistics/property-market-report-2024-25) | RoS (2024-25) |
| Edinburgh share | >50% | [RoS](https://www.ros.gov.uk/__data/assets/pdf_file/0006/299184/Registers-of-Scotland-Property-Market-Report-2024-25-June.pdf) |
| **Estimated revenue** | **£18.5m/year** | Analysis |

### Revenue Calculation

Since Scotland hasn't announced rates, we use [UK Autumn Budget 2025 rates](https://www.gov.uk/government/publications/high-value-council-tax-surcharge/high-value-council-tax-surcharge) as benchmark:

| Band | UK Rate | Est. Stock | Revenue |
|------|---------|------------|---------|
| Band I (£1m-£2m) | £1,500/yr | 10,252 (89%) | £15.4m |
| Band J (£2m+) | £2,500/yr | 1,229 (11%) | £3.1m |
| **Total** | | **11,481** | **£18.5m** |

*Band split (89%/11%) from [Savills 2024 Scotland £1m+ Market Analysis](https://www.savills.co.uk/research_articles/229130/372275-0): 416 sales £1m-£2m, 50 sales £2m+.*

```
Revenue = Stock × Average Rate = 11,481 × £1,607 = £18.5m
```

*Finance Secretary verbally estimated [£16m](https://www.lbc.co.uk/article/wealthy-scots-in-snp-sights-as-budget-proposes-mansion-house-tax-and-a-tax-on-pr-5HjdQg9_2/). Our estimate uses UK benchmark rates.*

### Rate Uncertainty

> **Important**: Scotland has not announced rates. Our £18.5m estimate uses UK benchmark rates. Actual revenue will depend on rates Scotland chooses.

The Finance Secretary's £16m estimate implies lower rates than the UK benchmark. Here's how revenue varies with different rate assumptions:

| Scenario | Band I | Band J | Avg Rate | Revenue |
|----------|--------|--------|----------|---------|
| **UK benchmark** | £1,500 | £2,500 | £1,607 | **£18.5m** |
| Mid estimate | £1,350 | £2,250 | £1,447 | £16.6m |
| Matches £16m target | £1,200 | £2,000 | £1,286 | £14.8m |
| Conservative | £1,000 | £1,750 | £1,080 | £12.4m |

*Revenue range: £12.4m - £18.5m depending on rates chosen.*

### Top 10 Constituencies

| Rank | Constituency | Revenue | Share |
|------|-------------|---------|-------|
| 1 | Edinburgh Central | £2.21m | 12.0% |
| 2 | Edinburgh Western | £1.80m | 9.8% |
| 3 | Edinburgh Southern | £1.57m | 8.5% |
| 4 | East Lothian | £1.51m | 8.2% |
| 5 | Edinburgh Northern and Leith | £1.39m | 7.5% |
| 6 | Strathkelvin and Bearsden | £1.08m | 5.8% |
| 7 | Edinburgh Pentlands | £0.91m | 5.0% |
| 8 | Edinburgh Eastern | £0.72m | 3.9% |
| 9 | Stirling | £0.43m | 2.3% |
| 10 | Eastwood | £0.43m | 2.3% |

**Key finding**: Edinburgh Central now leads (was 2nd with population weights), reflecting its high £1m+ property concentration in New Town/Stockbridge areas. Edinburgh has 6 of top 8 constituencies (~47% of total revenue).

## Methodology

### Data Challenge

| | England/Wales | Scotland |
|--|---------------|----------|
| Data source | Land Registry | Registers of Scotland |
| Availability | Free, postcode-level | Paid, council-level only |
| Methodology | Direct property analysis | Weighted distribution |

Scotland's RoS charges for transaction data and only publishes council-level aggregates.

### Our Approach

1. **Stock → Revenue**: 11,481 properties × £1,607 avg rate = £18.5m total
2. **Sales → Distribution**: Use [391 sales by council](https://www.ros.gov.uk/data-and-statistics/property-market-statistics/property-market-report-2024-25) for geographic shares
3. **Council → Constituency**: Distribute within councils using **wealth-adjusted weights**:
   - Base: [NRS population weights](https://www.nrscotland.gov.uk/publications/scottish-parliamentary-constituency-population-estimates/)
   - Adjustment: Wealth factors derived from postcode sales concentrations (EH3, EH4, etc.)
   - Formula: `Weight = (Population × Wealth Factor) / Council Total`

**Wealth factors** account for £1m+ property concentrations within councils:
- Edinburgh Central (New Town): 1.8× (highest density)
- Edinburgh Western (Barnton): 1.6×
- Edinburgh Southern (Morningside): 1.5×
- Edinburgh Eastern (Portobello): 0.6× (lower density)

Stock tells us **how many** properties; sales tells us **where** they are; wealth factors tell us **how properties are distributed within councils**.

## Comparison with UK Mansion Tax

| | [uk-mansion-tax](https://github.com/PolicyEngine/uk-mansion-tax) | scotland-mansion-tax |
|--|-----------------|----------------------|
| Threshold | £2m+ | £1m+ |
| Revenue | £400m (OBR) | £18.5m (analysis) |
| Data | Property-level | Council-level |
| Top area | Cities of London & Westminster | Edinburgh Northern & Leith |

## Data Sources

- [Registers of Scotland Property Market Report 2024-25](https://www.ros.gov.uk/data-and-statistics/property-market-statistics/property-market-report-2024-25)
- [Savills £1m+ property stock](https://www.savills.com/insight-and-opinion/savills-news/339380/1-in-40-homes-now-valued-£1-million-or-more--according-to-savills)
- [NRS Constituency Population Estimates](https://www.nrscotland.gov.uk/publications/scottish-parliamentary-constituency-population-estimates/)
- [Scottish Budget 2026-27](https://www.gov.scot/publications/scottish-budget-2026-27/)
- [UK High Value Council Tax Surcharge](https://www.gov.uk/government/publications/high-value-council-tax-surcharge/high-value-council-tax-surcharge)

## Limitations

1. Constituency figures are modeled estimates, not direct observations
2. Sales data from single year; may vary annually
3. Assumes stock distributed geographically like sales
4. No behavioral response modeled
5. **Temporal mismatch**: Stock data (2022) predates sales data (2024-25) by ~2 years. Scottish house prices rose ~5-10% over this period, so actual 2024 stock may be higher than 11,481, potentially underestimating revenue by a similar margin
6. **Council estimates**: RoS reports 391 total sales but only provides aggregates ("over half" in Edinburgh). Council-level breakdown is estimated from postcode data; estimates total 429 due to different source methodologies. Geographic distribution is used, not absolute numbers
7. **Rate uncertainty**: Scotland has not announced rates. Revenue estimates use UK benchmark rates (£1,500/£2,500); actual revenue could range from £12.4m to £18.5m depending on rates chosen (see sensitivity table above)

*Data extracted: January 2026*
