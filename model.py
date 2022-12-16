import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
import csv

class BayesModel:
    def __init__(self, attr, objs, clss, clssIndex):
        self.attributes=attr
        self.dataObjects=objs
        self.classes=clss
        self.classIndex=clssIndex

    def setResultsFile(self, fileName):
        self.resultFile=fileName

    def setWeights(self, w):
        self.weights=w

    def findClassProbabilities(self):
        classCounts=[]
        self.classProbabilities=[]
        for i in range(len(self.classes)):
            classCounts.append(0)
            self.classProbabilities.append(0)

        for dataObject in self.dataObjects:
            classIndex=self.classes.index(dataObject[self.classIndex])
            classCounts[classIndex]+=1
        
        for i in range(len(self.classes)):
            self.classProbabilities[i]=classCounts[i]/len(self.dataObjects)

    def findAttributeProbabilities(self, fixZero):
        attributeCounts=[[0 for x in range(len(self.classes))] for y in range(len(self.attributes))] 
        self.attributeProbabilities=[[0 for x in range(len(self.classes))] for y in range(len(self.attributes))] 

        for i in range(len(self.attributes)):
            for dataObject in self.dataObjects:
                classIndex=self.classes.index(dataObject[self.classIndex])
                if dataObject[i+1]=="1":
                    attributeCounts[i][classIndex]+=1

        for i in range(len(self.attributes)):
            counts=[]
            total=0
            for k in range(len(self.classes)):
                total+=attributeCounts[i][k]
                counts.append(attributeCounts[i][k])
            counts.sort()
            min=-1
            for count in counts:
                if count!=0:
                    min=count
                    break
            if min==-1:
                min=1
            for j in range(len(self.classes)):
                if total==0 and fixZero:
                    self.attributeProbabilities[i][j]=1/len(self.classes)
                elif total==0:
                    self.attributeProbabilities[i][j]=0
                elif fixZero and attributeCounts[i][j]==0:
                    if j==0:
                        self.attributeProbabilities[i][j]=(min*0.00000001)/total
                    elif j==1:
                        self.attributeProbabilities[i][j]=(min*0.00000001)/total
                    elif j==2:
                        self.attributeProbabilities[i][j]=(min*0.001)/total
                    elif j==3:
                        self.attributeProbabilities[i][j]=(min*0.001)/total
                    elif j==4:
                        self.attributeProbabilities[i][j]=(min*0.0000002)/total
                    elif j==5:
                        self.attributeProbabilities[i][j]=(min*0.00000001)/total
                    elif j==6:
                        self.attributeProbabilities[i][j]=(min*0.00001)/total
                else:
                    self.attributeProbabilities[i][j]=attributeCounts[i][j]/total

    def findBayesProbabilities(self):
        for i in range(len(self.attributes)):
            for j in range(len(self.classes)):
                self.attributeProbabilities[i][j]=self.attributeProbabilities[i][j]*self.classProbabilities[j]

    def createTrainedModel(self, fileName):
        self.resultFile=fileName
        with open(self.resultFile, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.classes)
            for probability in self.attributeProbabilities:
                writer.writerow(probability)
        
            file.close()

    def retrieveAttributeProbabilities(self):
        file = open(self.resultFile)
        csvreader = csv.reader(file)

        rows = []
        for row in csvreader:
            rows.append(row)
        file.close()
        rows.pop(0)

        self.attributeProbabilities=[[0 for x in range(len(self.classes))] for y in range(len(self.attributes))] 
        for i in range(len(self.attributes)):
            for j in range(len(self.classes)):
                self.attributeProbabilities[i][j]=float(rows[i][j])
        
    def train(self, isZeroFixed, fileName):
        self.findClassProbabilities()
        self.findAttributeProbabilities(isZeroFixed)
        self.findBayesProbabilities()
        self.createTrainedModel(fileName)

    def test(self, testObjects, fileName):
        self.testObjects=testObjects
        self.retrieveAttributeProbabilities()
        self.resultClasses=[]
        self.resultClassCountsCorrect=[0]*len(self.classes)
        self.resultClassCountsFalse=[0]*len(self.classes)
        self.correctCount=0
        self.falseCount=0
        for object in testObjects:
            classP=[1]*len(self.classes)
            for i in range(len(self.attributes)):
                if object[i+1]=="1":
                    for j in range(len(self.classes)):
                        classP[j]*=self.attributeProbabilities[i][j]
            max=-1
            maxIndex=-1
            for i in range(len(classP)):
                if classP[i]>max:
                    max=classP[i]
                    maxIndex=i

            if object[0]==self.classes[maxIndex]:
                self.correctCount+=1
                self.resultClassCountsCorrect[maxIndex]+=1
            else:
                self.falseCount+=1
                self.resultClassCountsFalse[maxIndex]+=1
            self.resultClasses.append(self.classes[maxIndex])

        with open(fileName, 'w', newline='') as file:
            writer = csv.writer(file)
            for result in self.resultClasses:
                writer.writerow([result])
        
            file.close()

    def retrieveInfo(self, rows):
        cuisineMealCount=[0]*len(self.classes)
        i=0
        while i < len(rows):
            index=self.classes.index(rows[i][0])
            cuisineMealCount[index]+=1
            i+=1

        return cuisineMealCount

    def printAccuracies(self):
        print("Total Accuracy")
        print("Accurate: "+str(self.correctCount)+", False: "+str(self.falseCount)+" -> %"+str((self.correctCount/(self.correctCount+self.falseCount))*100))
        print("\nClass Accuracies")
        realCounts=self.retrieveInfo(self.testObjects)
        for i in range(len(self.classes)):
            print(""+self.classes[i]+": Total:"+str(realCounts[i])+", Accurate:"+str(self.resultClassCountsCorrect[i])+", False:"+str(self.resultClassCountsFalse[i])+" -> %"+str((self.resultClassCountsCorrect[i]/(realCounts[i]))*100))

    def getCorrectCount(self):
        return self.correctCount

    def getFalseCount(self):
        return self.falseCount

    def getTestObjects(self):
        return self.testObjects

    def getWeights(self):
        return self.weights










