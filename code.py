import streamlit as st
import pandas as pd
import altair as alt

# Load your dataset
df = pd.read_csv("Sample - Superstore.csv", encoding="ISO-8859-1")


# Preprocessing
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month_name()

st.title("Superstore Business Decision Dashboard")

# Sidebar filters
st.sidebar.header("Filter Data")
region = st.sidebar.multiselect("Select Region(s):", options=df["Region"].unique(), default=df["Region"].unique())
category = st.sidebar.multiselect("Select Category:", options=df["Category"].unique(), default=df["Category"].unique())
year = st.sidebar.multiselect("Select Year(s):", options=sorted(df["Year"].unique()), default=sorted(df["Year"].unique()))

# Apply filters
filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Year"].isin(year))
]

# KPI Section
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
avg_discount = filtered_df["Discount"].mean()

st.metric("Total Sales", f"${total_sales:,.2f}")
st.metric("Total Profit", f"${total_profit:,.2f}")
st.metric("Avg Discount", f"{avg_discount:.2%}")

# Sales by Category
st.subheader("Sales by Category")
sales_cat = filtered_df.groupby("Category")["Sales"].sum().reset_index()
chart1 = alt.Chart(sales_cat).mark_bar().encode(
    x=alt.X("Category", sort='-y'),
    y="Sales",
    color="Category"
)
st.altair_chart(chart1, use_container_width=True)

# Profit by Region
st.subheader("Profit by Region")
profit_region = filtered_df.groupby("Region")["Profit"].sum().reset_index()
chart2 = alt.Chart(profit_region).mark_bar().encode(
    x=alt.X("Region", sort='-y'),
    y="Profit",
    color=alt.condition(
        alt.datum.Profit > 0, alt.value("green"), alt.value("red")
    )
)
st.altair_chart(chart2, use_container_width=True)

# Discount vs Profit Scatter
st.subheader("Discount vs Profit")
chart3 = alt.Chart(filtered_df).mark_circle(size=60).encode(
    x="Discount",
    y="Profit",
    color="Category",
    tooltip=["Category", "Sub-Category", "Sales", "Profit", "Discount"]
).interactive()
st.altair_chart(chart3, use_container_width=True)

# Ship Mode Breakdown
st.subheader("Shipping Mode Distribution")
ship_mode = filtered_df["Ship Mode"].value_counts().reset_index()
ship_mode.columns = ["Ship Mode", "Count"]
chart4 = alt.Chart(ship_mode).mark_arc().encode(
    theta="Count",
    color="Ship Mode",
    tooltip=["Ship Mode", "Count"]
)
st.altair_chart(chart4, use_container_width=True)
