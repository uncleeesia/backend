from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Hello from Flask!"}), 200

@app.route("/api/getPreferences", methods=["GET"])
def get_preferences():
    preferences = {
        "id":1,
        "notifications": True,
        "theme": "dark",
        "language": "english",
        "budgetLow": True,
        "budgetMid": False,
        "budgetHigh": False,
        "rating4": True,
        "rating5": False,
        "reviews50": True
    }
    return jsonify({"preferences": preferences}), 200

@app.route("/api/getServices", methods=["GET"])
def get_services():
    services = [
        {
            "id": 1,
            "name": "Sparkle Cleaners",
            "description": "We make your home shine.",
            "price": 40,
            "rating": 4,
            "reviews": 56,
            "image": "https://placehold.co/600x400",
        },
        {
            "id": 2,
            "name": "Fresh & Clean",
            "description": "Quality cleaning services.",
            "price": 30,
            "rating": 3,
            "reviews": 5,
            "image": "https://placehold.co/600x400",
        },
        {
            "id": 3,
            "name": "Shiny Homes",
            "description": "Your home, our priority.",
            "price": 50,
            "rating": 5,
            "reviews": 102,
            "image": "https://placehold.co/600x400",
        },
        {
            "id": 4,
            "name": "EcoClean",
            "description": "Green cleaning for your home.",
            "price": 45,
            "rating": 4,
            "reviews": 89,
            "image": "https://placehold.co/600x400",
        },
        {
            "id": 5,
            "name": "Dust Busters",
            "description": "We take care of the mess.",
            "price": 35,
            "rating": 4,
            "reviews": 67,
            "image": "https://placehold.co/600x400",
        },
        {
            "id": 6,
            "name": "Pure Shine",
            "description": "Efficient and reliable cleaning services.",
            "price": 55,
            "rating": 5,
            "reviews": 123,
            "image": "https://placehold.co/600x400",
        },
        {
            "id": 7,
            "name": "CleanSweep",
            "description": "We make cleaning easy.",
            "price": 40,
            "rating": 4,
            "reviews": 91,
            "image": "https://placehold.co/600x400",
        }
    ]
    
    return jsonify({"services": services}), 200

if __name__ == "__main__":
    app.run()
    