import psycopg
import os
import heroku3

from psycopg import ProgrammingError

class DBTalker:
    """
    DBTalker class object version 1.4

    Use this class for executing sql queries to the database.

    Variable:

    - api_key: Your heroku api key. Accounts Settings -> *Scroll Down* API Key -> Copy and use value.
    """

    def __init__(self, api_key):

        heroku_apiKey = str.strip(api_key)

        try:

            self.connString = os.environ["DATABASE_URL"]

        except Exception:

            conn_heroku = heroku3.from_key(api_key=heroku_apiKey)
            app = conn_heroku.apps()["sim-assignment-csit314"]
            self.connString = app.config()["DATABASE_URL"]

    def callToDB(self, sqlCommand: str, para: set) -> tuple | list | str | Exception:
        """
        A generic function to communicate with the database. 
        The command and parameters will be wiped at the end of this function.

        **Parameters**

        - sqlCommand (str): The sql command that you want to execute.
        - para (set): The parameters that you need.
        
        **Returns**

        - result (tuple | list | str|  Exception)
        
        >>> tuple: The result of the query if the query only retrieves 1 row.
        >>> list: The result of the query if the query retrieves > 1 row.
        >>> str: The result of the query if the query retrieves 0 rows.
        >>> Exception: Any exceptions that may occur from the command or the connection.
        """

        result = None

        try: 

            ##This is the connection info that psycopg uses to connect to the postgres server
            conn = psycopg.connect(self.connString, autocommit=True)

            cursor = conn.cursor()

            cursor.execute(sqlCommand, para)

            if cursor.rowcount == 1:
                
                result = cursor.fetchall()[0] ##The result will be a tuple.

            elif cursor.rowcount <= 0:

                result = "" ##If the execute operation did not return a value, usually for UPDATE/INSERT commands without a returning statement.

            elif cursor.rowcount > 1:

                result = cursor.fetchall() ##The result will be return as a list containing 1 or more tuples.

            """Start of result processing"""
            if isinstance(result, ProgrammingError) and "didn't produce a result" in str(result): ##This occurs if the SELECT command does not retrieve any value/s.

                result = ""

            elif isinstance(result, Exception):

                raise result ##This is here to handle any Python Exception Class objects or any derivative.
            
            elif result is None: ##This is here just in case the code did not assign the value of cursor.fetchall() to result.

                raise Exception("Unknown error, no exception or result detected from the query") 

            else:

                pass
            """End of result processing"""

        except Exception as e:

            if isinstance(e, ProgrammingError) and "didn't produce a result" in str(e):

                result = ""

            else:

                result = e

        finally:

            conn.commit()

            cursor.close()
            conn.close()

            return result