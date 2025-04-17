import streamlit as st
import requests

st.title("🔄 Auto Task Scheduler")

# Input from user
task_ids = st.text_input("Enter Task IDs (comma-separated)", "task_001,task_002")
priority = st.selectbox("Select Priority", ["high", "medium", "low"])
availability = st.checkbox("Consider User Availability", value=True)

# When user clicks "Schedule"
if st.button("Schedule Tasks"):
    tasks_list = [tid.strip() for tid in task_ids.split(",")]

    payload = {
        "tasks": tasks_list,
        "priority": priority,
        "user_availability": availability
    }

    try:
        response = requests.post("http://127.0.0.1:5000/tasks/auto-schedule", json=payload)

        if response.status_code == 200:
            result = response.json()
            st.success(result["message"])
            st.write("### 📋 Scheduled Tasks:")
            for task in result["scheduled_tasks"]:
                st.write(f"- **{task['task_id']}** → {task['assigned_time']}")
        else:
            st.error("Something went wrong. Status code: " + str(response.status_code))

    except Exception as e:
        st.error("⚠️ Error connecting to the API.")
        st.text(str(e))
