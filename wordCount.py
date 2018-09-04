#!/urs/bin/env python3

import sys    # Take in files
import re     # Regular expressions (required)
import os     #check for files

#check for format
if len(sys.argv) is not 3:
    print("Wrong format. usage = wordCount.py <input> <output>" )
    exit()

#grab the first arg file
fileName = sys.argv[1]

# check for all files to exist
if not os.path.exists(fileName):
    print ("file %s does not exists!" % fileName)
    exit()

#format  = { word : times }
wordList  = {}

# open file
with open(fileName,"r") as inputFile:
    for line in inputFile:                  # parse the words
        splicedList = re.split(r'\W+',line)
        for  word  in  splicedList:
            word =  word.lower()

            if word not  in wordList.keys():
                 wordList[word] = 1          #add to dict 
            else:
                wordList[word] += 1         #add to value
del wordList[""]
inputFile.close()

#write to the file
with open(sys.argv[2],'w') as outputFile:
    for x ,y in sorted(wordList.items()):  # iterate over a sorted list
        outputFile.write( "%s %d\n" % (x , y) )
outputFile.close()
print("file written")
