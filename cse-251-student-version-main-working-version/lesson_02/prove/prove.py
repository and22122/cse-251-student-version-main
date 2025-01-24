"""
Course: CSE 251 
Lesson: L02 Prove
File:   prove.py
Author: Jalen Anderson
Self rating: 3-4 I did my best to meet the requirements despite several struggles.
Although the program may currently take too long to run, I did manage at one point
to bring its run time down significantly, from about 210 seconds to 94 or fewer
seconds.

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py" and leave it running.
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the description of the assignment.
  Note that the names are sorted.
- You are required to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a separate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}

Outline of API calls to server

1) Use TOP_API_URL to get the dictionary above
2) Add "6" to the end of the films endpoint to get film 6 details
3) Use as many threads possible to get the names of film 6 data (people, starships, ...)

"""

from datetime import datetime, timedelta
import requests
import json
import threading

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
    
    def run(self):
        self.response = requests.get(self.url)

        if self.response.status_code == 200:
            self.data = self.response.json()

            if self.do_print:
                print(self.data)
        else:
            print("The best laid code... gang aft agley.")
# TODO Add any functions you need here

def main():
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

    for i in range(len(film.data['characters'])):
        threads.append(Request_thread(film.data['characters'][i]))
        threads[i].start()
        threads[i].join()
        call_count += 1
    for i in range(len(threads)):
        threads[i] = threads[i].data['name']

    print(f"{", ".join(sorted(threads))}\n")

    
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
    main()