#!/usr/bin/env python
import json
from difflib import SequenceMatcher
nameMatchCounter = 0
dataTypeMatchCounter = 0
numerator = 0
denominator = 0
SMSililarityVal = 0
finalKeyMatchRatio = 0
match = 0
with open('out1.json', 'r') as f1:
     data1 = json.load(f1)
with open('out2.json', 'r') as f2:
    data2 = json.load(f2)
    for key1 in data1:
        for key2 in data2:
            keyMatchRatio = SequenceMatcher(None, key1, key2).ratio()
            match = match+1
            if keyMatchRatio >= 0.7:
                nameMatchCounter = nameMatchCounter + 1
                dataType1, dataType1Uniqueness = data1[key1].split('::',1)
                dataType2, dataType2Uniqueness = data2[key2].split('::',1)
                if dataType1 == dataType2:
                    dataTypeMatchCounter = dataTypeMatchCounter + 1
                    break
            else:
                finalKeyMatchRatio = keyMatchRatio+finalKeyMatchRatio
numerator = (dataTypeMatchCounter+nameMatchCounter)/2
denominator = (len(data1)+len(data2))/2
SMSililarityVal = finalKeyMatchRatio/match + numerator/denominator
if SMSililarityVal > 1:
    SMSililarityVal = 1
print("Structural Matching Value: "+str(SMSililarityVal))