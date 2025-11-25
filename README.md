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

