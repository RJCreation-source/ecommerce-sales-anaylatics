import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Analytics", layout="wide")
st.title("📊 E-Commerce Sales Analytics Dashboard")

@st.cache_data
def get_data():
    df = pd.read_csv('data/sales_data.csv')
    return df

df = get_data()
st.metric("Total Sales", f"₹ {df['Sales'].sum():,}")
st.metric("Total Orders", len(df))

fig = px.bar(df.groupby('Category')['Sales'].sum().reset_index(), x='Category', y='Sales', color='Category')
st.plotly_chart(fig, use_container_width=True)
st.dataframe(df.head(100))