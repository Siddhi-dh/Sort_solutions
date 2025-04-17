import streamlit as st
import requests

st.title("Task Time Tracker")

# User inputs
task_id = st.text_input("Enter Task ID:")
start_time = st.text_input("Enter Start Time (ISO 8601 format):")
end_time = st.text_input("Enter End Time (ISO 8601 format):")

if st.button("Submit"):
    if task_id and start_time and end_time:
        url = f"http://127.0.0.1:5000/tasks/{task_id}/set-time"
        payload = {
            "start_time": start_time,
            "end_time": end_time
        }
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            st.success("Start and end times recorded successfully!")
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
    else:
        st.error("Please fill all fields!")
