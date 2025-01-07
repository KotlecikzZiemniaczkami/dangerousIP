# Checks country

import re
import psycopg2
from psycopg2 import sql
import geoip2.database

class CountryParser:
    def __init__(self):
        self.banned_countries = ['Russia']
        try:
            with open('/home/ubuntumil/parsers/credentials.txt', 'r') as cred:
                posw = [line.strip() for line in cred.readlines()]
                self.connection = psycopg2.connect(
                    dbname=posw[0],
                    user=posw[1],
                    password=posw[2],
                    host=posw[3],
                    port=posw[4]
                )
            self.cursor = self.connection.cursor()
        except Exception as e:
            print('error during conncting:' + e)

    def parse(self, log):
        message = log.get('message', '')
        pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        match = pattern.search(message)
        ip = match[0]
        if ('Django Log' in message) and ip:
            reader = geoip2.database.Reader(
                "/home/ubuntumil/Downloads/GeoLite2-Country.mmdb")  ####### this is the place to put your database path
            try:
                try:
                    response = reader.country(ip)
                    country = response.country.name
                except Exception:
                    country = ""

                query = sql.SQL("""
                    INSERT INTO ip_country
                    VALUES (%s, %s);
                """)
                self.cursor.execute(query, (ip, country))
                self.connection.commit()

                if country in self.banned_countries:
                    query = sql.SQL("""
                                        INSERT INTO potential
                                        VALUES (%s, %s);
                                    """)

                    self.cursor.execute(query, (ip, "COUNTRY"))
                    self.connection.commit()
            except Exception:
                print('error during analyzing and adding')
            reader.close()

    def __del__(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()
