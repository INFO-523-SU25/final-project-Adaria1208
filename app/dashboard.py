import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("data/Mental_Health_Final_Project_data.csv")

# Page config
st.set_page_config(page_title="Mental Health Dashboard", layout="wide")

# Title
st.markdown("# 🧠 Mental Health Care Access During COVID-19")
st.markdown(
    "This dashboard explores how mental health care access in the past 4 weeks varied by "
    "**state, gender, and time period** using data from the U.S. Census Household Pulse Survey."
)

# Sidebar filters
st.sidebar.header("🔍 Filter Data")

# Step 1: Select Group (e.g., By State, By Sex, etc.)
group_options = df["Group"].dropna().unique()
selected_group = st.sidebar.selectbox("Select Grouping", sorted(group_options))

# Step 2: Filter Subgroup based on selected Group
filtered_df = df[df["Group"] == selected_group]
subgroup_options = filtered_df["Subgroup"].dropna().unique()
selected_subgroups = st.sidebar.multiselect("Select Subgroup(s)", sorted(subgroup_options))

# Step 3: Filter Time Periods
time_options = df["Time Period Label"].dropna().unique()
selected_times = st.sidebar.multiselect("Select Time Period(s)", sorted(time_options))

# Apply filters to dataframe
mask = (
    (df["Group"] == selected_group) &
    (df["Subgroup"].isin(selected_subgroups)) &
    (df["Time Period Label"].isin(selected_times))
)
df_filtered = df[mask]

# Line Chart: Mental Health Care Access Over Time
st.markdown("## 📈 Mental Health Care Access Over Time")

if not df_filtered.empty:
    line_chart = px.line(
        df_filtered,
        x="Time Period Label",
        y="Value",
        color="Subgroup",
        markers=True,
        labels={"Value": "% Receiving Care", "Time Period Label": "Time Period"},
        title="Adults Receiving Mental Health Care (Past 4 Weeks)"
    )
    st.plotly_chart(line_chart, use_container_width=True)
else:
    st.info("No data to display with current filters.")

# Bar Chart: Average Access by Subgroup
st.markdown("## 📊 Average Mental Health Care Access by Subgroup")

if not df_filtered.empty:
    avg_df = df_filtered.groupby("Subgroup")["Value"].mean().reset_index()
    bar_chart = px.bar(
        avg_df,
        x="Subgroup",
        y="Value",
        labels={"Value": "Average % Receiving Care"},
        title="Average Mental Health Care Access by Subgroup"
    )
    st.plotly_chart(bar_chart, use_container_width=True)
else:
    st.info("Bar chart unavailable with current filters.")

# Data source footer
st.markdown("---")
st.markdown(
    "Data Source: U.S. Census Bureau Household Pulse Survey via [data.gov](https://data.gov)"
)
