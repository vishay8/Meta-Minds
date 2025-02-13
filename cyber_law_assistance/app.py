from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Hugging Face API details
HUGGINGFACE_API_URL ="https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
HEADERS = {"Authorization": "Bearer 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"}

def ask_huggingface(prompt):
    """Function to get chatbot responses from Hugging Face API"""
    payload = {"inputs": prompt}
    response = requests.post(HUGGINGFACE_API_URL, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return "Sorry, I couldn't process that request."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    bot_response = ask_huggingface(user_input)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
