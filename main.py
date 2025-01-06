import json
from dangerous import DangerParser
from country import CountryParser
from dataAndTime import DataAndTimeParser

def main():
    dangerParser = DangerParser()
    countryParser = CountryParser()
    timeParser = DataAndTimeParser()

    while True:
        try:
            log_line = input()  # Here comes some logs
            log = json.loads(log_line)  # ????
            dangerParser.parse(log)
            countryParser.parse(log)
            timeParser.parse(log)
        except Exception as e:
            print(f"Error processing log: {e}")

if __name__ == "__main__":
    main()
