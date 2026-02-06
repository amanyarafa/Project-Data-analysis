# -------------------------------
# IMPORT LIBRARY
# ------------------------------

import streamlit as st
import pandas as pd
import numpy as np
# ---------------------------------------------------------------------

st.set_page_config(page_title="Software Bug Analysis Dashboard", layout="wide")

st.title("Mid-Project By Amany Arafa")
st.header("Database used is 50k Bug Dataset")

# -------------------------------
# LOAD DATA
# -------------------------------

df = pd.read_csv('data/bug_dataset_50k.csv')

# -------------------------------
# CLEANING DATA
# -------------------------------

df["error_code"] = df["error_code"].astype("Int64")  # Convert Error code to int instead of float
df["bug_id"] = df["bug_id"].astype("string").str.strip().str.upper() # Convert BUG_ID to string instead of object
df["severity"] = df["severity"].astype("string").str.strip().str.capitalize() # Convert severity to string instead of object
df["created_at"] = pd.to_datetime(df["created_at"])  # Convert created_at to datetime instead of object


# -------------------------------
# SIDEBAR
# -------------------------------

st.sidebar.title("Main Tasks")
page = st.sidebar.radio(
    "Go to",
    [
        "Bug Dataset Overview",
        "Severity Analysis",
        "Time Trends",
        "Domain & Tech Risk",
        "Root Cause Analysis",
        "Developer Role Analysis"
    ]
)

# -------------------------------
# BUG DATASET OVERVIEW PAGE
# -------------------------------
if page == "Bug Dataset Overview":

    st.title("Bug Dataset Overview")

    total_bugs = len(df)
    critical_count = (df["severity"] == "Critical").sum() #vCount Critical bugs
    critical_percent = round((critical_count / total_bugs) * 100, 2) # Critical Bugs Percentages
    missing_values = df["error_code"].isnull().sum() # Count the missing values

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Bugs", total_bugs)
    col2.metric("Critical Bugs (%)", f"{critical_percent}%")
    col3.metric("Missing Error Codes", missing_values)

    st.subheader("Dataset Sample Preview")
    st.dataframe(df.head())


# -------------------------------
# SEVERITY ANALYSIS
# -------------------------------
elif page == "Severity Analysis":

    st.title("Severity Distribution")

    severity_counts = df["severity"].value_counts().sort_index()
    st.bar_chart(severity_counts)

    st.subheader("Severity by Environment")
    env_sev = pd.crosstab(df["environment"], df["severity"])
    env_sev["Total"] = env_sev.sum(axis=1)
    st.dataframe(env_sev)

    st.subheader("Severity by Domain")
    dom_sev = pd.crosstab(df["bug_domain"], df["severity"])
    dom_sev["Total"] = dom_sev.sum(axis=1)
    st.dataframe(dom_sev)

    st.subheader("Severity by Teck")
    tech_sev = pd.crosstab(df["tech_stack"], df["severity"])
    tech_sev["Total"] = tech_sev.sum(axis=1)
    st.dataframe(tech_sev)


# -------------------------------
# TIME TRENDS
# -------------------------------
elif page == "Time Trends":

    st.title("Bug Trends Over Time")

    monthly_trend = (
        df.groupby(df["created_at"].dt.to_period("M"))
        .size() # Count all bugs in one month
    )

    monthly_trend.index = monthly_trend.index.astype(str)
    st.line_chart(monthly_trend)

    st.subheader("Critical Bugs Trend")

    critical_trend = (
        df[df["severity"] == "Critical"]
        .groupby(df["created_at"].dt.to_period("M"))
        .size()
    )

    critical_trend.index = critical_trend.index.astype(str)
    st.line_chart(critical_trend)


# -------------------------------
# DOMAIN & TECH RISK
# -------------------------------
elif page == "Domain & Tech Risk":

    st.title("Domain & Tech Risk Analysis")

    severity_score_map = {
        "Low": 1,
        "Medium": 2,
        "High": 3,
        "Critical": 4
    }

    df["severity_score"] = df["severity"].map(severity_score_map)

    st.subheader("Average Severity by Domain")
    domain_risk = df.groupby("bug_domain")["severity_score"].mean().sort_values(ascending=False)
    st.bar_chart(domain_risk)

    st.subheader("Average Severity by Tech Stack")
    tech_risk = df.groupby("tech_stack")["severity_score"].mean().sort_values(ascending=False)
    st.bar_chart(tech_risk)


# -------------------------------
# ROOT CAUSE ANALYSIS
# -------------------------------
elif page == "Root Cause Analysis":

    st.title("Root Cause Analysis")

    st.subheader("Top Root Causes")
    root_counts = df["root_cause"].value_counts().head(10)
    st.bar_chart(root_counts)

    st.subheader("Root Cause vs Severity")
    root_sev = pd.crosstab(df["root_cause"], df["severity"])
    st.dataframe(root_sev.head(15))


# -------------------------------
# DEVELOPER ROLE ANALYSIS
# -------------------------------
elif page == "Developer Role Analysis":

    st.title("Developer Role Analysis")

    st.subheader("Top Developer Affect Software Bugs")
    dev_counts = df["developer_role"].value_counts().head(3)
    st.bar_chart(dev_counts)

    st.subheader("Developer Role vs Severity")
    root_sev = pd.crosstab(df["developer_role"], df["severity"])
    st.dataframe(root_sev.head(15))

