from faker import Faker
from argon2 import PasswordHasher
from models import General_user, Feedback, Payment, Review, Service
from dbtalker_psql import DBTalker
from psycopg import sql
from user_controller import UserController
from service_controller import ServiceController
from review_controller import ReviewController
from payment_controller import PaymentController
from datetime import datetime

import pytz
import json
import random

faker_seed = random.randint(123456, 1234567)

fake = Faker('')

fake.seed_instance(faker_seed)

schema_name = "csit314_schma"
api_key = "HRKU-4e9e0d78-2234-4999-8391-13e14ec05360"
hashbrown = PasswordHasher(time_cost=1,memory_cost=64 * 1024,parallelism=4,hash_len=32,salt_len=10,)

def create_fake_users():

    for x in range(10):

        username = fake.user_name()
        password = hashbrown.hash(password=fake.password(length=8))
        email = fake.email(safe=True)
        phone_num = "+6598125432"
        address = fake.address()
        is_cleaner = random.choice([True, False])
        service_id_list = []
        profile_description = fake.sentence(nb_words=10, variable_nb_words=False)
        picture_url = ""
        preferences = {"theme": "light"}

        user_dict = {
            "user_id": 0, 
            "username": username, 
            "password": password, 
            "email": email, 
            "phone_number": phone_num, 
            "address": address, 
            "is_cleaner": is_cleaner, 
            "service_id_list": service_id_list, 
            "profile_description": profile_description, 
            "picture_url": picture_url, 
            "preferences": preferences
            }

        dbt_obj = DBTalker(api_key=api_key)

        user_controller = UserController(dbt_obj, schema_name)

        user_controller.create_user(user_dict)

def create_fake_service():

    for _ in range(5):

        service_name = fake.sentence(nb_words=2, variable_nb_words=False)
        by_user_id = random.choice([1, 4, 6, 9, 10, 12, 13])
        price = "40.50"
        duration = "2 Hours"
        service_description = fake.sentence(nb_words=10, variable_nb_words=False)
        service_tags = [random.choice(["Deep Cleaning", "Window Cleaning", "Aircondition Cleaning", "Full Cleaning"])]
        picture_url = ["asd", "dsa", "asd"]
        tz = pytz.timezone("Asia/Kuala_Lumpur")
        listing_timestamp =  datetime.now(tz)

        service_dict = {
            "service_id": 0, 
            "service_name": service_name, 
            "by_user_id": by_user_id, 
            "price": price, 
            "duration": duration, 
            "service_description": service_description, 
            "service_tags": service_tags, 
            "picture_url": picture_url, 
            "listing_timestamp": listing_timestamp
            }

        dbt_obj = DBTalker(api_key=api_key)

        service_controller = ServiceController(dbt_obj, schema_name)

        service_controller.create_service(service_dict)

def create_fake_review():

    for i in range(0, 5):
            
            service_id_list = [2, 3, 4, 5, 6, 7]

            for  _ in range(5):

                review_id = 0
                review_score = random.randint(0, 10)
                review_text = fake.sentence(nb_words=10, variable_nb_words=False)
                user_id = random.choice([3, 5, 7, 8, 11])
                service_id = service_id_list[i]

                review_dict = {
                     "review_id": review_id,
                     "review_score": review_score,
                     "review_text": review_text,
                     "by_user_id": user_id,
                     "service_id": service_id
                }

                dbt_obj = DBTalker(api_key=api_key)

                review_controller = ReviewController(dbt_obj, schema_name)

                review_controller.create_review(review_dict)

def create_fake_payment():
     
     tz = pytz.timezone("Asia/Kuala_Lumpur")
     
     cleaner_ids = [13,9,4,12,9,10]
     
     for i in range(0, 5):
     
        for _ in range(5):
            
            payment_id = 0
            service_id = random.choice([2, 3, 4, 5, 6, 7])
            from_user_id = random.choice([3, 5, 7, 8, 11])
            to_user_id = cleaner_ids[i]
            price = "40.50"
            payment_timestamp =  datetime.now(tz)
            booking_timestamp = datetime.now(tz)

            payment_dict = {
                "payment_id": payment_id,
                "service_id": service_id,
                "from_user_id": from_user_id,
                "to_user_id": to_user_id,
                "price": price,
                "payment_timestamp": payment_timestamp,
                "booking_timestamp": booking_timestamp
            }

            dbt_obj = DBTalker(api_key=api_key)

            review_controller = PaymentController(dbt_obj, schema_name)

            review_controller.create_payment(payment_dict)