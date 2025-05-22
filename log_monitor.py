import csv
from datetime import datetime, timedelta
from collections import defaultdict
import logging
import sys

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

    #Read given csv log file and store data to a list
    try:
        with open(input_log_file, newline='') as csvfile:
            log_reader = csv.reader(csvfile, delimiter=',', quotechar='"')

            logs_line_list = [item for item in log_reader]
            return logs_line_list
           
    except FileNotFoundError:
        logging.exception(f"Log file logs.csv not found.")
        sys.exit(1)
    except Exception as e:
        logging.exception(f"An error occurred while processing the log file: {e}")
        sys.exit(1)
    

def parse_logs(logs_line_list):
    """
    Parses job logs from a CSV reader and evaluates their durations.
    Returns a list of warning/error lines for the report.
    """

    results = []
    for row in logs_line_list:

        if len(row) != 4:
            logging.warning(f"skipping as row contains invalid fields : {row}")
        else:
            timestamp, description, jobstatus , pid = [item.strip() for item in row]
                               
        try:
            time = datetime.strptime(timestamp, TIME_FORMAT)
            logging.info("invalid time format")
        except ValueError:
            logging.exception("invalid time format")
            continue
        line = evaluate_job_duration(time, description, jobstatus , pid)

        if line is not None:
            results.append(line)
    return results

def evaluate_job_duration(time, description, jobstatus , pid):
    """
    Tracks START/END jobs and logs warnings/errors if thresholds are breached.
    Returns a report line if the job exceeds warning or error thresholds.
    """

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
    """
    Writes the list of report lines to the given file path and generate report with WARNING and Error messages
    """

    try:
        with open(output_path, 'w') as f:
            for line in results:
                f.write(line + '\n')
    except Exception as e:
        logging.exception(f"An error occurred while generating the report: {e}")
        sys.exit(1)

def main():
    input_log_file = "logs.log"
    logs_line_list = read_logs_file(input_log_file)
    warning_error_list = parse_logs(logs_line_list)
    generate_report(warning_error_list)
    
if __name__ == '__main__':
    main()