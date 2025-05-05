import json

from typing import Any
from pydantic import BaseModel, Field
from datetime import datetime
from dbtalker_psql import DBTalker

class Gen_User(BaseModel):

    user_id: int
    username: str
    email: str
    password: str
    phone_num: int
    notification_method: int = 1
    payment_method: int = 0
    hidden_count: int = 0
    removed_count: int = 0
    favourite_list: dict[str, Any] | None = None
    unstruct_data: dict[str, Any] | None = None

class UserController:

    def __init__(self, DBTalker_Obj: DBTalker):
        
        self.dbt = DBTalker_Obj

    def extract_by_id(self, user_id: int) -> list | Exception:
        """"""

        result = None

        try:

            # Arguement Check
            if user_id and user_id > 0:
                
                pass

            else:

                raise Exception(f"Invalid or Missing Arguement. Name: user_id, ID: {user_id}")
            
            
        except Exception:

            pass

        finally:

            pass