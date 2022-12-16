import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
import csv

from model import BayesModel

def retrieveRows(fileName):
    #Retrieving info about the dataset
    #Retrieve rows from data.csv
    file = open(fileName)
    csvreader = csv.reader(file)

    rows = []
    for row in csvreader:
        rows.append(row)

    file.close()
    return rows

#main
#Get attributes and data objects
rows=retrieveRows('trainSet2.csv')
attributes=rows[0][1:len(rows[0])]
dataObjects=rows[1:len(rows)]

#Get classes
classes=[]
for dataObject in dataObjects:
    if dataObject[0] not in classes:
        classes.append(dataObject[0])

model=BayesModel(attributes, dataObjects, classes, 0)
model.train(False, "trainResults.csv")
model.setResultsFile("trainResults.csv")

testRows=retrieveRows('trainSet2.csv')
testRows=testRows[1:len(rows)]
model.test(testRows, "trainTestResult.csv")
model.printAccuracies()

testRows=retrieveRows('testSet2.csv')
testRows=testRows[1:len(rows)]
model.test(testRows, "testResult.csv")
model.printAccuracies()




