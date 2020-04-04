import sys
import time
import itertools


#ARG SETTINGS
minimumSupportPosition = 1
inputFilePosition = 2
outputFilePosition = 3
filePath = "../"


#Read transaction file and return the transactions as collections of integers
def readFile():

    #Each line is a transaction 
    #Each item is separated by a tab
    transactions = []
    with open(filePath + sys.argv[inputFilePosition], 'r') as f:
        for transaction in f.read().split('\n'):
            
            #a) If we want the items to be stored as strings (slower)
            #transactions.append(transaction.split('\t'))

            #b) If we want the items to be stored as integers and not strings (faster):
            transactions.append( [int(item) for item  in transaction.split('\t')])
    
    return transactions


#Writing the solution in the output file
def writeFile(FPList):

    #with open(filePath + sys.argv[outputFilePosition], 'w') as f:
        
        #Write the data
        print("\nWRITE FILE")


#Gets each different item in the database and returns a list of sets 
# (needs to be frozenset in order to be used as keys in other parts of the code)
# we need to add the individual items as lists of items
def generate_1_itemset_candidates(transactions):
    
    candidates = []
    for transaction in transactions:
        for item in transaction:
            if [item] not in candidates:
                candidates.append([item])
    candidates.sort()

    return list(map(frozenset, candidates))


#We compare each candidate with the database and return a list of the frequent ones
#We also take the chance to get the support of each new itemset
def prune(transactions, candidates, minSup):
    
    support_count = {}
    for transaction in transactions:
        for candidate in candidates:
            if candidate.issubset(transaction):
                if candidate not in support_count:
                    support_count[candidate] = 1
                else:
                    support_count[candidate] += 1
    
    lenTransactions = float(len(transactions))
    frequent_sets = []
    itemsets_support = {}
    
    for itemset in support_count:
        support = float("{:.2f}".format(support_count[itemset] / lenTransactions))
        if support >= minSup:
            frequent_sets.insert(0,itemset)
        itemsets_support[itemset] = support
    
    return frequent_sets, itemsets_support


#APRIORI
def apriori(transactions, minSup):

    #1 - Get frequent 1-itemsets
    candidates_1 = generate_1_itemset_candidates(transactions)
    
    #Reformat transactions from a list of lists of integers to a list of sets
    transactions_sets = list(map(set, transactions))
    
    #Get the first list of frequent 1-itemsets and their support
    frequent_patterns_1, itemsets_support = prune(transactions_sets, candidates_1, minSup)
    
    #Initialize list of solutions with the first patterns
    frequent_patterns = [frequent_patterns_1]

    #Set k=2 (k+1) to start looping until we run out of patterns
    k = 2


    print(frequent_patterns)
    return(frequent_patterns)


if __name__ == '__main__':

    #------SOME INPUT TESTING-------

    #Check we have the correct number of arguments
    if len(sys.argv) < 3:
        print("\nLess than three arguments\nExiting\n")
        sys.exit()

    #Check if the first argument is an integer
    elif not sys.argv[minimumSupportPosition].isdigit:
        print("First argument is not an integer\nExiting\n")
        sys.exit()

    elif int(sys.argv[minimumSupportPosition]) > 100 or int(sys.argv[minimumSupportPosition]) < 0:
        print("Minimum Support is not a percentage (0-100)\nExiting\n")
        sys.exit()

    #Triying to open Input files
    try:
        open(filePath + sys.argv[inputFilePosition])
    except Exception:
        print("Could not read input file\nExiting\n")
        sys.exit()
    
    #---END INPUT TESTING------


    #If nothing fails, we go to the main function
    #Time counter to show the execution time 
    startTime = time.time()
        
    #We set the minimum support in a 2 decimal format
    minSup = float("{:.2f}".format( int( sys.argv[minimumSupportPosition]) / 100))
    
    #We read the file and loads the transactions in the desired format
    transactions = readFile()

    #Main function
    writeFile( apriori( transactions, minSup))

    print("\nExecution time: %ss\n" % (time.time() - startTime))