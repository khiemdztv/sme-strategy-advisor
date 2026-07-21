import pandas as pd
import os
import streamlit as st


def format_currency(val):
    if pd.isna(val) or val is None:
        return "N/A"
    return f"${val:,.0f}"


def format_percent(val):
    if pd.isna(val) or val is None:
        return "0.0%"
    return f"{val:.1f}%"


@st.cache_data(ttl=600)
def load_processed_data(processed_file="data/processed/tasks_scored.csv"):
    """
    Loads pre-scored processed dataset with caching.
    """
    if os.path.exists(processed_file):
        return pd.read_csv(processed_file, encoding="utf-8")
    else:
        from etl import load_and_merge_raw_data
        from scoring import calculate_scores_and_flags
        df_merged = load_and_merge_raw_data()
        df_scored = calculate_scores_and_flags(df_merged)
        return df_scored
