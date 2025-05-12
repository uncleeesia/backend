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

        result = None

        try:

            if feedback_detail and feedback_detail.__len__ > 0:

                pass

            else: 

                raise Exception("Invalid or Missing Arguement.")
            
            # I will get back to this
            sql_command = sql.SQL("""INSERT INTO {}.feedback ()""").format(sql.Identifier(self.schema))

        except Exception as e:

            self.logger.error(e)

            result = e

        finally:

            return result
        
    def extract_feedback(self, feedback_id: int | None, from_user_id: int | None, to_user_id: int | None, feedback_timestamp: datetime):
        """"""

        result = None

        try:

            if feedback_id and feedback_id > 0:

                sql_command = sql.SQL("""""").format(sql.Identifier(self.schema))
                para = (feedback_id,)


            elif from_user_id and from_user_id > 0:

                sql_command = sql.SQL("""""").format(sql.Identifier(self.schema))
                para = (from_user_id)

            elif to_user_id and to_user_id > 0:

                sql_command = sql.SQL("""""").format(sql.Identifier(self.schema))
                para = (to_user_id)

            elif feedback_timestamp and feedback_timestamp.year > 0:

                sql_command = sql.SQL("""""").format(sql.Identifier(self.schema))
                para = (feedback_timestamp)

        except Exception as e:

            self.logger.error(e)

            result = e

        finally:

            return result