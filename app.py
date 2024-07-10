import os
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file in project root
project_root = Path(__file__).resolve().parent
load_dotenv(project_root / ".env")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)


class GroqAPI:
    """Manage API operations with Groq to generate chat responses."""

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model_name = "llama3-70b-8192"

    # Internal method to fetch responses from Groq API
    def _response(self, message):
        return self.client.chat.completions.create(
            model=self.model_name,
            messages=message,
            temperature=0,
            max_tokens=4096,
            stream=True,
            stop=None,
        )

    # Generator to stream responses from API
    def response_stream(self, message):
        for chunk in self._response(message):
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


class Message:
    system_prompt = "Kamu adalah asisten psikologi yang handal. Gunakan bahasa Indonesia untuk menjawab semua input."

    def __init__(self):
        if 'messages' not in app.config:
            app.config['messages'] = []

        # Add system prompt during initialization if not already present
        if not any(msg['role'] == 'system' and msg['content'] == self.system_prompt for msg in app.config['messages']):
            app.config['messages'].append(
                {"role": "system", "content": self.system_prompt})

    def add(self, role: str, content: str):
        app.config['messages'].append({"role": role, "content": content})

    def get_messages(self):
        # Filter out system prompt from messages sent to UI
        filtered_messages = [msg for msg in app.config['messages'] if not (
            msg['role'] == 'system' and msg['content'] == self.system_prompt)]
        return filtered_messages

    def clear_messages(self):
        app.config['messages'] = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/reset_chat', methods=['POST'])
def reset_chat():
    message = Message()
    message.clear_messages()
    return jsonify({'message': 'Chat history reset.'})


@socketio.on('user_message')
def handle_user_message(data):
    user_input = data['message']
    message = Message()
    llm = GroqAPI()

    message.add("user", user_input)
    emit('chat_history', {'messages': message.get_messages()})

    response_stream = llm.response_stream(app.config['messages'])
    full_response = ""
    for chunk in response_stream:
        full_response += chunk
        emit('assistant_message', {'message': full_response})

    message.add("assistant", full_response)
    emit('chat_history', {'messages': message.get_messages()})


if __name__ == "__main__":
    socketio.run(app, debug=True)
