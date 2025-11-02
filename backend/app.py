import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Load preloaded content
with open('student_content.json', 'r', encoding='utf-8') as f:
    preloaded_content = json.load(f)

# Groq API settings
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Set your API key in environment variables

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get("question", "").strip().lower()

    # Check preloaded content
    for item in preloaded_content.get("topics", []):
        if item['question'].lower() in question:
            return jsonify({"answer": item['answer']})

    # If not found, call Groq API
    if GROQ_API_KEY:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "messages": [{"role": "user", "content": question}],
            "model": "openai/gpt-oss-120b"  # Choose the appropriate model
        }
        try:
            response = requests.post(GROQ_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            answer = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response")
        except requests.exceptions.RequestException as e:
            answer = f"Error contacting Groq API: {str(e)}"
    else:
        answer = "Groq API key is not set."

    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
