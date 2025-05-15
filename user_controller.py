import re

from argon2 import PasswordHasher
from logging import Logger
from datetime import datetime
from dbtalker_psql import DBTalker
from psycopg import sql
from models import General_user

class UserController:

    def __init__(self, DBTalker_Obj: DBTalker, Logger_Obj: Logger, Schema_Name: str):
        
        self.dbt = DBTalker_Obj
        self.logger = Logger_Obj
        self.schema = str.strip(Schema_Name)
        self.hash_setting = PasswordHasher(time_cost=1,memory_cost=64 * 1024,parallelism=4,hash_len=32,salt_len=10,)

    def create_user(self, user_details: dict):
        """"""

        result = None

        try:

            if user_details and user_details.__len__ > 0:

                pass

            else:

                raise Exception("Invalid or missing arguement.")
            
            # Insert a fake user id into user_details 1st to use Pydantic model validation
            pending_user = General_user.model_validate(user_details)
            
            sql_command = sql.SQL("""INSERT INTO {}.general_user (username, password, email, phone_number, address, is_cleaner, service_id_list, profile_description, picture_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING user_id, username, password, email, phone_number, address, is_cleaner, service_id_list, profile_description, picture_url""").format(sql.Identifier(self.schema))
            para = (pending_user,)

            callToDB_result = self.dbt.callToDB(sql_command, para)

            if isinstance(callToDB_result, tuple):

                pass

            elif isinstance(callToDB_result, Exception):

                raise callToDB_result
            
            else:

                raise Exception("Unable to create user.")
            
            result = General_user.model_validate(callToDB_result)

        except Exception as e:

            self.logger.error(e)

            result = e

        finally:

            return result

    def extract_user(self, user_id: int | None, email: str | None) -> General_user | Exception:
        """"""

        result = None

        try:

            # Arguement Check
            if user_id and user_id > 0:
                
                sql_command = sql.SQL("""SELECT user_id. username, password, email, phone_number, address, is_cleaner, service_id_list, profile_description, picture_url, preferences FROM {}.general_user WHERE user_id = %s""").format(sql.Identifier(self.schema))
                para = (user_id,)

            elif email:

                sql_command = sql.SQL("""SELECT user_id. username, password, email, phone_number, address, is_cleaner, service_id_list, profile_description, picture_url, preferences FROM {}.general_user WHERE email = %s""").format(sql.Identifier(self.schema))
                para = (email,)

            else:

                raise Exception("Invalid or missing arguements.")

            db_results = self.dbt.callToDB(sql_command, para)

            # Database result processing
            if isinstance(db_results, tuple) and db_results:

                pass

            elif isinstance(db_results, str) and db_results == "":

                raise Exception("Unable to extract user.")
            
            elif isinstance(db_results, Exception):

                raise db_results
            
            result = General_user.model_validate(db_results)
            
        except Exception as e:

            self.logger.error(e)

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

            db_results = self.dbt.callToDB(sql_command, para)

            # Database result processing
            if isinstance(db_results, tuple) and db_results:

                pass

            elif isinstance(db_results, str) and db_results == "":

                raise Exception("Unable to update user.")
            
            elif isinstance(db_results, Exception):

                raise db_results
            
            result = General_user.model_validate(db_results)

        except Exception as e:

            self.logger.error(e)

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

            self.logger.error(e)

            result = e

        finally:

            return result

    def verify_registration(self, user_details: dict) -> dict | Exception:
        """"""

        result = None

        try:

            if user_details and user_details.__len__ > 0:

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

            #Check Username
            if bool(re.match(pattern=username_pattern, string=unverified_username)) and unverified_username.__len__ >= 5:

                pass

            else:

                raise Exception("Invalid input for field 'username'.")

            # Check password
            if bool(re.match(pattern=password_pattern, string=unverified_password)) and unverified_password.__len__ >= 8:

                pass

            else:

                raise Exception("Invalid input for field 'password'.")

            # Check email
            if bool(re.match(pattern=email_pattern,string=unverified_email)) and unverified_email.count("@") == 1:

                pass

            else:

                raise Exception("Invalid input for field 'email'.")
            
            # Check phone number
            if bool(re.match(pattern=phone_number_pattern, string=unverified_phone_number)):

                pass

            else:

                raise Exception("INvalid input for field 'phone_number'.")
            
            # Hash the password
            hash_password = self.hash_setting.hash(password=unverified_password)

            if isinstance(hash_password, str):

                user_details["password"] = hash_password

            else:

                raise Exception(hash_password)
            
            result = user_details

        except Exception as e:

            self.logger.error(e)

            result = e

        finally:

            return result