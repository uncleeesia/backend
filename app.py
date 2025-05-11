from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

conn = psycopg2.connect(
    "postgres://u8dd30h9brbpjq:pf3390a930040c9e19e9c5ce482dcfbf829ee969f2ed886456eef7dc3a9519e88@ce0lkuo944ch99.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d3tpurv791l296", sslmode='require')
cursor = conn.cursor()


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend Server Connected"}), 200


@app.route("/api/routes", methods=["GET"])
def list_routes():
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        output.append({
            'endpoint': rule.endpoint,
            'methods': methods,
            'rule': str(rule)
        })
    return jsonify(output)


@app.route("/api/getPreferences", methods=["GET"])
def get_preferences():
    # logic to update get from db
    preferences = {
        "id": 1,
        "theme": "light",
        "House Cleaning": False,
        "Car Cleaning": False,
        "Bathroom Cleaning": True,
        "Window Cleaning": False,
        "Indonesian": True,
        "Filipino": False,
        "Burmese": False,
        "Vietnamese": False,
    }
    # preferences = {}
    return jsonify({"preferences": preferences}), 200


@app.route("/api/UpdatePreferences", methods=["POST"])
def update_preferences(preferences):
    # logic to update db
    return jsonify({"preferences": preferences}), 200


@app.route("/api/getServiceProviders", methods=["GET"])
def get_services():
    # logic to update get from db
    servicesProvider = [
        {
            "id": 1,
            "name": "Sparkle Cleaners",
            "cleaningTypes": [
                {
                    "id": 1,
                    "type": "House Cleaning",
                    "price": 100,
                    "rating": 4,
                    "reviews": 56,
                    "summary": "Comprehensive cleaning for your entire home.",
                    "duration": 120  # 2 hours in minutes
                },
                {
                    "id": 2,
                    "type": "Bathroom Cleaning",
                    "price": 50,
                    "rating": 4,
                    "reviews": 56,
                    "summary": "Deep cleaning for bathrooms and toilets.",
                    "duration": 60  # 1 hour in minutes
                },
                {
                    "id": 3,
                    "type": "Window Cleaning",
                    "price": 75,
                    "rating": 4,
                    "reviews": 56,
                    "summary": "Streak-free cleaning of interior and exterior windows.",
                    "duration": 90  # 1.5 hours in minutes
                }
            ],
            "description": "We make your home shine.",
            "image": "https://placehold.co/600x400",
        },
        {
            "id": 2,
            "name": "Fresh & Clean",
            "cleaningTypes": [
                {
                    "id": 4,
                    "type": "Car Cleaning",
                    "price": 150,
                    "rating": 3,
                    "reviews": 5,
                    "summary": "Interior and exterior car wash with polish.",
                    "duration": 180  # 3 hours in minutes
                }
            ],
            "description": "Quality cleaning services.",
            "image": "https://placehold.co/600x400",
        },
        {
            "id": 3,
            "name": "Shiny Homes",
            "cleaningTypes": [
                {
                    "id": 5,
                    "type": "House Cleaning",
                    "price": 120,
                    "rating": 5,
                    "reviews": 102,
                    "summary": "Detailed home cleaning for every room.",
                    "duration": 180  # 3 hours in minutes
                },
                {
                    "id": 6,
                    "type": "Bathroom Cleaning",
                    "price": 60,
                    "rating": 5,
                    "reviews": 102,
                    "summary": "Disinfecting and scrubbing of all bathroom surfaces.",
                    "duration": 60  # 1 hour in minutes
                }
            ],
            "description": "Your home, our priority.",
            "image": "https://placehold.co/600x400",
        },
        {
            "id": 4,
            "name": "EcoClean",
            "cleaningTypes": [
                {
                    "id": 7,
                    "type": "Window Cleaning",
                    "price": 80,
                    "rating": 4,
                    "reviews": 89,
                    "summary": "Eco-friendly window cleaning with natural products.",
                    "duration": 90  # 1.5 hours in minutes
                },
                {
                    "id": 8,
                    "type": "Bathroom Cleaning",
                    "price": 50,
                    "rating": 4,
                    "reviews": 89,
                    "summary": "Safe and sustainable bathroom cleaning.",
                    "duration": 60  # 1 hour in minutes
                }
            ],
            "description": "Green cleaning for your home.",
            "image": "https://placehold.co/600x400",
        },
        {
            "id": 5,
            "name": "Dust Busters",
            "cleaningTypes": [
                {
                    "id": 9,
                    "type": "House Cleaning",
                    "price": 110,
                    "rating": 4,
                    "reviews": 67,
                    "summary": "General house cleaning to maintain cleanliness.",
                    "duration": 150  # 2.5 hours in minutes
                },
                {
                    "id": 10,
                    "type": "Window Cleaning",
                    "price": 75,
                    "rating": 4,
                    "reviews": 67,
                    "summary": "Crystal clear window washing.",
                    "duration": 90  # 1.5 hours in minutes
                }
            ],
            "description": "We take care of the mess.",
            "image": "https://placehold.co/600x400",
        },
        {
            "id": 6,
            "name": "Pure Shine",
            "cleaningTypes": [
                {
                    "id": 11,
                    "type": "House Cleaning",
                    "price": 130,
                    "rating": 5,
                    "reviews": 123,
                    "summary": "Thorough home cleaning for a spotless living space.",
                    "duration": 180  # 3 hours in minutes
                },
                {
                    "id": 12,
                    "type": "Car Cleaning",
                    "price": 160,
                    "rating": 5,
                    "reviews": 123,
                    "summary": "Premium auto detailing for a brand-new look.",
                    "duration": 240  # 4 hours in minutes
                },
                {
                    "id": 13,
                    "type": "Bathroom Cleaning",
                    "price": 70,
                    "rating": 5,
                    "reviews": 123,
                    "summary": "High-standard cleaning for a fresh-smelling bathroom.",
                    "duration": 60  # 1 hour in minutes
                }
            ],
            "description": "Efficient and reliable cleaning services.",
            "image": "https://placehold.co/600x400",
        },
        {
            "id": 7,
            "name": "CleanSweep",
            "cleaningTypes": [
                {
                    "id": 14,
                    "type": "Bathroom Cleaning",
                    "price": 50,
                    "rating": 4,
                    "reviews": 91,
                    "summary": "Quick and effective cleaning for restrooms.",
                    "duration": 60  # 1 hour in minutes
                },
                {
                    "id": 15,
                    "type": "Window Cleaning",
                    "price": 70,
                    "rating": 4,
                    "reviews": 91,
                    "summary": "Professional-grade window cleaning service.",
                    "duration": 90  # 1.5 hours in minutes
                }
            ],
            "description": "We make cleaning easy.",
            "image": "https://placehold.co/600x400",
        }
    ]

    return jsonify({"servicesProvider": servicesProvider}), 200


@app.route("/api/getServicesById", methods=["GET"])
def get_serviceById():

    service_provider_id = request.args.get('id', type=int)

    # add logic to get data by id

    services = [{
        "id": 7,
        "name": "CleanSweep",
        "cleaningTypes": [
                {
                    "id": 14,
                    "type": "Bathroom Cleaning",
                    "price": 50,
                    "rating": 4,
                    "reviews": 91,
                    "summary": "Quick and effective cleaning for restrooms.",
                    "duration": 60
                },
            {
                    "id": 15,
                    "type": "Window Cleaning",
                    "price": 70,
                    "rating": 4,
                    "reviews": 91,
                    "summary": "Professional-grade window cleaning service.",
                    "duration": 90
                },{
                    "id": 16,
                    "type": "Bathroom Cleaning",
                    "price": 50,
                    "rating": 4,
                    "reviews": 91,
                    "summary": "Quick and effective cleaning for restrooms.",
                    "duration": 60
                },
            {
                    "id": 17,
                    "type": "Window Cleaning",
                    "price": 70,
                    "rating": 4,
                    "reviews": 91,
                    "summary": "Professional-grade window cleaning service.",
                    "duration": 90
                }
        ],
        "description": "We make cleaning easy.",
        "image": "https://placehold.co/600x400",
    }]
    if service_provider_id is None:
        return jsonify({"error": "Missing service ID"}), 400
    if not services:
        return jsonify({"error": "Service not found"}), 404
    return jsonify({"services": services})


@app.route("/api/getReviews", methods=["GET"])
def get_reviews():
    # some logic to get reviews tagged to specific services
    reviews = [
        {
            "id": 1,
            "serviceId": 1,
            "author": "Alice",
            "rating": 5,
            "review": "Excellent service!",
            "date": "2023-10-01",
        }, {
            "id": 2,
            "serviceId": 1,
            "author": "alicia",
            "rating": 3,
            "review": "moderate service!",
            "date": "2023-10-01",
        }, {
            "id": 3,
            "serviceId": 1,
            "author": "coconut",
            "rating": 3,
            "review": "moderate service!",
            "date": "2023-10-01",
        }, {
            "id": 4,
            "serviceId": 1,
            "author": "apple",
            "rating": 3,
            "review": "moderate service!",
            "date": "2023-10-01",
        }, {
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
