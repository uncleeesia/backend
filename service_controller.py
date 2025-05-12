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

                sql_command = sql.SQL("""SELECT service_id, service_name, user_id, from_date, 
                to_date, view_count, engagement_count, category_tags, 
                picture_url FROM {}.service WHERE service_id = %s""").format(sql.Identifier(self.schema))
                para = (service_id,)

            if user_id:

                sql_command = sql.SQL("""SELECT service_id, service_name, user_id, from_date, 
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

            if service_obj and service_obj.service_id:

                pass

            else: 

                raise Exception("Invalid or Missing Arguement.")
            
            sql_command = sql.SQL("""UPDATE {}.service SET service_name = %(service_name)s, from_date = %(from_date)s, to_date = %(to_date)s, view_count = %(view_count)s, engagement_count = %(engagement_count)s, category_tags = %(category_tags)s, picture_url = %(picture_url)s WHERE service_id = %(service_id)s RETURNING service_id, service_name, user_id, from_date, to_date, view_count, engagement_count, category_tags, picture_url""").format(sql.Identifier(self.schema))
            para = service_obj.model_dump()

            db_results = self.dbt.callToDB(sql_command, para)

            # Database result processing
            if isinstance(db_results, tuple) and db_results:

                pass

            elif isinstance(db_results, str) and db_results == "":

                raise Exception("Unable to update service")
            
            elif isinstance(db_results, Exception):

                raise db_results
            
            result = Service.model_validate(db_results)

        except Exception as e:

            self.logger.error(e)

            result = e

        finally:

            return result
        
    def sort_service(self, list_of_service: list[Service], sorting_type: str) -> list | Exception:
        """"""

        result = None

        try:

            if list_of_service and list_of_service.__len__ > 0:

                pass

            else:

                raise Exception("Invalid or Missing Arguement.")
            
            if sorting_type and sorting_type.__len__ > 0:

                pass

            else:

                sorting_type = "popularity"

            for s in list_of_service:
            
                # Sort by engagement count
                if str.strip(str.lower(sorting_type)) == "popularity":

                    list_of_service.sort(key=Service.engagement_count, reverse=True)

                # Sort by from_date need to dicuss further
                elif str.strip(str.lower(sorting_type)) == "newest":

                    list_of_service.sort(key=Service.from_date, reverse=True)

                # Sort by name smallest
                elif str.strip(str.lower(sorting_type)) == "name_small":

                    list_of_service.sort(key=Service.service_name, reverse=False)

                # Sort by name biggest
                elif str.strip(str.lower(sorting_type)) == "name_small":

                    list_of_service.sort(key=Service.service_name, reverse=True)      

                # Sort by tags, need further discussion
                elif str.strip(str.lower(sorting_type)) == "tags":

                    pass

                continue

            result = list_of_service

        except Exception as e:

            self.logger.error(e)

            result = e

        finally:

            return result