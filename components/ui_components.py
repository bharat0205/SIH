# components/ui_components.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Apply global seaborn style
sns.set_theme(style="whitegrid")

def render_styling():
    """Injects custom CSS for a more dynamic and 'fancy' UI, including animations."""
    st.markdown("""
    <style>
        @keyframes slideInFade {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .main-title {
            font-size: 38px !important; font-weight: bold; color: #1E2A78; padding-bottom: 20px;
            animation: slideInFade 0.8s ease-out;
        }
        div[data-testid="metric-container"] {
            background-color: #FFFFFF; border: 1px solid #E0E0E0; border-radius: 12px;
            padding: 20px; box-shadow: 0 6px 12px rgba(0,0,0,0.08);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            animation: slideInFade 0.8s ease-out forwards;
        }
        div[data-testid="metric-container"]:hover {
            transform: translateY(-5px); box-shadow: 0 12px 24px rgba(0,0,0,0.12);
        }
        .section-header {
            font-size: 26px; font-weight: bold; color: #333; padding-top: 20px;
            padding-bottom: 15px; border-bottom: 2px solid #1E2A78; margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar_filters(df):
    """Renders the sidebar with interactive filters and returns the selections."""
    st.sidebar.header("Filter & Analyze")

    platforms = sorted(df['platform'].unique())
    selected_platforms = st.sidebar.multiselect(
        "Filter by E-Commerce Platform",
        options=platforms,
        default=platforms
    )

    violation_types = sorted(df[df['violation_type'].notna()]['violation_type'].unique())
    selected_violations = st.sidebar.multiselect(
        "Filter by Violation Type",
        options=violation_types,
        default=violation_types
    )
    
    min_date = df['timestamp'].min().date()
    max_date = df['timestamp'].max().date()
    selected_date_range = st.sidebar.date_input(
        "Filter by Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    st.sidebar.markdown("---")
    st.sidebar.info("Use the filters above to dynamically update the dashboard.")

    return selected_platforms, selected_violations, selected_date_range


def render_header_and_kpis(df):
    """Displays the main title and the top-level KPI metrics based on filtered data."""
    st.markdown('<p class="main-title">Automated Compliance Dashboard</p>', unsafe_allow_html=True)
    
    active_violations = len(df[df['is_compliant'] == False])
    platforms_monitored = df['platform'].nunique()
    overall_compliance_rate = (len(df[df['is_compliant'] == True]) / len(df)) * 100 if not df.empty else 0

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric(label="Overall Compliance", value=f"{overall_compliance_rate:.1f}%")
    kpi2.metric(label="Active Violations in View", value=f"{active_violations}")
    kpi3.metric(label="Platforms in View", value=f"{platforms_monitored}")


def render_charts(df, df_violations):
    """Renders the data visualization charts based on filtered data."""
    st.markdown('<p class="section-header">Compliance Analytics</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if not df.empty:
            compliance_by_platform = df.groupby('platform')['is_compliant'].mean().reset_index()
            compliance_by_platform['compliance_rate'] = compliance_by_platform['is_compliant'] * 100
            
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.barplot(
                data=compliance_by_platform,
                x="compliance_rate", y="platform",
                palette="RdYlGn", ax=ax
            )
            ax.set_title("Compliance Rate by Platform")
            ax.set_xlabel("Compliance Rate (%)")
            ax.set_ylabel("Platform")
            ax.set_xlim(0, 100)
            st.pyplot(fig)
    
    with col2:
        if not df_violations.empty:
            violation_counts = df_violations['violation_type'].value_counts().reset_index()
            violation_counts.columns = ['violation_type', 'count']

            fig, ax = plt.subplots(figsize=(5, 5))
            wedges, texts, autotexts = ax.pie(
                violation_counts['count'],
                labels=violation_counts['violation_type'],
                autopct='%1.1f%%',
                startangle=90
            )
            # Donut effect
            centre_circle = plt.Circle((0, 0), 0.70, fc='white')
            fig.gca().add_artist(centre_circle)
            ax.set_title("Violations Breakdown")
            st.pyplot(fig)


def render_historical_trend(df_violations):
    """Renders a line chart showing the trend of violations over time."""
    st.markdown('<p class="section-header">Historical Violation Trends</p>', unsafe_allow_html=True)
    if not df_violations.empty:
        df_violations['date'] = df_violations['timestamp'].dt.date
        violations_over_time = df_violations.groupby('date').size().reset_index(name='count')

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(
            violations_over_time['date'],
            violations_over_time['count'],
            marker="o", color="#1E2A78"
        )
        ax.set_title("Daily Violation Count")
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Violations")
        plt.xticks(rotation=45)
        st.pyplot(fig)


def render_violations_feed(df_violations):
    """Renders the real-time feed and data export button."""
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        st.markdown('<p class="section-header">Filtered Violations Feed</p>', unsafe_allow_html=True)
    with col2:
        if not df_violations.empty:
            csv = df_violations.to_csv(index=False).encode('utf-8')
            st.download_button(
               "📥 Download Data as CSV",
               csv,
               "compliance_violations.csv",
               "text/csv",
               key='download-csv'
            )

    for index, row in df_violations.head(10).iterrows():
        with st.expander(f"🔴 **{row['violation_type']}** on **{row['platform']}**"):
            st.write(f"**Product:** {row['product_name']}")
            st.write(f"**Brand:** {row['brand']}")
            st.write(f"**Severity:** `{row['severity']}`")
            st.write(f"**Date Detected:** {row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
