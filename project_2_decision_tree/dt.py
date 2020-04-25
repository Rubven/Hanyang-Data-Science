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


#Get header first, then read data and store in a list
def readFile(input_file_name):
    
    attributes = []
    data = []

    with open(input_file_name, 'r') as f:  
        attributes = f.readline().split()
        for line in f.read().split('\n'):
            if line != '':
                data.append(line.split('\t'))

    return attributes, data


#Select all the different attribues in a specific column (to get)
def get_unique_values(data, attribute_column):

    return set([different_values[attribute_column] for different_values in data])
    



def main():
    
    #Read data
    input_file = sys.argv[1]
    
    attributes, data = readFile(input_file)

    #Get all the different values for each column
    for i in range(len(attributes)):
        print(attributes[i])
        print(get_unique_values(data, i))
        print('\n')


if __name__ == '__main__':

    #Setting timer to print execution time
    startTime = time.time()
    main()
    print("\nExecution time: %ss\n" % (time.time() - startTime))