from flask import Flask, request, jsonify, render_template
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

DATASET_PATH = "reported_content.csv"

# Load dataset or create one if not exists
if not os.path.exists(DATASET_PATH):
    df = pd.DataFrame(columns=["ID", "Type", "Content", "Report_Count", "First_Report_Date", "Last_Report_Date", "Organizations"])
    df.to_csv(DATASET_PATH, index=False)

def load_dataset():
    return pd.read_csv(DATASET_PATH)

def save_dataset(df):
    df.to_csv(DATASET_PATH, index=False)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check_content():
    user_input = request.json["content"]
    input_type = request.json["type"]

    df = load_dataset()
    
    # Check if content exists
    match = df[df["Content"] == user_input]
    
    if not match.empty:
        response = {
            "exists": True,
            "report_count": int(match.iloc[0]["Report_Count"]),
            "first_report": match.iloc[0]["First_Report_Date"],
            "last_report": match.iloc[0]["Last_Report_Date"],
            "organizations": match.iloc[0]["Organizations"]
        }
    else:
        response = {"exists": False}

    return jsonify(response)

@app.route("/report", methods=["POST"])
def report_content():
    data = request.json
    user_input = data["content"]
    input_type = data["type"]
    orgs = data.get("organizations", "https://www.scamwatch.gov.au, https://www.fbi.gov/investigate/cyber")

    df = load_dataset()

    # Check if content exists
    match = df[df["Content"] == user_input]

    if not match.empty:
        index = match.index[0]
        df.at[index, "Report_Count"] += 1
        df.at[index, "Last_Report_Date"] = datetime.today().strftime('%Y-%m-%d')
    else:
        new_entry = {
            "ID": len(df) + 1,
            "Type": input_type,
            "Content": user_input,
            "Report_Count": 1,
            "First_Report_Date": datetime.today().strftime('%Y-%m-%d'),
            "Last_Report_Date": datetime.today().strftime('%Y-%m-%d'),
            "Organizations": orgs
        }
        df = df.append(new_entry, ignore_index=True)

    save_dataset(df)
    
    return jsonify({"message": "Report submitted successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
