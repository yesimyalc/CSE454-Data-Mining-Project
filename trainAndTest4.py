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

def combineResults(classes, modelCount):
    rowSet=[]
    for i in range(modelCount):
        rows=retrieveRows("trainResults"+str(i)+".csv")
        rows.pop(0)
        rowSet.append(rows)

    resultsRow=[[0 for x in range(len(rowSet[0][0]))] for y in range(len(rowSet[0]))] 
    for i in range(len(rowSet[0])):
        for j in range(len(rowSet[0][0])):
            for k in range(len(rowSet)):
                resultsRow[i][j]+=float(rowSet[k][i][j])

    for i in range(len(resultsRow)):
        for j in range(len(resultsRow[0])):
            resultsRow[i][j]=resultsRow[i][j]/modelCount

    with open("trainResultsCV.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(classes)
        for probability in resultsRow:
            writer.writerow(probability)
        
        file.close()

#main
#Get attributes and data objects
modelCount=10
correctCounts=[0]*11
falseCounts=[0]*11
realCounts=[[0 for x in range(11)] for y in range(7)] 
resultClassCountsCorrect=[[0 for x in range(11)] for y in range(7)] 
resultClassCountsFalse=[[0 for x in range(11)] for y in range(7)] 
for i in range(modelCount):
    rows=retrieveRows("trainSet"+str(i)+".csv")
    attributes=rows[0][1:len(rows[0])]
    dataObjects=rows[1:len(rows)]

    #Get classes
    classes=[]
    for dataObject in dataObjects:
        if dataObject[0] not in classes:
            classes.append(dataObject[0])

    model=BayesModel(attributes, dataObjects, classes, 0)
    model.train(True, "trainResults"+str(i)+".csv")
    model.setResultsFile("trainResults"+str(i)+".csv")

    testRows=retrieveRows("trainSet"+str(i)+".csv")
    testRows=testRows[1:len(rows)]
    model.test(testRows, "trainTestResults"+str(i)+".csv")
    correctCounts[10]+=model.getCorrectCount()
    correctCounts[i]=model.getCorrectCount()
    falseCounts[10]+=model.getFalseCount()
    falseCounts[i]=model.getFalseCount()
    counts=model.retrieveInfo(model.getTestObjects())
    for j in range(7):
        realCounts[j][10]+=counts[j]
        realCounts[j][i]=counts[j]
        resultClassCountsCorrect[j][10]+=model.resultClassCountsCorrect[j]
        resultClassCountsCorrect[j][i]=model.resultClassCountsCorrect[j]
        resultClassCountsFalse[j][10]+=model.resultClassCountsFalse[j]
        resultClassCountsCorrect[j][i]=model.resultClassCountsCorrect[j]

    model.printAccuracies()

combineResults(classes, modelCount)

correctCounts[10]/=10
falseCounts[10]/=10
for i in range(7):
    realCounts[i][10]/=10
    resultClassCountsCorrect[i][10]/=10
    resultClassCountsFalse[i][10]/=10

print()
print("Train Results from Cross Validation:")
print("Total Accuracy")
print("Accurate: "+str(round(correctCounts[10]))+", False: "+str(round(falseCounts[10]))+" -> %"+str((correctCounts[10]/(correctCounts[10]+falseCounts[10]))*100))
print("\nClass Accuracies")
for i in range(len(classes)):
    print(""+classes[i]+": Total:"+str(round(realCounts[i][10]))+", Accurate:"+str(round(resultClassCountsCorrect[i][10]))+", False:"+str(round(resultClassCountsFalse[i][10]))+" -> %"+str((resultClassCountsCorrect[i][10]/(realCounts[i][10]))*100))

placeholder=[]
model=BayesModel(attributes, placeholder, classes, 0)
model.setResultsFile("trainResultsCV.csv")
print()
print("Test Results from Cross Validation:")
testRows=retrieveRows('testSet.csv')
testRows=testRows[1:len(rows)]
model.test(testRows, "testResultsCV.csv")
model.printAccuracies()
