# run with streamlit run app.py 
import streamlit as st
import google.generativeai as genai
import os
import json

# Configure Gemini
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel(model_name="gemini-2.0-flash-lite")

# Streamlit UI
st.set_page_config(page_title="Auto Task Prioritizer", layout="centered")
st.title("📋 Auto Task Prioritizer")
st.write("Enter your list of tasks, and let AI sort them by priority!")

# Text input
task_input = st.text_area("Enter tasks (one per line):", height=200)
if st.button("Auto-Prioritize"):
    if not task_input.strip():
        st.warning("Please enter some tasks.")
    else:
        # Prepare tasks
        tasks = [line.strip() for line in task_input.strip().split("\n") if line.strip()]
        formatted_tasks = "\n".join([f"- {task}" for task in tasks])

        prompt = f"""
        Given the following tasks:
        {formatted_tasks}

        Classify each task into one of the following priority levels:
        High = High priority 
        Medium = Medium priority
        Low = Low priority

        Return the result in JSON format like:
        {{
            "High": ["task1", "task2"],
            "Medium": ["task3"],
            "Low": ["task4"]
        }}
        """

        try:
            with st.spinner("Thinking..."):
                response = model.generate_content(prompt)
                output = response.text.strip()

                  # Try to extract JSON safely from the response
                start = output.find('{')
                end = output.rfind('}') + 1
                json_text = output[start:end]

                priorities = json.loads(json_text)

                # Display results
                st.success("Tasks Prioritized!")
                priority_map = {
                              "High": "🔥 High Priority Tasks",
                              "Medium": "⏳ Medium Priority Tasks",
                              "Low": "💤 Low Priority Tasks"
                }
                for level in ["High", "Medium", "Low"]:
                    st.subheader(priority_map[level])
                    for t in priorities.get(level, []):
                        st.markdown(f"- ✅ {t}")

        except Exception as e:
            st.error(f"Error: {str(e)}")

