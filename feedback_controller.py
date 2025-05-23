from logging import Logger
from datetime import datetime
from dbtalker_psql import DBTalker
from psycopg import sql
from models import Feedback, CreateFeedback


class FeedbackController:

    def __init__(self, DBTalker_Obj: DBTalker, Schema_Name: str):

        self.dbt = DBTalker_Obj
        self.schema = str.strip(Schema_Name)

    def create_feedback(self, feedback_detail: dict) -> Feedback | Exception:
        result = None
        try:
            if not feedback_detail:
                raise Exception("Invalid or Missing Argument.")

            pending_feedback = CreateFeedback.model_validate(feedback_detail)

            sql_command = sql.SQL("""
                INSERT INTO {}.feedback (username, phone_number, feedback_text)
                VALUES (%(username)s, %(phone_number)s, %(feedback_text)s)
                RETURNING feedback_id
            """).format(sql.Identifier(self.schema))

            para = pending_feedback.model_dump()
            callToDB_result = self.dbt.callToDB(sql_command, para)

            if isinstance(callToDB_result, tuple):
                result = True
            elif isinstance(callToDB_result, Exception):
                raise callToDB_result
            else:
                raise Exception("Unable to create feedback.")

        except Exception as e:
            result = e

        finally:
            return result
