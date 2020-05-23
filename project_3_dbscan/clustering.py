"""
1 - Read whole db
2 - Select one object, see if its a core object
    - If it is, set as cluster and look for more objects belonging to that cluster
      by cheching all the neighbour objects (direct-density reachable) recursively 
      until we find borders.
3 - If object is not core, get next.
4 - If no more objects are left in db, we're done.
"""

import sys

print("hello")