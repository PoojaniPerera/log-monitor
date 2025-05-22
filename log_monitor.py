import csv

def read_logs_file(input_log_file):
    with open(input_log_file, newline='') as csvfile:
        log_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')

        logs_object = [item for item in log_reader]
           
    return logs_object


def main():
    input_log_file = "logs.log"
    print(read_logs_file(input_log_file))
 

if __name__ == '__main__':
    main()