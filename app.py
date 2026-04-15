import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="Handwashing Dashboard", layout="wide")

# -----------------------
# TITLE + DESCRIPTION
# -----------------------
st.title("Handwashing Dashboard")
st.markdown("""
This dashboard explores trends from 1844, when Semmelweis discovered that childbed 
            fever mortality rates were significantly higher in clinics staffed 
            by doctors compared to those staffed by midwives. He believed this 
            difference existed because midwives did not perform autopsies 
            before delivery procedures. As a result, he proposed that 
            practitioners should wash their hands to remove any foreign 
            materials, especially those from dead bodies.
""")


# -----------------------
# LOAD DATA
# -----------------------
# Replace with your dataset path
df = pd.read_csv(r"C:\Users\jayso\.vscode\DSBA-5122-Streamlit-Visualization\yearly_deaths_by_clinic-1.csv")

# -----------------------
# Mortality Rates Variable
# -----------------------

df["Mortality_Rates"] = df["Deaths"] / df["Births"].replace(0, pd.NA)

# -----------------------
# FILTERS (OPTIONAL)
# -----------------------
st.sidebar.header("Filters")

years = sorted(df["Year"].unique())
selected_years = st.sidebar.slider(
    "Select Year Range",
    min_value=int(min(years)),
    max_value=int(max(years)),
    value=(int(min(years)), int(max(years)))
)

filtered_df = df[(df["Year"] >= selected_years[0]) & (df["Year"] <= selected_years[1])]

# Optional category filter
if "Clinic" in df.columns:
    categories = df["Clinic"].unique()
    selected_categories = st.sidebar.multiselect(
        "Select Clinics",
        categories,
        default=categories
    )
    filtered_df = filtered_df[filtered_df["Clinic"].isin(selected_categories)]

# -----------------------
# VISUALIZATION 1: LINE CHART
# -----------------------
st.subheader("Mortality Rates Over Time")

line_fig = px.line(
    filtered_df,
    x="Year",
    y="Mortality_Rates",
    color="Clinic" if "Clinic" in df.columns else None,
    markers=True,
    title="Trend Over Time"
)

st.plotly_chart(line_fig, use_container_width=True)

# -----------------------
# VISUALIZATION 2: BAR CHART
# -----------------------
st.subheader("Comparison Across Clinics Total Deaths")

bar_fig = px.bar(
    filtered_df,
    x="Clinic" if "Clinic" in df.columns else "Year",
    y="Deaths",
    color="Clinic" if "Clinic" in df.columns else None,
    barmode="group",
    title="Comparison View"
)

st.plotly_chart(bar_fig, use_container_width=True)

# -----------------------
# FINDINGS / EXPLANATION
# -----------------------
st.subheader("Key Findings")

st.markdown("""
At the start in 1841, there was a large difference in mortality rates between 
            the two clinics. Clinic 1 consisted of trainee doctors with unwashed
             hands from autopsies, while Clinic 2 was staffed only by midwives 
            who focused on helping deliver babies. There was a reduction in 
            mortality rates over time, especially after the introduction of 
            handwashing practices in both clinics in 1847.
""")