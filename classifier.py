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
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import FreqDist

import parser
import extractor

import math
import random
import nltk


top_words = []

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

    print classifier.show_most_informative_features()
    return nltk.classify.accuracy(classifier, test_data)




def main():
    userInput = parser.getInput()
    fileList = parser.getFiles(userInput['train'])
    parsedata = parser.parseFiles(fileList)


    allsent = ''
    for f in parsedata:
        allsent += f[3]

    all_words = FreqDist(w.lower()
                    for w in word_tokenize(allsent)
                        if w not in stopwords.words('english') )

    global top_words
    top_words = all_words.keys()[:500]


    featdata = extractor.featureAggregator(parsedata)



    # print featdata[20]




    print "Sample Data Item:\n\n"

    print "%20s %4s %4s %20s" % ("FILENAME", "LINENUM", "VOTE", "SENTENCE" )
    print "-" * 79
    print "%10s %4s %4s %20s" % (featdata[20][0], featdata[20][1], featdata[20][2], featdata[20][3])

    print "\n\nFeatures of this Data Item"
    print "-" * 79
    for key,val in featdata[20][4].items():
        print "%50s : %10s" % (key, val )
    # print  "A sample feature: %s" % (featdata[20][4])




    allacc = splitfeatdata(featdata)

    print "\n\n"
    print "-" * 60
    print "Accuracy Values: %s" % (allacc)
    print "==" * 60
    print "Overall Classifier Accuracy %4.4f " % (sum(allacc)/len(allacc))






if __name__ == '__main__':
    main()

