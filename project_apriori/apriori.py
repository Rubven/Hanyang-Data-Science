import sys
import time

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
    
    one_itemsets = {}
    for transaction in transactions:
        for item in transaction:
            if item not in one_itemsets:
                one_itemsets[item] = 1
            else:
                one_itemsets[item]+= 1
    return one_itemsets


#Given some candidates, get the frequent sets
def get_frequent_itemsets(candidates, minSup):
    
    frequentItemsets = {}

    #We set the local minSup for these candidates (instead of calculating it everytime)
    local_minSup = minSup * len(candidates)

    #We select those items whose count is greater or equal than the local_minSup we just calculated
    frequentItemsets = {itemSet: candidates[itemSet] for itemSet in candidates if candidates[itemSet] >= local_minSup}

    return frequentItemsets


#Writing the solution in the output file
def writeFile(FPList):

    #with open(filePath + sys.argv[outputFilePosition], 'w') as f:
        
        #Write the data
        print("\nFP-LIST dictionary:")
        print(FPList)


#APRIORI
def apriori(transactions, minSup):
    
    print("\nTRANSACTIONS:")
    print(transactions)

    #1 - Get frequent 1-itemsets
    frequentPatterns = []
    frequentPatterns.append( get_frequent_itemsets( generate_1_itemsets( transactions), minSup))


    return(frequentPatterns)





if __name__ == '__main__':

    #Check we have the correct number of arguments
    if len(sys.argv) < 3:
        print("\nLess than three arguments\nExiting\n")
        exit

    #Check if the first argument is an integer
    elif not sys.argv[minimumSupportPosition].isdigit:
        print("First argument is not an integer\nExiting\n")
        exit

    #Triying to open Input files
    try:
        open(filePath + sys.argv[inputFilePosition])
    except Exception:
        print("Could not read input file\nExiting\n")
        exit
    
    #If nothing fails, we go to the main function
    else:
        #Time counter to show the execution time 
        startTime = time.time()
           
        #MAIN
        #We set the minimum support in a 2 decimal format
        minSup = float("{:.2f}".format( int( sys.argv[minimumSupportPosition]) / 100))
        
        writeFile( apriori( readFile(), minSup))

        print("\nExecution time: %ss\n" % (time.time() - startTime))