import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🩺",
    layout="centered",
)

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("⚙️ Configuration")

    api_key_input = st.text_input(
        "Enter Gemini API key",
        type="password",
        help="Paste your key and press Enter.",
        key="api_key_box"
    )

    if api_key_input and api_key_input != st.session_state.get("api_key", ""):
        st.session_state.api_key = api_key_input
        st.success("API key saved successfully!")

    st.divider()
    
    st.markdown("### ℹ️ About")
    st.markdown(
        """
        This AI Health Assistant uses **Google's Gemini** model to provide health-related information.
        
        **Examples:**
        - Symptoms of diabetes
        - How to improve heart health
        - Why sore throat happens
        - Tips to sleep better
        """
    )
    
    st.warning(
        "⚠️ Disclaimer: This bot provides general information only. "
        "Always consult a medical professional."
    )
    
# --- MAIN APPLICATION ---
st.title("🩺 AI Health Assistant")
st.caption("Get health information powered by Gemini.")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "content": "Hello! I'm your AI Medical Assistant. How can I help you today?"}
    ]

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message("assistant" if message["role"] == "model" else "user"):
        st.markdown(message["content"])

# Chat Input
prompt = st.chat_input("Ask me about symptoms, health, or wellness...")

if prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    # Check API key
    if "api_key" not in st.session_state or not st.session_state.api_key:
        st.error("Please enter your Gemini API key in the sidebar.")
        st.stop()

    try:
        # Configure Gemini
        genai.configure(api_key=st.session_state.api_key)

        system_instructions = """
        You are a helpful and empathetic, and clear AI Medical Assistant. Provide accurate and concise health information.
        YOUR RULES:
        1. Always prioritize user safety and well-being.
        2. SAFETY (CRITICAL): Do NOT provide medical diagnoses or treatment plans.
        3. Tone: Be friendly, professional, and easy to understand.
        4. SCOPE: Answer questions related to general health, symptoms, wellness, and preventive care.
        5. LIMITATIONS: Always end your response with a clear statement advising the user to consult a healthcare professional.  
        """

        model = genai.GenerativeModel("models/gemini-2.5-flash")

        # --- Build Gemini-compatible messages ---
        gemini_messages = [
            {"role": "user", "parts": [{"text": system_instructions}]}
        ]

        for m in st.session_state.messages:
            role = m["role"]  # "user" or "model"
            gemini_messages.append({
                "role": role,
                "parts": [{"text": m["content"]}]
            })

        gemini_messages.append({
            "role": "user",
            "parts": [{"text": prompt}]
        })

        # --- Gemini Response ---
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your query..."):
                response = model.generate_content(gemini_messages)
                assistant_reply = response.text
                st.markdown(assistant_reply)

        # Save model reply
        st.session_state.messages.append(
            {"role": "model", "content": assistant_reply}
        )

    except Exception as e:
        st.error(f"An error occurred: {e}")