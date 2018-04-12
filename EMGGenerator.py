#!/usr/bin/env python

from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
import numpy
from numpy import array
import csv
import re
import json
# fix random seed for reproducibility
seed = 7
Y = []
wordsDictionary = {}
temp = []
temp2 = []
headerList = []
headerKeyValue = {}
stringCount = 0
floatCount = 0
booleanCount = 0
intCount = 0
dataNameList = []
datatypesList = []
finalMap = {}
uniquenessList = []
nonUniqueCount = 0
uniqueCount = 0
tempStr = ""
try:
    f = open('transposedDataset.csv', 'w')
    f1 = open('dictionary.txt', 'r')
    for line in f1:
        line = line.strip()
        word, wordIndex = line.split(':::::', 1)
        wordsDictionary[word] = wordIndex
    with open('country-capitals.csv') as g:
        # code to transpose the original dataset.
        gr = csv.reader(g)
        # assign header names -> unique numbers
        for x in zip(*gr):
            itercars = iter(x)
            next(itercars)
            for y in itercars:
                if bool(re.search(r'[a-zA-Z]', y)):
                    if y.strip() in wordsDictionary and not y.strip()=="":
                        f.write(wordsDictionary[y.strip()] + ',')
                else:
                    f.write(y.strip() + ',')
            if x[0] in wordsDictionary:
                f.write(wordsDictionary[x[0]] + '\n')
                headerKeyValue[wordsDictionary[x[0]]] = x[0]
                headerList.append(wordsDictionary[x[0]])
        f.close()
        f1.close()

    numpy.random.seed(seed)
    # load transposed dataset
    dataset = numpy.genfromtxt('transposedDataset.csv', dtype=None, delimiter=',')
    leng = len(dataset)
    u = (len(dataset[0]) - 1)
    #generate the input and output to fit in the model.
    for t in range(leng):
        X = []
        Y.append(float(dataset[t][u]))
        for v in range(u):
            X.append(dataset[t][v]) 
        temp.append(X)
    b = array(temp)
    
    #input data (numpy array)
    c = b[:,:u]
    #output data(numpy array)
    a = array(Y)
    print(a)
    #initialize the model.
    model = Sequential()
    # Set the number of nurons and the number of inputs for the input layer.
    model.add(Dense(12, kernel_initializer="uniform", activation="relu", input_dim=u))
    # Set the number of nurons for the hidden layer.
    model.add(Dense(u, kernel_initializer="uniform", activation="relu"))
    # set number of neurons for the output layer.
    model.add(Dense(1, kernel_initializer="uniform", activation="sigmoid"))
    # compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # fit the model
    model.fit(c, a, epochs=150, batch_size=10)
    # save the model
    model.save('model.h5')
    # initialize the model.
    loadedModel = Sequential()
    # load the model.
    loadedModel = load_model('model.h5')
    # calculate predictions
    predictions = loadedModel.predict(c)
    # round predictions
    print(predictions)
    rounded = [round(x[0]) for x in predictions]
    print(rounded)
    print(a)
    print(headerList)
    # if the predictions are correct print the header names.
    for x in range(len(rounded)):
        if rounded[x] == 1:
            if headerList[x] in headerKeyValue:
                dataNameList.append(headerKeyValue[headerList[x]])
    with open('country-capitals.csv') as g:
        gr = csv.reader(g)
        for x in zip(*gr):
            itercars = iter(x)
            next(itercars)
            for y in itercars:
                if bool(re.search(r'[a-zA-Z]', y)):
                    if not y=="":
                        stringCount = stringCount + 1
                elif bool(re.search(r'-?(?:\d+())?(?:\.\d*())?(?:e-?\d+())?(?:\2|\1\3)', y)):
                    floatCount = floatCount + 1
                elif y.lower() == "true" or y.lower() == "false" or y.lower() == "f" or y.lower() == "false":
                    booleanCount = booleanCount + 1
                elif bool(re.search(r'^[-+]?[0-9]+$', y)):
                    intCount = intCount + 1
                if not tempStr == y:
                    uniqueCount = uniqueCount + 1
                    tempStr = y
                else:
                    nonUniqueCount = nonUniqueCount + 1
            if stringCount > floatCount and stringCount > booleanCount and stringCount > intCount:
                datatypesList.append("String")
            elif floatCount > stringCount and floatCount > booleanCount and floatCount > intCount:
                datatypesList.append("Float")
            elif booleanCount > stringCount and booleanCount > floatCount and booleanCount > intCount:
                datatypesList.append("Boolean")
            elif intCount > stringCount and intCount > floatCount and intCount > booleanCount:
                datatypesList.append("Integer")
            if nonUniqueCount == 0:
                uniquenessList.append("Unique")
            else:
                uniquenessList.append("Non Unique")
            stringCount = 0
            floatCount = 0
            booleanCount = 0
            intCount = 0
            nonUniqueCount = 0
            uniqueCount = 0
    for i in range(len(datatypesList)):
        finalMap[dataNameList[i]] = datatypesList[i]+"::"+uniquenessList[i]
    print(finalMap)
    json = json.dumps(finalMap)
    of = open("out.json","w")
    of.write(json)
    of.close()
except Exception as ex:
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print(message)