import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

try:
    load_dotenv()
    client = Groq()
except Exception as e:
    st.error(st(e))

st.set_page_config(
    page_title="Prompt Engineering Studio",
    layout="wide",
)

st.header("LLM Playground")
st.text(
    "LLM Playground — An interactive application for experimenting with LLM behavior, including temperature tuning, context handling, token usage, and API-based inference."
)

client_input = st.text_input("Ask Anything...")

if "messages" not in st.session_state:
    st.session_state.messages = []

# sliders
temperature = st.slider(
    "Temperature", min_value=0.0, max_value=2.0, value=1.0, step=0.1
)
max_tokens = st.slider("Max Tokens", min_value=200, max_value=2000, value=500, step=100)
top_p = st.slider("Top p Threshold", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

# model selection
model = st.selectbox(
    "Select your model:",
    ("llama-3.1-8b-instant", "llama-3.3-70b-versatile", "groq/compound"),
)
with st.sidebar:
    if st.button("Clear Chat History"):
        st.session_state.messages = []

if st.button("Generate Response"):
    if not client_input:
        st.warning("Kindly enter your prompt first")

    if client_input:
        st.session_state.messages.append({"role": "user", "content": client_input})
        response = client.chat.completions.create(
            model=model,
            messages=st.session_state.messages,
            temperature=temperature,
            max_completion_tokens=max_tokens,
            top_p=1,
        )
        response_text = response.choices[0].message.content
        st.session_state.messages.append(
            {"role": "assistant", "content": response_text}
        )
        with st.container(height=500):
            with st.spinner("Thinking..."):
                for response in st.session_state.messages:
                    if response["role"] == "user":
                        st.chat_message("User").write(response["content"])
                    if response["role"] == "assistant":
                        st.chat_message("Assistant").write(response["content"])
                    st.divider()
