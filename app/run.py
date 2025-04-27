import streamlit as st
import google.generativeai as genai
from datetime import datetime
import pandas as pd
import os

# 🔐 Replace with your Gemini API Key
genai.configure(api_key="AIzaSyAY7aqKIeRvnVSpenyaufVWH5JiQIN0c34")

# 📁 CSV Log File
LOG_FILE = "doctor_training_sessions.csv"

# 🧠 Initialize Chat
def init_chat():
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.user_replies = []
    st.session_state.ai_replies = []
    st.session_state.start_time = datetime.now()

# 📊 Evaluate the doctor's replies
def evaluate_doctor(user_replies, patient_issue):
    evaluator = genai.GenerativeModel("gemini-1.5-pro-latest")
    prompt = (
        f"You are evaluating a psychologist-in-training.\n"
        f"The simulated patient was dealing with: '{patient_issue}'.\n"
        f"Doctor's responses:\n" +
        "\n".join([f"{i+1}. {msg}" for i, msg in enumerate(user_replies)]) +
        "\n\nEvaluate their empathy, supportiveness, and effectiveness. Give a score out of 100 and explain why."
    )
    response = evaluator.generate_content(prompt)
    return response.text

# 📝 Save session data to CSV
def save_session_to_csv(issue, user_replies, ai_replies, evaluation):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session_data = {
        "Timestamp": timestamp,
        "Patient_Issue": issue,
        "Doctor_Replies": " || ".join(user_replies),
        "Patient_Replies": " || ".join(ai_replies),
        "Evaluation_Report": evaluation
    }

    df_new = pd.DataFrame([session_data])

    if os.path.exists(LOG_FILE):
        df_old = pd.read_csv(LOG_FILE)
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_csv(LOG_FILE, index=False)

# 🌐 Streamlit App UI
def start_ui():
    st.title("🧠 Simulated Patient Chatbot")
    st.caption("Practice counseling. The AI will act as a patient and evaluate your skills after the session.")

    if "started" not in st.session_state:
        issue = st.text_input("👤 Patient's Problem", placeholder="e.g., I feel lonely and anxious.")
        if st.button("🩺 Start Simulation") and issue:
            st.session_state.issue = issue
            st.session_state.started = True
            init_chat()
            st.session_state.chat.send_message(
    f"""You are roleplaying as a real patient in a therapy simulation. 
Your issue is: "{issue}". You are not an AI, therapist, or expert — you are a normal person seeking help. 
Act like you're feeling overwhelmed, anxious, sad, confused, or whatever suits the issue.

Be emotional, vulnerable, and human. Do not give advice or switch roles. Respond only as the patient — 
sometimes uncertain, sometimes guarded, sometimes expressive. Be consistent in your tone throughout.

Use everyday language, small pauses, and human expressions. Make the doctor feel like they’re talking to a real patient."""
)

            st.success("✅ Patient is ready to chat.")
    
    # 🧑‍⚕️ Live Session
    if "started" in st.session_state:
        st.markdown(f"💬 **Patient's Problem**: *{st.session_state.issue}*")
        duration = datetime.now() - st.session_state.start_time
        st.markdown(f"⏱️ **Session Time:** {duration.seconds // 60} min {duration.seconds % 60} sec")

        # 🔁 Show full conversation history
        for user_msg, ai_msg in zip(st.session_state.user_replies, st.session_state.ai_replies):
            with st.chat_message("You 🧑‍⚕️"):
                st.markdown(user_msg)
            with st.chat_message("Patient 🧠"):
                st.markdown(ai_msg)

        user_input = st.chat_input("Your message to the patient...")
        if user_input:
            st.session_state.user_replies.append(user_input)
            with st.chat_message("You 🧑‍⚕️"):
                st.markdown(user_input)

            response = st.session_state.chat.send_message(user_input)
            ai_reply = response.text
            st.session_state.ai_replies.append(ai_reply)

            with st.chat_message("Patient 🧠"):
                st.markdown(ai_reply)

        # ✅ End session
        if st.button("📊 End Session and Get Evaluation"):
            st.info("Evaluating your responses...")
            evaluation = evaluate_doctor(st.session_state.user_replies, st.session_state.issue)

            st.subheader("📋 Evaluation Report")
            st.markdown(evaluation)

            # Save to CSV
            save_session_to_csv(
                st.session_state.issue,
                st.session_state.user_replies,
                st.session_state.ai_replies,
                evaluation
            )
            st.success("✅ Session saved to CSV.")

            # Clear session
            for key in ["started", "issue", "chat", "user_replies", "ai_replies", "start_time"]:
                st.session_state.pop(key, None)

# 🚀 Run app
if __name__ == "__main__":
    start_ui()
