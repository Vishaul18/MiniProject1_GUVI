import streamlit as st
import sqlite3
import pandas as pd
conn = sqlite3.connect("uber.db")
df = pd.read_sql("SELECT * FROM restaurants", conn)
st.dataframe(df.head())
st.sidebar.header("Filters")

# Location filter
location = st.sidebar.selectbox( "Select Location",df['location'].dropna().unique())

# Filter data
filtered_df = df[df['location'] == location]
st.subheader("Filtered Data")
st.dataframe(filtered_df)

st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Restaurants", len(filtered_df))
col2.metric("Avg Rating", round(filtered_df['normalized_rating'].mean(), 2))
col3.metric("Avg Cost for Two", int(filtered_df['cost_for_two'].mean()))

st.subheader("Top Locations")
top_locations = df['location'].value_counts().head(10)
st.bar_chart(top_locations)

st.subheader("Top Rated Restaurants")
top_restaurants = df.sort_values(by="normalized_rating",ascending=False).head(10)
st.dataframe(top_restaurants[['name', 'location', 'normalized_rating']])

st.subheader("Business Insights")

question = st.selectbox("Select Question", ["Best Price Category", "Top Locations for Premium","Online vs Table Booking Impact"])
if question == "Best Price Category":
    st.write("High-priced restaurants have the highest average ratings.")
elif question == "Top Locations for Premium":
    st.write("Koramangala, Indiranagar, and Marathahalli are top premium locations.")
elif question == "Online vs Table Booking Impact":
    st.write("Table booking has a stronger impact on ratings than online ordering.")

st.subheader("Business Queries")

question = st.selectbox("Select Question", [
    "Q1 Top Rated Restaurants",
    "Q2 Restaurant Count by Location",
    "Q3 Online Order Impact",
    "Q4 Table Booking Impact",
    "Q5 Price Category vs Rating",
    "Q6 Restaurants per Location",
    "Q7 Most Common Cuisines",
    "Q8 Highest Rated Cuisines",
    "Q9 Niche High Performing Cuisines",
    "Q10 Cost vs Rating",
    "Q11 Premium Locations",
    "Q12 High Demand Low Rating",
    "Q13 Online + Table Booking",
    "Q14 Best Location + Price Combo",
    "Q15 Top Restaurants per Price"])

queries = {"Q1 Top Rated Restaurants": """
SELECT name, location, normalized_rating
FROM restaurants
ORDER BY normalized_rating DESC
LIMIT 10;
""",

"Q2 Restaurant Count by Location": """
SELECT location, COUNT(*) AS total_restaurants
FROM restaurants
GROUP BY location
ORDER BY total_restaurants DESC;
""",

"Q3 Online Order Impact": """
SELECT online_order, ROUND(AVG(normalized_rating),2) AS avg_rating
FROM restaurants
GROUP BY online_order;
""",

"Q4 Table Booking Impact": """
SELECT book_table, ROUND(AVG(normalized_rating),2) AS avg_rating
FROM restaurants
GROUP BY book_table;
""",

"Q5 Price Category vs Rating": """
SELECT 
CASE 
    WHEN cost_for_two < 500 THEN 'Low'
    WHEN cost_for_two BETWEEN 500 AND 1000 THEN 'Mid'
    ELSE 'High'
END AS price_category,
ROUND(AVG(normalized_rating),2) AS avg_rating
FROM restaurants
GROUP BY price_category;
""",

"Q6 Restaurants per Location": """
SELECT location, COUNT(*) AS total_restaurants
FROM restaurants
GROUP BY location
ORDER BY total_restaurants DESC
LIMIT 10;
""",

"Q7 Most Common Cuisines": """
SELECT cuisines, COUNT(*) AS total_restaurants
FROM restaurants
GROUP BY cuisines
ORDER BY total_restaurants DESC
LIMIT 10;
""",

"Q8 Highest Rated Cuisines": """
SELECT cuisines, ROUND(AVG(normalized_rating),2) AS avg_rating
FROM restaurants
GROUP BY cuisines
ORDER BY avg_rating DESC
LIMIT 10;
""",

"Q9 Niche High Performing Cuisines": """
SELECT cuisines, COUNT(*) AS total_restaurants,
ROUND(AVG(normalized_rating),2) AS avg_rating
FROM restaurants
GROUP BY cuisines
HAVING COUNT(*) < 50
ORDER BY avg_rating DESC
LIMIT 10;
""",

"Q10 Cost vs Rating": """
SELECT cost_for_two, ROUND(AVG(normalized_rating),2) AS avg_rating
FROM restaurants
GROUP BY cost_for_two
ORDER BY cost_for_two;
""",

"Q11 Premium Locations": """
SELECT location, COUNT(*) AS total,
ROUND(AVG(normalized_rating),2) AS avg_rating
FROM restaurants
WHERE cost_for_two > 1000
GROUP BY location
HAVING COUNT(*) >= 5
ORDER BY avg_rating DESC;
""",

"Q12 High Demand Low Rating": """
SELECT location, COUNT(*) AS total,
ROUND(AVG(normalized_rating),2) AS avg_rating
FROM restaurants
GROUP BY location
HAVING COUNT(*) > 50 AND AVG(normalized_rating) < 3.8;
""",

"Q13 Online + Table Booking": """
SELECT online_order, book_table,
COUNT(*) AS total,
ROUND(AVG(normalized_rating),2) AS avg_rating
FROM restaurants
GROUP BY online_order, book_table
ORDER BY avg_rating DESC;
""",

"Q14 Best Location + Price Combo": """
SELECT location,
CASE 
    WHEN cost_for_two < 500 THEN 'Low'
    WHEN cost_for_two BETWEEN 500 AND 1000 THEN 'Mid'
    ELSE 'High'
END AS price_category,
COUNT(*) AS total,
ROUND(AVG(normalized_rating),2) AS avg_rating
FROM restaurants
GROUP BY location, price_category
HAVING COUNT(*) >= 5
ORDER BY avg_rating DESC
LIMIT 10;
""",

"Q15 Top Restaurants per Price": """
SELECT name, location, normalized_rating,
CASE 
    WHEN cost_for_two < 500 THEN 'Low'
    WHEN cost_for_two BETWEEN 500 AND 1000 THEN 'Mid'
    ELSE 'High'
END AS price_category
FROM restaurants
ORDER BY price_category, normalized_rating DESC
LIMIT 20;
"""
}
query = queries[question]
result_df = pd.read_sql(query, conn)
st.dataframe(result_df)