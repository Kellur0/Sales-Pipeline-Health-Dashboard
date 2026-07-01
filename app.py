import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Pipeline Dashboard", layout="wide")

st.title("📊 Sales Pipeline Health Dashboard")
st.markdown("Interactive dashboard for monitoring sales pipeline health.")

# Public CRM Sales Pipeline Dataset
DATA_URL = "https://raw.githubusercontent.com/ikebude/CRM-Sales-Analysis/main/sales_pipeline.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # Clean column names
    df.columns = df.columns.str.strip().str.replace(" ", "_")

    # Rename columns
    rename = {
        "sales_agent": "Sales_Rep",
        "close_value": "Deal_Value",
        "deal_stage": "Stage",
        "product": "Product",
        "close_date": "Close_Date"
    }

    df.rename(columns=rename, inplace=True)

    df["Close_Date"] = pd.to_datetime(df["Close_Date"], errors="coerce")
    df["Deal_Value"] = pd.to_numeric(df["Deal_Value"], errors="coerce")

    df.dropna(subset=["Deal_Value"], inplace=True)

    probability = {
        "Prospecting":0.10,
        "Engaging":0.25,
        "Qualification":0.40,
        "Proposal":0.60,
        "Negotiation":0.80,
        "Won":1.0,
        "Lost":0.0
    }

    df["Probability"] = df["Stage"].map(probability).fillna(0.50)
    df["Forecast"] = df["Deal_Value"] * df["Probability"]

    return df

df = load_data()

# Sidebar Filters

st.sidebar.header("Filters")

start = st.sidebar.date_input(
    "Start Date",
    value=df["Close_Date"].min().date()
)

end = st.sidebar.date_input(
    "End Date",
    value=df["Close_Date"].max().date()
)

df = df[
    (df["Close_Date"] >= pd.to_datetime(start)) &
    (df["Close_Date"] <= pd.to_datetime(end))
]

reps = sorted(df["Sales_Rep"].dropna().unique())

selected_rep = st.sidebar.multiselect(
    "Sales Representative",
    reps,
    default=reps
)

df = df[df["Sales_Rep"].isin(selected_rep)]

products = sorted(df["Product"].dropna().unique())

selected_product = st.sidebar.multiselect(
    "Product",
    products,
    default=products
)

df = df[df["Product"].isin(selected_product)]

# KPIs

pipeline_value = df["Deal_Value"].sum()
average_deal = df["Deal_Value"].mean()
forecast = df["Forecast"].sum()

won = len(df[df["Stage"]=="Won"])
lost = len(df[df["Stage"]=="Lost"])

win_rate = won/(won+lost) if (won+lost)>0 else 0

c1,c2,c3,c4 = st.columns(4)

c1.metric("Pipeline Value",f"${pipeline_value:,.0f}")
c2.metric("Average Deal Size",f"${average_deal:,.0f}")
c3.metric("Forecast Revenue",f"${forecast:,.0f}")
c4.metric("Win Rate",f"{win_rate:.1%}")

st.divider()

# Pipeline Value by Stage

stage = df.groupby("Stage",as_index=False)["Deal_Value"].sum()

fig = px.bar(
    stage,
    x="Stage",
    y="Deal_Value",
    color="Stage",
    title="Pipeline Value by Stage"
)

st.plotly_chart(fig,width="stretch")

# Average Deal Size by Stage

avg = df.groupby("Stage",as_index=False)["Deal_Value"].mean()

fig = px.bar(
    avg,
    x="Stage",
    y="Deal_Value",
    color="Stage",
    title="Average Deal Size by Stage"
)

st.plotly_chart(fig,width="stretch")

# Revenue Forecast

forecast_df = df.groupby("Stage",as_index=False)["Forecast"].sum()

fig = px.bar(
    forecast_df,
    x="Stage",
    y="Forecast",
    color="Stage",
    title="Weighted Revenue Forecast"
)

st.plotly_chart(fig,width="stretch")

# Sales Rep Performance

rep = (
    df.groupby("Sales_Rep",as_index=False)["Deal_Value"]
    .sum()
    .sort_values("Deal_Value",ascending=False)
)

fig = px.bar(
    rep,
    x="Sales_Rep",
    y="Deal_Value",
    color="Sales_Rep",
    title="Sales Rep Performance"
)

st.plotly_chart(fig,width="stretch")

# Conversion Rates

conversion = df.groupby("Stage").size().reset_index(name="Deals")
conversion["Conversion Rate (%)"] = (
    conversion["Deals"] /
    conversion["Deals"].sum()
)*100

st.subheader("Conversion Rates")

st.dataframe(conversion,width="stretch")

# Raw Data

with st.expander("View Dataset"):
    st.dataframe(df,width="stretch")
