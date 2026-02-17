from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

app = Flask(__name__)

# --------------------------------------------------
# MongoDB Atlas Connection (PART 2 requirement)
# --------------------------------------------------
mongo_uri = os.getenv("MONGO_URI")

print("MONGO_URI =", mongo_uri)

if not mongo_uri:
    print("❌ MONGO_URI not loaded from .env")
    users_collection = None
else:
    try:
        client = MongoClient(mongo_uri)
        db = client.assignment_db
        users_collection = db.users
        print("✅ Connected to MongoDB Atlas")
    except Exception as e:
        print("❌ MongoDB connection error:", e)
        users_collection = None


# --------------------------------------------------
# PART 1: API Route (reads from backend file)
# --------------------------------------------------
@app.route("/submittodoitem", methods=["POST"])
def submit_to-do_item():
    item_name = request.form.get("itemName")
    item_description = request.form.get("itemDescription")

    if not item_name or not item_description:
        return jsonify({"error": "Both fields are required"}), 400

    todo_item = {
        "itemName": item_name,
        "itemDescription": item_description
    }   

    
    db.todo_item.insert_one(todo_item)

    return jsonify({"message": "To-Do item submitted successfully!"})
# --------------------------------------------------
# Home Route – Form Page
# --------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------------
# Form Submission Route (PART 2)
# --------------------------------------------------
@app.route("/submit", methods=["POST"])
def submit():
    if users_collection is None:
        return render_template("index.html", error="Database connection failed")

    name = request.form.get("name")
    email = request.form.get("email")

    if not name or not email:
        return render_template("index.html", error="All fields are required")

    try:
        users_collection.insert_one({
            "name": name,
            "email": email
        })
        return redirect(url_for("success"))
    except Exception as e:
        print(e)
        return render_template("index.html", error="Something went wrong!")


# --------------------------------------------------
# Success Route
# --------------------------------------------------
@app.route("/success")
def success():
    return render_template("success.html")


# --------------------------------------------------
# Run Application
# --------------------------------------------------
if __name__ == "__main__":
    app.run(debug=os.getenv("APP_DEBUG", "False") == "True")
