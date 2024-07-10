from groq import Groq
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

st.title("🗿 Batu psikologi")
st.caption("🚀 daripada kalian gabut mending curhat sama ini ini menggunakan llama3")

# Initialize chat history and system prompt
system_prompt = "Kamu adalah asisten psikologi yang handal. Gunakan bahasa Indonesia untuk menjawab semua input."
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}, {
        "role": "assistant", "content": "kalian bisa curhat disini dengan profesor batu lulusan S 1000 psikologi"}]

# Display chat history, excluding system prompt
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])


# Handle user input
if prompt := st.chat_input():
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Initialize Groq API client
    client = Groq(api_key=groq_api_key)

    # Fetch response from Groq API
    response = client.chat.completions.create(
        model="llama3-70b-8192", messages=st.session_state.messages, temperature=0, max_tokens=4096, stream=False, stop=None)
    msg = response.choices[0].message.content

    # Append assistant message to chat history
    # st.session_state.messages.append({"role": "assistant", "content": msg})
    # Append assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("🗿").write(msg)

    # st.chat_message("assistant").write(msg)
