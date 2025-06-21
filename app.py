import os
from flask import Flask, request, render_template, jsonify
from kaelira_writer import generate_code, save_code
from deepseek import DeepSeekClient

app = Flask(__name__)

# DeepSeek Setup
deepseek_client = DeepSeekClient(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    message = request.json.get("message", "").strip()
    if not message:
        return jsonify({"response": "No message received."})

    # Talk to DeepSeek
    response = deepseek_client.send_chat(message)
    return jsonify({"response": response, "mood_color": "#7755ff"})

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.json.get("prompt", "")
    code = generate_code(prompt)
    save_code(code)
    return jsonify({"generated": code})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
