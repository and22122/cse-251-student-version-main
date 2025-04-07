"""
Course: CSE 251, week 14
File: functions.py
Author: Jalen Anderson

Instructions:

Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU

Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04


Requesting a family from the server:
family_id = 6128784944
request = Request_thread(f'{TOP_API_URL}/family/{family_id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 6128784944, 
    'husband_id': 2367673859,        # use with the Person API
    'wife_id': 2373686152,           # use with the Person API
    'children': [2380738417, 2185423094, 2192483455]    # use with the Person API
}

Requesting an individual from the server:
person_id = 2373686152
request = Request_thread(f'{TOP_API_URL}/person/{person_id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 2373686152, 
    'name': 'Stella', 
    'birth': '9-3-1846', 
    'parent_id': 5428641880,   # use with the Family API
    'family_id': 6128784944    # use with the Family API
}

You will lose 10% if you don't detail your part 1 and part 2 code below

Describe how to speed up part 1

<Add your comments here> NOT SURE YET!
CHECK PREVIOUS WORK TO SEE HOW RECURSION WORKS WITH THREADS, THEN MAKE RECURSIVE FUNCTION INTO THREADED FUNCTION?


Describe how to speed up part 2

<Add your comments here> NOT SURE YET!
USE SHARED QUEUE TO KEEP TRACK OF PEOPLE?


Extra (Optional) 10% Bonus to speed up part 3

<Add your comments here> NOT SURE YET! MAYBE USE BARRIERS OR A POOL?

"""
from common import *
import queue

# -----------------------------------------------------------------------------
def depth_fs_pedigree(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement Depth first retrieval
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    # we use recursion to find each next generation, running through each family member's descendants before finishing each family member.

    # base case: family has no parents
    # response: add members of family to tree, return

    # return case: family has at least one parent
    # response: for each member of the family, call depth_fs_pedigree, and add member to the tree; then return

    # start by getting family information
    
    # request = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    # request.start()
    # request.join()
    request = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    request.start()
    request.join()

    family = request.get_response()

    for c in family['children']:
        # add child to tree
        ch_request = Request_thread(f'{TOP_API_URL}/person/{c}')
        ch_request.start()
        ch_request.join()

        child = ch_request.get_response()
        print(child['name'])

    if family['husband_id'] != None:
        hus_request = Request_thread(f'{TOP_API_URL}/person/{family['husband_id']}')
        hus_request.start()
        hus_request.join()

        husband = hus_request.get_response()

        print(f'father {husband['name']}')

        depth_fs_pedigree(husband['family_id'], tree)
    
    if family['wife_id'] != None:
        wife_request = Request_thread(f'{TOP_API_URL}/person/{family['wife_id']}')
        wife_request.start()
        wife_request.join()

        wife = wife_request.get_response()

        print (f'mother {wife['name']}')

        depth_fs_pedigree(wife['family_id'], tree)

    pass

# -----------------------------------------------------------------------------
def breadth_fs_pedigree(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    # Use a queue
    # Add the first person to the queue
    # the queue is used to iterate through family members before working through the next generation.
    """Until the queue is empty:
    1) add children to tree
    2) add parents to queue"""

    pass

# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    #      - Limit number of concurrent connections to the FS server to 5
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    pass