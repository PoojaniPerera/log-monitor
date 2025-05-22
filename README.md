# log-monitor
A python based app to monitor job duration from log files and print alerts

## Description

This application parses a log file containing job start and end events, calculates job durations, and generates alerts based on how long each job takes.

### Features

- Parses CSV log files
- Tracks job duration from START to END
- Logs a:
  - **Warning** if a job exceeds 5 minutes
  - **Error** if a job exceeds 10 minutes
- Outputs both to `job_monitor.log` and a summary `report_<timestamp>.txt`

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
