import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

conn = psycopg2.connect("postgres://u8dd30h9brbpjq:pf3390a930040c9e19e9c5ce482dcfbf829ee969f2ed886456eef7dc3a9519e88@ce0lkuo944ch99.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d3tpurv791l296", sslmode='require')
cursor = conn.cursor()
logging.basicConfig(level=logging.INFO)
@app.route("/", methods=["GET"])
def home():
    app.logger.info(f"URL: {request.url}")
    app.logger.info(f"Method: {request.method}")
    app.logger.info(f"Headers: {request.headers}")
    cursor.execute("SELECT 1")
    myresult = cursor.fetchall()

    for x in myresult:
        print(x)
    
    return jsonify({"message": "Hello from Flask!"}), 200

@app.route("api/getPreferences", methods=["GET"])
def get_preferences():
    # preferences = {
    #     "id":1,
    #     "notifications": True,
    #     "theme": "dark",
    #     "language": "english",
    #     "budgetLow": True,
    #     "budgetMid": False,
    #     "budgetHigh": False,
    #     "rating4": True,
    #     "rating5": False,
    #     "reviews50": False,
    #     "reviews200": True
    # }
    preferences={}
    return jsonify({"preferences": preferences}), 200

@app.route("/api/UpdatePreferences", methods=["POST"])
def update_preferences(preferences):
    # logic to update
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

@app.route("/api/getReviews", methods=["GET"])
def get_reviews():
    #some logic to get reviews tagged to specific services
    reviews = [
        {
            "id": 1,
            "serviceId": 1,
            "author": "Alice",
            "rating": 5,
            "review": "Excellent service!",
            "date": "2023-10-01",
        },{
            "id": 2,
            "serviceId": 1,
            "author": "alicia",
            "rating": 3,
            "review": "moderate service!",
            "date": "2023-10-01",
        },{
            "id": 3,
            "serviceId": 1,
            "author": "coconut",
            "rating": 3,
            "review": "moderate service!",
            "date": "2023-10-01",
        },{
            "id": 4,
            "serviceId": 1,
            "author": "apple",
            "rating": 3,
            "review": "moderate service!",
            "date": "2023-10-01",
        },{
            "id": 5,
            "serviceId": 1,
            "author": "orange",
            "rating": 3,
            "review": "moderate service!",
            "date": "2023-10-01",
        }]
    return jsonify({"reviews": reviews}), 200

if __name__ == "__main__":
    app.run()
    