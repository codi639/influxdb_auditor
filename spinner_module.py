# spinner_module.py
import sys
import time
import threading

# Spinner animation
def spinner_animation(message="Processing", stop_event=None):
    spinner = ['|', '/', '-', '\\']
    idx = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{message}... {spinner[idx % len(spinner)]}")
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)

def start_spinner(message="Processing"):
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=spinner_animation, args=(message, stop_event))
    spinner_thread.start()
    return stop_event, spinner_thread

def stop_spinner(stop_event, spinner_thread):
    stop_event.set()
    spinner_thread.join()
    sys.stdout.write("\r")  # Clear the spinner line

