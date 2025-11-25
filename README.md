# 🩺 AI Health Chatbot

A Streamlit-based AI-powered **Health Information Chatbot** built using **Google Gemini**.  
This chatbot provides **general wellness and symptom-related information** while following strict safety rules.  
It does **NOT** provide diagnoses or medical treatment.

---

## ✨ Features

### 🔐 API Key Input
- Secure API key entry inside the sidebar  
- Press Enter → Key is stored → Success popup  
- Key is safely stored inside `st.session_state`

### 💬 Chat Interface
- Smooth ChatGPT-like messaging experience  
- Messages stored in session state so chat persists  
- AI and user messages displayed with chat bubbles

### 🤖 Powered by Google Gemini
- Uses **Gemini 2.5 Flash** model  
- Uses proper Gemini message structure (`role`, `parts`) to avoid API errors  
- Includes system instructions to ensure safe behavior

### 🛡️ Safety First
- No diagnoses  
- No medical or treatment instructions  
- Always includes a reminder to consult a real doctor

---

## 🚀 Installation

### 1️⃣ Create & Activate Virtual Environment

```bash
python -m venv .venv
```
---

## Windows
```bash
.venv\Scripts\activate
```
---

## macOS / Linux
```bash
source .venv/bin/activate
```
---

## Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Run the App
```bash
streamlit run health_bot.py
```

---

## How It Works
1. **Sidebar collects API key**
When the user types an API key and presses Enter: 
```python
st.session_state.api_key = api_key_input
```

---

2. **Chat messages saved in session**
```python
st.session_state.messages = [...]
```
This creates a ChatGPT-style conversation loop.
---

3. **Messages formatted for Gemini**\
```python
{
  "role": "user",
  "parts": [{ "text": "message text here" }]
}
```

---

4. **Model generates response**
```python
model = genai.GenerativeModel("models/gemini-2.5-flash")
response = model.generate_content(gemini_messages)
```

---

5. **Response shown & added to chat**
Displayed using:
```python
with st.chat_message("assistant"):
    ...
```

---

## ⚠️ Disclaimer
This chatbot provides general informational health guidance only.
It does not diagnose conditions, recommend treatments, or replace medical professionals.
Always consult a licensed doctor for real medical concerns.

