import sys
import time
import math


# Global variable storing the data
data = {}


""" --- I/O FUNCTIONS --- """
# Reads the file and stores the first value in each line as dictionary key (as an int)
# Sets the following 2 values as float values for that key
# Prepares the third value as an empty set, which will be filled with neighbours
# Adds a fourth field, which will store to cluster it belongs to
def read_file(input_data_file):
  
  global data

  with open(input_data_file, 'r') as f:
    for line in f.read().split('\n'):
      if line != '':  
        object_id, coord = line.split('\t', 1)
        data[int(object_id)] = [float(value) for value in coord.split()]
        data[int(object_id)].append(set())
        data[int(object_id)].append(None)


def write_files(n_clusters, sorted_cluster_sets):

  input_file_name = sys.argv[1].replace('.txt','')

  for i in range(n_clusters):
    file_name = input_file_name + '_cluster_' + str(i) + '.txt'
    
    with open(file_name, 'w') as f:    
      for point in sorted_cluster_sets[i]:
        f.writelines(str(int(point)) + '\n')



""" --- HELPER FUNCTIONS --- """
# Sets recursion limit according to the db size
def set_recursion_limit():
  global data

  # Python's default recursion limit is not enough to handle big dbs)
  sys.setrecursionlimit(len(data))


# Calculates pythagorean distance between two 2-dimensional points
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



"""" --- DBSCAN ALGORITHM ---"""
# Stores which points are within the minimum radius for each point
def find_close_points(eps):

  global data

  # Used to reduce the number of operations from 8000^8000 to 8000!
  last_visited_point = 0
  for point_id in range(len(data)):
    for candidate_point in range(last_visited_point, len(data)):
      
      # If we don't know have the point already in the set, we check
      if candidate_point not in data[point_id][2]:  

        # Function used for clarity, but it slows the execution time a lot (double)
        # distance = calculate_distance(data[point_id][:2], data[candidate_point][:2])
        distance = math.sqrt( ((data[candidate_point][0] - data[point_id][0])**2) + ((data[candidate_point][1]-data[point_id][1])**2))

        # If the two points are within distance, updates both sets
        if distance <= eps:
          data[point_id][2].add(candidate_point)
          data[candidate_point][2].add(point_id)

    last_visited_point += 1


# Starts clustering, starting from a random point
def get_clusters(min_pts):

  global data
  cluster_sets = []

  # Initialize labels
  label_id = 0

  for point_id in range(len(data)):

    if data[point_id][3] == None:
      reachable_points = set()
      cluster_sets.append(get_density_reachable_points(point_id, min_pts, reachable_points, label_id))
      label_id += 1

  return cluster_sets


# Returns all the density-reachable points from one point
# Recursively looks for all direct-reachable points
def get_density_reachable_points(point_id, min_pts, reachable_points, label_id):

  global data

  # Each reachable point
  for neighbour in data[point_id][2]:
    if neighbour not in reachable_points:
      # Add it to the set of reachable points in the cluster and label it
      reachable_points.add(neighbour)
      data[neighbour][3] = label_id
      
      # If it's core, repeat
      if len(data[neighbour][2]) >= min_pts:
        reachable_points.union(get_density_reachable_points(neighbour, min_pts, reachable_points, label_id))

  return reachable_points



def main():

  input_data_file = sys.argv[1]
  n_clusters = int(sys.argv[2])
  eps = int(sys.argv[3])
  min_pts = int(sys.argv[4])

  # Dictionary with point_id as key, coordinates as values
  read_file(input_data_file)

  # Set the new recursion limit according to the data size
  set_recursion_limit()

  # Get close points for each point
  find_close_points(eps)

  # Get clusters
  cluster_sets = get_clusters(min_pts)

  # Sort clusters in descending length order (larger ones first)
  sorted_cluster_sets = sorted(cluster_sets, reverse=True,  key=len)

  # Print the N first clusters
  write_files(n_clusters, sorted_cluster_sets)


if __name__ == '__main__':

    # Setting timer to print execution time
    startTime = time.time()
    main()
    print("\nExecution time: %ss\n" % (time.time() - startTime))