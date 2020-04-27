"""
PSEUDO-CODE from textbook:

(1) create a node N;
(2) if tuples in D are all of the same class, C, then
(3)     return N as a leaf node labeled with the class C;
(4) if attribute list is empty then
(5)     return N as a leaf node labeled with the majority class in D; // majority voting
(6) apply Attribute selection method(D, attribute list) to find the “best” splitting criterion;
(7) label node N with splitting criterion;
(8) if splitting attribute is discrete-valued and
        multiway splits allowed then // not restricted to binary trees
(9)     attribute list ← attribute list − splitting attribute; // remove splitting attribute
(10) for each outcome j of splitting criterion
        // partition the tuples and grow subtrees for each partition
(11)    let Dj be the set of data tuples in D satisfying outcome j; // a partition
(12)    if Dj is empty then
(13)        attach a leaf labeled with the majority class in D to node N;
(14)    else 
            attach the node returned by Generate decision tree(Dj, attribute list) to node N;
    endfor
(15) return N;

"""

"""
PLAN:
0 - Create Node class
1 - Read DB
2 - Identify different objects
3 - Find best question (metric)
4 - Split
5 - Repeat

"""

import sys
import time
import math

""" --- CLASSES --- """
# Node that holds a dictionary with a label and the number of times it appears in the dataset
class Leaf:
    def __init__(self, data):
        self.predictions = count_values(data)


# Decision node. Stores the attribute used for the partition and
# has references to the best partition branch (bpb) and the other branch (leftovers)
class Node:
    def __init__(self, attribute, bpb, leftovers):
        self.attribute = attribute
        self.best_partition_branch = bpb
        self.other_branch = leftovers


# Stores the column number for each attribute and the label
class Attribute:
    def __init__(self, column, value):
        self.column = column
        self.value = value

    def compare(self, target):
        return target[self.column] == self.value


""" --- I/O FUNCTIONS --- """
# Get header first, then read data and store in a list
def read_file(input_file_name):
    
    attributes = []
    data = []

    with open(input_file_name, 'r') as f:  
        attributes = f.readline().split()
        for line in f.read().split('\n'):
            if line != '':
                data.append(line.split('\t'))

    return attributes, data


""" --- ANALYZE DATA --- """
# Select all the different attribues in a specific column (to get)
def get_unique_values(data, attribute_column):

    return set([different_values[attribute_column] for different_values in data])


# Count the number of each attribute in the given data
def count_values(data):
    
    count = {}
    for row in data:
        # the attribute we want to track is in the last position always
        label = row[-1]
        if label not in count:
            count[label] = 0
        count[label] += 1
    return count


#Build the tree recursively
def build_decision_tree(data):

    # 1) Find best split - Calculate information gain for each attribute
    gain, attribute =  best_split(data)

    # 2) Divide into branches
    # 2.1) If no information gained, return leaf
    if gain == 0:
        return Leaf(data)

    # 2.2) Else, we divide the data
    best_partition_rows, other_rows = divide(data, attribute)

    # 3) Build branches recursively
    best_partition_branch = build_decision_tree(best_partition_rows)
    other_branch = build_decision_tree(other_rows)
    
    # 4) Return node with the branches
    return Node(attribute, best_partition_branch, other_branch)


# Divide the data based on the value of an attribute
def divide(data, attribute):
    match_rows, other_rows = [], []
    for row in data:
        if attribute.compare(row):
            match_rows.append(row)
        else:
            other_rows.append(row)
    return match_rows, other_rows


#Find best split trying to separate each attribute
def best_split(data):

    best_gain = 0
    best_question = None
    node_uncertainty = gini(data)
    n_cols = len(data[0]) - 1

    for column in range(n_cols):

        values = set([value[column] for value in data])

        for value in values:

            attribute = Attribute(column, value)

            #attemp to partition data
            best_split_rows, other_rows = divide(data, attribute)

            #Check if it actually divided the data
            if len(best_split_rows) == 0 or len(other_rows) == 0:
                continue

            #Calculate information gain with this split
            gain = information_gain(best_split_rows, other_rows, node_uncertainty)

            if gain > best_gain:
                best_gain, best_question = gain, attribute
    
    return best_gain, best_question


# Calculate information gain using Gini Impurity (Gini Index)
def information_gain(best_split_rows, other_rows, node_uncertainty):
    
    prob = float(len(best_split_rows)) / (len(other_rows) + len(best_split_rows))
    
    return node_uncertainty - prob * gini(best_split_rows) - (1-prob) * gini(other_rows) 


# Calculate gini impurity
def gini(data):
    
    values = count_values(data)
    impurity = 1
    for value in values:
        probability = values[value] /float(len(data))
        impurity -= probability**2

    return impurity


def classify(data, node):

    if isinstance(node, Leaf):
        return node.predictions

        if node.attribute.compare(data):
            return classify(data, node.best_partition_branch)
        else:
            return classify(data, node.other_branch)


""" --- MAIN --- """
def main():
    
    #Read data
    training_data_file = sys.argv[1]
    test_data_file = sys.argv[2]
    training_data_labels, training_data = read_file(training_data_file)
    test_data_labels, test_data = read_file(test_data_file)

    dt = build_decision_tree(training_data)





if __name__ == '__main__':

    #Setting timer to print execution time
    startTime = time.time()
    main()
    print("\nExecution time: %ss\n" % (time.time() - startTime))