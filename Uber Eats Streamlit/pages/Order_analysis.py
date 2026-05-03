import streamlit as st
import sqlite3
import pandas as pd
st.title("Order Analysis Dashboard")
conn = sqlite3.connect("uber.db")
question = st.selectbox("Select Analysis", [
    "Total Orders & Revenue",
    "Top Restaurants by Revenue",
    "Average Order Value",
    "Monthly Order Trend",
    "Peak Ordering Month",
    "High Revenue Restaurants"
])
if question == "Total Orders & Revenue":
    query = """
    SELECT 
        COUNT(*) as total_orders,
        ROUND(SUM(order_value),2) as total_revenue
    FROM orders
    """

elif question == "Top Restaurants by Revenue":
    query = """
    SELECT restaurant_name, ROUND(SUM(order_value),2) as revenue
    FROM orders
    GROUP BY restaurant_name
    ORDER BY revenue DESC
    LIMIT 10
    """

elif question == "Average Order Value":
    query = """
    SELECT ROUND(AVG(order_value),2) as avg_order_value
    FROM orders
    """

elif question == "Monthly Order Trend":
    query = """
    SELECT month, COUNT(*) as total_orders
    FROM orders
    GROUP BY month
    ORDER BY month
    """

elif question == "Peak Ordering Month":
    query = """
    SELECT month, COUNT(*) as total_orders
    FROM orders
    GROUP BY month
    ORDER BY total_orders DESC
    LIMIT 1
    """


elif question == "High Revenue Restaurants":
    query = """
    SELECT restaurant_name, ROUND(SUM(order_value),2) as revenue
    FROM orders
    GROUP BY restaurant_name
    HAVING revenue > 10000
    ORDER BY revenue DESC
    """
df = pd.read_sql(query, conn)
st.subheader("Result")

if df.empty:
    st.warning("No data found. Check your orders table.")
else:
    st.dataframe(df)
st.caption("Tip: If monthly queries fail, ensure 'month' column exists in orders table.")