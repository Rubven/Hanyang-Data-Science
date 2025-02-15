import sys
import time


""" --- CLASSES --- """
# Node that holds a dictionary with a label and the number of 
# times it appears in the dataset
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
    
    attributes, data = [], []

    with open(input_file_name, 'r') as f:  
        attributes = f.readline().split()
        for line in f.read().split('\n'):
            if line != '':
                data.append(line.split('\t'))

    return attributes, data


def write_file(output_file_name, labels, test_data, results):

    with open(output_file_name, 'w') as f:
        
        # Write labels
        for column in range(len(labels)):
            f.write(labels[column] + "\t")
        f.write("\n")

        # Write results
        for row in range(len(test_data)):
            test_data[row].append(results[row])
            
            for column in range(len(test_data[row])-1):
                f.write(test_data[row][column] + "\t")
            f.write(test_data[row][column +1] + "\n")
            


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
    # 2.1) If no information gained, return Leaf
    if gain == 0:
        return Leaf(data)

    # 2.2) Else, we divide the data
    best_partition_rows, other_rows = divide(data, attribute)

    # 3) Build branches recursively
    best_partition_branch = build_decision_tree(best_partition_rows)
    other_branch = build_decision_tree(other_rows)
    
    # 4) Return node with the branches
    return Node(attribute, best_partition_branch, other_branch)


# Find best split trying each attribute
def best_split(data):

    best_gain = 0
    best_attribute = None
    node_uncertainty = gini(data)
    n_cols = len(data[0]) - 1

    for column in range(n_cols):

        values = set([value[column] for value in data])
        for value in values:

            attribute = Attribute(column, value)

            # Attemp to partition data
            best_split_rows, other_rows = divide(data, attribute)

            # Check if it actually divided the data, else go next
            if len(best_split_rows) == 0 or len(other_rows) == 0:
                continue

            # Calculate information gain with this split
            gain = information_gain(best_split_rows, other_rows, node_uncertainty)

            # Using >= instead of > increases the ammount of correct answers
            if gain >= best_gain:
                best_gain, best_attribute = gain, attribute
    
    return best_gain, best_attribute


# Divide the data based on the value of an attribute
def divide(data, attribute):
    
    match_rows, other_rows = [], []
    for row in data:
        if attribute.compare(row):
            match_rows.append(row)
        else:
            other_rows.append(row)
    return match_rows, other_rows


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

    # Returns the key of the dictionary 
    # (could return the whole dic, but we don't need the count anymore)
    if isinstance(node, Leaf):
        #return node.predictions
        return max(node.predictions, key=node.predictions.get)

    if node.attribute.compare(data):
        return classify(data, node.best_partition_branch)
    else:
        return classify(data, node.other_branch)


""" --- MAIN --- """
def main():
    
    # Read data and store labels
    training_data_file = sys.argv[1]
    test_data_file = sys.argv[2]
    result_file = sys.argv[3]
    
    training_data_labels, training_data = read_file(training_data_file)
    test_data_labels, test_data = read_file(test_data_file)

    # Create tree using training data
    dt = build_decision_tree(training_data)

    # Get predictions for each row
    results = []
    for row in test_data:
        results.append(classify(row, dt))

    # Write output file
    write_file(result_file, training_data_labels, test_data, results)


if __name__ == '__main__':

    # Setting timer to print execution time
    startTime = time.time()
    main()
    print("\nExecution time: %ss\n" % (time.time() - startTime))