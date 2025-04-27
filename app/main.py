import streamlit as st
from datetime import datetime
import google.generativeai as genai

# --- CONFIGURE YOUR GEMINI API KEY ---
genai.configure(api_key="AIzaSyAY7aqKIeRvnVSpenyaufVWH5JiQIN0c34")  # Replace with your real key

def init_chat():
    """Initialize chat session"""
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    st.session_state.chat = model.start_chat(history=[])

def start_ui():
    """Streamlit UI and logic"""
    st.title("🧠 AI Mental Health Chatbot")
    st.caption("Get emotional support from an AI therapist based on your current concern.")

    # Step 1: Select concern
    if "issue" not in st.session_state:
        issue = st.text_input("What are you dealing with today?", placeholder="e.g., depression, anxiety, stress")
        if st.button("Start Chat") and issue:
            st.session_state.issue = issue
            st.session_state.start_time = datetime.now()  # Track chat start time
            init_chat()
            st.session_state.chat.send_message(
                f"You are a supportive therapist. The user is dealing with {issue}. "
                "Reply with empathy, support, and mental health guidance."
            )
            st.success("✅ Chat session started. Start your conversation below.")
    else:
        # Display issue and session time
        st.markdown(f"🩺 You're chatting about: **{st.session_state.issue}**")
        if "start_time" in st.session_state:
            duration = datetime.now() - st.session_state.start_time
            minutes, seconds = divmod(duration.seconds, 60)
            st.markdown(f"⏱️ Time in session: **{minutes} min {seconds} sec**")

    # Step 2: Chat interface
    if "issue" in st.session_state and "chat" in st.session_state:
        user_input = st.chat_input("Say something to your therapist...")

        if user_input:
            # Show user message
            with st.chat_message("You", avatar="🧑"):
                st.markdown(user_input)

            # Show AI thinking
            with st.chat_message("Therapist", avatar="🧠"):
                with st.spinner("Therapist is thinking..."):
                    response = st.session_state.chat.send_message(user_input)
                    st.markdown(response.text)

                # Feedback buttons (emoji-based)
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.button("👍 Helpful", key=f"up_{user_input[:5]}")
                with col2:
                    st.button("👎 Not helpful", key=f"down_{user_input[:5]}")

# --- MAIN ---
if __name__ == "__main__":
    start_ui()
