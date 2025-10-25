import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

# Database connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='orderlytics'
)

# Functions to fetch data
@st.cache_data
def get_monthly_revenue():
    query = """
    SELECT DATE_FORMAT(InvoiceDate, '%Y-%m') AS Month,
           ROUND(SUM(Quantity * UnitPrice), 2) AS Revenue
    FROM Sales s JOIN Products p USING(StockCode)
    GROUP BY Month
    ORDER BY Month;
    """
    return pd.read_sql(query, conn)

@st.cache_data
def get_top_products():
    query = """
    SELECT p.Description,
           SUM(s.Quantity) AS UnitsSold,
           ROUND(SUM(s.Quantity * p.UnitPrice),2) AS Revenue
    FROM Sales s JOIN Products p USING(StockCode)
    GROUP BY p.StockCode
    ORDER BY Revenue DESC
    LIMIT 10;
    """
    return pd.read_sql(query, conn)

st.title("Orderlytics Retail Dashboard 📊")

tab1, tab2 = st.tabs(["📈 Revenue Trend", "🏆 Top Products"])

with tab1:
    st.subheader("Monthly Revenue")
    df = get_monthly_revenue()
    st.line_chart(df, x='Month', y='Revenue')

with tab2:
    st.subheader("Top 10 Best Selling Products")
    df2 = get_top_products()
    st.bar_chart(df2, x='Description', y='Revenue')
    st.dataframe(df2)
