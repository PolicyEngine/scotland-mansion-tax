#!/usr/bin/env python3
"""
Download all required data files for UK mansion tax analysis.

This script downloads:
1. UK Land Registry Price Paid Data (2024)
2. ONS National Statistics Postcode Lookup (NSPL)
3. ONS Westminster Parliamentary Constituency names/codes
4. Census 2021 TS003 Household Composition data

Data sources:
- Land Registry: https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads
- ONS NSPL: https://geoportal.statistics.gov.uk/
- Census 2021: https://www.nomisweb.co.uk/
"""

import os
import zipfile
import requests
from pathlib import Path

def download_file(url, destination, description):
    """Download a file with progress indicator."""
    print(f"\nDownloading {description}...")
    print(f"URL: {url}")
    print(f"Destination: {destination}")

    # Check if file already exists
    if os.path.exists(destination):
        response = input(f"File already exists. Re-download? (y/N): ")
        if response.lower() != 'y':
            print("Skipping download.")
            return

    # Create directory if needed
    Path(destination).parent.mkdir(parents=True, exist_ok=True)

    # Download
    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get('content-length', 0))
    block_size = 8192
    downloaded = 0

    with open(destination, 'wb') as f:
        for chunk in response.iter_content(block_size):
            f.write(chunk)
            downloaded += len(chunk)
            if total_size > 0:
                percent = (downloaded / total_size) * 100
                print(f"\rProgress: {percent:.1f}% ({downloaded / 1024 / 1024:.1f} MB)", end='')

    print(f"\n✓ Downloaded {description}")

def extract_zip(zip_path, extract_to, description):
    """Extract a zip file."""
    print(f"\nExtracting {description}...")
    print(f"From: {zip_path}")
    print(f"To: {extract_to}")

    Path(extract_to).mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    print(f"✓ Extracted {description}")

def main():
    print("="*80)
    print("UK MANSION TAX ANALYSIS - DATA DOWNLOAD SCRIPT")
    print("="*80)

    # 1. Land Registry Price Paid Data - 2024
    download_file(
        url="http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-2024.csv",
        destination="pp-2024.csv",
        description="Land Registry Price Paid Data 2024 (147 MB)"
    )

    # 2. ONS NSPL - February 2025
    nspl_zip = "NSPL_FEB_2025.zip"
    download_file(
        url="https://www.arcgis.com/sharing/rest/content/items/7606baba633d4bbca3f2510ab78acf61/data",
        destination=nspl_zip,
        description="ONS National Statistics Postcode Lookup February 2025 (192 MB)"
    )

    # Extract NSPL to Data/multi_csv/
    if os.path.exists(nspl_zip):
        # First extract the main zip
        extract_zip(nspl_zip, "Data/NSPL_temp", "NSPL main archive")

        # Find the Data folder inside and extract multi_csv
        data_folder = Path("Data/NSPL_temp/Data")
        if data_folder.exists():
            # Find the multi_csv zip inside
            multi_csv_zip = list(data_folder.glob("multi_csv*.zip"))
            if multi_csv_zip:
                extract_zip(
                    multi_csv_zip[0],
                    "Data/multi_csv",
                    "NSPL postcode files (124 CSVs)"
                )
            else:
                print("Warning: Could not find multi_csv zip file")
        else:
            print("Warning: NSPL structure may have changed")

    # 3. Westminster Parliamentary Constituency names and codes
    download_file(
        url="https://geoportal.statistics.gov.uk/datasets/ons::westminster-parliamentary-constituencies-july-2024-names-and-codes-in-the-uk-v2/about",
        destination="Documents/Westminster_Parliamentary_Constituency_names_and_codes_UK_as_at_12_24.csv",
        description="Westminster Parliamentary Constituency names and codes (July 2024)"
    )

    print("\n" + "="*80)
    print("NOTE: Census 2021 TS003 household data")
    print("="*80)
    print("\nThe Census 2021 TS003 household composition data must be downloaded")
    print("manually from the UK Data Service:")
    print("\n  URL: https://statistics.ukdataservice.ac.uk/dataset/ons_2021_ts003_demography_household_composition")
    print("\nDownload:")
    print("  - TS003-Household-Composition-2021-p19wpc-ONS.xlsx")
    print("\nSave as:")
    print("  - TS003_household_composition_p19wpc.xlsx")
    print("\nThis file contains household counts for all 2024 Westminster constituencies.")

    print("\n" + "="*80)
    print("DATA DOWNLOAD COMPLETE!")
    print("="*80)
    print("\nNext steps:")
    print("1. Manually download Census TS003 data (see note above)")
    print("2. Run: python analyze_2024_complete.py")
    print("3. See 2024_ANALYSIS_SUMMARY.md for results")

if __name__ == '__main__':
    main()
