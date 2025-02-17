"""
Course: CSE 251 
Lesson: L06 Prove
File:   prove.py
Author: <Jalen Anderson>

Purpose: Processing Plant

Instructions:

- Implement the necessary classes to allow gifts to be created.
"""

import random
import multiprocessing as mp
import os.path
import time
import datetime

# Include cse 251 common Python files - Don't change
from cse251 import *

CONTROL_FILENAME = 'settings.json'
BOXES_FILENAME   = 'boxes.txt'

# Settings constants
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
NUMBER_OF_MARBLES_IN_A_BAG = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables

class Bag():
    """ Bag of marbles - Don't change """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

class Gift():
    """
    Gift of a large marble and a bag of marbles - Don't change

    Parameters:
        large_marble (string): The name of the large marble for this gift.
        marbles (Bag): A completed bag of small marbles for this gift.
    """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'

class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda', 
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green', 
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green', 
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple', 
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue', 
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow', 
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink', 
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue', 
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, sleeptime, out, max_marbles, tracker):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.outPipe = out
        self.sleeptime = sleeptime
        self.max_marbles = max_marbles
        self.tracker = tracker

    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        while self.tracker.value <= self.max_marbles:
            self.outPipe.send(self.colors[random.randint(0, len(self.colors) - 1)])
            self.tracker.value += 1
            time.sleep(self.sleeptime)
        self.outPipe.send(-1)
        pass


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self, sleeptime, inp, out, bagsize):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.size = bagsize
        self.counter = 0
        self.bag = Bag()
        self.inPipe = inp
        self.outPipe = out
        self.sleeptime = sleeptime

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        while True:
            result = self.inPipe.receive()
            if result == -1:
                break
            elif self.counter == self.bag_size:
                self.outPipe .send(self.bag)
                self.bag = Bag()
                time.sleep(self.sleeptime)
            else {
                self.bag.add(self.inPipe.receive())
            }
        self.outPipe.send(-1)


class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'Big Joe', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, sleeptime, inp, out):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.sleeptime = sleeptime
        self.inPipe = inp
        self.outPipe = out

    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        while True:
            result = self.inPipe.receive()
            if result == -1:
                break
            else:
                largeMarble = self.marble_names[random.randint(0, len(self.marble_names))]
                self.outPipe.send(Gift(largeMarble, result))
                time.sleep(self.sleeptime)
        self.outPipe.send(-1)

class Wrapper(mp.Process):
    """ Takes created gifts and "wraps" them by placing them in the boxes file. """
    def __init__(self, sleeptime, inp, filename):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.sleeptime = sleeptime
        self.inPipe = inp
        self.filename = filename

    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''
        with open(self.filename, "w") as file:
            while True:
                result = self.inPipe.receive()
                if result == -1:
                    break
                else:
                    file.write(f"Created - {datetime.now().time()}: {str(result)}")
                    time.sleep(self.sleeptime)


def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')



def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count     = {settings[MARBLE_COUNT]}')
    log.write(f'Marble delay     = {settings[CREATOR_DELAY]}')
    log.write(f'Marbles in a bag = {settings[NUMBER_OF_MARBLES_IN_A_BAG]}') 
    log.write(f'Bagger delay     = {settings[BAGGER_DELAY]}')
    log.write(f'Assembler delay  = {settings[ASSEMBLER_DELAY]}')
    log.write(f'Wrapper delay    = {settings[WRAPPER_DELAY]}')

    # TODO: create Pipes between creator -> bagger -> assembler -> wrapper
    creator_pipe, bag_hopper = mp.Pipe()
    bag_pipe, assembler_hopper = mp.Pipe()
    assembler_pipe, wrapper_hopper = mp.Pipe()
    # TODO create variable to be used to count the number of gifts
    gift_counter = mp.Value('i', 0)

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')

    # TODO Create the processes (ie., classes above)
    creator = Marble_Creator(settings[CREATOR_DELAY], creator_pipe, settings[MARBLE_COUNT], gift_counter)
    bagger = Bagger(settings[BAGGER_DELAY], bag_hopper, bag_pipe, settings[NUMBER_OF_MARBLES_IN_A_BAG])
    assembler = Assembler(settings[ASSEMBLER_DELAY], assembler_hopper, assembler_pipe)
    wrapper = Wrapper(settings[WRAPPER_DELAY], wrapper_hopper, BOXES_FILENAME)

    log.write('Starting the processes')
    # TODO add code here
    creator.start()
    bagger.start()
    assembler.start()
    wrapper.start()

    log.write('Waiting for processes to finish')
    # TODO add code here
    creator.join()
    bagger.join()
    assembler.join()
    wrapper.join()

    display_final_boxes(BOXES_FILENAME, log)
    
    # TODO Log the number of gifts created.
    log.write(f"{gift_counter.value} gifts created.")

    log.stop_timer(f'Total time')




if __name__ == '__main__':
    main()
