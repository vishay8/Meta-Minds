from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from chatbot import get_chat_response

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "secret"
jwt = JWTManager(app)

users = {"admin": "password"}
courses = ["Cybersecurity Basics", "Ethical Hacking", "Network Security"]

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if data["username"] in users and users[data["username"]] == data["password"]:
        return jsonify(token=create_access_token(identity=data["username"]))
    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/course", methods=["GET"])
@jwt_required()
def get_courses():
    return jsonify({"courses": courses})

@app.route("/chatbot", methods=["POST"])
@jwt_required()
def chatbot():
    message = request.json["message"]
    reply = get_chat_response(message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
