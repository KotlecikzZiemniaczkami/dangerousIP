import json
from dangerous import DangerParser
from country import CountryParser
from dataAndTime import DataAndTimeParser
import sys

def validate_json(json_data):
    try:
        json.loads(json_data)
        return True
    except json.decoder.JSONDecodeError as e:
        print('Pronlem with Json')
        return False

def main():
    dangerParser = DangerParser()
    countryParser = CountryParser()
    timeParser = DataAndTimeParser()

    while True:
        try:
            log_line = sys.stdin.readline()  # Here comes some logs
            log_line = log_line.strip()
            #log_line = log_line.replace('"', '')
            #log_line = log_line.replace("'", '')
            if not validate_json(log_line):
                print(log_line)
                break
            log = json.loads(log_line)  # ????
            dangerParser.parse(log)
            countryParser.parse(log)
            timeParser.parse(log)
        except Exception as e:
            print(f"Error processing log: {e}: {log_line}")

if __name__ == "__main__":
    main()
