from logging import Logger
from datetime import datetime
from dbtalker_psql import DBTalker
from psycopg import sql
from models import Service, Payment, Review
from review_controller import ReviewController
from payment_controller import PaymentController

class ServiceController:

    def __init__(self, DBTalker_Obj: DBTalker, Schema_Name: str):
        
        self.dbt = DBTalker_Obj
        self.schema = str.strip(Schema_Name)

    def extract_service(self, service_id: int | None, user_id: int | None) -> Service | list | Exception:
        """"""

        result = None

        try:

            if service_id:

                sql_command = sql.SQL("""SELECT service_id, service_name, by_user_id, price, duration, sercice_description, service_tags, picture_url, listing_timestamp FROM {}.service WHERE service_id = %s""").format(sql.Identifier(self.schema))
                para = (service_id,)

            elif user_id:

                sql_command = sql.SQL("""SELECT service_id, service_name, by_user_id, price, duration, sercice_description, service_tags, picture_url, listing_timestamp FROM {}.service WHERE by_user_id = %s""").format(sql.Identifier(self.schema))
                para = (user_id,)

            else:

                sql_command = sql.SQL("""SELECT service_id, service_name, by_user_id, price, duration, sercice_description, service_tags, picture_url, listing_timestamp FROM {}.service""").format(sql.Identifier(self.schema))
                para = ()

            callToDB_result = self.dbt.callToDB(sql_command, para)
            service_list = []

            # Database result processing
            if isinstance(callToDB_result, tuple) and callToDB_result:

                cols = ('service_id', 'service_name', 'by_user_id', 'price', 'duration', 'service_description', 'service_tags', 'picture_url', 'listing_timestamp')
                
                data = dict(zip(cols, callToDB_result))

                result = Service.model_validate(data)

            elif isinstance(callToDB_result, list) and callToDB_result:

                for s in callToDB_result:

                    cols = ('service_id', 'service_name', 'by_user_id', 'price', 'duration', 'service_description', 'service_tags', 'picture_url', 'listing_timestamp')
                    
                    data = dict(zip(cols, callToDB_result))

                    service_list.append(Service.model_validate(data))

                result = service_list

            elif isinstance(callToDB_result, str) and callToDB_result == "":

                raise Exception("Unable to find service.")
            
            elif isinstance(callToDB_result, Exception):

                raise callToDB_result

        except Exception as e:

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
            
            sql_command = sql.SQL("""UPDATE {}.service SET service_name=%(service_name)s, by_user_id=%(by_user_id)s, price=%(price)s, duration=%(duration)s, service_description=%(service_description)s, service_tags=%(service_tags)s, picture_url=%(picture_url)s, listing_timestamp=%(listing_timestamp)s WHERE service_id=%(service_id)s RETURNING service_id, service_name, by_user_id, price, duration, sercice_description, service_tags, picture_url, listing_timestamp""").format(sql.Identifier(self.schema))
            para = service_obj.model_dump()

            callToDB_result = self.dbt.callToDB(sql_command, para)

            # Database result processing
            if isinstance(callToDB_result, tuple) and callToDB_result:

                pass

            elif isinstance(callToDB_result, str) and callToDB_result == "":

                raise Exception("Unable to update service.")
            
            elif isinstance(callToDB_result, Exception):

                raise callToDB_result
            
            cols = ('service_id', 'service_name', 'by_user_id', 'price', 'duration', 'service_description', 'service_tags', 'picture_url', 'listing_timestamp')
            
            data = dict(zip(cols, callToDB_result))

            result = Service.model_validate(data)

        except Exception as e:
            
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

                # Call review controller here to get reviews
                review_controller = ReviewController(self.dbt, self.schema)
                
                service_reviews = review_controller.extract_review(service_id=s.service_id)

                # Call payment controller here to get payments
                payment_controller = PaymentController(self.dbt, self.schema)

                service_payments = payment_controller.extract_payment(service_id=s.service_id)
            
                # Sort by number of payment
                if str.strip(str.lower(sorting_type)) == "popularity":

                    most_popular = 0

                    if service_payments.__len__ >= most_popular:

                        list_of_service.insert(0, s)
                        most_popular = service_payments.__len__

                    else:

                        list_of_service.append(s)

                # Sort by listing timestamp
                elif str.strip(str.lower(sorting_type)) == "newest":

                    list_of_service.sort(key=lambda service: service.listing_timestamp, reverse=True)

                # Sort by name smallest
                elif str.strip(str.lower(sorting_type)) == "name_small":

                    list_of_service.sort(key=lambda service: service.service_name, reverse=False)

                # Sort by name biggest
                elif str.strip(str.lower(sorting_type)) == "name_big":

                    list_of_service.sort(key=lambda service: service.service_name, reverse=True)      

                # Sort by review score followed by number of reviews
                elif str.strip(str.lower(sorting_type)) == "rating":
                    
                    average_rating = 0
                    total_rating = 0

                    if isinstance(service_reviews, list):

                        for r in service_reviews:

                            total_rating += r.review_score

                    else:

                        total_rating = service_reviews.review_score

                    service_average_rating = total_rating / service_reviews.__len__

                    if service_average_rating >= average_rating:

                        list_of_service.insert(0, s)

                        average_rating = service_average_rating

                    else:

                        list_of_service.append(s)

                # Sort by price
                elif str.strip(str.lower(sorting_type)) == "price":

                    list_of_service.sort(key=lambda service: service.price, reverse=True)  

                continue

            result = list_of_service

        except Exception as e:

            result = e

        finally:

            return result
        
    def create_service(self, service_details: dict):
        """"""

        result = None

        try:

            if service_details:

                pass

            else:

                raise Exception("Invalid or missing arguements.")
            
            pending_service = Service.model_validate(service_details)

            sql_command = sql.SQL("""INSERT INTO {}.service (service_name, by_user_id, price, duration, service_description, service_tags, picture_url, listing_timestamp) VALUES (%(service_name)s, %(by_user_id)s, %(price)s, %(duration)s, %(service_description)s, %(service_tags)s, %(picture_url)s, %(listing_timestamp)s) RETURNING service_id, service_name, by_user_id, price, duration, service_description, service_tags, picture_url, listing_timestamp""").format(sql.Identifier(self.schema))
            para = pending_service.model_dump()

            callToDB_result = self.dbt.callToDB(sql_command, para)

            if isinstance(callToDB_result, tuple):

                pass

            elif isinstance(callToDB_result, Exception):

                raise callToDB_result
            
            else:

                raise Exception("Unable to create service.")
            
            cols = ('service_id', 'service_name', 'by_user_id', 'price', 'duration', 'service_description', 'service_tags', 'picture_url', 'listing_timestamp')
            
            data = dict(zip(cols, callToDB_result))

            result = Service.model_validate(data)

        except Exception as e:

            result = e

        finally:

            return result