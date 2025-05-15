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

    def extract_review():
        """"""

    def insert_review(self, review_details: Review):
        """"""

        result = None

        try:

            sql_command = sql.SQL("""INSERT INTO {}.review review_score""").format(sql.Identifier(self.schema))

        except Exception as e:

            self.logger.error(e)

            result = e

        finally:

            return result