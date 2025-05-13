import json

from argon2 import PasswordHasher
from logging import Logger
from datetime import datetime
from dbtalker_psql import DBTalker
from psycopg import sql
from models import Gen_User

class UserController:

    def __init__(self, DBTalker_Obj: DBTalker, Logger_Obj: Logger, Schema_Name: str):
        
        self.dbt = DBTalker_Obj
        self.logger = Logger_Obj
        self.schema = str.strip(Schema_Name)
        self.hash_setting = PasswordHasher(time_cost=1,memory_cost=64 * 1024,parallelism=4,hash_len=32,salt_len=10,)


    def extract_user(self, user_id: int | None, email: str | None) -> Gen_User | Exception:
        """"""

        result = None

        try:

            # Arguement Check
            if user_id and user_id > 0:
                
                sql_command = sql.SQL("""SELECT user_id, username, email, password, phone_num, notification_method, 
                payment_method, hidden_count, removed_count, favourite_list, unstruct_data FROM {}.general_user
                WHERE user_id = %s""").format(sql.Identifier(self.schema))
                para = (user_id,)

            elif email:

                sql_command = sql.SQL("""SELECT user_id, username, email, password, phone_num, notification_method, 
                payment_method, hidden_count, removed_count, favourite_list, unstruct_data FROM {}.general_user
                WHERE email = %s""").format(sql.Identifier(self.schema))
                para = (email,)

            else:

                raise Exception("Invalid or Missing Arguement.")

            db_results = self.dbt.callToDB(sql_command, para)

            # Database result processing
            if isinstance(db_results, tuple) and db_results:

                pass

            elif isinstance(db_results, str) and db_results == "":

                raise Exception("Unable to Find User.")
            
            elif isinstance(db_results, Exception):

                raise db_results
            
            result = Gen_User.model_validate(db_results)
            
        except Exception as e:

            self.logger.error(e)

            result = e

        finally:

            return result
        
    def update_user(self, user_obj: Gen_User) -> Gen_User | Exception:
        """"""

        result = None

        try:

            # Arguement Check
            if user_obj:

                pass

            else:

                raise Exception("Invalid or Missing Arguement.")
            
            # This hurts T_T
            sql_command = sql.SQL("""UPDATE {}.general_user SET username=%(username)s, 
            email=%(email)s, password=%(password)s, 
            phone_num=%(phone_num)s, notification_method=%(notification_method)s, 
            payment_method=%(payment_method)s, hidden_count=%(hidden_count)s, 
            removed_count=%(removed_count)s, favourite_list=%(favourite_list)s, 
            unstruct_data=%(unstruct_data)s WHERE user_id=%(user_id)s 
            RETURNING user_id, username, email, password, phone_num, notification_method, 
            payment_method, hidden_count, removed_count, favourite_list, unstruct_data
            """).format(sql.Identifier(self.schema))
            para = user_obj.model_dump()

            db_results = self.dbt.callToDB(sql_command, para)

            # Database result processing
            if isinstance(db_results, tuple) and db_results:

                pass

            elif isinstance(db_results, str) and db_results == "":

                raise Exception("Unable to update user")
            
            elif isinstance(db_results, Exception):

                raise db_results
            
            result = Gen_User.model_validate(db_results)

        except Exception as e:

            self.logger.error(e)

            result = e

        finally:

            return result
        
    def verify_login(self, raw_email: str, raw_password: str) -> bool | Exception:
        """"""

        result = None

        try:

            # Arguement Check
            if raw_email and raw_password:

                user_data = self.extract_user(email=raw_email)
            
            else:

                raise Exception("Invalid or Missing Arguement.")
            
            # Result processing
            if isinstance(user_data, Gen_User):

                pass

            else:

                raise Exception("Unable to Find User")
            
            stored_pw = user_data.password

            is_match = self.hash_setting.verify(stored_pw, raw_password)

            if is_match and isinstance(is_match, bool):

                result = True

            elif not is_match and isinstance(is_match, bool):

                result = False

            else:

                raise Exception("Failed to Verify Login")

        except Exception as e:

            self.logger.error(e)

            result = e

        finally:

            return result
        
    def create_account(self, user_details: tuple):
        """"""

        result = None

        try:

            if user_details and user_details.__len__ > 0:

                pass

            else:

                raise Exception("Invalid or Missing Arguement.")
            
            verification_result = self.verify_user_details(user_details)

            if isinstance(verification_result, bool) and verification_result:

                pending_user = Gen_User.model_validate(user_details)

            elif isinstance(verification_result, bool) and not verification_result:

                raise Exception("Failed To Verify User Details.")

            else:

                raise Exception("Failed To Create User Account.")
            
            sql_command = sql.SQL("""""").format(sql.Identifier(self.schema))
            para = (pending_user)

            callToDB_result = self.dbt.callToDB(sql_command, para)

            if isinstance(callToDB_result, tuple):

                pass

            elif isinstance(callToDB_result, Exception):

                raise callToDB_result
            
            else:

                raise Exception("Unable To Create User.")
            
            result = Gen_User.model_validate(callToDB_result)

        except Exception as e:

            self.logger.error(e)

            result = e

        finally:

            return result

    def verify_user_details(self, user_details: tuple) -> bool | Exception:
        """"""

        # Vibe code here

        # Check email for naughty stuff like double @ symbols

        # Check phone_num for naughty stuff like double + symbols