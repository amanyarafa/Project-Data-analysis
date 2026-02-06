import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st


st.title("Data Analysis Project")
st.title("Mid-Project Presented By Amany Arafa")
st.header("Database used is 50k Bug Dataset")

df = pd.read_csv('data/bug_dataset_50k.csv')

st.header("Where do most bugs fall?")
severity_counts = df["severity"].value_counts().sort_index()
st.bar_chart(severity_counts)