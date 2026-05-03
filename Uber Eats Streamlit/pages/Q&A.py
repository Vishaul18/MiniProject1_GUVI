import streamlit as st
import sqlite3
import pandas as pd

st.title("Business Q&A")

conn = sqlite3.connect("uber.db")

question = st.selectbox("Select a Business Question", [
    "1. Highest Avg Rating Locations",
    "2. Most Saturated Locations",
    "3. Online Order Impact",
    "4. Table Booking Impact",
    "5. Best Price Category",
    "6. Price Category vs Rating",
    "7. Most Common Cuisines",
    "8. Highest Rated Cuisines",
    "9. Niche Cuisines (Low count, high rating)",
    "10. Cost vs Rating"
])
if question == "1. Highest Avg Rating Locations":
    query = """
    SELECT location, ROUND(AVG(normalized_rating),2) as avg_rating
    FROM restaurants
    GROUP BY location
    ORDER BY avg_rating DESC
    """

elif question == "2. Most Saturated Locations":
    query = """
    SELECT location, COUNT(*) as total
    FROM restaurants
    GROUP BY location
    ORDER BY total DESC
    """

elif question == "3. Online Order Impact":
    query = """
    SELECT online_order, ROUND(AVG(normalized_rating),2) as avg_rating
    FROM restaurants
    GROUP BY online_order
    """

elif question == "4. Table Booking Impact":
    query = """
    SELECT book_table, ROUND(AVG(normalized_rating),2) as avg_rating
    FROM restaurants
    GROUP BY book_table
    """

elif question == "5. Best Price Category":
    query = """
    SELECT 
    CASE 
        WHEN cost_for_two < 300 THEN 'Low'
        WHEN cost_for_two BETWEEN 300 AND 700 THEN 'Mid'
        ELSE 'High'
    END AS price_category,
    ROUND(AVG(normalized_rating),2) as avg_rating
    FROM restaurants
    GROUP BY price_category
    ORDER BY avg_rating DESC
    """

elif question == "6. Price Category vs Rating":
    query = """
    SELECT 
    CASE 
        WHEN cost_for_two < 300 THEN 'Low'
        WHEN cost_for_two BETWEEN 300 AND 700 THEN 'Mid'
        ELSE 'High'
    END AS price_category,
    COUNT(*) as total,
    ROUND(AVG(normalized_rating),2) as avg_rating
    FROM restaurants
    GROUP BY price_category
    """

elif question == "7. Most Common Cuisines":
    query = """
    SELECT cuisines, COUNT(*) as total
    FROM restaurants
    GROUP BY cuisines
    ORDER BY total DESC
    LIMIT 10
    """

elif question == "8. Highest Rated Cuisines":
    query = """
    SELECT cuisines, ROUND(AVG(normalized_rating),2) as avg_rating
    FROM restaurants
    GROUP BY cuisines
    ORDER BY avg_rating DESC
    LIMIT 10
    """

elif question == "9. Niche Cuisines (Low count, high rating)":
    query = """
    SELECT cuisines, COUNT(*) as total, ROUND(AVG(normalized_rating),2) as avg_rating
    FROM restaurants
    GROUP BY cuisines
    HAVING total < 50
    ORDER BY avg_rating DESC
    LIMIT 10
    """

elif question == "10. Cost vs Rating":
    query = """
    SELECT cost_for_two, ROUND(AVG(normalized_rating),2) as avg_rating
    FROM restaurants
    GROUP BY cost_for_two
    ORDER BY cost_for_two
    """
df = pd.read_sql(query, conn)

st.subheader("Result")
st.dataframe(df)