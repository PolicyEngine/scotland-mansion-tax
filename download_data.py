#!/usr/bin/env python3
"""Download data for UK mansion tax analysis."""

import os
import zipfile
import requests
from pathlib import Path

def download(url, dest, desc):
    """Download file with progress."""
    print(f"\n{desc}...")
    if os.path.exists(dest):
        if input(f"{dest} exists. Re-download? (y/N): ").lower() != 'y':
            return

    Path(dest).parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(url, stream=True)
    r.raise_for_status()

    total = int(r.headers.get('content-length', 0))
    downloaded = 0
    with open(dest, 'wb') as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)
            downloaded += len(chunk)
            if total:
                print(f"\r  {downloaded/1024/1024:.1f} MB", end='')
    print(f"\n  ✓ {dest}")

# Download data files
download(
    "http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-2024.csv",
    "data/pp-2024.csv",
    "Land Registry 2024 data (147 MB)"
)

download(
    "https://www.arcgis.com/sharing/rest/content/items/7606baba633d4bbca3f2510ab78acf61/data",
    "data/NSPL_FEB_2025.zip",
    "ONS postcode lookup (192 MB)"
)

# Extract NSPL
if os.path.exists("data/NSPL_FEB_2025.zip"):
    print("\nExtracting NSPL...")
    with zipfile.ZipFile("data/NSPL_FEB_2025.zip") as z:
        z.extractall("data/NSPL_temp")

    # Find and extract multi_csv
    multi_csv = list(Path("data/NSPL_temp/Data").glob("multi_csv*.zip"))[0]
    with zipfile.ZipFile(multi_csv) as z:
        z.extractall("data/NSPL")
    print("  ✓ data/NSPL/")

print("\n" + "="*60)
print("Manual download required:")
print("="*60)
print("\n1. Visit: https://statistics.ukdataservice.ac.uk/dataset/ons_2021_ts003_demography_household_composition")
print("2. Download: TS003-Household-Composition-2021-p19wpc-ONS.xlsx")
print("3. Save as: data/TS003_household_composition_p19wpc.xlsx")
print("\n4. Visit: https://geoportal.statistics.gov.uk/")
print("5. Search: Westminster Parliamentary Constituencies July 2024 names codes")
print("6. Save as: data/Westminster_Parliamentary_Constituency_names_and_codes_UK_as_at_12_24.csv")
