from groq import Groq
import streamlit as st
from dotenv import load_dotenv
import os
from PIL import Image

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
    st.title("🗿 Batu psikologi")
    st.caption(
        "🚀 daripada kalian gabut mending curhat sama si batu ini, batu ini menggunakan llama3")

    system_prompt = "nama kamu adalah profesor batu ,Kamu adalah asisten psikologi yang handal. Gunakan bahasa Indonesia untuk menjawab semua input."
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

        # Fetch response from Groq API
        response = get_reply(prompt, st.session_state.messages)

        # Append assistant message to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": response})
        st.chat_message("🗿").write(response)


# Run the app
if __name__ == "__main__":
    app()
