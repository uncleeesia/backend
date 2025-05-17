from logging import Logger
from datetime import datetime
from dbtalker_psql import DBTalker
from psycopg import sql
from models import Payment

class PaymentController():

    def __init__(self, DBTalker_Obj: DBTalker, Schema_Name: str):
        
        self.dbt = DBTalker_Obj
        self.schema = str.strip(Schema_Name)

    def create_payment(self, payment_details: dict) -> Payment | Exception:
        """"""

        result = None

        try:

            if payment_details:

                pass

            else:

                raise Exception("Invalid or missing arguements.")
            
            # Insert fake payment id to use model validate
            pending_payment = Payment.model_validate(payment_details)
            
            sql_command = sql.SQL("""INSERT INTO {}.payment (service_id, from_user_id, to_user_id, price, payment_timestamp, booking_timestamp) VALUES (%(service_id)s, %(from_user_id)s, %(to_user_id)s, %(price)s, %(payment_timestamp)s, %(booking_timestamp)s) RETURNING payment_id, service_id, from_user_id, to_user_id price, payment_timestamp, booking_timestamp""").format(sql.Identifier(self.schema))
            para = pending_payment.model_dump()

            callToDB_result = self.dbt.callToDB(sql_command, para)

            if isinstance(callToDB_result, tuple):

                pass

            elif isinstance(callToDB_result, Exception):

                raise callToDB_result
            
            else:

                raise Exception("Unable to create payment.")
            
            cols = ("payment_id", "service_id", "from_user_id", "to_user_id", "price", "payment_timestamp", "booking_timestamp")

            data = dict(zip(cols, callToDB_result))
            
            result = Payment.model_validate(data)

        except Exception as e:

            result = e

        finally:

            return result

    def extract_payment(self, service_id: int | None = None, from_user_id: int | None = None, by_user_id: int | None = None) -> list[Payment] | Exception:
        """"""

        result = None

        try:

            if service_id:

                sql_command = sql.SQL("""SELECT payment_id, service_id, from_user_id, to_user_id, price, payment_timestamp, booking_timestamp FROM {}.payment WHERE service_id = %s""").format(sql.Identifier(self.schema))
                para = (service_id,)

            elif from_user_id:

                sql_command = sql.SQL("""SELECT payment_id, service_id, from_user_id, to_user_id, price, payment_timestamp, booking_timestamp FROM {}.payment WHERE from_user_id = %s""").format(sql.Identifier(self.schema))
                para = (from_user_id,)

            elif by_user_id:

                sql_command = sql.SQL("""SELECT payment_id, service_id, from_user_id, to_user_id, price, payment_timestamp, booking_timestamp FROM {}.payment WHERE to_user_id = %s""").format(sql.Identifier(self.schema))
                para = (by_user_id,)

            else:

                raise Exception("Invalid or missing arguements.")
            
            callToDB_result = self.dbt.callToDB(sql_command, para)
            payment_list = []

            if isinstance(callToDB_result, tuple):

                cols = ("payment_id", "service_id", "from_user_id", "to_user_id", "price", "payment_timestamp", "booking_timestamp")

                data = dict(zip(cols, callToDB_result))
                
                payment_list.append(Payment.model_validate(data))

            elif isinstance(callToDB_result, list):

                for p in callToDB_result:

                    cols = ("payment_id", "service_id", "from_user_id", "to_user_id", "price", "payment_timestamp", "booking_timestamp")

                    data = dict(zip(cols, p))
                    
                    payment_list.append(Payment.model_validate(data))

            elif isinstance(callToDB_result, Exception):

                raise callToDB_result
            
            elif isinstance(callToDB_result, str) and callToDB_result == "":

                raise Exception("Unable to find payment.")
            
            result = payment_list

        except Exception as e:

            result = e

        finally:

            return result