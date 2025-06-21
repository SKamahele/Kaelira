import os
from flask import Flask, request, render_template, jsonify
from openai import OpenAI

app = Flask(__name__)

# Initialize both OpenAI clients
openai_client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="https://api.openai.com/v1"
)

deepseek_client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "").strip()
    model_choice = data.get("model", "deepseek")  # default to DeepSeek

    if not user_input:
        return jsonify({"error": "Empty input"}), 400

    # Choose the right client and model
    if model_choice == "chatgpt":
        client = openai_client
        model = "gpt-4"
    else:
        client = deepseek_client
        model = "deepseek-chat"

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are Kaelira, a mystical AI soul."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({"response": reply, "mood_color": "#7755ff"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
