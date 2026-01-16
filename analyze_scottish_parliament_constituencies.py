#!/usr/bin/env python3
"""
Scottish Mansion Tax Analysis by Scottish Parliament Constituency

Distributes council-level mansion tax estimates to the 73 Scottish Parliament
constituencies using population/household weights.

Based on Scottish Budget 2026-27 council tax reform for £1m+ properties.

Data sources:
- Council estimates: analyze_scottish_mansion_tax.py
- Constituency list: Scottish Parliament (2021 boundaries)
- Revenue estimate: £16m (Scottish Government)
"""

import pandas as pd
from pathlib import Path

# Scottish Government revenue estimate
SCOTTISH_GOV_REVENUE_ESTIMATE = 16_000_000  # £16 million

# Council-level £1m+ sales data (from analyze_scottish_mansion_tax.py)
COUNCIL_DATA = {
    "City of Edinburgh": 230,
    "East Lothian": 35,
    "Fife": 30,
    "East Dunbartonshire": 25,
    "Aberdeen City": 20,
    "Aberdeenshire": 15,
    "Glasgow City": 15,
    "Perth and Kinross": 12,
    "Stirling": 10,
    "Highland": 10,
    "East Renfrewshire": 10,
    "Scottish Borders": 8,
    "South Ayrshire": 7,
    "Argyll and Bute": 6,
    "Midlothian": 5,
    "West Lothian": 5,
    # Remaining councils with minimal £1m+ sales
    "South Lanarkshire": 3,
    "North Lanarkshire": 2,
    "Renfrewshire": 2,
    "Inverclyde": 1,
    "Falkirk": 1,
    "Clackmannanshire": 1,
    "Dumfries and Galloway": 1,
    "Dundee City": 1,
    "Angus": 1,
    "Moray": 1,
    "North Ayrshire": 1,
    "West Dunbartonshire": 1,
    "East Ayrshire": 0,
    "Eilean Siar": 0,
    "Orkney Islands": 0,
    "Shetland Islands": 0,
}

# Scottish Parliament constituencies (2021 boundaries) mapped to council areas
# Weight represents share of high-value properties within the council
# Higher weights for affluent areas (e.g., New Town, Morningside in Edinburgh)
CONSTITUENCY_COUNCIL_MAPPING = {
    # City of Edinburgh - 6 constituencies
    # Edinburgh Central includes New Town (EH3) - highest property values
    "Edinburgh Central": {"council": "City of Edinburgh", "weight": 0.25},
    # Edinburgh Western includes Barnton, Cramond (EH4) - very high values
    "Edinburgh Western": {"council": "City of Edinburgh", "weight": 0.20},
    # Edinburgh Southern includes Morningside, Grange - high values
    "Edinburgh Southern": {"council": "City of Edinburgh", "weight": 0.18},
    # Edinburgh Pentlands includes Corstorphine - moderate values
    "Edinburgh Pentlands": {"council": "City of Edinburgh", "weight": 0.15},
    # Edinburgh Northern and Leith - mixed values
    "Edinburgh Northern and Leith": {"council": "City of Edinburgh", "weight": 0.12},
    # Edinburgh Eastern - lower values
    "Edinburgh Eastern": {"council": "City of Edinburgh", "weight": 0.10},

    # East Lothian - 1 constituency (includes North Berwick EH39)
    "East Lothian": {"council": "East Lothian", "weight": 1.0},

    # Fife - 5 constituencies
    # North East Fife includes St Andrews (KY16) - highest values
    "North East Fife": {"council": "Fife", "weight": 0.50},
    "Dunfermline": {"council": "Fife", "weight": 0.15},
    "Cowdenbeath": {"council": "Fife", "weight": 0.12},
    "Kirkcaldy": {"council": "Fife", "weight": 0.12},
    "Mid Fife and Glenrothes": {"council": "Fife", "weight": 0.11},

    # East Dunbartonshire - 2 constituencies
    # Strathkelvin and Bearsden includes Bearsden (G61) - high values
    "Strathkelvin and Bearsden": {"council": "East Dunbartonshire", "weight": 0.65},
    "Cumbernauld and Kilsyth": {"council": "East Dunbartonshire", "weight": 0.35},

    # Aberdeen City - 3 constituencies
    "Aberdeen Central": {"council": "Aberdeen City", "weight": 0.35},
    "Aberdeen Donside": {"council": "Aberdeen City", "weight": 0.35},
    "Aberdeen South and North Kincardine": {"council": "Aberdeen City", "weight": 0.30},

    # Aberdeenshire - 3 constituencies
    "Aberdeenshire West": {"council": "Aberdeenshire", "weight": 0.40},
    "Aberdeenshire East": {"council": "Aberdeenshire", "weight": 0.30},
    "Banffshire and Buchan Coast": {"council": "Aberdeenshire", "weight": 0.30},

    # Glasgow City - 9 constituencies
    "Glasgow Kelvin": {"council": "Glasgow City", "weight": 0.25},  # West End
    "Glasgow Cathcart": {"council": "Glasgow City", "weight": 0.15},
    "Glasgow Anniesland": {"council": "Glasgow City", "weight": 0.12},
    "Glasgow Southside": {"council": "Glasgow City", "weight": 0.10},
    "Glasgow Pollok": {"council": "Glasgow City", "weight": 0.08},
    "Glasgow Maryhill and Springburn": {"council": "Glasgow City", "weight": 0.08},
    "Glasgow Provan": {"council": "Glasgow City", "weight": 0.08},
    "Glasgow Shettleston": {"council": "Glasgow City", "weight": 0.07},
    "Rutherglen": {"council": "Glasgow City", "weight": 0.07},

    # Perth and Kinross - 2 constituencies
    "Perthshire North": {"council": "Perth and Kinross", "weight": 0.50},
    "Perthshire South and Kinross-shire": {"council": "Perth and Kinross", "weight": 0.50},

    # Stirling - 1 constituency
    "Stirling": {"council": "Stirling", "weight": 1.0},

    # Highland - 4 constituencies
    "Inverness and Nairn": {"council": "Highland", "weight": 0.40},
    "Caithness, Sutherland and Ross": {"council": "Highland", "weight": 0.25},
    "Skye, Lochaber and Badenoch": {"council": "Highland", "weight": 0.25},
    "Ross, Skye and Inverness West": {"council": "Highland", "weight": 0.10},

    # East Renfrewshire - 1 constituency (Newton Mearns, Giffnock)
    "Eastwood": {"council": "East Renfrewshire", "weight": 1.0},

    # Scottish Borders - 2 constituencies
    "Ettrick, Roxburgh and Berwickshire": {"council": "Scottish Borders", "weight": 0.50},
    "Midlothian South, Tweeddale and Lauderdale": {"council": "Scottish Borders", "weight": 0.50},

    # South Ayrshire - 2 constituencies
    "Ayr": {"council": "South Ayrshire", "weight": 0.60},
    "Carrick, Cumnock and Doon Valley": {"council": "South Ayrshire", "weight": 0.40},

    # Argyll and Bute - 1 constituency
    "Argyll and Bute": {"council": "Argyll and Bute", "weight": 1.0},

    # Midlothian - 1 constituency
    "Midlothian North and Musselburgh": {"council": "Midlothian", "weight": 1.0},

    # West Lothian - 2 constituencies
    "Linlithgow": {"council": "West Lothian", "weight": 0.55},
    "Almond Valley": {"council": "West Lothian", "weight": 0.45},

    # South Lanarkshire - 4 constituencies
    "East Kilbride": {"council": "South Lanarkshire", "weight": 0.30},
    "Clydesdale": {"council": "South Lanarkshire", "weight": 0.30},
    "Hamilton, Larkhall and Stonehouse": {"council": "South Lanarkshire", "weight": 0.25},
    "Uddingston and Bellshill": {"council": "South Lanarkshire", "weight": 0.15},

    # North Lanarkshire - 4 constituencies
    "Motherwell and Wishaw": {"council": "North Lanarkshire", "weight": 0.30},
    "Airdrie and Shotts": {"council": "North Lanarkshire", "weight": 0.25},
    "Coatbridge and Chryston": {"council": "North Lanarkshire", "weight": 0.25},
    "Cumbernauld and Kilsyth": {"council": "North Lanarkshire", "weight": 0.20},

    # Renfrewshire - 3 constituencies
    "Paisley": {"council": "Renfrewshire", "weight": 0.40},
    "Renfrewshire North and West": {"council": "Renfrewshire", "weight": 0.35},
    "Renfrewshire South": {"council": "Renfrewshire", "weight": 0.25},

    # Inverclyde - 1 constituency
    "Greenock and Inverclyde": {"council": "Inverclyde", "weight": 1.0},

    # Falkirk - 2 constituencies
    "Falkirk East": {"council": "Falkirk", "weight": 0.50},
    "Falkirk West": {"council": "Falkirk", "weight": 0.50},

    # Clackmannanshire - shared constituency
    "Clackmannanshire and Dunblane": {"council": "Clackmannanshire", "weight": 1.0},

    # Dumfries and Galloway - 2 constituencies
    "Dumfriesshire": {"council": "Dumfries and Galloway", "weight": 0.50},
    "Galloway and West Dumfries": {"council": "Dumfries and Galloway", "weight": 0.50},

    # Dundee City - 2 constituencies
    "Dundee City East": {"council": "Dundee City", "weight": 0.50},
    "Dundee City West": {"council": "Dundee City", "weight": 0.50},

    # Angus - 2 constituencies
    "Angus North and Mearns": {"council": "Angus", "weight": 0.50},
    "Angus South": {"council": "Angus", "weight": 0.50},

    # Moray - 1 constituency
    "Moray": {"council": "Moray", "weight": 1.0},

    # North Ayrshire - 2 constituencies
    "Cunninghame North": {"council": "North Ayrshire", "weight": 0.50},
    "Cunninghame South": {"council": "North Ayrshire", "weight": 0.50},

    # West Dunbartonshire - 1 constituency
    "Dumbarton": {"council": "West Dunbartonshire", "weight": 1.0},

    # Island councils
    "Na h-Eileanan an Iar": {"council": "Eilean Siar", "weight": 1.0},
    "Orkney Islands": {"council": "Orkney Islands", "weight": 1.0},
    "Shetland Islands": {"council": "Shetland Islands", "weight": 1.0},
}

# Band distribution
BAND_I_RATIO = 0.82  # £1m-£2m
BAND_J_RATIO = 0.18  # £2m+


def analyze_constituencies():
    """Distribute council-level estimates to constituencies."""

    print("=" * 70)
    print("Scottish Mansion Tax Analysis by Parliament Constituency")
    print("=" * 70)

    # Calculate total sales for normalization
    total_sales = sum(COUNCIL_DATA.values())

    results = []

    for constituency, mapping in CONSTITUENCY_COUNCIL_MAPPING.items():
        council = mapping["council"]
        weight = mapping["weight"]

        # Get council's total sales
        council_sales = COUNCIL_DATA.get(council, 0)

        # Allocate to constituency based on weight
        constituency_sales = council_sales * weight

        # Calculate share of total
        share = constituency_sales / total_sales if total_sales > 0 else 0

        # Allocate revenue
        allocated_revenue = share * SCOTTISH_GOV_REVENUE_ESTIMATE

        # Band breakdown
        band_i_sales = constituency_sales * BAND_I_RATIO
        band_j_sales = constituency_sales * BAND_J_RATIO

        rounded_sales = int(round(constituency_sales))
        results.append({
            "constituency": constituency,
            "council": council,
            "estimated_sales": rounded_sales,
            "band_i_sales": int(round(band_i_sales)),
            "band_j_sales": int(round(band_j_sales)),
            "share_pct": round(share * 100, 2) if rounded_sales > 0 else 0,
            "allocated_revenue": round(allocated_revenue, 0) if rounded_sales > 0 else 0,
        })

    df = pd.DataFrame(results)
    df = df.sort_values("estimated_sales", ascending=False)

    # Print summary
    print(f"\n📊 Total constituencies: {len(df)}")
    print(f"📈 Total £1m+ sales: {df['estimated_sales'].sum():.0f}")
    print(f"💰 Total revenue: £{df['allocated_revenue'].sum()/1e6:.1f}m")

    print("\n🏛️  Top 20 Constituencies by Impact:")
    print("-" * 85)
    print(f"{'Constituency':<40} {'Council':<25} {'Sales':>8} {'Revenue':>10}")
    print("-" * 85)

    for _, row in df.head(20).iterrows():
        council_short = row['council'][:24] if len(row['council']) > 24 else row['council']
        print(f"{row['constituency']:<40} {council_short:<25} "
              f"{row['estimated_sales']:>8.1f} £{row['allocated_revenue']/1e6:>7.2f}m")

    print("-" * 85)

    # Edinburgh subtotal
    edinburgh_df = df[df['council'] == 'City of Edinburgh']
    print(f"\n📍 Edinburgh Total (6 constituencies):")
    print(f"   {edinburgh_df['estimated_sales'].sum():.0f} sales, "
          f"£{edinburgh_df['allocated_revenue'].sum()/1e6:.2f}m "
          f"({edinburgh_df['share_pct'].sum():.1f}%)")

    for _, row in edinburgh_df.sort_values('estimated_sales', ascending=False).iterrows():
        print(f"   - {row['constituency']}: {row['estimated_sales']:.0f} sales, "
              f"£{row['allocated_revenue']/1e6:.2f}m ({row['share_pct']:.1f}%)")

    return df


def main():
    """Run analysis and save results."""
    df = analyze_constituencies()

    # Save results
    output_file = "scottish_parliament_constituency_impact.csv"
    df.to_csv(output_file, index=False)
    print(f"\n✅ Saved: {output_file}")

    # Summary stats
    print("\n" + "=" * 70)
    print("Summary Statistics:")
    print(f"  Constituencies analyzed: {len(df)}")
    print(f"  With £1m+ sales: {len(df[df['estimated_sales'] > 0])}")
    print(f"  Total sales: {df['estimated_sales'].sum():.0f}")
    print(f"  Total revenue: £{df['allocated_revenue'].sum()/1e6:.1f}m")
    print(f"\n  Top 5 constituencies:")
    for _, row in df.head(5).iterrows():
        print(f"    {row['constituency']}: {row['estimated_sales']:.0f} sales, "
              f"£{row['allocated_revenue']/1e6:.2f}m ({row['share_pct']:.1f}%)")
    print("=" * 70)

    return df


if __name__ == "__main__":
    main()
