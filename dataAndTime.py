# checks how many times ip tried to connect

import re
import psycopg2
from psycopg2 import sql

class DataAndTimeParser:
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
            self.cursor = self.connection.cursor()
        except Exception:
            print('error during conncting')

    def parse(self, log):
        message = log.get('MESSAGE', '')
        pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        match = pattern.search(message)
        ip = match[0]
        if ('Django Log' in message) and ip:
            try:
                query = sql.SQL("""
                    INSERT INTO ip_time
                    VALUES (%s, %s);
                """)

                self.cursor.execute(query, (ip, log.get('DATE', '')))
                self.connection.commit()

                query = sql.SQL("""
                                    SELECT COUNT(*) AS connection_count
                                    FROM ip_time
                                    WHERE date >= NOW() - INTERVAL '10 seconds' AND ip_addr = %s;
                                """)

                self.cursor.execute(query, (ip,))
                self.connection.commit()
                result = self.cursor.fetchone()

                if result[0] > 5:
                    query = sql.SQL("""
                                        INSERT INTO potential (ip_addr, time)
                                        VALUES (%s, %s);
                                    """)

                    self.cursor.execute(query, (ip, "probability of ongoing attack"))
                    self.connection.commit()

            except Exception:
                print('error during analyzing and adding')

    def __del__(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()
