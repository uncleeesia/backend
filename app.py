# Middle layer imports
from flask import Flask, jsonify, request
from flask_cors import CORS

# Back End imports
from dbtalker_psql import DBTalker
from user_controller import UserController
from service_controller import ServiceController
from review_controller import ReviewController
from payment_controller import PaymentController
from feedback_controller import FeedbackController
from models import General_user

app = Flask(__name__)
CORS(app)

api_key = "HRKU-4e9e0d78-2234-4999-8391-13e14ec05360"  # Remove before zipping
schema_name = "csit314_schma"

# Creating of Objects
dbtalker_obj = DBTalker(api_key)
user_controller = UserController(dbtalker_obj, schema_name)
sevice_controller = ServiceController(dbtalker_obj, schema_name)
review_controller = ReviewController(dbtalker_obj, schema_name)
payment_controller = PaymentController(dbtalker_obj, schema_name)
feedback_controller = FeedbackController(dbtalker_obj, schema_name)


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

# @app.route("/api/postFeedback", methods=["POST"])
# def post_feedback():
#     data = request.get_json()
#     # logic to update db
#     return jsonify({"message": "Feedback received", "data": data}), 200

# @app.route("/api/postPayment", methods=["POST"])
# def post_payment():
#     data = request.get_json()
#     # logic to update db
#     return jsonify({"message": "Payment received", "data": data}), 200


@app.route("/api/getAllPaymentTransactionByUserId", methods=["GET"])
def get_all_payment_transaction_by_user_id():

    result = None

    try:

        user_id = request.args.get('user_id', type=int)

        # Check if valid integer
        if isinstance(user_id, int):

            pass

        else:

            raise Exception("Invalid user id was given.")

        payment_list = payment_controller.extract_payment_for_report(
            user_id=user_id)

        # Verify if it is a valid object
        if isinstance(payment_list, list):

            pass

        else:

            raise Exception("Unable to get payment transaction.")

        temp_payment_list = [payment.model_dump(
            mode='json') for payment in payment_list]

        result = jsonify({"payment": temp_payment_list}), 200

    except Exception as e:

        result = jsonify({"error": str(e)}), 400

    finally:

        return result


@app.route("/api/getUser", methods=["GET"])
def get_user():
    result = None

    try:
        email = request.args.get('email', type=str)
        user_id = request.args.get('user_id', type=int)
        admin = request.args.get('admin', type=bool)
        # Check if valid integer
        if isinstance(email, str):
            pass

        elif isinstance(user_id, int):
            pass

        elif isinstance(admin, bool):
            pass

        else:
            raise Exception("Invalid user id was given.")

        if (email is not None):
            user_obj = user_controller.extract_user(email=email)

        elif (user_id is not None):
            user_obj = user_controller.extract_user(user_id=user_id)

        elif (admin is not None):
            user_obj = user_controller.extract_user(is_admin=admin)

        # Verify if it is a valid object
        if isinstance(user_obj, list):

            pass

        else:

            raise Exception("Unable to get user.")

        user = user_obj[0]

        # If only one user expected
        if user_id or email:
            user = user_obj[0]
            result = jsonify({"user": user.model_dump(mode='json')}), 200

        # If multiple users expected
        elif admin is not None:
            result = jsonify(
                {"users": [u.model_dump(mode='json') for u in user_obj]}), 200

    except Exception as e:

        result = jsonify({"error": str(e)}), 400

    finally:

        return result


@app.route("/api/UpdateUserById", methods=["PUT"])
def update_user_by_id():
    try:
        data = request.get_json()

        user_id = data.get("user_id")
        reason = data.get("reason")
        is_blacklist = data.get("is_blacklist")

        if not isinstance(user_id, int) or user_id <= 0:
            raise Exception("Invalid or missing user_id.")
        if not isinstance(is_blacklist, bool):
            raise Exception("Invalid or missing is_blacklist flag.")
        if reason is not None and not isinstance(reason, str):
            raise Exception("Invalid reason.")

        # Call your update method
        update_result = user_controller.update_blacklist_user(
            user_id=user_id,
            is_blacklist=is_blacklist,
            blacklist_reason=reason
        )

        if isinstance(update_result, Exception):
            raise update_result

        # Return success JSON response
        return jsonify({"message": "User blacklist updated successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/getPreferences", methods=["GET"])
def get_preferences():

    result = None

    try:

        user_id = request.args.get('user_id', type=int)

        # Check if valid integer
        if isinstance(user_id, int):

            pass

        else:

            raise Exception("Invalid user id was given.")

        user_obj = user_controller.extract_user(user_id=user_id)

        # Verify if it is a valid object
        if isinstance(user_obj, list):

            pass

        else:

            raise Exception("Unable to get preferences.")

        user = user_obj[0]

        user_preferences = user.preferences

        result = jsonify({"preferences": user_preferences}), 200

    except Exception as e:

        result = jsonify({"error": str(e)}), 400

    finally:

        return result

    # preferences = {
    #     "id": 1,
    #     "theme": "light",
    #     "House Cleaning": False,
    #     "Car Cleaning": False,
    #     "Bathroom Cleaning": True,
    #     "Window Cleaning": False,
    #     "Indonesian": True,
    #     "Filipino": False,
    #     "Burmese": False,
    #     "Vietnamese": False,
    # }
    # preferences = {}
    # return jsonify({"preferences": preferences}), 200


@app.route("/api/UpdatePreferences", methods=["POST"])
def update_preferences(preferences):

    result = None

    try:

        user_id = request.args.get('user_id', type=int)

        # Check if valid integer
        if isinstance(user_id, int):

            pass

        else:

            raise Exception("Invalid user id was given.")

        user_obj = user_controller.extract_user(user_id=user_id)

        # Check if it is a valid object
        if isinstance(user_obj, list):

            pass

        else:

            raise Exception("Unable to find user.")

        user = user_obj[0]

        user.preferences = preferences

        updated_user_obj = user_controller.update_user(user_obj)

        # Check if it is a valid object
        if isinstance(updated_user_obj, General_user):

            pass

        else:

            raise Exception("Unable to update preferences.")

        updated_user = updated_user_obj

        user_preferences = updated_user.preferences

        result = jsonify({"preferences": user_preferences}), 200

    except Exception as e:

        result = jsonify({"error": str(e)}), 400

    finally:

        return result


@app.route("/api/getServiceProviders", methods=["GET"])
def get_services():

    result = None

    try:

        # Get all users that are cleaners
        cleaner_list = user_controller.extract_user(is_cleaner=True)

        if isinstance(cleaner_list, list):

            pass

        else:

            raise Exception("Unable to get services.")

        response_body = []

        # Get all services under user_id
        for user in cleaner_list:

            service_list = sevice_controller.extract_service(
                user_id=user.user_id)

            if isinstance(service_list, list):

                pass

            else:

                raise Exception(
                    f"Unable to get services for cleaner {user.username}.")

            # sorted_service_list = sevice_controller.sort_service(list_of_service=service_list)

            # if isinstance(sorted_service_list, list):

            #     pass

            # else:

            #     raise Exception("Unable to sort services by default type.")

            # temp_service_list = [service.model_dump(mode='json') for service in sorted_service_list]

            # response_body.append({
            #     "cleaner": user.model_dump(mode="json"),
            #     "service_list": temp_service_list
            # })
            response_body.append({
                "cleaner": user.model_dump(mode="json"),
                "service_list": service_list
            })

        result = jsonify({"serviceProviders": response_body}), 200

    except Exception as e:

        result = jsonify({"error": str(e)}), 400

    finally:

        return result
    # logic to update get from db
    # servicesProvider = [
    #     {
    #         "id": 1,
    #         "name": "Sparkle Cleaners",
    #         "cleaningTypes": [
    #             {
    #                 "id": 1,
    #                 "type": "House Cleaning",
    #                 "price": 100,
    #                 "rating": 4,
    #                 "reviews": 56,
    #                 "summary": "Comprehensive cleaning for your entire home.",
    #                 "duration": 120  # 2 hours in minutes
    #             },
    #             {
    #                 "id": 2,
    #                 "type": "Bathroom Cleaning",
    #                 "price": 50,
    #                 "rating": 4,
    #                 "reviews": 56,
    #                 "summary": "Deep cleaning for bathrooms and toilets.",
    #                 "duration": 60  # 1 hour in minutes
    #             },
    #             {
    #                 "id": 3,
    #                 "type": "Window Cleaning",
    #                 "price": 75,
    #                 "rating": 4,
    #                 "reviews": 56,
    #                 "summary": "Streak-free cleaning of interior and exterior windows.",
    #                 "duration": 90  # 1.5 hours in minutes
    #             }
    #         ],
    #         "description": "We make your home shine.",
    #         "image": "https://placehold.co/600x400",
    #     },
    #     {
    #         "id": 2,
    #         "name": "Fresh & Clean",
    #         "cleaningTypes": [
    #             {
    #                 "id": 4,
    #                 "type": "Car Cleaning",
    #                 "price": 150,
    #                 "rating": 3,
    #                 "reviews": 5,
    #                 "summary": "Interior and exterior car wash with polish.",
    #                 "duration": 180  # 3 hours in minutes
    #             }
    #         ],
    #         "description": "Quality cleaning services.",
    #         "image": "https://placehold.co/600x400",
    #     },
    #     {
    #         "id": 3,
    #         "name": "Shiny Homes",
    #         "cleaningTypes": [
    #             {
    #                 "id": 5,
    #                 "type": "House Cleaning",
    #                 "price": 120,
    #                 "rating": 5,
    #                 "reviews": 102,
    #                 "summary": "Detailed home cleaning for every room.",
    #                 "duration": 180  # 3 hours in minutes
    #             },
    #             {
    #                 "id": 6,
    #                 "type": "Bathroom Cleaning",
    #                 "price": 60,
    #                 "rating": 5,
    #                 "reviews": 102,
    #                 "summary": "Disinfecting and scrubbing of all bathroom surfaces.",
    #                 "duration": 60  # 1 hour in minutes
    #             }
    #         ],
    #         "description": "Your home, our priority.",
    #         "image": "https://placehold.co/600x400",
    #     },
    #     {
    #         "id": 4,
    #         "name": "EcoClean",
    #         "cleaningTypes": [
    #             {
    #                 "id": 7,
    #                 "type": "Window Cleaning",
    #                 "price": 80,
    #                 "rating": 4,
    #                 "reviews": 89,
    #                 "summary": "Eco-friendly window cleaning with natural products.",
    #                 "duration": 90  # 1.5 hours in minutes
    #             },
    #             {
    #                 "id": 8,
    #                 "type": "Bathroom Cleaning",
    #                 "price": 50,
    #                 "rating": 4,
    #                 "reviews": 89,
    #                 "summary": "Safe and sustainable bathroom cleaning.",
    #                 "duration": 60  # 1 hour in minutes
    #             }
    #         ],
    #         "description": "Green cleaning for your home.",
    #         "image": "https://placehold.co/600x400",
    #     },
    #     {
    #         "id": 5,
    #         "name": "Dust Busters",
    #         "cleaningTypes": [
    #             {
    #                 "id": 9,
    #                 "type": "House Cleaning",
    #                 "price": 110,
    #                 "rating": 4,
    #                 "reviews": 67,
    #                 "summary": "General house cleaning to maintain cleanliness.",
    #                 "duration": 150  # 2.5 hours in minutes
    #             },
    #             {
    #                 "id": 10,
    #                 "type": "Window Cleaning",
    #                 "price": 75,
    #                 "rating": 4,
    #                 "reviews": 67,
    #                 "summary": "Crystal clear window washing.",
    #                 "duration": 90  # 1.5 hours in minutes
    #             }
    #         ],
    #         "description": "We take care of the mess.",
    #         "image": "https://placehold.co/600x400",
    #     },
    #     {
    #         "id": 6,
    #         "name": "Pure Shine",
    #         "cleaningTypes": [
    #             {
    #                 "id": 11,
    #                 "type": "House Cleaning",
    #                 "price": 130,
    #                 "rating": 5,
    #                 "reviews": 123,
    #                 "summary": "Thorough home cleaning for a spotless living space.",
    #                 "duration": 180  # 3 hours in minutes
    #             },
    #             {
    #                 "id": 12,
    #                 "type": "Car Cleaning",
    #                 "price": 160,
    #                 "rating": 5,
    #                 "reviews": 123,
    #                 "summary": "Premium auto detailing for a brand-new look.",
    #                 "duration": 240  # 4 hours in minutes
    #             },
    #             {
    #                 "id": 13,
    #                 "type": "Bathroom Cleaning",
    #                 "price": 70,
    #                 "rating": 5,
    #                 "reviews": 123,
    #                 "summary": "High-standard cleaning for a fresh-smelling bathroom.",
    #                 "duration": 60  # 1 hour in minutes
    #             }
    #         ],
    #         "description": "Efficient and reliable cleaning services.",
    #         "image": "https://placehold.co/600x400",
    #     },
    #     {
    #         "id": 7,
    #         "name": "CleanSweep",
    #         "cleaningTypes": [
    #             {
    #                 "id": 14,
    #                 "type": "Bathroom Cleaning",
    #                 "price": 50,
    #                 "rating": 4,
    #                 "reviews": 91,
    #                 "summary": "Quick and effective cleaning for restrooms.",
    #                 "duration": 60  # 1 hour in minutes
    #             },
    #             {
    #                 "id": 15,
    #                 "type": "Window Cleaning",
    #                 "price": 70,
    #                 "rating": 4,
    #                 "reviews": 91,
    #                 "summary": "Professional-grade window cleaning service.",
    #                 "duration": 90  # 1.5 hours in minutes
    #             }
    #         ],
    #         "description": "We make cleaning easy.",
    #         "image": "https://placehold.co/600x400",
    #     }
    # ]

    # return jsonify({"servicesProvider": servicesProvider}), 200


@app.route("/api/getServicesById", methods=["GET"])
def get_serviceById():

    result = None

    try:

        service_id = request.args.get('service_id', type=int)
        cleaner_id = request.args.get('user_id', type=int)

        if isinstance(cleaner_id, int):

            pass
        elif isinstance(service_id, int):

            pass
        else:

            raise Exception("Invalid by_user_id was given.")

        if isinstance(cleaner_id, int) and service_id is None:
            service_list = sevice_controller.extract_service(
                user_id=cleaner_id)
        elif isinstance(service_id, int) and cleaner_id is None:
            service_list = sevice_controller.extract_service(
                service_id=service_id)

        if isinstance(service_list, list):

            pass

        else:

            raise Exception("Unable to get services.")

        # sorted_service_list = sevice_controller.sort_service(list_of_service=service_list)

        # if isinstance(sorted_service_list, list):

        #     pass

        # else:

        #     raise Exception("Unable to sort services by default type.")

        # temp_service_list = [service.model_dump(mode='json') for service in sorted_service_list]

        # result = jsonify({"services": temp_service_list}), 200
        result = jsonify({"services": service_list}), 200

    except Exception as e:

        result = jsonify({"error": str(e)}), 400

    finally:

        return result

    # add logic to get data by id

    # services = [{
    #     "id": 7,
    #     "name": "CleanSweep",
    #     "cleaningTypes": [
    #             {
    #                 "id": 14,
    #                 "type": "Bathroom Cleaning",
    #                 "price": 50,
    #                 "rating": 4,
    #                 "reviews": 91,
    #                 "summary": "Quick and effective cleaning for restrooms.",
    #                 "duration": 60
    #             },
    #         {
    #                 "id": 15,
    #                 "type": "Window Cleaning",
    #                 "price": 70,
    #                 "rating": 4,
    #                 "reviews": 91,
    #                 "summary": "Professional-grade window cleaning service.",
    #                 "duration": 90
    #             },{
    #                 "id": 16,
    #                 "type": "Bathroom Cleaning",
    #                 "price": 50,
    #                 "rating": 4,
    #                 "reviews": 91,
    #                 "summary": "Quick and effective cleaning for restrooms.",
    #                 "duration": 60
    #             },
    #         {
    #                 "id": 17,
    #                 "type": "Window Cleaning",
    #                 "price": 70,
    #                 "rating": 4,
    #                 "reviews": 91,
    #                 "summary": "Professional-grade window cleaning service.",
    #                 "duration": 90
    #             }
    #     ],
    #     "description": "We make cleaning easy.",
    #     "image": "https://placehold.co/600x400",
    # }]
    # if service_provider_id is None:
    #     return jsonify({"error": "Missing service ID"}), 400
    # if not services:
    #     return jsonify({"error": "Service not found"}), 404
    # return jsonify({"services": services})


@app.route("/api/getAllReviewsById", methods=["GET"])
def get_reviews():
    result = None

    try:
        service_id = request.args.get('service_id', type=int)

        if not isinstance(service_id, int):
            raise Exception("Invalid value for service id.")

        review_list = review_controller.extract_review(service_id=service_id)

        if not isinstance(review_list, list):
            raise Exception("Unable to find review for service.")

        if len(review_list) == 0:
            result = jsonify({"message": "No reviews found."}), 200
        else:
            temp_review_list = [review.model_dump(mode='json') for review in review_list]
            result = jsonify({"reviews": temp_review_list}), 200

    except Exception as e:
        result = jsonify({"error": str(e)}), 400

    finally:
        return result


    # reviews = [
    #     {
    #         "id": 1,
    #         "serviceId": 1,
    #         "name": "Alice",
    #         "rating": 5,
    #         "review": "Excellent service!",
    #         "date": "2023-10-01",
    #     }, {
    #         "id": 2,
    #         "serviceId": 1,
    #         "name": "alicia",
    #         "rating": 3,
    #         "review": "moderate service!",
    #         "date": "2023-10-01",
    #     }, {
    #         "id": 3,
    #         "serviceId": 1,
    #         "name": "coconut",
    #         "rating": 3,
    #         "review": "moderate service!",
    #         "date": "2023-10-01",
    #     }, {
    #         "id": 4,
    #         "serviceId": 1,
    #         "name": "apple",
    #         "rating": 3,
    #         "review": "moderate service!",
    #         "date": "2023-10-01",
    #     }, {
    #         "id": 5,
    #         "serviceId": 1,
    #         "name": "orange",
    #         "rating": 3,
    #         "review": "moderate service!",
    #         "date": "2023-10-01",
    #     }]
    # return jsonify({"reviews": reviews}), 200


if __name__ == "__main__":
    app.run()
