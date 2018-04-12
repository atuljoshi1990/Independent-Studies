#!/usr/bin/env python
import csv
from difflib import SequenceMatcher

keyMatchRatio = 0
matchCount = 0
count = 0
tempList1 = []
tempList2 = []
length = 0
try:
    file_1 = csv.reader(open('free-zipcode-database.csv', 'r'), delimiter=',')
    file_2 = csv.reader(open('country-capitals.csv', 'r'), delimiter=',')
    next(file_1)
    next(file_2)
    for row1 in file_1:
        for item1 in row1:
            tempList1.append(item1)
    for row2 in file_2:
        for item2 in row2:
            tempList2.append(item2)
    if len(tempList1) <= len(tempList2):
        length = len(tempList1)
    if len(tempList1) > len(tempList2):
        length = len(tempList2)
    for item in range(length):
        temp1 = tempList1[item]
        temp2 = tempList2[item]
        keyMatchRatio = SequenceMatcher(None, temp1, temp2).ratio()
        matchCount = matchCount + keyMatchRatio
        count = count + 1
    totalRatio = matchCount/count
    print("Constraint Matching Value: "+str(totalRatio))
except Exception as ex:
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print(message)