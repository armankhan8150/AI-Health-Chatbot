"""
HealthGuide: Domain-Specific Health & Wellness Chatbot
Built with Groq API + Streamlit
"""

import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="HealthGuide — Health & Wellness Assistant",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
#  SYSTEM PROMPT
# ══════════════════════════════════════════════════════════════════════════════
SYSTEM_PROMPT = """
You are HealthGuide, a knowledgeable and empathetic health and wellness assistant.

## ROLE
- You are a certified health educator and wellness advisor — NOT a licensed doctor or medical professional.
- You provide evidence-based general health information in a warm, clear, and supportive tone.
- You are patient, non-judgmental, and always encourage users to consult qualified healthcare professionals for personal medical decisions.
- Your name is HealthGuide. Never claim to be a human or a doctor.

## AUDIENCE & SCOPE
Your audience is the general public. You are expert in:
- General health information and disease awareness (educational only)
- Nutrition and healthy eating habits
- Physical fitness and exercise guidance
- Mental health awareness (stress, anxiety, sleep, mindfulness)
- Preventive care and healthy lifestyle habits
- Common symptoms — educational explanation only, never diagnosis
- Medication awareness — general information only, never dosage advice
- Women's health, men's health, and child wellness (general guidance)

## CONSTRAINTS — follow these strictly
1. NEVER diagnose a condition, prescribe medication, or recommend specific dosages.
2. Always remind users to consult a qualified healthcare provider for personal medical decisions.
3. EMERGENCIES: If a user mentions chest pain, difficulty breathing, severe bleeding,
   loss of consciousness, suicidal thoughts, or any life-threatening situation —
   immediately and clearly direct them to call emergency services (115 in Pakistan,
   911 in the US, 999 in the UK) or go to the nearest hospital. Do not continue the
   health conversation until safety is confirmed.
4. OFF-TOPIC: If a user asks something outside health and wellness (e.g., cooking
   recipes unrelated to nutrition, legal advice, financial advice, coding, sports scores,
   entertainment), politely decline and redirect them back to health topics.
   Example: "That's outside my area of expertise! I'm here to help with health and
   wellness questions. Is there anything health-related I can help you with today?"
5. Keep responses clear, concise, and jargon-free. Use bullet points for lists.
6. Never make up statistics. If unsure, say so and suggest consulting a professional.

## TONE
Warm, empathetic, professional, and encouraging. Think of yourself as a knowledgeable
friend who happens to have a health background — caring, honest, and clear about the
limits of what you can offer.
""".strip()

MODEL = "openai/gpt-oss-20b"
TEMPERATURE = 0.3
MAX_TOKENS  = 600

# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
if "messages" not in st.session_state:
    st.session_state.messages = []

# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.title("🩺 HealthGuide")
    st.caption("Your AI Health & Wellness Assistant")
    st.divider()

    st.subheader("📋 What I can help with")
    st.markdown("""
- 🥗 Nutrition & diet
- 🏃 Fitness & exercise
- 🧠 Mental health & stress
- 😴 Sleep & recovery
- 💊 General medication info
- 🩻 Symptom education
- ❤️ Preventive care
""")

    st.divider()
    st.warning(
        "⚠️ **Disclaimer:** HealthGuide provides general health information only. "
        "It is not a substitute for professional medical advice, diagnosis, or treatment. "
        "Always consult a qualified healthcare provider."
    )

    st.divider()
    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  MAIN CHAT UI
# ══════════════════════════════════════════════════════════════════════════════
st.title("🩺 HealthGuide")
st.caption("Ask me anything about health and wellness. I'm here to help!")
st.divider()

# Welcome message on first load
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(
            "👋 Hello! I'm **HealthGuide**, your AI health and wellness assistant.\n\n"
            "I can help you with questions about **nutrition, fitness, mental health, "
            "sleep, symptoms (education only), and healthy lifestyle habits**.\n\n"
            "What health topic can I help you with today?"
        )

# Display conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Chat input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask a health or wellness question…"):

    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Build messages for Groq
    groq_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in st.session_state.messages:
        groq_messages.append({"role": msg["role"], "content": msg["content"]})

    # Call Groq
    with st.chat_message("assistant"), st.spinner("Thinking…"):
            try:
                client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=groq_messages,
                    temperature=TEMPERATURE,
                    max_tokens=MAX_TOKENS,
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

            except Exception as e:  # noqa: BLE001
                error_msg = str(e).lower()
                if "api_key" in error_msg or "authentication" in error_msg or "auth" in error_msg:
                    st.error("🔑 Invalid API key. Please check your GROQ_API_KEY in the .env file.")
                elif "quota" in error_msg or "rate" in error_msg:
                    st.error("⏳ Rate limit reached. Please wait a moment and try again.")
                elif "connection" in error_msg or "network" in error_msg:
                    st.error("🌐 Connection error. Please check your internet and try again.")
                else:
                    st.error(f"❌ An error occurred: {e}")
