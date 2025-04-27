# 🧠 AI Mental Health Chatbot

A compassionate AI therapist built with **Google Gemini API** and **Streamlit** to help users get mental health support in a conversational manner.

## 💡 Features

- Ask about your mental health concern (e.g., stress, anxiety, depression)
- Chat with a friendly AI therapist trained to respond with kindness and advice
- Lightweight web UI powered by Streamlit

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/mental-health-chatbot.git
cd mental-health-chatbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add Your Gemini API Key

In `app/main.py`, replace:
```python
genai.configure(api_key="YOUR_API_KEY")
```

with your actual Google Gemini API key.

### 4. Run the App

```bash
streamlit run app/main.py
```

---

## 📦 Requirements

All dependencies are listed in `requirements.txt`.

---

## 🛠 Tech Stack

- [Streamlit](https://streamlit.io/)
- [Google Generative AI (Gemini)](https://makersuite.google.com/app)
