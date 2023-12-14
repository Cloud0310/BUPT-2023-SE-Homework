from flask import request
from flask import session
import threading
import time
from queue import Queue


def check_csrf_token(token):
    if token == session.get('csrf_token'):
        return True
    return False


def dispatch():
    pass


# Waiting for test
"""
def dispatch():
    # Create a queue to hold the tasks
    task_queue = Queue()
    
    # Add tasks to the queue
    task_queue.put(task1)
    task_queue.put(task2)
    task_queue.put(task3)
    # ...
    
    # Create worker threads to process the tasks
    num_workers = 4
    workers = []
    
    for _ in range(num_workers):
        worker = threading.Thread(target=process_task, args=(task_queue,))
        worker.start()
        workers.append(worker)
    
    # Wait for all tasks to be processed
    task_queue.join()
    
    # Stop the worker threads
    for worker in workers:
        worker.join()

# Function to process a task
def process_task(task_queue):
    while True:
        task = task_queue.get()
        
        # Process the task here
        
        task_queue.task_done()

"""