#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
ClassifierTest
================
Testing classifier after training

author = "Shreyas"
email = "shreyas@ischool.berkeley.edu"
python_version = "Python 2.7.5 :: Anaconda 1.6.1 (x86_64)"
"""
from __future__ import division
from optparse import OptionParser
from cPickle import load

import parser
import extractor


def getInput():
    optionparser = OptionParser()

    optionparser.add_option('-t', '--test', dest='test')

    (option, args) = optionparser.parse_args()

    if not option.test:
        return optionparser.error('data not provided.\n Usage: --data="path.to.data"')

    return { 'test' : option.test }




def getClassifier():
    fObj = open('mySentClassifier.pickle')

    cl = load(fObj)
    fObj.close()

    return cl



def main():
    classifier = getClassifier()


    userInput = getInput()
    fileList = parser.getFiles(userInput['test'])
    pdata = parser.parseFiles(fileList)

    featdata = extractor.featureAggregator(pdata)



    output = []
    outputFileObj = open('../../output.txt', 'w')
    for featdatarow in featdata:
        cl = classifier.classify(featdatarow[4])

        if cl == 'pos':
            label = '1'
        elif cl == 'neutral':
            label = '0'
        else:
            label = '-1'

        print featdatarow[0], featdatarow[1], label
        outputRow = str(featdatarow[0]) + '\t' + str(featdatarow[1]) + '\t' + str(label) + '\n'
        output.append(outputRow)
        outputFileObj.write(outputRow)

    outputFileObj.close()








if __name__ == '__main__':
    main()
