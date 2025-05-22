import csv
from datetime import datetime, timedelta
from collections import defaultdict


WARNING_TIME_DELTA = timedelta(minutes=5)
ERROR_TIME_DELTA = timedelta(minutes=10)
job_tracking_dict = defaultdict(dict)

def read_logs_file(input_log_file):
    
    with open(input_log_file, newline='') as csvfile:
        log_reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        logs_line_list = [item for item in log_reader]
           
    return logs_line_list

def parse_logs(logs_line_list):
    
    for row in logs_line_list:
        timestamp, description, jobstatus , pid = [item.strip() for item in row]    
                      
        time = datetime.strptime(timestamp, "%H:%M:%S")
        evaluate_job_duration(time, description, jobstatus , pid)

def evaluate_job_duration(time, description, jobstatus , pid):

    if jobstatus == "START":                       
        job_tracking_dict[pid]['start'] = time
    elif jobstatus == "END":

        if "start" in job_tracking_dict[pid]:
            job_tracking_dict[pid]['end'] = time
            duration =  job_tracking_dict[pid]['end'] - job_tracking_dict[pid]['start']
            if  WARNING_TIME_DELTA <= duration <= ERROR_TIME_DELTA:
                print(f"WARNING : PID - {pid} Job {description} took {duration} seconds.Higher than warning Threashold!!")
            elif duration >  ERROR_TIME_DELTA:
                print(f"ERROR : PID - {pid} Job {description} took {duration} seconds.Higher than error Threashold!!")
            else:
                print(f"PID - {pid} Job {description} took {duration} seconds. Normal duration")

        else:
            print(f"no start job found for job {description} PID - {pid}")       
    else:
        print(f"invalid job status!")    



    





def main():
    input_log_file = "logs.log"
    logs_line_list = read_logs_file(input_log_file)
    parse_logs(logs_line_list)
    

if __name__ == '__main__':
    main()