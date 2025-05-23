from logging import Logger
from datetime import datetime
from dbtalker_psql import DBTalker
from psycopg import sql
from models import Payment, InputPayment
from models import PaymentReport
from models import PaymentMethod


class PaymentController():

    def __init__(self, DBTalker_Obj: DBTalker, Schema_Name: str):

        self.dbt = DBTalker_Obj
        self.schema = str.strip(Schema_Name)

    def create_payment(self, payment_details: dict) -> bool | Exception:
        try:
            print("Incoming payment_details:", payment_details)

            # Validate input with your Pydantic model (InputPayment)
            validated_input = InputPayment.model_validate(payment_details)
            print("Validated input:", validated_input)

            sql_command = sql.SQL("""
                INSERT INTO {}.payment (
                    service_id, from_user_id, to_user_id, price, payment_timestamp, booking_timestamp
                ) VALUES (
                    %(service_id)s, %(from_user_id)s, %(to_user_id)s, %(price)s, %(payment_timestamp)s, %(booking_timestamp)s
                )
                RETURNING payment_id, service_id, from_user_id, to_user_id, price, payment_timestamp, booking_timestamp;
            """).format(sql.Identifier(self.schema))

            # Use dict form of validated input for query parameters
            para = validated_input.model_dump()

            # Call DB and get inserted row back
            call_result = self.dbt.callToDB(sql_command, para)

            if isinstance(call_result, Exception):
                raise call_result

            if not call_result:
                raise Exception("Insert succeeded but no data was returned")

            # You can do further processing here if needed, e.g.:
            inserted_payment = dict(zip(
                ("payment_id", "service_id", "from_user_id", "to_user_id",
                "price", "payment_timestamp", "booking_timestamp"),
                call_result
            ))

            print("Inserted payment:", inserted_payment)

            return True

        except Exception as e:
            print("Create Payment Error:", e)
            return e

    def extract_payment(self, service_id: int | None = None, from_user_id: int | None = None, by_user_id: int | None = None) -> list[Payment] | Exception:
        """"""

        result = None

        try:

            if service_id:

                sql_command = sql.SQL("""SELECT payment_id, service_id, from_user_id, to_user_id, price, payment_timestamp, booking_timestamp FROM {}.payment WHERE service_id = %s""").format(
                    sql.Identifier(self.schema))
                para = (service_id,)

            elif from_user_id:

                sql_command = sql.SQL("""SELECT payment_id, service_id, from_user_id, to_user_id, price, payment_timestamp, booking_timestamp FROM {}.payment WHERE from_user_id = %s""").format(
                    sql.Identifier(self.schema))
                para = (from_user_id,)

            elif by_user_id:

                sql_command = sql.SQL("""SELECT payment_id, service_id, from_user_id, to_user_id, price, payment_timestamp, booking_timestamp FROM {}.payment WHERE to_user_id = %s""").format(
                    sql.Identifier(self.schema))
                para = (by_user_id,)

            else:

                raise Exception("Invalid or missing arguements.")

            callToDB_result = self.dbt.callToDB(sql_command, para)
            payment_list = []

            if isinstance(callToDB_result, tuple):

                cols = ("payment_id", "service_id", "from_user_id", "to_user_id",
                        "price", "payment_timestamp", "booking_timestamp")

                data = dict(zip(cols, callToDB_result))

                payment_list.append(Payment.model_validate(data))

            elif isinstance(callToDB_result, list):

                for p in callToDB_result:

                    cols = ("payment_id", "service_id", "from_user_id", "to_user_id",
                            "price", "payment_timestamp", "booking_timestamp")

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

    def extract_payment_method(self):
        """
        Extract all payment methods from the database
        """
        result = None

        try:
            sql_command = sql.SQL(
                "SELECT payment_method_id, payment_method_name, payment_method_icon FROM {}.paymentMethod"
            ).format(sql.Identifier(self.schema))

            callToDB_result = self.dbt.callToDB(sql_command, tuple())

            if isinstance(callToDB_result, list):
                # Map each row to PaymentMethod model
                result = [
                    PaymentMethod.model_validate(dict(zip(
                        ("payment_method_id", "payment_method_name",
                         "payment_method_icon"),
                        row)))
                    for row in callToDB_result
                ]

            elif isinstance(callToDB_result, Exception):
                raise callToDB_result

            elif isinstance(callToDB_result, str) and callToDB_result == "":
                raise Exception("Unable to find payment methods.")

            else:
                raise Exception("Unexpected response from database.")

        except Exception as e:
            result = e

        finally:
            return result
        
    def extract_payment_for_report(self, user_id: int | None = None) -> list[PaymentReport] | Exception:
            """"""

            result = None

            try:

                if user_id:

                    sql_command = sql.SQL("""SELECT     user_from.username, user_from.user_id, user_to.username, user_to.user_id,
                                                        s.service_id, s.service_tags, 
                                                        p.price, p.payment_timestamp, p.booking_timestamp
                                            FROM {}.payment p 
                                            INNER JOIN {}.service AS s ON s.service_id = p.service_id
                                            INNER JOIN {}.general_user AS user_from ON p.from_user_id = user_from.user_id
                                            INNER JOIN {}.general_user AS user_to ON p.to_user_id = user_to.user_id
                                            WHERE p.to_user_id = %s""").format(sql.Identifier(self.schema), sql.Identifier(self.schema), sql.Identifier(self.schema), sql.Identifier(self.schema))
                    para = (user_id,)

                else:

                    raise Exception("Invalid or missing arguements.")

                callToDB_result = self.dbt.callToDB(sql_command, para)
                payment_list = []

                if isinstance(callToDB_result, tuple):

                    cols = ("user_from_username", "user_from_user_id", "user_to_username", "user_to_user_id", "service_id", "service_tags",
                            "price", "payment_timestamp", "booking_timestamp")

                    data = dict(zip(cols, callToDB_result))

                    payment_list.append(PaymentReport.model_validate(data))

                elif isinstance(callToDB_result, list):

                    for p in callToDB_result:

                        cols = ("user_from_username", "user_from_user_id", "user_to_username", "user_to_user_id", "service_id", "service_tags",
                                "price", "payment_timestamp", "booking_timestamp", "review_score", "by_user_id")

                        data = dict(zip(cols, p))

                        payment_list.append(PaymentReport.model_validate(data))

                elif isinstance(callToDB_result, Exception):

                    raise callToDB_result

                elif isinstance(callToDB_result, str) and callToDB_result == "":

                    raise Exception("Unable to find payment.")

                result = payment_list

            except Exception as e:

                result = e

            finally:

                return result
