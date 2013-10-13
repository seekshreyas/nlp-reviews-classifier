#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Classifier
==========
After Feature Extraction, that returns a data of the format
[(filename, linenum, vote, sentence, feat1, feat2, ...)]

build a classifier so that for a give new sentence it could predict
the positive, neutral or negative sentiment

author = "Shreyas"
email = "shreyas@ischool.berkeley.edu"
python_version = "Python 2.7.5 :: Anaconda 1.6.1 (x86_64)"
"""
from __future__ import division

import parser
import extractor

import math
import random
import nltk



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




def main():
    userInput = parser.getInput()
    fileList = parser.getFiles(userInput['train'])
    parsedata = parser.parseFiles(fileList)

    featdata = extractor.featureAggregator(parsedata)

    allacc = splitfeatdata(featdata)

    print "Accuracy Values: %s" % (allacc)
    print "Overall Classifier Accuracy %4.2f " % (sum(allacc)/len(allacc))






if __name__ == '__main__':
    main()

