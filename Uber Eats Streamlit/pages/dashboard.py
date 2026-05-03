import streamlit as st
import sqlite3
import pandas as pd

st.title("Uber Eats Decision Dashboard")

conn = sqlite3.connect("uber.db")
# -------------------
# LOAD FILTER VALUES
#-------------------
# SQ# -------------------

locations = pd.read_sql("SELECT DISTINCT location FROM restaurants", conn)['location']
location = st.sidebar.selectbox("Location", locations)
online = st.sidebar.selectbox("Online Order", ["yes", "no"])
table = st.sidebar.selectbox("Table Booking", ["yes", "no"])

# QUERY
# -------------------

query = f"SELECT * FROM restaurants WHERE location = '{location}' AND online_order = '{online}' AND book_table ='{table}'"
df = pd.read_sql(query, conn)

# -------------------
# OUTPUT
# -------------------

st.subheader("Filtered Restaurants")
st.write(f"Rows returned: {len(df)}")  # debug
st.dataframe(df)

# -------------------
# INSIGHTS
# -------------------

st.subheader("Location Intelligence")
loc_df = pd.read_sql("""
SELECT location, ROUND(AVG(normalized_rating),2) as avg_rating, COUNT(*) as total
FROM restaurants
GROUP BY location
ORDER BY avg_rating DESC
""", conn)
st.dataframe(loc_df)

st.subheader("Pricing Optimization")
price_df = pd.read_sql("""
SELECT 
CASE 
    WHEN cost_for_two < 300 THEN 'Low'
    WHEN cost_for_two BETWEEN 300 AND 700 THEN 'Mid'
    ELSE 'High'
END AS price_category,
ROUND(AVG(normalized_rating),2) as avg_rating
FROM restaurants
GROUP BY price_category
""", conn)
st.dataframe(price_df)

st.subheader("Feature Impact")
feature_df = pd.read_sql("""
SELECT online_order, ROUND(AVG(normalized_rating),2) as avg_rating
FROM restaurants
GROUP BY online_order
""", conn)
st.dataframe(feature_df)