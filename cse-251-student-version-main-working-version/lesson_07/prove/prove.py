"""
Course: CSE 251 
Lesson: L07 Prove
File:   prove.py
Author: Jalen Anderson

Purpose: Process Task Files.

Instructions:

See Canvas for the full instructions for this assignment. You will need to complete the TODO comment
below before submitting this file:

Note: each of the 5 task functions need to return a string.  They should not print anything.

TODO:

The name task seems to be the only one that isn't number crunching, so I think it needs more cores.
That being said, I also tested with different pool sizes to see which turned out to be fastest.
Previous experience tells me that 3 cores is probably a good starting point parallel processing on my computer.

After testing, It seems that the fastest configuration was a pool size of 1 for every task.
That doesn't seem right to me, but those were the results I got.

Add your comments here on the pool sizes that you used for your assignment and why they were the best choices.
"""

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math 

# Include cse 251 common Python files - Dont change
from cse251 import *

# Constants - Don't change
TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# TODO: Change the pool sizes and explain your reasoning in the header comment

PRIME_POOL_SIZE = 1
WORD_POOL_SIZE  = 1
UPPER_POOL_SIZE = 1
SUM_POOL_SIZE   = 1
NAME_POOL_SIZE  = 1

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []

def is_prime(n: int):
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def task_prime(value):
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    pass


def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    pass


def task_upper(text):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    pass


def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of all numbers between start_value and end_value
        answer = {start_value:,} to {end_value:,} = {total:,}
    """
    pass


def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    pass


def main():
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create process pools
    pool1 = mp.Pool(PRIME_POOL_SIZE)
    pool2 = mp.Pool(WORD_POOL_SIZE)
    pool3 = mp.Pool(UPPER_POOL_SIZE)
    pool4 = mp.Pool(SUM_POOL_SIZE)
    pool5 = mp.Pool(NAME_POOL_SIZE)
    results1 = []
    results2 = []
    results3 = []
    results4 = []
    results5 = []
    output1 = []
    output2 = []
    output3 = []
    output4 = []
    output5 = []

    # TODO change the following if statements to start the pools
    
    count = 0
    task_files = glob.glob("tasks/*.task")
    for filename in task_files:
        # print()
        # print(filename)
        task = load_json_file(filename)
        print(task)
        count += 1
        task_type = task['task']
        if task_type == TYPE_PRIME:
            result_primes.append(pool1.apply_async(task_prime, args=(task['value'],)))
        elif task_type == TYPE_WORD:
            result_words.append(pool2.apply_async(task_word, args=(task['word'],)))
        elif task_type == TYPE_UPPER:
            result_upper.append(pool3.apply_async(task_upper, args=(task['text'])))
        elif task_type == TYPE_SUM:
            result_sums.append(pool4.apply_async(task_sum, args=(task['start'], task['end'])))
        elif task_type == TYPE_NAME:
            result_names.append(pool5.apply_async(task_name, args=(task['url'],)))
            task_name(task['url'])
        else:
            log.write(f'Error: unknown task type {task_type}')

    # TODO wait on the pools
    pool1.close()
    pool2.close()
    pool3.close()
    pool4.close()
    pool5.close()

    pool1.join()
    pool2.join()
    pool3.join()
    pool4.join()
    pool5.join()

    # DO NOT change any code below this line!
    #---------------------------------------------------------------------------
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Number of Primes tasks: {len(result_primes)}')
    log.write(f'Number of Words tasks: {len(result_words)}')
    log.write(f'Number of Uppercase tasks: {len(result_upper)}')
    log.write(f'Number of Sums tasks: {len(result_sums)}')
    log.write(f'Number of Names tasks: {len(result_names)}')
    log.stop_timer(f'Total time to process {count} tasks')


if __name__ == '__main__':
    main()