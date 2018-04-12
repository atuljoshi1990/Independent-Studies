#!/usr/bin/env python
import csv
import re
wordsList = []
count = 1
try:
    f = open('dictionary.txt', 'w')
        #get the dataset
    with open('country-capitals.csv') as g:
        gr = csv.reader(g)
        for x in gr:
            itercars = iter(x)
            for y in itercars:
                if bool(re.search(r'[a-zA-Z]', y)):
                    if not y=="":
                        if y.strip() not in wordsList:
                            wordsList.append(y.strip())
    wordsList.sort()
    for item in wordsList:
        f.write(item+':::::'+str(count)+'\n')
        count = count + 1
    f.close()
    print('done')
except Exception as ex:
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print(message)