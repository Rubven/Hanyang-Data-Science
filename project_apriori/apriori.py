import sys
import re
import multiprocessing
import time

#SETTINGS
minimumSupport = 1
inputFilePosition = 2
outputFilePosition = 3
filePath = "../"

#MAP    
def map(items):

    itemMap = []
    for i in range(len(items)):
        itemMap.append([items[i].lower(),1])
    itemMap.sort()
    return itemMap


#SHUFFLE
def shuffle(itemMap):
    
    dic = {}
    for i in range(len(itemMap)):
        if itemMap[i][0] not in dic:
            dic[itemMap[i][0]] = []
        dic[itemMap[i][0]].append(itemMap[i][1])
    return dic
    

#REDUCE    
def reduce(mainDic, dic):
       
    for item in dic:
        if item not in mainDic:
            mainDic[item] = []
            mainDic[item].append(sum(dic[item]))
        else:
            transaction_items = sum(dic[item])
            mainDic_items = mainDic[item][0]
            mainDic[item] = []
            mainDic[item].append(transaction_items + mainDic_items)
    return mainDic
         
def processTransaction(transaction):
      
    #clean text (just in case)
    transaction = re.sub("\n", '', transaction)
    
    #MAPPING
    items = map(transaction.split("\t"))                    
    items = shuffle(items)
    return items           


def processFile(pool, stack, mainDic):
    
    with open(filePath + sys.argv[inputFilePosition]) as f:            
        #send threads to handle different transactions
        for transaction in f: 
            async_result = pool.apply_async(processTransaction, args = (transaction, ))
            dic = async_result.get()

            #add result to the stack to handle it when its turn comes
            stack.append(dic)

     
def main():

    #Setting thread pool (takes machine's # of cores by default)
    pool = multiprocessing.Pool(1)
    
    #Global dictionay contaning the frequent transactions
    mainDic = {}
   
    #stack to collect the solutions from the threads and manage them in order, so that they don't overlap
    stack = []

    #read the file and identify the items
    processFile(pool, stack, mainDic)

    #manage concurrency      
    wait = True
    while wait:
        if len(stack) > 0:
            wait = False
    
    #modify main dictionary
    while (len(stack) > 0):
        mainDic = reduce(mainDic, stack.pop())

    print("mainDic:\n")      
    print (mainDic)   

#time counter to show the execution time    
if __name__ == '__main__':
   startTime = time.time()
   main()
   print("Execution time: %ss" % (time.time() - startTime))