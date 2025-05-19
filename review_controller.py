from logging import Logger
from datetime import datetime
from dbtalker_psql import DBTalker
from psycopg import sql
from models import Review, ReviewReport


class ReviewController():

    def __init__(self, DBTalker_Obj: DBTalker, Schema_Name: str):

        self.dbt = DBTalker_Obj
        self.schema = str.strip(Schema_Name)

    def extract_review(self, review_id: int | None = None, user_id: int | None = None, service_id: int | None = None) -> list[Review] | Exception:
        """"""

        result = None

        try:

            if review_id:

                sql_command = sql.SQL("SELECT review_id, review_score, review_text, by_user_id, service_id FROM {}.review WHERE review_id = %s").format(
                    sql.Identifier(self.schema))
                para = (review_id,)

            elif user_id:

                sql_command = sql.SQL("SELECT r.review_id, r.review_score, r.service_id FROM {}.review r INNER JOIN {}.service s ON s.service_id = r.service_id WHERE s.by_user_id = %s").format(
                    sql.Identifier(self.schema), sql.Identifier(self.schema))
                para = (user_id,)

            elif isinstance(service_id, (list, tuple)):
                placeholders = sql.SQL(', ').join(
                    sql.Placeholder() * len(service_id))
                sql_command = sql.SQL(
                    "SELECT username, review_id, review_score, review_text, by_user_id, service_id "
                    "FROM {}.review r INNER JOIN {}.general_user u ON u.user_id = r.by_user_id "
                    "WHERE service_id IN ({})"
                ).format(sql.Identifier(self.schema), sql.Identifier(self.schema), placeholders)
                para = tuple(service_id)

            elif isinstance(service_id, int):
                sql_command = sql.SQL(
                    "SELECT username, review_id, review_score, review_text, by_user_id, service_id "
                    "FROM {}.review r INNER JOIN {}.general_user u ON u.user_id = r.by_user_id "
                    "WHERE service_id = %s"
                ).format(sql.Identifier(self.schema), sql.Identifier(self.schema))
                para = (service_id,)

            else:

                raise Exception("Invalid or missing arguements.")

            callToDB_result = self.dbt.callToDB(sql_command, para)
            review_list = []

            # Database result processing
            if isinstance(callToDB_result, list) and user_id:
                cols = ("review_id", "review_score", "service_id")

                data = dict(zip(cols, callToDB_result))

                review_list.append(ReviewReport.model_validate(data))

            if isinstance(callToDB_result, tuple) and callToDB_result:

                cols = ("username", "review_id", "review_score",
                        "review_text", "by_user_id", "service_id")

                data = dict(zip(cols, callToDB_result))

                review_list.append(Review.model_validate(data))

            elif isinstance(callToDB_result, list) and callToDB_result:

                for s in callToDB_result:

                    cols = ("username", "review_id", "review_score",
                            "review_text", "by_user_id", "service_id")

                    data = dict(zip(cols, s))

                    review_list.append(Review.model_validate(data))

            elif isinstance(callToDB_result, str) and callToDB_result == "":

                raise Exception("Unable to find review.")

            elif isinstance(callToDB_result, Exception):

                raise callToDB_result

            result = review_list

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

            sql_command = sql.SQL("""INSERT INTO {}.review (review_score, review_text, by_user_id, service_id) VALUES (%(review_score)s, %(review_text)s, %(by_user_id)s, %(service_id)s) RETURNING review_id, review_score, review_text, by_user_id, service_id""").format(
                sql.Identifier(self.schema))
            para = pending_review.model_dump()

            callToDB_result = self.dbt.callToDB(sql_command, para)

            if isinstance(callToDB_result, tuple):

                pass

            elif isinstance(callToDB_result, Exception):

                raise callToDB_result

            else:

                raise Exception("Unable to create review.")

            cols = ("review_id", "review_score",
                    "review_text", "by_user_id", "service_id")

            data = dict(zip(cols, callToDB_result))

            result = Review.model_validate(data)

        except Exception as e:

            result = e

        finally:

            return result
