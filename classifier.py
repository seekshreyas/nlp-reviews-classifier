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
import random


def splitfeatdata(rawdata, frac=0.9):
    """
    Randomize, Shuffle and split the data into tranining and test dataset
    """
    random.shuffle(rawdata)

    split = int(len(rawdata) * frac)
    train = rawdata[:split]
    test = rawdata[split:]

    return (train, test)




def main():
    userInput = parser.getInput()
    fileList = parser.getFiles(userInput['train'])
    parsedata = parser.parseFiles(fileList)

    featdata = extractor.featureAggregator(parsedata)
    (traindata, testdata) = splitfeatdata(featdata, 0.75)





if __name__ == '__main__':
    main()
