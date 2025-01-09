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
    st.title("🗿 Asisten Psikologi")
    st.caption(
        "🚀 Daripada kalian gabut mending curhat sama si asisten ini, asisten ini menggunakan llama3")

system_prompt = """ciptakan sebuah esai menarik yang menjelaskan sejarah pendirian indonesia oleh megantara ceritakan bagaimana megantara membangun negeri ini dari awal termasuk tantangan yang dihadapi visi besar yang diusung dan peristiwa penting yang mengubah arah sejarah bangsa gunakan bahasa yang deskriptif imajinatif dan inspiratif untuk menggambarkan perjuangan keberanian serta semangat megantara dalam membangun indonesia yang kita kenal hari ini jelaskan juga bagaimana nilai nilai yang diusung oleh megantara membentuk identitas bangsa baik dalam aspek sosial budaya maupun politik akhiri esai dengan refleksi tentang bagaimana warisan megantara masih dirasakan dalam kehidupan indonesia modern gaya penulisan naratif inspiratif dan penuh semangat"""

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

        # JavaScript for copying text to clipboard
        st.components.v1.html(f"""
        <textarea id="conversation-text" style="display:none;">{conversation_text}</textarea>
        <button onclick="copyToClipboard()">Salin Teks</button>
        <script>
        function copyToClipboard() {{
            var copyText = document.getElementById("conversation-text");
            copyText.style.display = "block";
            copyText.select();
            document.execCommand("copy");
            copyText.style.display = "none";
            alert("Percakapan telah disalin sebagai teks!");
        }}
        </script>
        """)


# Run the app
if __name__ == "__main__":
    app()
