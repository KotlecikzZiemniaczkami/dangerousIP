import pandas as pd
import psycopg2
from psycopg2 import sql

class Raport:
    def __init__(self):
        try:
            with open('credentials.txt', 'r') as cred:
                posw = [line.strip() for line in cred.readlines()]
                self.connection = psycopg2.connect(
                    dbname=posw[0],
                    user=posw[1],
                    password=posw[2],
                    host=posw[3],
                    port=posw[4]
                )
        except Exception:
            print('error during conncting')

    def generate_me_raport(self):
        try:
            query = """
                SELECT DISTINCT * FROM potential;
            """

            data = pd.read_sql_query(query, self.connection)

            print("INCIDENTS".center(40,'*'))
            print(data)


        except Exception:
            print('error during generating raport')

    def __del__(self):
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()
