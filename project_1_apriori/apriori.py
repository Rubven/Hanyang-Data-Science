import sys
import time


#ARG SETTINGS
minimumSupportPosition = 1
inputFilePosition = 2
outputFilePosition = 3
filePath = "./"


#Read transaction file and return the transactions as collections of integers
def read_file():

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
def write_file(rules, support_dic):

    with open(filePath + sys.argv[outputFilePosition], 'w') as f:
        
        #Write the data
        for i in range(len(rules)):
            pattern = set(rules[i][0])
            associations = rules[i][1]
            support = support_dic[rules[i][0]]
            confidence = rules[i][2]

            f.write(str(pattern) + "\t" + str(associations) + "\t" + str(support) + "\t" + str(confidence) + "\n")


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


#Gets different combinations of k+1 items, given frequent k-itemsets
def generate_k_itemset_candidates(frequent_sets, k):
    
    candidate_k_itemsets = []
    lenFrequent_sets = len(frequent_sets)

    #There's probably a more efficient method for doing this
    for i in range(lenFrequent_sets):
        for j in range(i+1, lenFrequent_sets):
            combinations1 = list(frequent_sets[i])[:k-2]
            combinations2 = list(frequent_sets[j])[:k-2]
            combinations1.sort()
            combinations2.sort()
            if combinations1 == combinations2:
                candidate_k_itemsets.append(frequent_sets[i] | frequent_sets[j])
    
    return candidate_k_itemsets


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
    frequent_1_itemsets, itemsets_support = prune(transactions_sets, candidates_1, minSup)
    
    #Initialize list of solutions with the first patterns
    frequent_itemsets = [frequent_1_itemsets]

    #Set k=2 (k+1) to start looping until we run out of patterns
    k = 2

    while (len(frequent_itemsets[k-2]) > 0):
        
        #Generate k-itemset candidates 
        k_itemset_candidates = generate_k_itemset_candidates(frequent_itemsets[k-2], k)
        
        #Prune
        frequent_k_itemsets, k_itemsets_support = prune(transactions_sets, k_itemset_candidates, minSup)
        
        #Update the support dictionary with the new itemsets
        itemsets_support.update(k_itemsets_support)

        #If the new generated itemset list is empty, we exit the loop
        if frequent_k_itemsets == []:
            break

        frequent_itemsets.append(frequent_k_itemsets)
        k += 1

    return frequent_itemsets, itemsets_support


#For all the itemsets in the frequent_itemsets list we search for possible association rules and calculate their confidence
def get_association_rules(frequent_itemsets, itemsets_support):
    
    rules = []
    for i in range(1, len(frequent_itemsets)):
        #Get sets with 2 or more items
        for itemset in frequent_itemsets[i]:
            #change to frozenset if it needs to be used as index
            associative_item_sets = [set([item]) for item in itemset]   

            #Try to generate more association rules
            if (i > 1):
                generate_more_rules(itemset, associative_item_sets, itemsets_support, rules)
            else:
                calculate_confidence(itemset, associative_item_sets, itemsets_support, rules)

    return rules


#We try to generate more associations recursively
def generate_more_rules(itemset, associative_item_sets, itemsets_support, rules):
    lais = len(associative_item_sets[0])
    candidates = []
    #Try to merge sets
    if (len(itemset) > (lais + 1)):
        candidates = generate_k_itemset_candidates(associative_item_sets, lais + 1)
        candidates = calculate_confidence(itemset, candidates, itemsets_support, rules)
        #Merge sets
        if (len(candidates) > 1):
            generate_more_rules(itemset, candidates, itemsets_support, rules)


#Calculate confidence for each association, append to the rules and return the new associations list 
#(in order to use it to generate more rules)
def calculate_confidence(itemset, associative_item_sets, itemsets_support, rules):
    associations = []
    for association in associative_item_sets:
        confidence = float("{:.2f}".format(itemsets_support[itemset] / itemsets_support[itemset - association]))
        rules.append((itemset-association, association, confidence))
        associations.append(association)
    return associations


if __name__ == '__main__':

    #------SOME INPUT TESTING-------
    support_input = sys.argv[minimumSupportPosition]

    #Check we have the correct number of arguments
    if len(sys.argv) < 3:
        print("\nLess than three arguments\nExiting\n")
        sys.exit()

    #Check if the first argument is an integer
    elif not support_input.isdigit:
        print("First argument is not an integer\nExiting\n")
        sys.exit()

    elif int(support_input) > 100 or int(support_input) <= 0:
        print("Minimum Support is not a percentage (Between 0-100)\nExiting\n")
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
    transactions = read_file()

    """
    -----------MAIN-------------
    """

    #Apriori algorithm
    frequent_patterns, support = apriori(transactions, minSup)

    #Association rules
    rules = get_association_rules(frequent_patterns, support)

    #Write in output file
    write_file(rules, support)   
    

    print("\nExecution time: %ss\n" % (time.time() - startTime))