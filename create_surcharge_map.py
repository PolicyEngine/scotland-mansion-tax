#!/usr/bin/env python3
"""
Create hexagonal map visualization of UK high value council tax surcharge impact.

Generates a Plotly hexagonal map showing the estimated revenue allocation from
the new council tax surcharge on properties valued over £2m, based on the
November 2025 Budget announcement.
"""

import json
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path


def load_hex_coordinates():
    """Load constituency hex grid coordinates from HexJSON."""
    print("Loading hex grid coordinates...")
    with open('data/uk-constituencies-2024.hexjson') as f:
        hexjson = json.load(f)

    constituencies = []
    for gss_code, hex_data in hexjson['hexes'].items():
        constituencies.append({
            'gss_code': gss_code,
            'constituency': hex_data['n'],
            'q': hex_data['q'],
            'r': hex_data['r'],
        })

    df = pd.DataFrame(constituencies)
    df['grid_x'] = df['q']
    df['grid_y'] = df['r']

    print(f"Loaded {len(df)} constituencies")
    return df


def load_impact_data():
    """Load surcharge impact data."""
    print("Loading surcharge impact data...")
    impact_file = 'constituency_surcharge_impact.csv'

    if not Path(impact_file).exists():
        print(f"ERROR: {impact_file} not found")
        print("Run: python analyze_autumn_budget.py")
        return None

    df = pd.read_csv(impact_file)
    print(f"Loaded data for {len(df)} constituencies")
    return df


def create_hex_map(hex_coords, impact_data, color_by='properties'):
    """Create hexagonal map visualization."""
    print(f"Creating hexagonal map (colored by {color_by})...")

    if color_by == 'properties':
        value_col = 'properties'
        colorbar_title = 'Properties<br>above £2m'
        hover_format = lambda row: (
            f"{row['constituency']}<br>"
            f"Properties above £2m: {int(row['properties'])}<br>"
            f"Allocated revenue: £{int(row['allocated_revenue']):,}"
        )
    else:  # revenue
        value_col = 'allocated_revenue'
        colorbar_title = 'Allocated<br>Revenue (£)'
        hover_format = lambda row: (
            f"{row['constituency']}<br>"
            f"Allocated revenue: £{int(row['allocated_revenue']):,}<br>"
            f"Properties above £2m: {int(row['properties'])}"
        )

    # Merge hex coordinates with impact data
    merged = hex_coords.merge(
        impact_data[['constituency', 'properties', 'allocated_revenue']],
        on='constituency',
        how='left'
    )

    # Fill NaN values
    merged['properties'] = merged['properties'].fillna(0)
    merged['allocated_revenue'] = merged['allocated_revenue'].fillna(0)

    # Apply hexagonal positioning
    merged['plot_x'] = merged.apply(
        lambda row: row['grid_x'] + 0.5 if row['grid_y'] % 2 != 0 else row['grid_x'],
        axis=1
    )
    merged['plot_y'] = merged['grid_y']

    # Create hover text
    merged['hover_text'] = merged.apply(hover_format, axis=1)

    # Create Plotly figure
    fig = go.Figure()

    max_val = merged[value_col].max()

    fig.add_trace(go.Scatter(
        x=merged['plot_x'],
        y=merged['plot_y'],
        mode='markers',
        marker=dict(
            size=12,
            color=merged[value_col],
            colorscale='Teal',
            cmin=0,
            cmax=max_val,
            colorbar=dict(
                title=colorbar_title,
                thickness=15,
                len=0.8,
                x=0.95,
            ),
            symbol='hexagon',
            line=dict(width=0.5, color='white')
        ),
        text=merged['hover_text'],
        hoverinfo='text',
        showlegend=False
    ))

    fig.update_layout(
        title=dict(
            text=(
                'High Value Council Tax Surcharge Impact by Constituency<br>'
                '<sub>Estimated revenue allocation from £400m total '
                '(OBR November 2025)</sub>'
            ),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            visible=False,
            showgrid=False,
            zeroline=False,
            scaleanchor='y',
            scaleratio=1
        ),
        yaxis=dict(
            visible=False,
            showgrid=False,
            zeroline=False
        ),
        height=800,
        width=1000,
        plot_bgcolor='white',
        margin=dict(t=100, b=40, l=40, r=120),
        hovermode='closest'
    )

    return fig


def main():
    """Main execution."""
    print("=" * 70)
    print("High Value Council Tax Surcharge - Hexagonal Map Visualization")
    print("=" * 70)

    hex_coords = load_hex_coordinates()
    impact_data = load_impact_data()

    if impact_data is None:
        return

    # Create maps by both properties and revenue
    for color_by in ['properties', 'revenue']:
        fig = create_hex_map(hex_coords, impact_data, color_by)

        output_file = f'surcharge_map_by_{color_by}.html'
        fig.write_html(output_file)
        print(f"Saved {output_file}")

        try:
            png_file = f'surcharge_map_by_{color_by}.png'
            fig.write_image(png_file, width=1200, height=900)
            print(f"Saved {png_file}")
        except Exception as e:
            print(f"Could not save PNG: {e}")

    print("\n" + "=" * 70)
    print("Visualization complete!")
    print("=" * 70)


if __name__ == '__main__':
    main()
