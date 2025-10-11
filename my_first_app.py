import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Title
st.title("📊 Sales Dashboard")

# Upload CSV
uploaded_file = st.file_uploader("Upload your Sales Data file", type=["csv","xlsx"])

if uploaded_file is not None:
    # check extension file and read accordingly
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)

    # Show dataset preview
    st.subheader("📋 Data Preview")
    st.dataframe(df.head())

    # Basic statistics
    st.subheader("📈 Basic Statistics")
    st.write(df.describe())

    # Sidebar filters
    st.sidebar.header("Filters")
    if "Region" in df.columns:
        regions = st.sidebar.multiselect("Select Region(s)", df["Region"].unique())
        if regions:
            df = df[df["Region"].isin(regions)]

    if "Category" in df.columns:
        categories = st.sidebar.multiselect("Select Category", df["Category"].unique())
        if categories:
            df = df[df["Category"].isin(categories)]

    # Layout for charts
    col1, col2 = st.columns(2)

    with col1:
        if "Sales" in df.columns and "Category" in df.columns:
            st.subheader("💰 Sales by Category")
            fig, ax = plt.subplots()
            sns.barplot(x="Category", y="Sales", data=df, estimator=sum, ci=None, ax=ax)
            st.pyplot(fig)

    with col2:
        if "Sales" in df.columns and "Region" in df.columns:
            st.subheader("🌍 Sales by Region")
            fig, ax = plt.subplots()
            sales_by_region = df.groupby("Region")["Sales"].sum().reset_index()
            sns.barplot(x="Region", y="Sales", data=sales_by_region, ax=ax)
            st.pyplot(fig)

    # Time series plot
    if "Date" in df.columns and "Sales" in df.columns:
        st.subheader("⏳ Sales Over Time")
        df["Date"] = pd.to_datetime(df["Date"])
        sales_over_time = df.groupby("Date")["Sales"].sum().reset_index()
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(sales_over_time["Date"], sales_over_time["Sales"], marker="o")
        ax.set_xlabel("Date")
        ax.set_ylabel("Total Sales")
        st.pyplot(fig)

else:
    st.info("👆 Please upload a CSV file to start.")