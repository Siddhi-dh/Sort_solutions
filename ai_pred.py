import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import LabelEncoder
from datetime import timedelta

st.title("🧠 AI Task Deadline Predictor")

@st.cache_data
def load_data_and_train_model():
    try:
        tasks_df = pd.read_csv("C:/Users/Rutika/Desktop/sort_solutions/ai power deadline/tasks.csv")
        time_logs_df = pd.read_csv("C:/Users/Rutika/Desktop/sort_solutions/ai power deadline/time_logs.csv")

        time_logs_df['start_time'] = pd.to_datetime(time_logs_df['start_time'])
        time_logs_df['end_time'] = pd.to_datetime(time_logs_df['end_time'])
        tasks_df['created_at'] = pd.to_datetime(tasks_df['created_at'])

        time_logs_df['duration_minutes'] = (time_logs_df['end_time'] - time_logs_df['start_time']).dt.total_seconds() / 60
        merged_df = pd.merge(time_logs_df, tasks_df, on='task_id', how='inner')
        task_avg_duration = merged_df.groupby('task_id')['duration_minutes'].mean().reset_index()
        task_avg_duration.columns = ['task_id', 'avg_logged_duration']

        model_data = pd.merge(tasks_df, task_avg_duration, on='task_id', how='inner')
        model_data['created_hour'] = model_data['created_at'].dt.hour

        priority_encoder = LabelEncoder()
        model_data['priority_encoded'] = priority_encoder.fit_transform(model_data['priority'].astype(str))
        model_data = model_data.dropna(subset=['estimated_duration_minutes', 'priority_encoded', 'created_hour', 'avg_logged_duration'])

        X = model_data[['estimated_duration_minutes', 'priority_encoded', 'created_hour']]
        y = model_data['avg_logged_duration']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        mae = mean_absolute_error(y_test, model.predict(X_test))

        return model, tasks_df, priority_encoder, mae
    except Exception as e:
        st.error(f"🚫 Failed to load or train model: {e}")
        return None, None, None, None

model, tasks_df, priority_encoder, mae = load_data_and_train_model()

def predict_deadline(task_id):
    task_row = tasks_df[tasks_df['task_id'] == task_id]
    if task_row.empty:
        return {"error": "Task ID not found"}

    created_hour = pd.to_datetime(task_row['created_at'].values[0]).hour
    estimated_duration = task_row['estimated_duration_minutes'].values[0]
    priority = task_row['priority'].values[0]

    try:
        priority_encoded = priority_encoder.transform([priority])[0]
    except:
        priority_encoded = 0  # default

    X_input = pd.DataFrame([[estimated_duration, priority_encoded, created_hour]],
                           columns=['estimated_duration_minutes', 'priority_encoded', 'created_hour'])
    
    predicted_duration = model.predict(X_input)[0]
    start_time = pd.to_datetime(task_row['created_at'].values[0])
    predicted_deadline = start_time + timedelta(minutes=predicted_duration)
    confidence = max(50, 100 - int((mae / predicted_duration) * 100))

    return {
        "predicted_deadline": predicted_deadline.isoformat(),
        "confidence": f"{confidence}%"
    }

# 👇 Streamlit UI
if model is not None:
    task_id_input = st.number_input("🔢 Enter Task ID", min_value=0, step=1)

    if st.button("Predict Deadline"):
        result = predict_deadline(task_id_input)
        if "error" in result:
            st.error(result["error"])
        else:
            st.success(f"🕒 Predicted Deadline: {result['predicted_deadline']}")
            st.info(f"🔒 Confidence: {result['confidence']}")

