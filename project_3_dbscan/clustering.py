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
import time
import math


""" --- I/O FUNCTIONS --- """
# Reads the file and stores the first value in each line as dictionary key (as an int)
# Sets the following 2 values as float values for that key
# Prepares the third value as an empty set, which will be filled with neighbours
def read_file(input_data_file):
  
  data = {}

  with open(input_data_file, 'r') as f:
    for line in f.read().split('\n'):
      if line != '':  
        object_id, coord = line.split('\t', 1)
        data[int(object_id)] = [float(value) for value in coord.split()]
        data[int(object_id)].append(set())

  return data


"""" --- ANALYZE DATA ---"""
# Stores which points are within the minimum radius for each point
def get_close_points(data, eps):

  # Used to reduce the number of operations from 8000^8000 to 8000!
  last_visited_point = 0
  for point_id in range(len(data)):
    for candidate_point in range(last_visited_point, len(data)):
      
      # If we don't know have the point already in the set, we check
      if candidate_point not in data[point_id][2]:  

        # Used for clarity, calculates pythagorean distance between points
        # distance = calculate_distance(data[point_id][:2], data[candidate_point][:2])
        distance = math.sqrt( ((data[candidate_point][0] - data[point_id][0])**2) + ((data[candidate_point][1]-data[point_id][1])**2))

        # If the two points are within distance, updates both sets
        if distance <= eps:
          data[point_id][2].add(candidate_point)
          data[candidate_point][2].add(point_id)

    last_visited_point += 1

  return data


# This function was used for clarity, but it slows the execution time a lot (double)
"""
#Calculates Pythagorean distance
def calculate_distance(point_1, point_2):
  x1 = point_1[0]
  y1 = point_1[1]
  x2 = point_2[0]
  y2 = point_2[1]

  x = (x2 - x1)
  y = (y2 - y1)

  distance = math.sqrt(x**2 + y**2)

  return distance
"""


# Checks the number of close points for each point and gets neighbours recursively
# until it finds borders. Then removes those points from the candidates list and
# checks next point until all candidates have been assigned to a cluster.
def get_clusters(data, min_pts, candidate_points):
  clusters = []
  



  return clusters


def main():

  input_data_file = sys.argv[1]
  n_clusters = int(sys.argv[2])
  eps = int(sys.argv[3])
  min_pts = int(sys.argv[4])

  # Dictionary with point_id as key, coordinates as values
  data = read_file(input_data_file)

  # Get close points for each point
  data = get_close_points(data, eps)

  # Get clusters
  candidate_points = [int(point_id) for point_id in range(len(data))]
  clusters = get_clusters(data, min_pts, candidate_points)

  print(data[0])


if __name__ == '__main__':

    # Setting timer to print execution time
    startTime = time.time()
    main()
    print("\nExecution time: %ss\n" % (time.time() - startTime))