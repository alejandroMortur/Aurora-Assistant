import multiprocessing
import time
import signal
import sys
import os

def log_writer(queue, log_file):
    
    """
    Function to write messages from a queue to a log file.
    
    Args:
    - queue (multiprocessing.Queue): The queue from which messages are read.
    - log_file (str): Path to the log file.
    """
    
    # Create the file if it does not exist
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            pass

    def flush_queue():
        """Function to flush all messages currently in the queue to the log file."""
        while not queue.empty():
            try:
                message = queue.get_nowait()
                with open(log_file, 'a') as f:
                    f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
            except queue.Empty:
                break

    # Continuously write messages from the queue to the log file
    with open(log_file, 'a') as f:
        while True:
            try:
                message = queue.get(timeout=1)  # Get message from queue, wait for 1 second
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")  # Write message to log file
                f.flush()  # Ensure that it is written immediately to the file
            except multiprocessing.queues.Empty:
                continue  # Continue if the queue is empty

def signal_handler(sig, frame):
    
    """
    Signal handler function to handle SIGINT signal (Ctrl+C).
    
    Args:
    - sig (int): Signal number.
    - frame (frame object): Current stack frame object.
    """
    
    global log_process
    
    print("---------------------------")
    print('Signal received, closing logger...')
    print("---------------------------")
    
    log_process.terminate()  # Terminate the logger process
    sys.exit(0)  # Exit the program

def start_logger(log_file):
    
    """
    Function to start the logger process.
    
    Args:
    - log_file (str): Path to the log file.
    
    Returns:
    - queue (multiprocessing.Queue): The queue used for communication with the logger process.
    - log_process (multiprocessing.Process): The logger process object.
    """
    
    queue = multiprocessing.Queue()  # Create a multiprocessing queue
    log_process = multiprocessing.Process(target=log_writer, args=(queue, log_file))  # Create logger process
    log_process.start()  # Start logger process

    # Configure signal handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)

    return queue, log_process