# log-monitor
A python based script to monitor job duration from log files and generate report containing warning and error alerts

## Description

This application parses a log file containing job start and end events, calculates job durations, and generates alerts based on how long each job takes.

### Features

- Parses CSV log files
- Tracks job duration from START to END
- Logs a:
  - **Warning** if a job exceeds 5 minutes
  - **Error** if a job exceeds 10 minutes
- Outputs both to `job_monitor.log` and a report `report_<timestamp>.txt`

### Log Structure:
- HH:MM:SS is a timestamp in hours, minutes, and seconds.
- The job description.
- Each log entry is either the “START” or “END” of a process.
- Each job has a PID associated with it e.g., 46578.

## Usage

### Run with sample logs:

python log_monitor.py

#### Unit test command:
python -m unittest test_log_monitor.py


## Improvements
- command line argument to pass log file name
- log rotate mechanism for job_monitor log
- Add more unit tests
- More user friendly report structure
