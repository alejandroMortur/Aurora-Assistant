import multiprocessing
import time
import signal
import sys
import os

def log_writer(queue, log_file):
    # Create the file if it does not exist
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            pass

    def flush_queue():
        while not queue.empty():
            try:
                message = queue.get_nowait()
                with open(log_file, 'a') as f:
                    f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
            except queue.Empty:
                break

    with open(log_file, 'a') as f:
        while True:
            try:
                message = queue.get(timeout=1)
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
                f.flush()  # Ensure that it is written immediately to the file
            except multiprocessing.queues.Empty:
                continue

def signal_handler(sig, frame):
    global log_process
    print("---------------------------")
    print('Signal received, closing logger...')
    print("---------------------------")
    log_process.terminate()  # Terminate the logger process
    sys.exit(0)

def start_logger(log_file):
    queue = multiprocessing.Queue()
    log_process = multiprocessing.Process(target=log_writer, args=(queue, log_file))
    log_process.start()

    # Configure signal handler for SIGINT
    signal.signal(signal.SIGINT, signal_handler)

    return queue, log_process