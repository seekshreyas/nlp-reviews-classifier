#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Classifier
==========
After Feature Extraction, that returns a data of the format
[(filename, linenum, vote, sentence, feat1, feat2, ...)]

build a classifier so that for a give new sentence it could predict
the positive, neutral or negative sentiment

author = "Shreyas" and "Charles"
email = "shreyas@ischool.berkeley.edu"
python_version = "Python 2.7.5 :: Anaconda 1.6.1 (x86_64)"
"""
from __future__ import division
from nltk.tokenize import word_tokenize

import parseReview
import extractorCW

import math
import random
import nltk

import os

def splitfeatdata(rawdata, fold=10):
    """
    Randomize, Shuffle and split the data into tranining and test dataset
    """

    labeldata = []
    for row in rawdata:

        if row[2] > 0:
            label = 'pos'
        elif row[2] == 0:
            label = 'neutral'
        else:
            label = 'neg'

        labeldata.append((row[4], label))

    random.shuffle(labeldata)

    size = int(math.floor(len(labeldata) / 10.0))
    # train = labeldata[:split]
    # test = labeldata[split:]

    # code for k-fold validation referred from:
    # http://stackoverflow.com/questions/16379313/how-to-use-the-a-10-fold-cross-validation-with-naive-bayes-classifier-and-nltk
    claccuracy = []
    for i in range(fold):
        test_this_round = labeldata[i*size:][:size]
        train_this_round = labeldata[:i*size] + labeldata[(i+1)*size:]

        acc = myclassifier(train_this_round, test_this_round)

        claccuracy.append(acc)

    return claccuracy




def myclassifier(train_data, test_data):
    classifier = nltk.NaiveBayesClassifier.train(train_data)

    # print classifier.show_most_informative_features()
    return nltk.classify.accuracy(classifier, test_data)


def getTestFiles(directory):
    os.chdir("../../../")
    os.chdir(directory)
    for files in sorted(os.listdir(".")):
        if files.endswith(".txt"):
            print files
    datafiles = [f for f in os.listdir('.') if f.endswith('.txt')]
    return datafiles


def parseTestFiles(fList):
    allSents = []

    for f in fList:
        fileObj = open(f)
        linenum = 0
        for l in fileObj:
            linenum += 1
            vote = 0
            l = l.split('\t')[1].replace("\n","")
            allSents.append((f, linenum, vote, l))
        fileObj.close()
    return allSents

def printOutput(testFeatureList, trainFeatureList):
    labeldata = []
    for row in trainFeatureList:

        if row[2] > 0:
            label = 1
        elif row[2] == 0:
            label = 0
        else:
            label = -1

        labeldata.append((row[4], label))

    random.shuffle(labeldata)
    print type(labeldata)
    classifier = nltk.NaiveBayesClassifier.train(labeldata)
    os.chdir("../../../")
    f = open('output-charles.txt', 'w')
    for sentTuple in testFeatureList:
        '''
        sensitivity = 0
        if sentTuple[2] > 0:
            sensitivity = 1
        elif sentTuple[2] < 0:
            sensitivity = -1
        '''
        sensitivity = classifier.classify(sentTuple[4])
        f.write(sentTuple[0].replace(" ","") + "\t" + str(sentTuple[1]) + "\t" + str(sensitivity) + "\n")
    f.close()

def main():
    parser = parseReview
    #userInput = parser.getInput()
    #fileList = parser.getFiles(userInput['train'])
    fileList = parser.getFiles("data/raw/training")
    parsedata = parser.parseFiles(fileList)
    featdata = extractorCW.featureAggregator(parsedata)
    allacc = splitfeatdata(featdata)

    print "Accuracy Values: %s" % (allacc)
    print "Overall Classifier Accuracy %4.2f " % (sum(allacc)/len(allacc))

    print "Test product files:"
    testFileList = getTestFiles("data/raw/charles-testing")
    testParseData = parseTestFiles(testFileList)
<<<<<<< HEAD
    testFeatdata = extractorCW.featureAggregator(testParseData)
    printOutput(testFeatdata, featdata)
=======
    featdata = extractorCW.featureAggregator(testParseData)
    printOutput(featdata)
>>>>>>> f881e733a9873442c2a754ee99d8167dd5d1ef87


if __name__ == '__main__':
    main()

