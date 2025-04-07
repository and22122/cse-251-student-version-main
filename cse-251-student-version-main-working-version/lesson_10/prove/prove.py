"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: Jalen Anderson

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)

- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  

- Do not use try...except statements

- Display the numbers received by the reader printing them to the console.

- Create WRITERS writer processes

- Create READERS reader processes

- You can NOT use sleep() statements.

- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s), or lock(s) in the wrong
  place will slow down your code.

- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment

- Not allowed to use Queue(), Pipe(), List(), Barrier() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

- When each reader reads a value from the sharedList, use the following code to display
  the value:
  
                    print(<variable from the buffer>, end=', ', flush=True)

Add any comments for me:

"""

import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp

BUFFER_SIZE = 10
READERS = 2
WRITERS = 2

# Ouroboros = buffer + head, tail, values written, values read
#             buffer,   -4,   -3,        -2,            -1
def Writer(li, itemMax, emptySlots, filledSlots, lock):
    while True:
        head = li[-4]
        tail = li[-3]
        inserted = li[-2]

        if inserted >= itemMax:
            with lock:
                while (tail + 1) % BUFFER_SIZE != head:
                    li[tail] = -1
                    filledSlots.release()
                    tail = (tail + 1) % BUFFER_SIZE
                li[-3] = tail
            break

        emptySlots.acquire()

        with lock:
            if (tail + 1) % BUFFER_SIZE != head:
                li[-2] += 1
                li[tail] = inserted + 1
                li[-3] = (tail + 1) % BUFFER_SIZE
        
        filledSlots.release()

def Reader(li, itemMax, emptySlots, filledSlots, lock):
    while True:
        filledSlots.acquire()

        with lock:
            head = li[-4]

            if li[head] == -1:
                break
            
            value = li[head]
            
            print(value, end=', ', flush=True)
            li[-4] = (head + 1) % BUFFER_SIZE
            li[-1] += 1

        emptySlots.release()

def main():

    # This is the number of values that the writer will send to the reader
    items_to_send = random.randint(1000, 10000)

    smm = SharedMemoryManager()
    smm.start()

    # TODO - Create a ShareableList to be used between the processes
    #      - The buffer should be size 10 PLUS at least three other
    #        values (ie., [0] * (BUFFER_SIZE + 3)).  The extra values
    #        are used for the head and tail for the circular buffer.
    #        The another value is the current number that the writers
    #        need to send over the buffer.  This last value is shared
    #        between the writers.
    #        You can add another value to the sharedable list to keep
    #        track of the number of values received by the readers.
    #        (ie., [0] * (BUFFER_SIZE + 4))

    # Buffer + head, tail, values written, values read
    ouroboros = smm.ShareableList([0] * BUFFER_SIZE + [0, 0, 0, 0])

    # TODO - Create any lock(s) or semaphore(s) that you feel you need
    emptied = mp.Semaphore(BUFFER_SIZE)
    filled = mp.Semaphore(0)
    pad = mp.Lock()

    # TODO - create reader and writer processes
    processes = []
    for i in range(WRITERS):
        processes.append(mp.Process(target=Writer, args=(ouroboros, items_to_send, emptied, filled, pad)))
    for i in range(READERS):
        processes.append(mp.Process(target=Reader, args=(ouroboros, items_to_send, emptied, filled, pad)))
    # TODO - Start the processes and wait for them to finish

    for p in processes:
        p.start()
    
    for p in processes:
        p.join()

    print(f'{items_to_send} values sent')

    # TODO - Display the number of numbers/items received by the reader.
    #        Can not use "items_to_send", must be a value collected
    #        by the reader processes.
    # print(f'{<your variable>} values received')

    print(f'{ouroboros[-1]} values received')

    smm.shutdown()


if __name__ == '__main__':
    main()
