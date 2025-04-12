import streamlit as st
import requests
import datetime
import time
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(page_title="Pomodoro Timer 🍅", layout="centered")

# ---------- HEADER ----------
st.markdown("<h1 style='text-align: center; color: #D7263D;'>🍅 Pomodoro Task Manager</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>Stay focused. Log your productivity. Crush your tasks!</p>", unsafe_allow_html=True)

# ---------- INPUT SECTION ----------
st.sidebar.header("🔧 Settings")
task_id = st.sidebar.text_input("🆔 Enter Task ID:", "task_001")
duration = st.sidebar.slider("⏱️ Select work duration (minutes):", 5, 60, 25)

if st.sidebar.button("🚀 Start Pomodoro"):
    response = requests.post(f"http://127.0.0.1:9000/tasks/{task_id}/start-pomodoro",
                             json={"task_id": task_id, "duration": duration})

    if response.status_code == 200:
        data = response.json()
        st.success(f"✅ {data['message']}")

        end_time = datetime.datetime.fromisoformat(data["end_time"])
        st.info(f"🕒 Session ends at: **{end_time.strftime('%H:%M:%S')}**")

        countdown_placeholder = st.empty()

        # Inject Lottie circular countdown timer
        with countdown_placeholder:
            total_seconds = duration * 60
            circle_timer_code = f"""
            <html>
            <head>
            <script>
                let total = {total_seconds};
                let timeLeft = total;
                function updateTimer() {{
                    const circle = document.querySelector('circle');
                    const text = document.querySelector('text');
                    let percent = timeLeft / total;
                    let dashoffset = 440 - (440 * percent);
                    circle.style.strokeDashoffset = dashoffset;
                    let minutes = Math.floor(timeLeft / 60);
                    let seconds = timeLeft % 60;
                    text.textContent = `${{minutes.toString().padStart(2, '0')}}:${{seconds.toString().padStart(2, '0')}}`;
                    if (timeLeft > 0) {{
                        timeLeft--;
                        setTimeout(updateTimer, 1000);
                    }} else {{
                        text.textContent = "Done!";
                    }}
                }}
                window.onload = updateTimer;
            </script>
            </head>
            <body style="display:flex;justify-content:center;align-items:center;height:300px;">
                <svg width="200" height="200">
                    <circle r="70" cx="100" cy="100" fill="none" stroke="#FF6B6B" stroke-width="10" stroke-dasharray="440" stroke-dashoffset="0"/>
                    <text x="50%" y="50%" text-anchor="middle" dy=".3em" font-size="24" fill="#333"></text>
                </svg>
            </body>
            </html>
            """
            components.html(circle_timer_code, height=300)

        time.sleep(duration * 60)
        st.balloons()
        st.success("⏰ Work session over! Time for a break! 💆")

    else:
        st.error("🚫 Failed to start Pomodoro session.")

# ---------- PAST SESSIONS ----------
st.markdown("---")
st.markdown("<h3 style='color:#6A0572;'>📜 Pomodoro Session History</h3>", unsafe_allow_html=True)

try:
    df = pd.read_csv("work_sessions.csv")
    df["start_time"] = pd.to_datetime(df["start_time"])
    df["end_time"] = pd.to_datetime(df["end_time"])
    df = df.sort_values("start_time", ascending=False)

    # Add missing column if needed
    if "session_type" not in df.columns:
        df["session_type"] = "Unknown"

    st.dataframe(df.tail(10), use_container_width=True)

    st.markdown("### 📊 Insights")
    view_mode = st.selectbox("Group by:", ["None", "Task ID", "Session Type"])

    if view_mode != "None":
        col = "task_id" if view_mode == "Task ID" else "session_type"

        if col in df.columns:
            st.bar_chart(df.groupby(col).size())
        else:
            st.warning(f"⚠️ Column '{col}' not found in session data.")
except FileNotFoundError:
    st.warning("⚠️ No session data available yet. Complete a Pomodoro to start tracking!")


# ---------- FOOTER ----------
st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: 12px; color: gray;'>Made with ❤️ • Pomodoro powered 🔥</p>",
    unsafe_allow_html=True
)

