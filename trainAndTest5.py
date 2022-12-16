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


def calculateWeights(modelC, correctC, falseC, realC, resultClassCC):
    weights=[0]*10
    points=[0]*10
    for i in range(modelC):
        accTotal=correctC[i]/(correctC[i]+falseC[i])*2
        points[i]+=accTotal

    order=np.argsort(points)   
    for i in range(len(order)):
        weights[order[i]]+=(i+1)*100

    return weights
    

def combineResults(classes, modelCount, weights):
    rowSet=[]
    totalWeights=0
    for i in range(modelCount):
        rows=retrieveRows("trainResults"+str(i)+".csv")
        rows.pop(0)
        rowSet.append(rows)
        totalWeights+=weights[i]

    resultsRow=[[0 for x in range(len(rowSet[0][0]))] for y in range(len(rowSet[0]))] 
    for i in range(len(rowSet[0])):
        for j in range(len(rowSet[0][0])):
            for k in range(len(rowSet)):
                resultsRow[i][j]+=float(rowSet[k][i][j])*weights[k]

    for i in range(len(resultsRow)):
        for j in range(len(resultsRow[0])):
            resultsRow[i][j]=resultsRow[i][j]/totalWeights

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
    correctCounts[i]=model.getCorrectCount()
    falseCounts[i]=model.getFalseCount()
    counts=model.retrieveInfo(model.getTestObjects())
    for j in range(7):
        realCounts[j][i]=counts[j]
        resultClassCountsCorrect[j][i]=model.resultClassCountsCorrect[j]
        resultClassCountsFalse[j][i]=model.resultClassCountsFalse[j]

    model.printAccuracies()

placeholder=[]
model=BayesModel(attributes, placeholder, classes, 0)
model.setResultsFile("trainResultsCV.csv")
weights=calculateWeights(modelCount, correctCounts, falseCounts, realCounts, resultClassCountsCorrect)
model.setWeights(weights)
combineResults(classes, modelCount, model.getWeights())
totalWeights=0

for j in range(10):
    totalWeights+=weights[j]
    correctCounts[10]+=correctCounts[j]*weights[j]
    falseCounts[10]+=falseCounts[j]*weights[j]
    for i in range(7):
        realCounts[i][10]+=realCounts[i][j]*weights[j]
        resultClassCountsCorrect[i][10]+=resultClassCountsCorrect[i][j]*weights[j]
        resultClassCountsFalse[i][10]+=resultClassCountsFalse[i][j]*weights[j]

correctCounts[10]/=totalWeights
falseCounts[10]/=totalWeights
for i in range(7):
    realCounts[i][10]/=totalWeights
    resultClassCountsCorrect[i][10]/=totalWeights
    resultClassCountsFalse[i][10]/=totalWeights

print()
print("Train Results from Cross Validation:")
print("Total Accuracy")
print("Accurate: "+str(round(correctCounts[10]))+", False: "+str(round(falseCounts[10]))+" -> %"+str((correctCounts[10]/(correctCounts[10]+falseCounts[10]))*100))
print("\nClass Accuracies")
for i in range(len(classes)):
    print(""+classes[i]+": Total:"+str(round(realCounts[i][10]))+", Accurate:"+str(round(resultClassCountsCorrect[i][10]))+", False:"+str(round(resultClassCountsFalse[i][10]))+" -> %"+str((resultClassCountsCorrect[i][10]/(realCounts[i][10]))*100))

print()
print("Test Results from Cross Validation:")
testRows=retrieveRows('testSet.csv')
testRows=testRows[1:len(rows)]
model.test(testRows, "testResultsCVBoosted.csv")
model.printAccuracies()
