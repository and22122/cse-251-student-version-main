"""
Course: CSE 251
Lesson Week: 11
File: team2.py
Author: Brother Comeau

Purpose: Team Activity 2: Queue, Stack

Instructions:

Part 1:
- Create classes for Queue_t and Stack_t that are thread safe.
- You can use the List() data structure in your classes.
- Once written, test them using multiple threads.

Part 2
- Create classes for Queue_p and Stack_p that are process safe.
- You can use the List() data structure in your classes.
- Once written, test them using multiple processes.

Queue methods:
    - constructor(<no arguments>)
    - size()
    - get()
    - put(item)

Stack methods:
    - constructor(<no arguments>)
    - push(item)
    - pop()

Steps:
1) write the Queue_t and test it with threads.
2) write the Queue_p and test it with processes.
3) Implement Stack_t and test it 
4) Implement Stack_p and test it 

Note: Testing means having lots of concurrency/parallelism happening.  Also
some methods for lists are thread safe - some are not.
"""

import time
import threading
import multiprocessing as mp

# -------------------------------------------------------------------
class Queue_t:
    def __init__(self):
        self.isAvailable = threading.Lock()
        self.items = []
    
    def size(self):
        with self.isAvailable:
            return len(self.items)
    
    def get(self, item):
        with self.isAvailable:
            if (self.size() > 0):
                    output = self.items[0]
                    self.items = self.items[1:]
                    return output
            else:
                print("You cannot use \"get(self, item)\" on an empty queue.")
                raise IndexError
    
    def put(self, item):
        with self.isAvailable:
            self.items.append(item)


# -------------------------------------------------------------------
class Stack_t:
    def __init__(self):
        self.isAvailable = threading.Lock()
        self.items = []
    
    def push(self, item):
        with self.isAvailable:
            self.items.append(item)
    
    def pop(self):
        with self.isAvailable:
            if len(self.items) > 0:
                    return self.items.pop()
            else:
                print("You cannot use \"pop()\" on an empty stack.")
                raise IndexError


# -------------------------------------------------------------------
class Queue_p:
    def __init__(self):
        self.isAvailable = mp.Lock()
        self.items = mp.Manager().list()
    
    def size(self):
        with self.isAvailable:
            return len(self.items)
    
    def get(self, item):
        with self.isAvailable:
            if (self.size() > 0):
                    output = self.items[0]
                    self.items = self.items[1:]
                    return output
            else:
                print("You cannot use \"get(self, item)\" on an empty queue.")
                raise IndexError
    
    def put(self, item):
        with self.isAvailable:
            self.items.append(item)


# -------------------------------------------------------------------
class Stack_p:
    def __init__(self):
        self.isAvailable = mp.Lock()
        self.items = mp.Manager().list()
    
    def push(self, item):
        with self.isAvailable:
            self.items.append(item)
    
    def pop(self):
        with self.isAvailable:
            if len(self.items) > 0:
                    return self.items.pop()
            else:
                print("You cannot use \"pop()\" on an empty stack.")
                raise IndexError

def tputter():
    counter = 0
    while counter < 


def main():
    tq = Queue_t()
    ts = Stack_t()
    pq = Queue_p()
    ps = Stack_p()


    pass


if __name__ == '__main__':
    main()
