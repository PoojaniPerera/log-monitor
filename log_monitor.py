import csv
import datetime
from collections import defaultdict

TIME_FORMAT = ""

def read_logs_file(input_log_file):
    job_tracking_dict = defaultdict(dict)
    with open(input_log_file, newline='') as csvfile:
        log_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')

        logs_line_list = [item for item in log_reader]
           
    return logs_line_list

def parse_logs(logs_line_list):
    for row in logs_line_list:
        timestamp, description, jobstatus , pid = [item.strip() for item in row]                         
        time = datetime.strptime(timestamp, "%H: %M: %S")
        evaluate_job_duration(time, description, jobstatus , pid)

def evaluate_job_duration(time, description, jobstatus , pid):
    

    





def main():
    input_log_file = "logs.log"
    logs_line_list = read_logs_file(input_log_file)
    parse_logs(logs_line_list)
    

if __name__ == '__main__':
    main()