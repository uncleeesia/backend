import re

from argon2 import PasswordHasher
from logging import Logger
from datetime import datetime
from dbtalker_psql import DBTalker
from psycopg import sql
from models import General_user


class UserController:

    def __init__(self, DBTalker_Obj: DBTalker, Schema_Name: str):

        self.dbt = DBTalker_Obj
        self.schema = str.strip(Schema_Name)
        self.hash_setting = PasswordHasher(
            time_cost=1, memory_cost=64 * 1024, parallelism=4, hash_len=32, salt_len=10,)

    def create_user(self, user_details: dict) -> General_user | Exception:
        """"""

        result = None

        try:

            if user_details:

                pass

            else:

                raise Exception("Invalid or missing arguement.")

            # Insert a fake user id into user_details 1st to use Pydantic model validation
            pending_user = General_user.model_validate(user_details)

            sql_command = sql.SQL("""INSERT INTO {}.general_user (username, password, email, phone_number, address, is_cleaner, service_id_list, profile_description, picture_url, preferences) VALUES (%(username)s, %(password)s, %(email)s, %(phone_number)s, %(address)s, %(is_cleaner)s, %(service_id_list)s, %(profile_description)s, %(picture_url)s, %(preferences)s) RETURNING user_id, username, password, email, phone_number, address, is_cleaner, service_id_list, profile_description, picture_url""").format(sql.Identifier(self.schema))
            para = pending_user.model_dump()

            callToDB_result = self.dbt.callToDB(sql_command, para)

            if isinstance(callToDB_result, tuple):

                pass

            elif isinstance(callToDB_result, Exception):

                raise callToDB_result

            else:

                raise Exception("Unable to create user.")

            cols = (
                "user_id", "username", "password", "email",
                "phone_number", "address", "is_cleaner",
                "service_id_list", "profile_description",
                "picture_url", "preferences"
            )

            data = dict(zip(cols, callToDB_result))

            result = General_user.model_validate(data)

        except Exception as e:

            result = e

        finally:

            return result

    def extract_user(self, user_id: int | None = None, email: str | None = None, is_cleaner: bool | None = None, is_admin:bool | None = None) -> list[General_user] | Exception:
        """"""

        result = None

        try:

            # Arguement Check
            if user_id and user_id > 0:

                sql_command = sql.SQL("""SELECT user_id, username, password, email, phone_number, address, is_cleaner, service_id_list, profile_description, picture_url, preferences, is_blacklist, blacklist_reason FROM {}.general_user WHERE user_id = %s""").format(
                    sql.Identifier(self.schema))
                para = (user_id,)

            elif email:

                sql_command = sql.SQL("""SELECT user_id, username, password, email, phone_number, address, is_cleaner, service_id_list, profile_description, picture_url, preferences, is_blacklist, blacklist_reason FROM {}.general_user WHERE email = %s""").format(
                    sql.Identifier(self.schema))
                para = (email,)

            elif isinstance(is_cleaner, bool):

                sql_command = sql.SQL("""SELECT DISTINCT user_id, username, password, email, phone_number, address, is_cleaner, service_id_list, profile_description, u.picture_url, preferences, is_blacklist, blacklist_reason FROM {}.general_user u inner join {}.service s on u.user_id = s.by_user_id WHERE is_cleaner = %s""").format(
                    sql.Identifier(self.schema), sql.Identifier(self.schema))
                para = (is_cleaner,)

            elif isinstance(is_admin, bool):
                sql_command = sql.SQL("""SELECT DISTINCT user_id, username, password, email, phone_number, address, is_cleaner, profile_description, picture_url, preferences, is_blacklist, blacklist_reason FROM {}.general_user""").format(
                    sql.Identifier(self.schema), sql.Identifier(self.schema))
                para = (is_admin,)
            else:

                raise Exception("Invalid or missing arguements.")

            callToDB_result = self.dbt.callToDB(sql_command, para)
            user_list = []

            # Database result processing
            if isinstance(callToDB_result, tuple) and callToDB_result:

                cols = (
                    "user_id", "username", "password", "email",
                    "phone_number", "address", "is_cleaner",
                    "service_id_list", "profile_description",
                    "picture_url", "preferences", "is_blacklist", "blacklist_reason"
                )

                data = dict(zip(cols, callToDB_result))

                user_list.append(General_user.model_validate(data))

            elif isinstance(callToDB_result, str) and callToDB_result == "":

                raise Exception("Unable to extract user.")

            elif isinstance(callToDB_result, list) and callToDB_result:

                for u in callToDB_result:

                    cols = (
                        "user_id", "username", "password", "email",
                        "phone_number", "address", "is_cleaner",
                        "service_id_list", "profile_description",
                        "picture_url", "preferences", "is_blacklist", "blacklist_reason"
                    )

                    data = dict(zip(cols, u))

                    user_list.append(General_user.model_validate(data))

            elif isinstance(callToDB_result, Exception):

                raise callToDB_result

            result = user_list

        except Exception as e:

            result = e

        finally:

            return result

    def update_user(self, user_obj: General_user) -> General_user | Exception:
        """"""

        result = None

        try:

            # Arguement Check
            if user_obj:

                pass

            else:

                raise Exception("Invalid or missing arguements")

            sql_command = sql.SQL("""UPDATE {}.general_user SET username=%(username)s, password=%(password)s, email=%(email)s, phone_number=%(phone_number)s, address=%(address)s, profile_description=%(profile_description)s, picture_url=%(picture_url)s, preferences=%(preferences)s WHERE user_id=%(user_id)s RETURNING user_id. username, password, email, phone_number, address, is_cleaner, service_id_list, profile_description, picture_url, preferences""").format(sql.Identifier(self.schema))
            para = user_obj.model_dump()

            callToDB_result = self.dbt.callToDB(sql_command, para)

            # Database result processing
            if isinstance(callToDB_result, tuple) and callToDB_result:

                pass

            elif isinstance(callToDB_result, str) and callToDB_result == "":

                raise Exception("Unable to update user.")

            elif isinstance(callToDB_result, Exception):

                raise callToDB_result

            cols = (
                "user_id", "username", "password", "email",
                "phone_number", "address", "is_cleaner",
                "service_id_list", "profile_description",
                "picture_url", "preferences"
            )

            data = dict(zip(cols, callToDB_result))

            result = General_user.model_validate(data)

        except Exception as e:

            result = e

        finally:

            return result

    def verify_login(self, raw_email: str, raw_password: str) -> General_user | Exception:
        """"""

        result = None

        try:

            # Arguement Check
            if raw_email and raw_password:

                pass

            else:

                raise Exception("Invalid or missing arguements.")

            user_data = self.extract_user(email=raw_email)

            # Result processing
            if isinstance(user_data, General_user):

                pass

            else:

                raise Exception("Unable to find user.")

            stored_pw = user_data.password

            is_match = self.hash_setting.verify(stored_pw, raw_password)

            if is_match and isinstance(is_match, bool):

                result = user_data

            else:

                raise Exception("Failed too verify login.")

        except Exception as e:

            result = e

        finally:

            return result

    def verify_registration(self, user_details: dict) -> dict | Exception:
        """"""

        result = None

        try:

            if user_details and len(user_details) > 0:

                pass

            else:

                raise Exception("Invalid or missing arguement.")

            unverified_username = str(user_details["username"])
            unverified_password = str(user_details["password"])
            unverified_email = str(user_details["email"])
            unverified_phone_number = str(user_details["phone_number"])

            email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            password_pattern = r"(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[^a-zA-Z0-9])"
            phone_number_pattern = r"^\+?[1-9]\d{1,14}$"
            username_pattern = r"[^a-zA-Z0-9]"

            # Check Username
            if bool(re.match(pattern=username_pattern, string=unverified_username)) and len(unverified_username) >= 5:

                pass

            else:

                raise Exception("Invalid input for field 'username'.")

            # Check password
            if bool(re.match(pattern=password_pattern, string=unverified_password)) and len(unverified_password) >= 8:

                pass

            else:

                raise Exception("Invalid input for field 'password'.")

            # Check email
            if bool(re.match(pattern=email_pattern, string=unverified_email)) and unverified_email.count("@") == 1:

                pass

            else:

                raise Exception("Invalid input for field 'email'.")

            # Check phone number
            if bool(re.match(pattern=phone_number_pattern, string=unverified_phone_number)):

                pass

            else:

                raise Exception("INvalid input for field 'phone_number'.")

            # Hash the password
            hash_password = self.hash_setting.hash(
                password=unverified_password)

            if isinstance(hash_password, str):

                user_details["password"] = hash_password

            else:

                raise Exception(hash_password)

            result = user_details

        except Exception as e:

            result = e

        finally:

            return result
