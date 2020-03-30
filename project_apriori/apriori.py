import multiprocessing
import sys
import time

#Global Setting
minimumSupport = 1
inputFileNumber = 2
outputFileNumber = 3
filePath = "../"

#Input (reading files)
def readFile(pool, mainDic):
    with open(filePath + sys.argv[inputFileNumber]) as f:
        print("LEÍDO")

#Main
def main():

    #Setting thread pool (takes # of cores by default)
    pool = multiprocessing.Pool(1)

    #Global dictionay contaning the frequent transactions
    mainDic = {}

    readFile(pool, mainDic)

    print("Test")

#Execute (with time)
if __name__ == '__main__':
    startTime = time.time()
    main()
    print("Execution time: %ss" % (time.time() - startTime) )