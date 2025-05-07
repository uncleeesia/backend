import json

from logging import Logger
from datetime import datetime
from dbtalker_psql import DBTalker
from psycopg import sql
from models import Service

class ServiceController:

    def __init__(self, DBTalker_Obj: DBTalker, Logger_Obj: Logger, Schema_Name: str):
        
        self.dbt = DBTalker_Obj
        self.logger = Logger_Obj
        self.schema = str.strip(Schema_Name)

    def extract_service(self, service_id: int | None, user_id: int | None) -> Service | list | Exception:
        """"""

        result = None

        try:

            if service_id:

                sql_command = sql.SQL("""SELECT service_id, user_id, from_date, 
                to_date, view_count, engagement_count, category_tags, 
                picture_url FROM {}.service WHERE service_id = %s""").format(sql.Identifier(self.schema))
                para = (service_id,)

            if user_id:

                sql_command = sql.SQL("""SELECT service_id, user_id, from_date, 
                to_date, view_count, engagement_count, category_tags, 
                picture_url FROM {}.service WHERE user_id = %s""").format(sql.Identifier(self.schema))
                para = (user_id,)

            db_results = self.dbt.callToDB(sql_command, para)
            service_list = []

            # Database result processing
            if isinstance(db_results, tuple) and db_results:

                result = Service.model_validate(db_results)

            elif isinstance(db_results, list) and db_results:

                for s in db_results:

                    service_list.append(Service.model_validate(s))

                result = service_list

            elif isinstance(db_results, str) and db_results == "":

                raise Exception("Unable to Find Service.")
            
            elif isinstance(db_results, Exception):

                raise db_results

        except Exception as e:

            self.logger.error(e)

            result = e

        finally:

            return result
        
    def update_service(self, service_obj: Service) -> Service | Exception:
        """"""

        result = None

        try:

            pass

        except Exception as e:

            self.logger.error(e)

            result = e

        finally:

            return result