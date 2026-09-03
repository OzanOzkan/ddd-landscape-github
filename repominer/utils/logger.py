import multiprocessing
from datetime import datetime

# Prints message with the current time and process.
def print_with_timestamp(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    process_name = multiprocessing.current_process().name
    print(f"[{timestamp}] [{process_name}] {message}")