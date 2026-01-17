# Scottish Mansion Tax Analysis

Analysis of Scotland's proposed council tax reform for £1m+ properties ([Scottish Budget 2026-27](https://www.gov.scot/publications/scottish-budget-2026-27/)), estimated by Scottish Parliament constituency.

**Live map**: [policyengine.github.io/scotland-mansion-tax](https://policyengine.github.io/scotland-mansion-tax/scottish_mansion_tax_map.html)

## Policy Summary

| Detail | Value |
|--------|-------|
| **Effective date** | 1 April 2028 |
| **Threshold** | £1 million |
| **Band I** | £1m - £2m (82% of properties) |
| **Band J** | £2m+ (18% of properties) |
| **Affected households** | <1% of Scottish households |
| **Rates announced?** | No - rates not yet confirmed |

## Results

| Metric | Value | Source |
|--------|-------|--------|
| £1m+ property stock | [11,481](https://www.savills.com/insight-and-opinion/savills-news/339380/1-in-40-homes-now-valued-£1-million-or-more--according-to-savills) | Savills |
| £1m+ sales/year | [391](https://www.ros.gov.uk/data-and-statistics/property-market-statistics/property-market-report-2024-25) | Registers of Scotland |
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

### Top 10 Constituencies

| Rank | Constituency | Revenue | Share |
|------|-------------|---------|-------|
| 1 | Edinburgh Northern and Leith | £1.58m | 8.6% |
| 2 | Edinburgh Central | £1.53m | 8.3% |
| 3 | East Lothian | £1.51m | 8.2% |
| 4 | Edinburgh Eastern | £1.50m | 8.1% |
| 5 | Edinburgh Western | £1.41m | 7.6% |
| 6 | Edinburgh Southern | £1.31m | 7.1% |
| 7 | Edinburgh Pentlands | £1.27m | 6.9% |
| 8 | Strathkelvin and Bearsden | £1.08m | 5.8% |
| 9 | Stirling | £0.43m | 2.3% |
| 10 | Eastwood | £0.43m | 2.3% |

**Key finding**: Edinburgh has 6 of top 7 constituencies (~47% of total revenue).

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
3. **Council → Constituency**: Distribute within councils using [NRS population weights](https://www.nrscotland.gov.uk/publications/scottish-parliamentary-constituency-population-estimates/)

Stock tells us **how many** properties; sales tells us **where** they are.

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
