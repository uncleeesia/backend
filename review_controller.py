from logging import Logger
from datetime import datetime
from dbtalker_psql import DBTalker
from psycopg import sql
from models import Review

class ReviewController():

    def __init__(self, DBTalker_Obj: DBTalker, Schema_Name: str):
        
        self.dbt = DBTalker_Obj
        self.schema = str.strip(Schema_Name)

    def extract_review(self, review_id: int | None, user_id: int | None, service_id: int | None) -> Review | list[Review] | Exception:
        """"""

        result = None

        try:

            if review_id:

                sql_command = sql.SQL("SELECT review_id, review_score, review_text, by_user_id, service_id FROM {}.review WHERE review_id = %s").format(sql.Identifier(self.schema))
                para = (review_id,)

            elif user_id:

                sql_command = sql.SQL("SELECT review_id, review_score, review_text, by_user_id, service_id FROM {}.review WHERE by_user_id = %s").format(sql.Identifier(self.schema))
                para = (user_id,)

            elif service_id:

                sql_command = sql.SQL("SELECT review_id, review_score, review_text, by_user_id, service_id FROM {}.review WHERE servic_id = %s").format(sql.Identifier(self.schema))
                para = (service_id,)

            else:

                raise Exception("Invalid or missing arguements.")
            
            callToDB_result = self.dbt.callToDB(sql_command, para)
            review_list = []

            # Database result processing
            if isinstance(callToDB_result, tuple) and callToDB_result:

                cols = ("review_id", "review_score", "review_text", "by_user_id", "service_id")

                data = dict(zip(cols, callToDB_result))
                
                result = Review.model_validate(data)

            elif isinstance(callToDB_result, list) and callToDB_result:

                for s in callToDB_result:

                    cols = ("review_id", "review_score", "review_text", "by_user_id", "service_id")

                    data = dict(zip(cols, callToDB_result))
                    
                    review_list.append(Review.model_validate(data))

                result = review_list

            elif isinstance(callToDB_result, str) and callToDB_result == "":

                raise Exception("Unable to find review.")
            
            elif isinstance(callToDB_result, Exception):

                raise callToDB_result

        except Exception as e:

            result = e

        finally:

            return result

    def create_review(self, review_details: dict) -> Review | Exception:
        """"""

        result = None

        try:

            if review_details:

                pass

            else:

                raise Exception("Invalid or missing arguements.")
            
            pending_review = Review.model_validate(review_details)

            sql_command = sql.SQL("""INSERT INTO {}.review (review_score, review_text, by_user_id, service_id) VALUES (%(review_score)s, %(review_text)s, %(by_user_id)s, %(service_id)s) RETURNING review_id, review_score, review_text, by_user_id, service_id""").format(sql.Identifier(self.schema))
            para = pending_review.model_dump()

            callToDB_result = self.dbt.callToDB(sql_command, para)

            if isinstance(callToDB_result, tuple):

                pass

            elif isinstance(callToDB_result, Exception):

                raise callToDB_result
            
            else:

                raise Exception("Unable to create review.")
            
            cols = ("review_id", "review_score", "review_text", "by_user_id", "service_id")

            data = dict(zip(cols, callToDB_result))
            
            result = Review.model_validate(data)

        except Exception as e:

            result = e

        finally:

            return result