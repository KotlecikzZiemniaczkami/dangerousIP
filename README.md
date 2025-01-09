# dangerousIP
This project is cumulated mechanism of collecting and analysing logs in client-server acrchitecture.  
It main purpose is to detect a dos attack aimed at the machine running the website https://github.com/KotlecikzZiemniaczkami/myLittleWebsite
## What this project contains
1. Parsers designed to work with syslog-ng (dataAndTime.py, dangerous.py and country.py),
2. program which is connecting parsers and syslog-ng (main.py),
3. syslog-ng configuration suggestions for client and for server (syslog-ng(client_side).conf, syslog-ng(server_side).conf)
4. postgreSQL queries to make proper database
5. file in which you should data needed to connect to Your Database and your key to abuseipdb.com API
   (credentials.txt-propositions of how the data might look like can be found in previous committees. Warning: they are fake and won't work)
7. app which connects to the database and generates raport in console based on data collected in the database (raport.py)
## Steps to run
### Warning: before using dangerousIP's You should have:
### 1.  re, psycopg2, geoip2.database, requests, json and pandas python libraries installed
### 2. https://www.maxmind.com/ account and their geolite country database downloaded
### 3. https://www.abuseipdb.com/ account and api key generated
Here are some steps how to run the project the way it was written for.
1. pull and reconfigure https://github.com/KotlecikzZiemniaczkami/myLittleWebsite
2. make a postgreSQL database on Your log server using queries from postgreSQL.txt
3. configure credential.txt with Your database and API data
4. run and configure syslog-ng on both machines as it was suggested
   (but after changing mentioned places-You need to change ip's, path's etc. Everything was mentioned in comments in the files)
5. reconfigure country.py-there is a path which You should change for Your path to geolite country database
### Congratulations-Now everything should be working fine
