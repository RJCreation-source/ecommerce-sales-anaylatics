import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-Commerce Analytics ", layout="wide", page_icon="📊")
st.title("📊 E-Commerce Sales Analytics ")

@st.cache_data
def get_data():
    df = pd.read_csv('data/sales_data.csv')
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    df['YearMonth'] = df['Order_Date'].dt.strftime('%Y-%m')
    return df

df = get_data()

# --- SIDEBAR ---
st.sidebar.header("🔍 Smart Filters")
search = st.sidebar.text_input("Search Product")
cat = st.sidebar.multiselect("Category", df['Category'].unique(), default=df['Category'].unique())
reg = st.sidebar.multiselect("Region", df['Region'].unique(), default=df['Region'].unique())
seg = st.sidebar.multiselect("Segment", df['Customer_Segment'].unique(), default=df['Customer_Segment'].unique())

filtered_df = df[(df['Category'].isin(cat)) & (df['Region'].isin(reg)) & (df['Customer_Segment'].isin(seg))]
if search:
    filtered_df = filtered_df[filtered_df['Product'].str.contains(search, case=False, na=False)]

# --- KPIs ---
c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Total Sales", f"₹ {filtered_df['Sales'].sum():,}")
c2.metric("Total Profit", f"₹ {filtered_df['Profit'].sum():,}")
c3.metric("Orders", len(filtered_df))
c4.metric("Avg Value", f"₹ {filtered_df['Sales'].mean():,.0f}")
profit_margin = (filtered_df['Profit'].sum() / filtered_df['Sales'].sum() * 100) if filtered_df['Sales'].sum()!=0 else 0
c5.metric("Profit Margin", f"{profit_margin:.1f}%")

# --- ROW 1 ---
col1, col2, col3 = st.columns([2,1,1])
with col1:
    fig = px.bar(filtered_df.groupby('Category')['Sales'].sum().reset_index(), x='Category', y='Sales', color='Category', title="Sales by Category")
    st.plotly_chart(fig, use_container_width=True)
with col2:
    fig = px.pie(filtered_df, names='Region', values='Sales', hole=0.4, title="Sales by Region")
    st.plotly_chart(fig, use_container_width=True)
with col3:
    fig = px.pie(filtered_df, names='Customer_Segment', values='Profit', hole=0.4, title="Profit by Segment")
    st.plotly_chart(fig, use_container_width=True)

# --- ROW 2 ---
c1,c2 = st.columns(2)
with c1:
    top_products = filtered_df.groupby('Product')['Sales'].sum().nlargest(10).reset_index()
    fig = px.bar(top_products, x='Sales', y='Product', orientation='h', title="Top 10 Products by Sales", color='Sales')
    st.plotly_chart(fig, use_container_width=True)
with c2:
    monthly = filtered_df.groupby('YearMonth')['Sales'].sum().reset_index()
    fig = px.line(monthly, x='YearMonth', y='Sales', markers=True, title="Monthly Sales Trend")
    st.plotly_chart(fig, use_container_width=True)

# --- AI INSIGHTS ---
st.subheader("💡 Auto Insights")
best_cat = filtered_df.groupby('Category')['Profit'].sum().idxmax() if not filtered_df.empty else "N/A"
loss_orders = len(filtered_df[filtered_df['Profit'] < 0])
st.info(f"✅ Best Profitable Category: *{best_cat}* | ⚠️ Loss Orders: *{loss_orders}* | 📈 Total Categories: *{filtered_df['Category'].nunique()}*")

# --- TABLES ---
st.subheader("📋 Data")
tab1, tab2 = st.tabs(["Top Products", "Loss Products"])
with tab1:
    st.dataframe(filtered_df.groupby('Product')[['Sales','Profit','Quantity']].sum().sort_values('Sales', ascending=False).head(20), use_container_width=True)
with tab2:
    loss_df = filtered_df[filtered_df['Profit'] < 0]
    st.dataframe(loss_df , use_container_width=True)

st.download_button("📥 Download Full Filtered CSV", filtered_df.to_csv(index=False).encode('utf-8'), "pro_sales.csv", "text/csv")
