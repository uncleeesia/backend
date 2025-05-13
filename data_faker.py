from faker import Faker
from argon2 import PasswordHasher
from models import Gen_User, HomeOwner, Cleaner
from dbtalker_psql import DBTalker
from psycopg import sql

import random

faker_seed = 123456

fake = Faker('')

fake.seed_instance(faker_seed)

schema_name = "softwaredev_schema"
api_key = ""

def create_gen_user():

    for x in range(10):

        username = fake.user_name()
        email = fake.email(safe=True)
        password = PasswordHasher.hash(password=fake.password(length=8))
        phone_num = fake.phone_number()
        favourite_list = {}
        unstruct_data = {}
        picture_url = ""

        # If true homeowner else cleaner
        whoami = random.choice([True, False])

        # Cleaner stuff change according to frontend
        view_count = 0
        engagement_count = 0

        # Insert into General user

        sql_command = sql.SQL("""""").format(sql.Identifier(schema_name))
        para = ()

        dbt_obj = DBTalker(api_key=api_key)

        callToDB_result = dbt_obj.callToDB(sql_command, para)

        # Insert into Homeowner / Cleaner

        if whoami:

            sql_command = sql.SQL("""""").format(sql.Identifier(schema_name))
            para = ()

        else:

            sql_command = sql.SQL("""""").format(sql.Identifier(schema_name))
            para = ()

        callToDB_result = dbt_obj.callToDB(sql_command, para)