# dashboard_app.py

import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# --- Add project root to Python's path ---
FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
# -----------------------------------------

from utils.data_loader import generate_dummy_data
from components.ui_components import (
    render_styling,
    render_sidebar_filters,
    render_header_and_kpis,
    render_charts,
    render_historical_trend,
    render_violations_feed,
)

def main():
    """Main function to orchestrate the Streamlit dashboard application."""
    st.set_page_config(
        page_title="Advanced Compliance Dashboard",
        page_icon="🔎",
        layout="wide",
        initial_sidebar_state="expanded" # Keep sidebar open by default
    )

    # --- Load Data ---
    # In a real app, you would load this once and cache it
    df_full = generate_dummy_data(500)

    # --- Render UI & Get Filters ---
    render_styling()
    selected_platforms, selected_violations, selected_date_range = render_sidebar_filters(df_full)

    # --- Apply Filters ---
    start_date, end_date = selected_date_range
    start_datetime = pd.to_datetime(start_date)
    end_datetime = pd.to_datetime(end_date) + pd.Timedelta(days=1)

    df_filtered = df_full[
        (df_full['platform'].isin(selected_platforms)) &
        (df_full['timestamp'] >= start_datetime) &
        (df_full['timestamp'] < end_datetime)
    ]
    df_violations_filtered = df_filtered[
        (df_filtered['is_compliant'] == False) &
        (df_filtered['violation_type'].isin(selected_violations))
    ]
    
    # --- Render Main Dashboard ---
    render_header_and_kpis(df_filtered)
    st.markdown("---")
    render_charts(df_filtered, df_violations_filtered)
    render_historical_trend(df_violations_filtered)
    render_violations_feed(df_violations_filtered)


if __name__ == "__main__":
    main()
