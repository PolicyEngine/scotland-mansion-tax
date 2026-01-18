"""
Data loading and downloading module.

Handles:
- Council Tax Band data from statistics.gov.scot
- NRS constituency population data
- Wealth factor calculations
"""

import urllib.parse
import urllib.request
from pathlib import Path
from typing import Tuple, Dict

import pandas as pd

# Default data directory (can be overridden)
# Try to find the data directory relative to the current working directory first,
# then fall back to relative to the package location
def get_data_dir() -> Path:
    """Get the data directory, creating if necessary.

    Searches in order:
    1. ./data (relative to current working directory)
    2. Package installation directory (for installed packages)
    """
    # First try current working directory
    cwd_data = Path.cwd() / "data"
    if cwd_data.exists():
        return cwd_data

    # Try relative to package location (for development)
    pkg_data = Path(__file__).parent.parent.parent.parent / "data"
    if pkg_data.exists():
        return pkg_data

    # Create in current working directory if doesn't exist
    cwd_data.mkdir(exist_ok=True)
    return cwd_data


def download_council_tax_data(data_dir: Path = None, verbose: bool = True) -> bool:
    """Download Council Tax Band data from statistics.gov.scot SPARQL endpoint.

    Args:
        data_dir: Directory to save data to. Defaults to package data dir.
        verbose: Print progress messages.

    Returns:
        True if download succeeded, False otherwise.
    """
    if data_dir is None:
        data_dir = get_data_dir()

    sparql_query = """
PREFIX qb: <http://purl.org/linked-data/cube#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sdmx: <http://purl.org/linked-data/sdmx/2009/dimension#>
PREFIX dim: <http://statistics.gov.scot/def/dimension/>

SELECT ?constituency ?band ?dwellings
WHERE {
  ?obs qb:dataSet <http://statistics.gov.scot/data/dwellings-by-council-tax-band-summary-current-geographic-boundaries> ;
       sdmx:refArea ?areaUri ;
       sdmx:refPeriod ?periodUri ;
       dim:councilTaxBand ?bandUri ;
       <http://statistics.gov.scot/def/measure-properties/count> ?dwellings .

  ?areaUri rdfs:label ?constituency .
  ?bandUri rdfs:label ?band .
  ?periodUri rdfs:label ?year .

  FILTER(CONTAINS(STR(?areaUri), 'S16'))
  FILTER(?year = '2023')
}
ORDER BY ?constituency ?band
"""
    endpoint = "https://statistics.gov.scot/sparql.csv"
    url = f"{endpoint}?query={urllib.parse.quote(sparql_query)}"

    if verbose:
        print("   Downloading Council Tax data from statistics.gov.scot...")

    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            data = response.read().decode("utf-8")

        # Save to file
        band_file = data_dir / "council_tax_bands_by_constituency.csv"
        band_file.write_text(data)
        if verbose:
            print(f"   ✓ Downloaded and saved {len(data.splitlines())} rows")
        return True
    except Exception as e:
        if verbose:
            print(f"   ⚠️ Download failed: {e}")
        return False


def load_wealth_factors(
    data_dir: Path = None, verbose: bool = True
) -> Tuple[Dict[str, float], str]:
    """Load wealth factors from Council Tax Band F-H data.

    Uses Band F-H (highest bands) as a proxy for high-value property concentration.
    Wealth factor = constituency's Band F-H % / Scotland average Band F-H %

    Why Band F-H instead of Band H alone?
    -------------------------------------
    Band H (>£212k in 1991, ~>£1.15m in 2024) would be the ideal proxy for £1m+
    properties. However, statistics.gov.scot only provides constituency-level data
    in the "summary" dataset which groups bands as A-C, D-E, F-H. The "detailed"
    dataset with individual bands A-H is only available at Data Zone level, not
    constituency level.

    Band F-H includes:
    - Band F: £80k-£106k (1991) → ~£430k-£570k (2024)
    - Band G: £106k-£212k (1991) → ~£570k-£1.15m (2024)
    - Band H: >£212k (1991) → >£1.15m (2024)

    This dilutes the signal with £400k-£1m properties, but is the best available
    proxy at constituency level. Areas with high Band F-H concentration still
    correlate strongly with £1m+ property density.

    Source: statistics.gov.scot (2023)
    https://statistics.gov.scot/data/dwellings-by-council-tax-band-summary-current-geographic-boundaries

    Args:
        data_dir: Directory containing data files. Defaults to package data dir.
        verbose: Print progress messages.

    Returns:
        tuple: (dict mapping constituency -> wealth factor, str data source indicator)
               Returns ({}, "fallback_population_only") if data unavailable
    """
    if data_dir is None:
        data_dir = get_data_dir()

    band_file = data_dir / "council_tax_bands_by_constituency.csv"

    # Download if not present
    if not band_file.exists():
        if verbose:
            print("   Council tax band data not found locally.")
        if not download_council_tax_data(data_dir, verbose):
            if verbose:
                print("=" * 60)
                print("⚠️  WARNING: Council Tax data unavailable!")
                print("   Results will use POPULATION-ONLY weights (less accurate).")
                print("   To fix: ensure statistics.gov.scot is accessible and retry.")
                print("=" * 60)
            return {}, "fallback_population_only"

    # Load the data
    df = pd.read_csv(band_file)

    # Pivot to get Band F-H and Total for each constituency
    df_fh = df[df["band"] == "Bands F-H"][["constituency", "dwellings"]].copy()
    df_fh.columns = ["constituency", "band_fh"]

    df_total = df[df["band"] == "Total Dwellings"][["constituency", "dwellings"]].copy()
    df_total.columns = ["constituency", "total"]

    # Merge and calculate percentages
    df_merged = df_fh.merge(df_total, on="constituency")
    df_merged["fh_pct"] = df_merged["band_fh"] / df_merged["total"]

    # Calculate Scotland average Band F-H percentage
    scotland_fh = df_merged["band_fh"].sum()
    scotland_total = df_merged["total"].sum()
    scotland_avg_pct = scotland_fh / scotland_total

    if verbose:
        print(
            f"   Scotland average Band F-H: {scotland_avg_pct:.1%} "
            f"({scotland_fh:,} of {scotland_total:,} dwellings)"
        )

    # Calculate wealth factor for each constituency
    # Factor = constituency Band F-H % / Scotland average Band F-H %
    wealth_factors = {}
    for _, row in df_merged.iterrows():
        factor = row["fh_pct"] / scotland_avg_pct
        wealth_factors[row["constituency"]] = round(factor, 2)

    if verbose:
        # Print top and bottom constituencies for verification
        sorted_factors = sorted(
            wealth_factors.items(), key=lambda x: x[1], reverse=True
        )
        print("   Top 5 by Band F-H concentration:")
        for name, factor in sorted_factors[:5]:
            pct = df_merged[df_merged["constituency"] == name]["fh_pct"].values[0]
            print(f"      {name}: {factor:.2f}x ({pct:.1%} Band F-H)")

        print("   Bottom 3 by Band F-H concentration:")
        for name, factor in sorted_factors[-3:]:
            pct = df_merged[df_merged["constituency"] == name]["fh_pct"].values[0]
            print(f"      {name}: {factor:.2f}x ({pct:.1%} Band F-H)")

    return wealth_factors, "band_fh"


def load_population_data(data_dir: Path = None, verbose: bool = True) -> pd.DataFrame:
    """Load NRS constituency population data.

    Args:
        data_dir: Directory containing data files. Defaults to package data dir.
        verbose: Print progress messages.

    Returns:
        DataFrame with constituency and population columns.

    Raises:
        FileNotFoundError: If population data file not found.
    """
    if data_dir is None:
        data_dir = get_data_dir()

    pop_file = data_dir / "constituency_population.csv"

    if not pop_file.exists():
        if verbose:
            print("⚠️  Population data not found. Checking for Excel source...")

        # Extract from Excel if CSV doesn't exist
        xlsx_file = data_dir / "nrs_constituency_population.xlsx"
        if xlsx_file.exists():
            if verbose:
                print("   Extracting from NRS Excel file...")
            df = pd.read_excel(xlsx_file, sheet_name="2021", skiprows=2)
            df.columns = ["constituency", "code", "sex", "total"] + [
                f"age_{i}" for i in range(len(df.columns) - 4)
            ]
            df_pop = df[df["sex"] == "Persons"][["constituency", "total"]].copy()
            df_pop.columns = ["constituency", "population"]
            df_pop = df_pop.dropna()
            df_pop["population"] = df_pop["population"].astype(int)
            df_pop.to_csv(pop_file, index=False)
            if verbose:
                print(f"   ✓ Saved {len(df_pop)} constituencies to {pop_file}")
        else:
            raise FileNotFoundError(
                f"Population data not found. Expected one of:\n"
                f"  - {pop_file}\n"
                f"  - {xlsx_file}\n\n"
                f"Run 'scotland-mansion-tax download --all' to download required data."
            )

    return pd.read_csv(pop_file)


def download_all(data_dir: Path = None, verbose: bool = True) -> bool:
    """Download all required data files.

    Args:
        data_dir: Directory to save data to. Defaults to package data dir.
        verbose: Print progress messages.

    Returns:
        True if all downloads succeeded, False otherwise.
    """
    if data_dir is None:
        data_dir = get_data_dir()

    success = True

    if verbose:
        print("Downloading required data files...")
        print()

    # Council Tax data
    if verbose:
        print("1. Council Tax Band data (statistics.gov.scot):")
    if not download_council_tax_data(data_dir, verbose):
        success = False

    if verbose:
        print()

    # Check population data
    pop_file = data_dir / "constituency_population.csv"
    if verbose:
        print("2. Population data (NRS):")
    if pop_file.exists():
        if verbose:
            print("   ✓ Already present")
    else:
        if verbose:
            print("   ⚠️ Not found - include in repo or download manually from NRS")
        success = False

    # Check geojson
    geojson_file = data_dir / "scottish_parliament_constituencies.geojson"
    if verbose:
        print()
        print("3. Constituency boundaries (GeoJSON):")
    if geojson_file.exists():
        if verbose:
            print("   ✓ Already present")
    else:
        if verbose:
            print("   ⚠️ Not found - include in repo")
        success = False

    return success
