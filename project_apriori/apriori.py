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
            
            #If we want the items to be stored as strings (slower)
            #transactions.append(transaction.split('\t'))

            #If we want the items to be stored as integers and not strings (faster):
            transactions.append( [int(item) for item  in transaction.split('\t')])
    
    return transactions


#Generate the dictionary containing all the different items and their support
def generate_1_itemsets(transactions):
    
    #We count each different item and add it to the dictionary, with its count number
    one_itemsets = {}
    for transaction in transactions:
        for item in transaction:
            if item not in one_itemsets:
                one_itemsets[item] = 1
            else:
                one_itemsets[item]+= 1

    #We take the count number and turn it into support
    len_transactions = len(transactions)
    for item in one_itemsets:
        one_itemsets[item] = float("{:.2f}".format( int( one_itemsets[item] / len_transactions * 100)))


    return one_itemsets


#Given some candidates, get the frequent sets
def get_frequent_1_itemsets(candidates, minSup, lenTransactions):
    
    #We select those items whose count is greater than or equal to the minSup
    frequentItemsets = {}
    frequentItemsets = {itemSet: candidates[itemSet] for itemSet in candidates if candidates[itemSet] >= minSup}

    return frequentItemsets


#Generate dictionary with k+1 candidates
def generate_k_plus_1_candidates(k_itemsets, k):
        
    candidates = []

    if k <= 2:
        candidate_combinations = list(itertools.combinations(k_itemsets, k))
        for itemset in candidate_combinations:
            #candidates.append(itemset)
            candidates.append(frozenset(itemset))
#-------!!!!!!!!!!!!!!!! CAMBIAR SET EN LA SALIDA??

    else:
        aux_candidates = []
        for itemset in k_itemsets:
            for item in itemset:
                if item not in aux_candidates:
                    aux_candidates.append(item)

        candidate_combinations = list(itertools.combinations(aux_candidates, k))

        for item in candidate_combinations:
            #candidates.append(item)
            candidates.append(frozenset(item))
#-------!!!!!!!!!!!!!!!! CAMBIAR SET EN LA SALIDA??

    print("\n",k,"-Itemset CANDIDATES:")
    print(candidates)

    return candidates


#
def get_frequent_k_plus_1_itemsets(candidates, itemsets, transactions, k):

    #We count each different itemset and add it to the dictionary if it's a subset, with its count number
    candidate_k_itemsets = {}
    for transaction in transactions:
        for candidate in candidates:
            if candidate.issubset(transaction):
                if candidate not in candidate_k_itemsets:
                    candidate_k_itemsets[candidate] = 1
                else:
                    candidate_k_itemsets[candidate] += 1
    
    #We take the count number and turn it into support
    len_transactions = len(transactions)

    for itemset in candidate_k_itemsets:
        candidate_k_itemsets[itemset] = float("{:.2f}".format( int( candidate_k_itemsets[itemset] / len_transactions * 100)))
        frequent_k_itemsets = {itemset: candidate_k_itemsets[itemset] for itemset in candidate_k_itemsets if candidate_k_itemsets[itemset] >= minSup}

    print("\nFREQUENT ",k,"-Itemset:")
    print(frequent_k_itemsets)
    return frequent_k_itemsets


#Writing the solution in the output file
def writeFile(FPList):

    #with open(filePath + sys.argv[outputFilePosition], 'w') as f:
        
        #Write the data
        print("\nFP-LIST dictionary:")
        print(FPList)


#APRIORI
def apriori(transactions, minSup):

    #1 - Get frequent 1-itemsets
    frequentPatterns = []
    frequentPatterns.append( get_frequent_1_itemsets( generate_1_itemsets( transactions), minSup, len(transactions)))

    #2 - We start generating candidates k+1 itemsets, starting at 2
    k_plus_1 = 2


    while True:

        #3 Generate candidate k+1 itemsets

        #Select items from the previous generated and tested frequent patterns
        #(Magic Number: -2 because the k=1 items will be in position 0 and k+1 is 2)
        k_itemsets = list(frequentPatterns[k_plus_1 - 2].keys())

        k_plus_1_candidates = generate_k_plus_1_candidates(k_itemsets, k_plus_1)
        
        k_plus_1_candidates = get_frequent_k_plus_1_itemsets(k_plus_1_candidates, k_itemsets, transactions, k_plus_1)

        break
   
    return(frequentPatterns)


if __name__ == '__main__':

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
    
    #If nothing fails, we go to the main function
    #Time counter to show the execution time 
    startTime = time.time()
        
    #MAIN
    #We set the minimum support in a 2 decimal format
    minSup = float("{:.2f}".format( int( sys.argv[minimumSupportPosition]) / 100))
    
    transactions = readFile()
    writeFile( apriori( transactions, minSup))

    print("\nExecution time: %ss\n" % (time.time() - startTime))