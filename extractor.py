#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Extractor
=========
After parsing, given a list of tuples of the format:
[(filename, linenumber, aggregatevote, sentence)]

output a list of tuples with
[(filename, linenumber, aggregatevote, sentence, feat1, feat2, ..)]

author = "Shreyas"
email = "shreyas@ischool.berkeley.edu"
python_version = "Python 2.7.5 :: Anaconda 1.6.1 (x86_64)"
"""
from __future__ import division
from optparse import OptionParser
from nltk.tokenize import word_tokenize

import os

#using my parser.py file for getting the input
import parser

def getInput():
    optionparser = OptionParser()

    optionparser.add_option('-t', '--train', dest='train')

    (option, args) = optionparser.parse_args()

    if not option.train:
        return optionparser.error('data not provided.\n Usage: --data="path.to.data"')

    return { 'train' : option.train }


def getFiles(dir):
    # os.lisdir(dir)
    os.chdir(dir)
    datafiles = [f for f in os.listdir('.') if f.endswith('.txt')]
    return datafiles


def featureAggregator(inputdata):
    """
    Given a sentence, call the feature extractor and aggregate the
    returned features into the same dataset
    """
    outputdata = []
    for inputLine in inputdata:
        # methods to return values of the features
        charCount = getCharCount(inputLine[3])
        wordCount = getWordCount(inputLine[3])

        # aggregate those values into 1 tuple of features
        features = (charCount, wordCount)

        # append those features
        inputLineList = list(inputLine)
        inputLineList.extend(features)
        outputLineTuple = tuple(inputLineList)
        outputdata.append(outputLineTuple)

    return outputdata

def getCharCount(sent):
    return int(len(sent))


def getWordCount(sent):
    return len(word_tokenize(sent))

def main():
    userInput = getInput()
    fileList = getFiles(userInput['train'])

    parsedata = parser.parseFiles(fileList)

    featdata = featureAggregator(parsedata)

    print featdata[:10]

    # print parsedata[:20]
    # print len(parsedata)

if __name__ == '__main__':
    main()