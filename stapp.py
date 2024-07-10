from groq import Groq
import streamlit as st
from dotenv import load_dotenv
import os
from PIL import Image
import pyperclip  # Library for copying text to clipboard

# Load environment variables from .env file
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")


def append_history(history, item):
    history.append(item)
    return history


def get_reply(input_string, messages):
    client = Groq(api_key=groq_api_key)
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        temperature=0,
        max_tokens=4096,
        stream=False,
        stop=None
    )
    answer = response.choices[0].message.content
    return answer


def app():
    st.set_page_config(layout="wide")

    # Load image from file
    img = Image.open("weebsu.png")
    new_size = (150, 150)
    img = img.resize(new_size)
    st.image(img)

    history = []
    st.title("🗿 Asisten Psikologi")
    st.caption(
        "🚀 Daripada kalian gabut mending curhat sama si asisten ini, asisten ini menggunakan llama3")

    system_prompt = "Nama kamu adalah asisten psikologi, kamu ahli dalam memberikan saran. Gunakan bahasa Indonesia untuk berkomunikasi."
    if 'messages' not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": system_prompt}, {
            "role": "assistant", "content": "Kalian bisa curhat di sini dengan asisten psikologi yang selalu siap membantu."}]

    # Display chat history, excluding system prompt
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            if msg["role"] == "assistant":
                st.chat_message("🗿").write(msg["content"])
            elif msg["role"] == "user":
                st.chat_message("🙂").write(msg["content"])

    # Handle user input
    if prompt := st.chat_input():
        # Append user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("🙂").write(prompt)

        # Fetch response from Groq API
        response = get_reply(prompt, st.session_state.messages)

        # Append assistant message to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": response})
        st.chat_message("🗿").write(response)

    # Button to copy conversation text
    if st.button("Salin Teks"):
        conversation_text = "\n".join(
            f"🙂: {msg['content']}" if msg["role"] == "user" else f"🗿: {msg['content']}"
            for msg in st.session_state.messages if msg["role"] != "system"
        )
        # Copy conversation text to clipboard
        pyperclip.copy(conversation_text)
        st.info("Percakapan telah disalin sebagai teks!")


# Run the app
if __name__ == "__main__":
    app()
