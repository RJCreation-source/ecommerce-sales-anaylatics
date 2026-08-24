import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Analytics", layout="wide")
st.title("📊 E-Commerce Sales Analytics Dashboard")

@st.cache_data
def get_data():
    df = pd.read_csv('data/sales_x5f_data.csv.xlsx')
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    return df

df = get_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filters")
category_filter = st.sidebar.multiselect("Category", options=df['Category'].unique(), default=df['Category'].unique())
region_filter = st.sidebar.multiselect("Region", options=df['Region'].unique(), default=df['Region'].unique())
segment_filter = st.sidebar.multiselect("Customer Segment", options=df['Customer_Segment'].unique(), default=df['Customer_Segment'].unique())

filtered_df = df[
    (df['Category'].isin(category_filter)) & 
    (df['Region'].isin(region_filter)) & 
    (df['Customer_Segment'].isin(segment_filter))
]

# --- TOP METRICS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"₹ {filtered_df['Sales'].sum():,}")
col2.metric("Total Profit", f"₹ {filtered_df['Profit'].sum():,}")
col3.metric("Total Orders", len(filtered_df))
col4.metric("Avg Order Value", f"₹ {filtered_df['Sales'].mean():,.0f}")

# --- GRAPHS ---
col_a, col_b = st.columns(2)

with col_a:
    fig1 = px.bar(filtered_df.groupby('Category')['Sales'].sum().reset_index(), x='Category', y='Sales', color='Category', title="Sales by Category")
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    fig2 = px.pie(filtered_df, names='Region', values='Sales', title="Sales by Region")
    st.plotly_chart(fig2, use_container_width=True)

col_c, col_d = st.columns(2)

with col_c:
    fig3 = px.bar(filtered_df.groupby('Customer_Segment')['Profit'].sum().reset_index(), x='Customer_Segment', y='Profit', color='Customer_Segment', title="Profit by Customer Segment")
    st.plotly_chart(fig3, use_container_width=True)

with col_d:
    fig4 = px.line(filtered_df.groupby('Order_Date')['Sales'].sum().reset_index(), x='Order_Date', y='Sales', title="Sales Over Time")
    st.plotly_chart(fig4, use_container_width=True)

# --- DATA TABLE ---
st.subheader("Detailed Data")
st.dataframe(filtered_df.head(200), use_container_width=True)

# --- DOWNLOAD ---
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download Filtered Data as CSV", csv, "filtered_sales.csv", "text/csv")
