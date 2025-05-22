import csv
from datetime import datetime, timedelta
from collections import defaultdict
import logging

logging.basicConfig(
    filename='job_monitor.log',
    filemode='a',  # Append to existing log file
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s : %(message)s',
    datefmt="%Y-%m-%d %H: %M: %S",
)

WARNING_TIME_DELTA = timedelta(minutes=5)
ERROR_TIME_DELTA = timedelta(minutes=10)
job_tracking_dict = defaultdict(dict)

def read_logs_file(input_log_file):
    
    with open(input_log_file, newline='') as csvfile:
        log_reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        logs_line_list = [item for item in log_reader]
           
    return logs_line_list

def parse_logs(logs_line_list):
    
    results = []
    for row in logs_line_list:
        timestamp, description, jobstatus , pid = [item.strip() for item in row]    
                      
        time = datetime.strptime(timestamp, "%H:%M:%S")
        line = evaluate_job_duration(time, description, jobstatus , pid)

        if line is not None:
            results.append(line)
    return results

def evaluate_job_duration(time, description, jobstatus , pid):

    line = None

    if jobstatus == "START":                       
        job_tracking_dict[pid]['start'] = time
        
        
    elif jobstatus == "END":

        if "start" in job_tracking_dict[pid]:
            job_tracking_dict[pid]['end'] = time
            duration =  job_tracking_dict[pid]['end'] - job_tracking_dict[pid]['start']
            if  WARNING_TIME_DELTA <= duration <= ERROR_TIME_DELTA:
                logging.warning(f"PID - {pid} Job {description} took {duration} seconds.Higher than warning Threashold!!")
                line = f"WARNING : PID - {pid} Job {description} took {duration} seconds.Higher than warning Threashold!!"
            elif duration >  ERROR_TIME_DELTA:
                logging.error(f"PID - {pid} Job {description} took {duration} seconds.Higher than error Threashold!!")
                line = f"ERROR : PID - {pid} Job {description} took {duration} seconds.Higher than error Threashold!!"
            else:
                logging.info(f"PID - {pid} Job {description} took {duration} seconds. Normal duration")

        else:
                logging.info(f"no start job found for job {description} PID - {pid}")
        
    else:
        logging.error(f"invalid job status!")    
    return line  


def generate_report(results, output_path='report.txt'):

    with open(output_path, 'w') as f:
        for line in results:
            f.write(line + '\n')


def main():
    input_log_file = "logs.log"
    logs_line_list = read_logs_file(input_log_file)
    warning_error_list = parse_logs(logs_line_list)
    generate_report(warning_error_list)
    
if __name__ == '__main__':
    main()