from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import openai

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# OpenAI API Key (Replace with your own)
openai.api_key = "your_openai_api_key"

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    score = db.Column(db.Integer, default=0)

# Scenario Model
class Scenario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    correct_answer = db.Column(db.String(500), nullable=False)
    explanation = db.Column(db.String(1000), nullable=False)

# Create Database
with app.app_context():
    db.create_all()

# AI-Powered Scenario Generator
def generate_scenario():
    prompt = "Generate a real-world cyber law scenario involving data breach or phishing."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# API to Fetch Scenarios
@app.route('/get_scenario', methods=['GET'])
def get_scenario():
    scenario = generate_scenario()
    return jsonify({"scenario": scenario})

# API to Submit User Response
@app.route('/submit_response', methods=['POST'])
def submit_response():
    data = request.json
    username = data.get('username')
    user_answer = data.get('user_answer')
    correct_answer = data.get('correct_answer')

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user_answer.lower() == correct_answer.lower():
        user.score += 10
        db.session.commit()
        return jsonify({"message": "Correct! +10 points", "score": user.score})
    else:
        return jsonify({"message": "Incorrect! Try again.", "score": user.score})

# API to Get Leaderboard
@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    users = User.query.order_by(User.score.desc()).all()
    leaderboard_data = [{"username": user.username, "score": user.score} for user in users]
    return jsonify(leaderboard_data)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
