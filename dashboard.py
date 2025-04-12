import streamlit as st
import requests
import pandas as pd

# Title
st.title("Flask API Data Visualization")

# Fetch data from Flask API
st.subheader("Fetching Data from Flask API...")

try:
    response = requests.get("http://127.0.0.1:5000/data")
    if response.status_code == 200:
        data = response.json()
        
        # Convert JSON to DataFrame
        df = pd.DataFrame(data)
        
        # Display data as table
        st.write("### Data Table")
        st.dataframe(df)

        # Show bar chart
        st.write("### Age Distribution")
        st.bar_chart(df.set_index("name"))

    else:
        st.error("Failed to fetch data from API")
except Exception as e:
    st.error(f"Error: {e}")
