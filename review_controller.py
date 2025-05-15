from logging import Logger
from datetime import datetime
from dbtalker_psql import DBTalker
from psycopg import sql
from models import Review

class ReviewController():

    def __init__(self, DBTalker_Obj: DBTalker, Logger_Obj: Logger, Schema_Name: str):
        
        self.dbt = DBTalker_Obj
        self.logger = Logger_Obj
        self.schema = str.strip(Schema_Name)

    def extract_review(self, review_id: int | None, user_id: int | None, service_id: int | None):
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
            
            db_results = self.dbt.callToDB(sql_command, para)
            review_list = []

            # Database result processing
            if isinstance(db_results, tuple) and db_results:

                result = Review.model_validate(db_results)

            elif isinstance(db_results, list) and db_results:

                for s in db_results:

                    review_list.append(Review.model_validate(s))

                result = review_list

            elif isinstance(db_results, str) and db_results == "":

                raise Exception("Unable to find review.")
            
            elif isinstance(db_results, Exception):

                raise db_results

        except Exception as e:

            self.logger.error(e)

            result = e

        finally:

            return result

    def insert_review(self, review_details: Review):
        """"""

        result = None

        try:

            sql_command = sql.SQL("""INSERT INTO {}.review review_score review_score=%(review_score)s, review_text=%(review_text)s, by_user_id=%(by_user_id)s, service_id=%(service_id)s""").format(sql.Identifier(self.schema))
            para = review_details.model_dump()

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