# UK high value council tax surcharge: constituency-level impact

In the November 2025 Autumn Budget, the UK government announced a new high value council tax surcharge on properties valued over £2 million. The Office for Budget Responsibility (OBR) [estimates](https://obr.uk/efo/economic-and-fiscal-outlook-november-2025/) this measure will raise £400 million in 2029-30.

Using 2024 Land Registry sales data, we estimate how this revenue will be distributed across Westminster constituencies.

Key findings:
- 559 of 650 constituencies contain properties above the £2 million threshold
- The top 10 constituencies account for 34% of the estimated revenue
- Cities of London and Westminster alone accounts for 10% (£40 million)
- London constituencies dominate, with 8 of the top 10 affected areas

[Explore the interactive map](#map) | [Download the data](https://github.com/PolicyEngine/uk-mansion-tax)

## The policy

From April 2028, owners of properties valued over £2 million (in 2026 prices) will pay an annual surcharge in addition to their existing council tax. The surcharge rises with property value:

| Property value | Annual surcharge |
|----------------|------------------|
| £2m - £2.5m | £2,500 |
| £2.5m - £3m | £3,500 |
| £3m - £5m | £5,000 |
| £5m+ | £7,500 |

The OBR expects the surcharge rates to increase with CPI inflation each year. Unlike standard council tax, the revenue flows to central government rather than local authorities.

## Constituency-level estimates

We estimate each constituency's share of the £400 million total by analysing 2024 property sales. We uprate sale prices to 2029-30 levels using OBR house price growth forecasts (13.4% cumulative growth from 2024), apply the surcharge band structure to each sale above £2 million, and allocate the OBR's total estimate proportionally based on each constituency's share of implied revenue.

### Top 20 constituencies by estimated revenue

| Rank | Constituency | Properties sold above £2m | Estimated annual revenue | Share of total |
|------|--------------|---------------------------|--------------------------|----------------|
| 1 | Cities of London and Westminster | 811 | £39.8m | 9.9% |
| 2 | Kensington and Bayswater | 634 | £28.4m | 7.1% |
| 3 | Chelsea and Fulham | 440 | £17.7m | 4.4% |
| 4 | Hampstead and Highgate | 286 | £11.6m | 2.9% |
| 5 | Battersea | 198 | £7.0m | 1.8% |
| 6 | Richmond Park | 186 | £7.0m | 1.8% |
| 7 | Holborn and St Pancras | 163 | £7.1m | 1.8% |
| 8 | Islington South and Finsbury | 174 | £6.5m | 1.6% |
| 9 | Hammersmith and Chiswick | 156 | £5.7m | 1.4% |
| 10 | Finchley and Golders Green | 133 | £5.6m | 1.4% |
| 11 | Runnymede and Weybridge | 118 | £5.0m | 1.2% |
| 12 | Wimbledon | 112 | £4.3m | 1.1% |
| 13 | Queen's Park and Maida Vale | 111 | £4.0m | 1.0% |
| 14 | Ealing Central and Acton | 104 | £3.7m | 0.9% |
| 15 | Esher and Walton | 101 | £3.4m | 0.8% |
| 16 | Windsor | 92 | £4.0m | 1.0% |
| 17 | Hornsey and Friern Barnet | 79 | £2.2m | 0.6% |
| 18 | Dulwich and West Norwood | 78 | £2.6m | 0.6% |
| 19 | Twickenham | 77 | £2.6m | 0.7% |
| 20 | Harpenden and Berkhamsted | 73 | £2.3m | 0.6% |

The top 20 constituencies account for 43% of the estimated revenue, despite representing just 3% of all constituencies.

## Geographic distribution {#map}

The map below shows the estimated revenue allocation by constituency. Darker shading indicates higher estimated revenue from the surcharge.

<iframe src="surcharge_map_by_revenue.html" width="100%" height="850" frameborder="0"></iframe>

The concentration in London and the Home Counties reflects the geography of UK property wealth. Of the 559 constituencies with properties above the £2 million threshold:
- 69 are in Greater London (accounting for 48% of estimated revenue)
- The remaining 490 constituencies share 52% of estimated revenue

London constituencies contain 48% of high-value property sales but represent just 11% of all constituencies.

### Distribution by surcharge band

Of the 10,371 property sales above £2 million in 2024 (after uprating to 2029 prices):

| Band | Properties | Share of properties | Revenue contribution |
|------|------------|---------------------|---------------------|
| £2m - £2.5m | 3,372 | 33% | 19% |
| £2.5m - £3m | 1,667 | 16% | 13% |
| £3m - £5m | 2,807 | 27% | 32% |
| £5m+ | 2,525 | 24% | 43% |

Properties valued over £5 million represent 24% of affected sales but contribute 43% of the estimated revenue due to the £7,500 annual surcharge rate.

## Methodology and limitations

### Data sources

- **Property sales**: UK Land Registry Price Paid Data for 2024 (881,757 transactions)
- **Revenue estimate**: OBR Economic and Fiscal Outlook, November 2025 (£400 million in 2029-30)
- **House price growth**: OBR forecasts of 2.9% in 2025, then 2.4-2.5% annually through 2029
- **Constituency boundaries**: MySoc 2025 Westminster constituencies

### Key limitation: sales vs stock

This analysis uses property sales data, not the full housing stock. The OBR's £400 million estimate is based on Valuation Office data covering all properties, not just those sold in a given year.

We found:
- Implied surcharge from 2024 sales: £47 million
- OBR estimate (full housing stock): £400 million
- Ratio: approximately 8.5x

This ratio is consistent with annual property turnover rates of 5-10% of housing stock. Our constituency-level allocations assume the geographic distribution of high-value sales reflects the distribution of high-value housing stock.

### Behavioural effects

The OBR's £400 million estimate incorporates behavioural responses including:
- Full pass-through of the surcharge into property prices
- Price bunching just below band boundaries
- Non-compliance and appeals

The OBR notes that these behavioural effects reduce revenue from other property taxes (stamp duty land tax, capital gains tax), which partly offsets the gross surcharge revenue in the early years of implementation.

## Conclusion

The high value council tax surcharge concentrates revenue collection in a small number of constituencies. The top 10 constituencies—all in London—account for over a third of the estimated £400 million annual revenue. This geographic concentration reflects the distribution of properties valued over £2 million, which are heavily concentrated in London and the South East.

---

*Analysis by PolicyEngine. Data and code available on [GitHub](https://github.com/PolicyEngine/uk-mansion-tax).*
