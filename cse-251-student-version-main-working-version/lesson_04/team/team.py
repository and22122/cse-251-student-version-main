"""
Course: CSE 251 
Lesson: L04 Team Activity
File:   team.py
Author: <Add name here>

Purpose: Practice concepts of Queues, Locks, and Semaphores.

Instructions:

- Review instructions in Canvas.

Question:

- Is the Python Queue thread safe? (https://en.wikipedia.org/wiki/Thread_safety)
"""

import threading
import queue
import requests
import json

# Include cse 251 common Python files
from cse251 import *

RETRIEVE_THREADS = 1        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

def retrieve_thread(que, log):  # TODO add arguments
    """ Process values from the data_queue """

    while True:
        # TODO check to see if anything is in the queue
        result = que.get()

        if result == NO_MORE_VALUES:
            return
        else:
            response = requests.get(result)

            if response.status_code == 200:
                data = response.json()

                log.write(data['name'])
            else:
                print("You know by know... gang aft agley.")

        pass


def file_reader(que, log, filename): # TODO add arguments
    """ This thread reading the data file and places the values in the data_queue """

    # TODO Open the data file "urls.txt" and place items into a queue

    with open(filename) as file:
        for line in file:
            que.put(line.strip())

    log.write('finished reading file')

    # TODO signal the retrieve threads one more time that there are "no more values"
    for i in range(RETRIEVE_THREADS):
        que.put(NO_MORE_VALUES)

threads = []

def main():
    """ Main function """

    log = Log(show_terminal=True)

    # TODO create queue
    q = queue.Queue()
    # TODO create semaphore (if needed)

    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread need to do their job
    filereader = threading.Thread(target=file_reader, args=(q, log, 'urls.txt'))

    for i in range(RETRIEVE_THREADS):
        threads.append(threading.Thread(target=retrieve_thread, args=(q, log)))

    log.start_timer()

    # TODO Get them going - start the retrieve_threads first, then file_reader
    filereader.start()
    for i in range(RETRIEVE_THREADS):
        threads[i].start()

    # TODO Wait for them to finish - The order doesn't matter
    filereader.join()
    for i in range(RETRIEVE_THREADS):
        threads[i].join()

    log.stop_timer('Time to process all URLS')


if __name__ == '__main__':
    main()



