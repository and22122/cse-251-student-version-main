"""
Course: CSE 251 
Lesson: L07 Team
File:   team.py
Author: <Add name here>

Purpose: Retrieve Star Wars details from a server.

Instructions:

1) Make a copy of your lesson 2 prove assignment. Since you are  working in a team for this
   assignment, you can decide which assignment 2 program that you will use for the team activity.

2) You can continue to use the Request_Thread() class that makes the call to the server.

3) Convert the program to use a process pool that uses apply_async() with callback function(s) to
   retrieve data from the Star Wars website. Each request for data must be a apply_async() call;
   this means 1 url = 1 apply_async call, 94 urls = 94 apply_async calls.
"""
from datetime import datetime, timedelta
import requests
import json
import threading
import multiprocessing as mp

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = r'http://127.0.0.1:8790'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class Request_thread(threading.Thread):
   def __init__(self, url, print_data = False):
      threading.Thread.__init__(self)
      self.url = url
      self.response = None
      self.data = None
      self.do_print = print_data
   
   def run(self, key):
      self.response = requests.get(self.url)

      if self.response.status_code == 200:
         self.data = self.response.json()

         if self.do_print:
               print(self.data)
      else:
         print("The best laid code... gang aft agley.")
      
      return self.data[key]

def getData(url, key):
   response = requests.get(url)

   if response.status_code == 200:
      data = response.json()

      return data[key]
   else:
      print("The best laid code... gang aft agley. Please abort.")
# TODO Add any functions you need here

def main(n):
   call_count = 0

   log = Log(show_terminal=True)
   log.start_timer('Starting to retrieve data from the server')

   # TODO Retrieve Top API urls
   db = Request_thread(TOP_API_URL)

   db.start();
   db.join();

   call_count += 1

   # TODO Retrieve Details on film 6
   film = Request_thread(db.data['films'] + "6")

   film.start()
   film.join()

   call_count += 1
   
   print('-' * 40)
   print(f"Title   : {film.data['title']}")
   print(f"Director: {film.data['director']}")
   print(f"Producer: {film.data['producer']}")
   print(f"Released: {film.data['release_date']}\n")
   
   # TODO Display results
   print(f"Characters: {len(film.data['characters'])}")

   threads = []

   character_pool = mp.Pool(n);
   results = [character_pool.apply_async(getData, args=(film.data['characters'][i], 'characters')) for i in range(len(film.data['characters']))]
   outString = ""
   # for i in range(len(film.data['characters'])):
   #    threads.append(Request_thread(film.data['characters'][i]))
   #    threads[i].start()
   #    threads[i].join()
   #    call_count += 1
   for i in results:
      outString += i.data['name']

   print(f"{outString}\n")

   
   print(f"Planets: {len(film.data['planets'])}")

   threads = []
   for i in range(len(film.data['planets'])):
      threads.append(Request_thread(film.data['planets'][i]))
      threads[i].start()
      threads[i].join()
      call_count += 1
   for i in range(len(threads)):
      threads[i] = threads[i].data['name']
   
   print(f"{", ".join(sorted(threads))}\n")

   
   print(f"Starships: {len(film.data['starships'])}")

   threads = []
   for i in range(len(film.data['starships'])):
      threads.append(Request_thread(film.data['starships'][i]))
      threads[i].start()
      threads[i].join()
      call_count += 1
   for i in range(len(threads)):
      threads[i] = threads[i].data['name']
   
   print(f"{", ".join(sorted(threads))}\n")

   
   print(f"Vehicles: {len(film.data['vehicles'])}")

   threads = []
   for i in range(len(film.data['vehicles'])):
      threads.append(Request_thread(film.data['vehicles'][i]))
      threads[i].start()
      threads[i].join()
      call_count += 1
   for i in range(len(threads)):
      threads[i] = threads[i].data['name']
   
   print(f"{", ".join(sorted(threads))}\n")

   
   print(f"Species: {len(film.data['species'])}")

   threads = []
   for i in range(len(film.data['species'])):
      threads.append(Request_thread(film.data['species'][i]))
      threads[i].start()
      threads[i].join()
      call_count += 1
   for i in range(len(threads)):
      threads[i] = threads[i].data['name']
   
   print(f"{", ".join(sorted(threads))}\n")
   

   log.stop_timer('Total Time To complete')
   log.write(f'There were {call_count} calls to the server')

if __name__ == "__main__":
   main(1)