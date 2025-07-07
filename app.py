import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("Book2.csv")
df.columns = df.columns.str.strip() \
                       .str.replace(r'[^a-zA-Z0-9 ]', '', regex=True) \
                       .str.replace(' ', '_') \
                       .str.replace(r'_+$', '', regex=True)

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

# Clean up any NaNs
df = df.dropna(subset=["Product"])

# Set page config
st.set_page_config(page_title="Perishable Product Dashboard", layout="wide")
st.title("📦 Perishable Products Dashboard")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"{df['total_selling_price'].sum():,.0f}")
col2.metric("Total Profit", f"{df['Profit'].sum():,.0f}")
col3.metric("Total Spoilage Loss", f"{df['Spoilage_Loss'].sum():,.0f}")

# Product summary
grouped = df.groupby("Product").agg({
    "Qty_Sold": "sum",
    "total_selling_price": "sum",
    "Profit": "sum",
    "Spoilage_Loss": "sum",
    "Profit_Margin": "mean"
}).sort_values("total_selling_price", ascending=False)

st.subheader("🔝 Top Selling Products")
st.bar_chart(grouped["Qty_Sold"].head(10))

st.subheader("💰 Most Profitable Products")
st.bar_chart(grouped["Profit"].head(10))

st.subheader("🗑️ Highest Spoilage Loss")
st.bar_chart(grouped["Spoilage_Loss"].sort_values(ascending=False).head(10))

# Daily trends
daily = df.groupby("Date")[["total_selling_price", "Profit", "Spoilage_Loss"]].sum()
st.subheader("📈 Daily Trends")
st.line_chart(daily)

# Alerts
df["Spoilage_Rate"] = (df["Spoilage"] / df["Qty_Bought"]) * 100
alerts = df[(df["Spoilage_Rate"] > 20) | (df["Profit_Margin"] < 5) | (df["Closing_Stock"] == 0)]

st.subheader("🚨 Alerts: High Spoilage, Low Margin, or Stockouts")
st.dataframe(alerts[["Date", "Product", "Spoilage_Rate", "Profit_Margin", "Closing_Stock"]])
