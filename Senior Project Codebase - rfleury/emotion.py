import json
import pandas as pd
#import pickle
from consts import FEATURE_NUMBER

with open("friends_test.json") as f:
    testData = json.load(f)

with open('friends_train.json') as f:
    trainData = json.load(f)

# print(len(trainData))

#dictionary creation for files
trainDict = { "speaker":[], 
                "utterance":[], 
                "emotion":[], 
                "annotation":[] }
                                
testDict = { "speaker":[], 
                "utterance":[], 
                "emotion":[], 
                "annotation":[] }

#append data to the dictionary
for entry in trainData:
    for info in entry:
        trainDict["speaker"].append(info["speaker"])
        trainDict["utterance"].append(info["utterance"])
        trainDict["emotion"].append(info["emotion"])
        trainDict["annotation"].append(info["annotation"])

for entry in testData:
    for info in entry:
        testDict["speaker"].append(info["speaker"])
        testDict["utterance"].append(info["utterance"])
        testDict["emotion"].append(info["emotion"])
        testDict["annotation"].append(info["annotation"])

#convert to a pandas dataframe
trainData = pd.DataFrame(trainDict)
testData = pd.DataFrame(testDict)

#drop the unecessary information from the input
trainData= trainData.drop(labels="speaker", axis = 1)
trainData= trainData.drop(labels="annotation", axis = 1)
testData= testData.drop(labels="speaker", axis = 1)
testData= testData.drop(labels="annotation", axis = 1)

#for feature extraction on the training text
from sklearn.feature_extraction.text import TfidfVectorizer
vectorBoi = TfidfVectorizer(max_features=FEATURE_NUMBER, stop_words= "english")

trainVext = vectorBoi.fit_transform(trainData["utterance"]) #transforming of training sentences
testVect = vectorBoi.transform(testData["utterance"]) #transforming of testing sentences
#print(len(trainData["utterance"]))

#function for testing purposes only
def buildAndTestKernel():
    from sklearn import svm
    from sklearn.svm import SVC
    clf = svm.SVC(kernel = 'poly', class_weight= "balanced")
    clf.fit(trainVext, trainData["emotion"])

    prediction = clf.predict(testVect)

    from sklearn.metrics import classification_report
    print(classification_report(prediction, testData["emotion"]))

    from sklearn import metrics
    print("Accuracy:",metrics.accuracy_score(prediction, testData["emotion"]))

#INFO: Uncomment this function and run file to see the current prediction accuracy
#buildAndTestKernel()

#function builds the kernal that is for the prediction of emotion
def buildKernal():

    from sklearn import svm
    from sklearn.svm import SVC
    clf = svm.SVC(kernel = 'poly', class_weight= "balanced")
    clf.fit(trainVext, trainData["emotion"])
    
    # prediction = clf.predict(testVect)
    
    #X-train - texts sanmples- amt 9061
    #X_test - tests sanmples- amt 2266
    #Y_train - emotion lables- amt 9061
    #Y_test - emotion lables- amt 2266

    # from sklearn.metrics import classification_report
    # print(classification_report(testData["emotion"], prediction))

    # from sklearn import metrics
    # print("Accuracy:",metrics.accuracy_score(testData["emotion"], prediction))

    return clf



