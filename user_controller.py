import json

from argon2 import PasswordHasher
from logging import Logger
from typing import Any
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from dbtalker_psql import DBTalker
from psycopg import sql

class Gen_User(BaseModel):

    user_id: int
    username: str
    email: str
    password: str
    phone_num: str
    notification_method: int = 1
    payment_method: int = 0
    hidden_count: int = 0
    removed_count: int = 0
    favourite_list: dict[str, Any] | None = None
    unstruct_data: dict[str, Any] | None = None

    @field_validator('username')
    def enforce_username(cls, v: str):

        if v.__len__ > 20 and v.__len__ < 5:

            raise Exception("The length of 'username' must be more than 5 and less than 20, please try again")
        
    @field_validator('password')
    def enforce_password(cls, v: str):

        if v.__len__ < 8 and v.__len__ > 20:

            raise Exception("The length of 'password' must be more than 8 and less than 20")
        
    @field_validator('phone_num')
    def enforce_phonenum(cls, v: str):

        if v.__len__ != 10:

            raise Exception("The length of 'phone_num' must be 10 characters")
    ##I got lazy :p

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

                raise Exception("Unable to find user")
            
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