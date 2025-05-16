from logging import Logger
from datetime import datetime
from dbtalker_psql import DBTalker
from psycopg import sql
from models import Feedback

class FeedbackController:

    def __init__(self, DBTalker_Obj: DBTalker, Logger_Obj: Logger, Schema_Name: str):
        
        self.dbt = DBTalker_Obj
        self.logger = Logger_Obj
        self.schema = str.strip(Schema_Name)

    def insert_feedback(self, feedback_detail: tuple):
        """"""

        result = None

        try:

            if feedback_detail and feedback_detail.__len__ > 0:

                pass

            else: 

                raise Exception("Invalid or Missing Arguement.")
            
            username = str.strip(str(feedback_detail[0]))
            phone_number = str.strip(str(feedback_detail[1]))
            feedback_text = str.strip(str(feedback_detail[2]))
            
            sql_command = sql.SQL("""INSERT INTO {}.feedback (username, phone_number, feedback_text) VALUES (%s, %s, %s) RETURNING feedback_id""").format(sql.Identifier(self.schema))
            para = (username, phone_number, feedback_text)

            callToDB_result = self.dbt.callToDB(sql_command, para)

            if isinstance(callToDB_result, tuple):

                pass

            elif isinstance(callToDB_result, Exception):

                raise callToDB_result
            
            else:

                raise Exception("Unable to create user.")
            
            result = True

        except Exception as e:

            self.logger.error(e)

            result = e

        finally:

            return result