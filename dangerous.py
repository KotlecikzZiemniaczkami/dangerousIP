# checks reputation

import re
import requests
import psycopg2
from psycopg2 import sql

class DangerParser:
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
                self.API_key=posw[5]
            self.cursor = self.connection.cursor()
        except Exception:
            print('error during conncting')

    def parse(self, log):
        message = log.get('MESSAGE', '')
        pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        match = pattern.search(message)
        ip = match[0]
        if ('Django Log' in message) and ip:
            url = f"https://api.abuseipdb.com/api/v2/check"
            headers = {
                'Accept': 'application/json',
                'Key': self.API_key
            }

            params = {
                'ipAddress': ip,
                'maxAgeInDays': 90
            }

            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                if data['data']['totalReports'] > 10:  #### how many times it occurred dangerous
                    try:
                        query = sql.SQL("""
                                       INSERT INTO potential
                                       VALUES (%s, %s);
                                   """)
                        self.cursor.execute(query, (ip, "DANGEROUS"))
                        self.connection.commit()

                    except Exception:
                        print('error during sending to database')

                elif data['data']['abuseConfidenceScore'] > 50:  #### how many times it occurred suspicious
                    try:
                        query = sql.SQL("""
                                       INSERT INTO potential
                                       VALUES (%s, %s);
                                   """)
                        self.cursor.execute(query, (ip, "SUSPICIOUS"))
                        self.connection.commit()

                    except Exception:
                        print('error during sending to database')
            else:
                print(f"ERROR: {response.status_code}")

    def __del__(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()
