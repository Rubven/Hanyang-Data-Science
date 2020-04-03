import sys
import time

#ARG SETTINGS
minimumSupportPosition = 1
inputFilePosition = 2
outputFilePosition = 3
filePath = "../"


#Read transaction file and return the transactions as collections of integers
def readFile():

    #Collection of transactions
    #Each line is a transaction 
    #Each item is separated by a tab
    transactions = []
    with open(filePath + sys.argv[inputFilePosition], 'r') as f:
        for transaction in f.read().split('\n'):
            transactions.append( [int(item) for item  in transaction.split('\t')])
    
    return transactions

#APRIORI
def apriori(transactions):
    
    print(transactions)






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
        apriori(readFile())

        print("\nExecution time: %ss\n" % (time.time() - startTime))