import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
import csv
import random

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

def retrieveInfo(rows, count, underSampling):
    #Retrieve unique cusine names, their amount, unique ingredient names
    ingredients=[]
    ingredientCount=[]
    cuisines=[]
    cuisineMealCount=[]
    i=0
    while i < len(rows):
        mealIngredients=[]
        for ingredient in rows[i]:
            if ingredient not in mealIngredients:
                mealIngredients.append(ingredient)
        mealIngredients.pop(0)

        if len(mealIngredients) <count:
            if underSampling and (rows[i][0]=="EastAsian" or rows[i][0]=="WesternEuropean" or rows[i][0]=="SouthAsian" or rows[i][0]=="SoutheastAsian"):
                rows.pop(i)
                continue
            elif not underSampling:
                rows.pop(i)
                continue

        if rows[i][0] not in cuisines:
            cuisines.append(rows[i][0])
        index=cuisines.index(rows[i][0])
        if len(cuisineMealCount)<=index:
            cuisineMealCount.append(1)
        else:
            cuisineMealCount[index]+=1

        for ingredient in mealIngredients:
            if ingredient not in ingredients:
                ingredients.append(ingredient)
            index=ingredients.index(ingredient)
            if len(ingredientCount)<=index:
                ingredientCount.append(1)
            else:
                ingredientCount[index]+=1
        i+=1

    return rows, ingredients, ingredientCount, cuisines, cuisineMealCount

def eliminateRowsCuisines(cuisines, rows):
    #Eliminating some ingredients
    i=0 
    while i < len(rows):
        if rows[i][0]==cuisines[3] or rows[i][0]==cuisines[5] or rows[i][0]==cuisines[9] or rows[i][0]==cuisines[2]:
            rows.pop(i)
            i-=1
        i+=1

    return rows

def visualizeInfo(cuisines, cuisineMealCount, ingredients, ingredientCount):
    #Visualize cuisines and their meal amounts
    plt.bar(cuisines, cuisineMealCount)
    plt.title("Cuisine Meal Amounts")
    plt.xlabel('Cuisines')
    plt.ylabel('Meal Amount')
    plt.show()

    #Visualize ingredients and their appearance count in meals
    print("Ingredients and their counts")
    df=pd.DataFrame({'count':ingredientCount}, index=ingredients)
    print(df.sort_values(by=['count'], ascending=False))
    print()

def divideSets(cuisines, cuisineMealCount, rows):
    rowTrain=[]
    rowTest=[]
    cuisineTestCount=[]

    for i in range(len(cuisines)):
        cuisineTestCount.append(0)

    for i in range(len(rows)):
        cuisineIndex=cuisines.index(rows[i][0])
        if cuisineTestCount[cuisineIndex] < (cuisineMealCount[cuisineIndex]/3.3):
            rowTest.append(rows[i])
            cuisineTestCount[cuisineIndex]+=1
        else:
            rowTrain.append(rows[i])

    return rowTrain, rowTest

def divideSetsRandom(cuisines, rows):
    testRows=[]
    trainRows=[]
    class0Rows=[]
    class0RowsT=[]
    class1Rows=[]
    class1RowsT=[]
    class2Rows=[]
    class2RowsT=[]
    class3Rows=[]
    class3RowsT=[]
    class4Rows=[]
    class4RowsT=[]
    class5Rows=[]
    class5RowsT=[]
    class6Rows=[]
    class6RowsT=[]
    class7Rows=[]
    class7RowsT=[]

    for row in rows:
        if cuisines.index(row[0])==0:
            class0Rows.append(row)
            class0RowsT.append(row)
        elif cuisines.index(row[0])==1:
            class1Rows.append(row)
            class1RowsT.append(row)
        elif cuisines.index(row[0])==2:
            class2Rows.append(row)
            class2RowsT.append(row)
        elif cuisines.index(row[0])==3:
            class3Rows.append(row)
            class3RowsT.append(row)
        elif cuisines.index(row[0])==4:
            class4Rows.append(row)
            class4RowsT.append(row)
        elif cuisines.index(row[0])==5:
            class5Rows.append(row)
            class5RowsT.append(row)
        elif cuisines.index(row[0])==6:
            class6Rows.append(row)
            class6RowsT.append(row)
        elif cuisines.index(row[0])==7:
            class7Rows.append(row)
            class7RowsT.append(row)

    class0TestCount=len(class0Rows)/10
    class1TestCount=len(class1Rows)/10
    class2TestCount=len(class2Rows)/10
    class3TestCount=len(class3Rows)/10
    class4TestCount=len(class4Rows)/10
    class5TestCount=len(class5Rows)/10
    class6TestCount=len(class6Rows)/10
    class7TestCount=len(class7Rows)/10

    newRows=[]
    newRows=np.random.choice(class0RowsT, int(class0TestCount), False)
    for row in newRows:
        testRows.append(row)
        class0Rows.remove(row)
    for row in class0Rows:
        trainRows.append(row)

    newRows=[]
    newRows=np.random.choice(class1RowsT, int(class1TestCount), False)
    for row in newRows:
        testRows.append(row)
        class1Rows.remove(row)
    for row in class1Rows:
        trainRows.append(row)

    newRows=[]
    newRows=np.random.choice(class2RowsT, int(class2TestCount), False)
    for row in newRows:
        testRows.append(row)
        class2Rows.remove(row)
    for row in class2Rows:
        trainRows.append(row)

    newRows=[]
    newRows=np.random.choice(class3RowsT, int(class3TestCount), False)
    for row in newRows:
        testRows.append(row)
        class3Rows.remove(row)
    for row in class3Rows:
        trainRows.append(row)

    newRows=[]
    newRows=np.random.choice(class4RowsT, int(class4TestCount), False)
    for row in newRows:
        testRows.append(row)
        class4Rows.remove(row)
    for row in class4Rows:
        trainRows.append(row)

    newRows=[]
    newRows=np.random.choice(class5RowsT, int(class5TestCount), False)
    for row in newRows:
        testRows.append(row)
        class5Rows.remove(row)
    for row in class5Rows:
        trainRows.append(row)

    newRows=[]
    newRows=np.random.choice(class6RowsT, int(class6TestCount), False)
    for row in newRows:
        testRows.append(row)
        class6Rows.remove(row)
    for row in class6Rows:
        trainRows.append(row)

    newRows=[]
    newRows=np.random.choice(class7RowsT, int(class7TestCount), False)
    for row in newRows:
        testRows.append(row)
        class7Rows.remove(row)
    for row in class7Rows:
        trainRows.append(row)

    return trainRows, testRows


def divideCVSets(cuisines, rows, modelCount):
    trainSets=[]
    testSets=[]
    class0Rows=[]
    class0RowsT=[]
    class1Rows=[]
    class1RowsT=[]
    class2Rows=[]
    class2RowsT=[]
    class3Rows=[]
    class3RowsT=[]
    class4Rows=[]
    class4RowsT=[]
    class5Rows=[]
    class5RowsT=[]
    class6Rows=[]
    class6RowsT=[]
    class7Rows=[]
    class7RowsT=[]

    for row in rows:
        if cuisines.index(row[0])==0:
            class0Rows.append(row)
            class0RowsT.append(row)
        elif cuisines.index(row[0])==1:
            class1Rows.append(row)
            class1RowsT.append(row)
        elif cuisines.index(row[0])==2:
            class2Rows.append(row)
            class2RowsT.append(row)
        elif cuisines.index(row[0])==3:
            class3Rows.append(row)
            class3RowsT.append(row)
        elif cuisines.index(row[0])==4:
            class4Rows.append(row)
            class4RowsT.append(row)
        elif cuisines.index(row[0])==5:
            class5Rows.append(row)
            class5RowsT.append(row)
        elif cuisines.index(row[0])==6:
            class6Rows.append(row)
            class6RowsT.append(row)
        elif cuisines.index(row[0])==7:
            class7Rows.append(row)
            class7RowsT.append(row)

    class0TestCount=len(class0Rows)/10
    class1TestCount=len(class1Rows)/10
    class2TestCount=len(class2Rows)/10
    class3TestCount=len(class3Rows)/10
    class4TestCount=len(class4Rows)/10
    class5TestCount=len(class5Rows)/10
    class6TestCount=len(class6Rows)/10
    class7TestCount=len(class7Rows)/10

    for i in range(modelCount):
        class0=class0Rows.copy()
        class1=class1Rows.copy()
        class2=class2Rows.copy()
        class3=class3Rows.copy()
        class4=class4Rows.copy()
        class5=class5Rows.copy()
        class6=class6Rows.copy()
        class7=class7Rows.copy()
        testRows=[]
        trainRows=[]

        newRows=[]
        if i!=modelCount-1:
            newRows=np.random.choice(class0RowsT, int(class0TestCount), False)
        else:
            newRows=class0RowsT.copy()
        for row in newRows:
            testRows.append(row)
            class0.remove(row)
            class0RowsT.remove(row)
        for row in class0:
            trainRows.append(row)

        newRows=[]
        if i!=modelCount-1:
            newRows=np.random.choice(class1RowsT, int(class1TestCount), False)
        else:
            newRows=class1RowsT.copy()
        for row in newRows:
            testRows.append(row)
            class1.remove(row)
            class1RowsT.remove(row)
        for row in class1:
            trainRows.append(row)

        newRows=[]
        if i!=modelCount-1:
            newRows=np.random.choice(class2RowsT, int(class2TestCount), False)
        else:
            newRows=class2RowsT.copy()
        for row in newRows:
            testRows.append(row)
            class2.remove(row)
            class2RowsT.remove(row)
        for row in class2:
            trainRows.append(row)

        newRows=[]
        if i!=modelCount-1:
            newRows=np.random.choice(class3RowsT, int(class3TestCount), False)
        else:
            newRows=class3RowsT.copy()
        for row in newRows:
            testRows.append(row)
            class3.remove(row)
            class3RowsT.remove(row)
        for row in class3:
            trainRows.append(row)

        newRows=[]
        if i!=modelCount-1:
            newRows=np.random.choice(class4RowsT, int(class4TestCount), False)
        else:
            newRows=class4RowsT.copy()
        for row in newRows:
            testRows.append(row)
            class4.remove(row)
            class4RowsT.remove(row)
        for row in class4:
            trainRows.append(row)

        newRows=[]
        if i!=modelCount-1:
            newRows=np.random.choice(class5RowsT, int(class5TestCount), False)
        else:
            newRows=class5RowsT.copy()
        for row in newRows:
            testRows.append(row)
            class5.remove(row)
            class5RowsT.remove(row)
        for row in class5:
            trainRows.append(row)

        newRows=[]
        if i!=modelCount-1:
            newRows=np.random.choice(class6RowsT, int(class6TestCount), False)
        else:
            newRows=class6RowsT.copy()
        for row in newRows:
            testRows.append(row)
            class6.remove(row)
            class6RowsT.remove(row)
        for row in class6:
            trainRows.append(row)

        newRows=[]
        if i!=modelCount-1:
            newRows=np.random.choice(class7RowsT, int(class7TestCount), False)
        else:
            newRows=class7RowsT.copy()
        for row in newRows:
            testRows.append(row)
            class7.remove(row)
            class7RowsT.remove(row)
        for row in class7:
            trainRows.append(row)

        trainSets.append(trainRows)
        testSets.append(testRows)

    return trainSets, testSets



def createDataset(ingredients, rows, fileName):
    #Organizing the dataset for training
    attributes=[]
    dataObjects=[]
    attributes.append("Cuisine")

    for ingredient in ingredients:
        attributes.append(ingredient)

    for row in rows:
        dataObject=[]
        dataObject.append(row[0])
        for ingredient in ingredients:
            if ingredient in row:
                dataObject.append("1")
            else:
                dataObject.append("0")
        dataObjects.append(dataObject)

    #Creating the dataset
    with open(fileName, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(attributes)
        for dataObject in dataObjects:
            writer.writerow(dataObject)
        file.close()

def underSample(rows):
    class1=[]
    class5=[]
    class6=[]
    class7=[]
    newRows=[]
    for row in rows:
        if row[0]=="EastAsian":
            class1.append(row)
        elif row[0]=="SouthAsian":
            class5.append(row)
        elif row[0]=="SoutheastAsian":
            class6.append(row)
        elif row[0]=="WesternEuropean":
            class7.append(row)
        newRows.append(row)

    i=0
    class1RemoveCount=len(class1)*70/100
    class5RemoveCount=len(class5)*60/100
    class6RemoveCount=len(class6)*50/100
    class7RemoveCount=len(class7)*70/100

    while i<class1RemoveCount:
        index=random.randrange(len(class1))
        newRows.remove(class1[index])
        class1.pop(index)
        i+=1

    i=0
    while i<class5RemoveCount:
        index=random.randrange(len(class5))
        newRows.remove(class5[index])
        class5.pop(index)
        i+=1

    i=0
    while i<class6RemoveCount:
        index=random.randrange(len(class6))
        newRows.remove(class6[index])
        class6.pop(index)
        i+=1

    i=0
    while i<class7RemoveCount:
        index=random.randrange(len(class7))
        newRows.remove(class7[index])
        class7.pop(index)
        i+=1

    return newRows

def overSample(rows):
    class0Count=0
    total0IngCount=0
    class0Ing=[]
    class0IngCounts=[]
    class2Count=0
    total2IngCount=0
    class2Ing=[]
    class2IngCounts=[]
    class3Count=0
    total3IngCount=0
    class3Ing=[]
    class3IngCounts=[]
    class4Count=0
    total4IngCount=0
    class4Ing=[]
    class4IngCounts=[]
    newRows=[]
    for row in rows:
        if row[0]=="African":
            class0Count+=1
            for ingredient in row:
                if ingredient!=row[0] and ingredient not in class0Ing:
                    class0Ing.append(ingredient)
                    class0IngCounts.append(1)
                    total0IngCount+=1
                elif ingredient!=row[0]:
                    class0IngCounts[class0Ing.index(ingredient)]+=1
                    total0IngCount+=1
        elif row[0]=="EasternEuropean":
            class2Count+=1
            for ingredient in row:
                if ingredient!=row[0] and ingredient not in class2Ing:
                    class2Ing.append(ingredient)
                    class2IngCounts.append(1)
                    total2IngCount+=1
                elif ingredient!=row[0]:
                    class2IngCounts[class2Ing.index(ingredient)]+=1
                    total2IngCount+=1
        elif row[0]=="MiddleEastern":
            class3Count+=1
            for ingredient in row:
                if ingredient!=row[0] and ingredient not in class3Ing:
                    class3Ing.append(ingredient)
                    class3IngCounts.append(1)
                    total3IngCount+=1
                elif ingredient!=row[0]:
                    class3IngCounts[class3Ing.index(ingredient)]+=1
                    total3IngCount+=1
        elif row[0]=="NorthernEuropean":
            class4Count+=1
            for ingredient in row:
                if ingredient!=row[0] and ingredient not in class4Ing:
                    class4Ing.append(ingredient)
                    class4IngCounts.append(1)
                    total4IngCount+=1
                elif ingredient!=row[0]:
                    class4IngCounts[class4Ing.index(ingredient)]+=1
                    total4IngCount+=1
        newRows.append(row)

    class0AddCount=class0Count*10/100
    class2AddCount=class2Count*90/100
    class3AddCount=class3Count*70/100
    class4AddCount=class4Count*65/100

    for i in range(len(class0IngCounts)):
        class0IngCounts[i]=class0IngCounts[i]/total0IngCount
    for i in range(len(class2IngCounts)):
        class2IngCounts[i]=class2IngCounts[i]/total2IngCount
    for i in range(len(class3IngCounts)):
        class3IngCounts[i]=class3IngCounts[i]/total3IngCount
    for i in range(len(class4IngCounts)):
        class4IngCounts[i]=class4IngCounts[i]/total4IngCount

    i=0
    while i<class0AddCount:
        ingCount=random.randrange(4,15)
        newRowIng=np.random.choice(class0Ing, ingCount, False)
        newRow=[]
        newRow.append("African")
        for ing in newRowIng:
            newRow.append(ing)
        newRows.append(newRow)
        i+=1

    i=0
    while i<class2AddCount:
        ingCount=random.randrange(4,15)
        newRowIng=np.random.choice(class2Ing, ingCount, False)
        newRow=[]
        newRow.append("EasternEuropean")
        for ing in newRowIng:
            newRow.append(ing)
        newRows.append(newRow)
        i+=1

    i=0
    while i<class3AddCount:
        ingCount=random.randrange(4,15)
        newRowIng=np.random.choice(class3Ing, ingCount, False)
        newRow=[]
        newRow.append("MiddleEastern")
        for ing in newRowIng:
            newRow.append(ing)
        newRows.append(newRow)
        i+=1

    i=0
    while i<class4AddCount:
        ingCount=random.randrange(4,15)
        newRowIng=np.random.choice(class4Ing, ingCount, False)
        newRow=[]
        newRow.append("NorthernEuropean")
        for ing in newRowIng:
            newRow.append(ing)
        newRows.append(newRow)
        i+=1

    return newRows


#main
rows=retrieveRows('data.csv')
rows, ingredients, ingredientCount, cuisines, cuisineMealCount=retrieveInfo(rows, 5, False)
rows = eliminateRowsCuisines(cuisines, rows)
rows, ingredients, ingredientCount, cuisines, cuisineMealCount=retrieveInfo(rows, 5, False)

#undersampling
rows, ingredients, ingredientCount, cuisines, cuisineMealCount=retrieveInfo(rows, 8, True)
rows=underSample(rows)
rows, ingredients, ingredientCount, cuisines, cuisineMealCount=retrieveInfo(rows, 8, True)

#oversampling
rows=overSample(rows)
rows, ingredients, ingredientCount, cuisines, cuisineMealCount=retrieveInfo(rows, 8, True)

visualizeInfo(cuisines, cuisineMealCount, ingredients, ingredientCount)
print(cuisines)
print(cuisineMealCount)
rowTrain, rowTest=divideSetsRandom(cuisines, rows)
rowTrainCV, rowTestCV=divideCVSets(cuisines, rows, 10)

createDataset(ingredients, rowTrain, "trainSet.csv")
createDataset(ingredients, rowTest, "testSet.csv")
for i in range(10):
    createDataset(ingredients, rowTrainCV[i], "trainSet"+str(i)+".csv")
    createDataset(ingredients, rowTestCV[i], "testSet"+str(i)+".csv")
    






