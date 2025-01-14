from datetime import datetime

import requests
from flask import Flask, jsonify, render_template, request
from openai import OpenAI

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI()

# Store conversation history
conversations = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    rag = data.get("rag", False)
    conversation_id = data.get("conversation_id", str(datetime.now().timestamp()))

    # Get or create conversation history
    if conversation_id not in conversations:
        conversations[conversation_id] = []

    if rag:
        try:
            html = requests.get(rag).text
            user_message = f'You are a RAG system. Use the provided "Knowledge" to respond to the user. Knowledge: {html} \n User Message: {user_message}'
        except Exception:
            pass

    # Get or create conversation history
    if conversation_id not in conversations:
        conversations[conversation_id] = []

    # Add user message to history
    conversations[conversation_id].append({"role": "user", "content": user_message})

    try:
        # Call OpenAI API with new client syntax
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=conversations[conversation_id]
        )

        # Get bot's response
        bot_message = response.choices[0].message.content

        # Add bot response to history
        conversations[conversation_id].append(
            {"role": "assistant", "content": bot_message}
        )

        return jsonify({"response": bot_message, "conversation_id": conversation_id})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/history/<conversation_id>", methods=["GET"])
def get_history(conversation_id):
    if conversation_id in conversations:
        return jsonify({"history": conversations[conversation_id]})
    return jsonify({"error": "Conversation not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
