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
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from nltk import FreqDist

#using my parser.py file for getting the input
import parser
import re



global top_words
top_words = []

def featureAggregator(inputdata):
    """
    Given a sentence, call the feature extractor and aggregate the
    returned features into the same dataset
    """
    outputdata = []
    for inputLine in inputdata:
        # aggregate those values into 1 tuple of features
        features = featureExtractor(inputLine[3])

        # append those features
        inputLineList = list(inputLine)
        inputLineList.append(features)
        outputLineTuple = tuple(inputLineList)
        outputdata.append(outputLineTuple)

    return outputdata


def featureExtractor(sentStr):
    featList = {}
    featList['charCount'] = getCharCount(sentStr)
    featList['wordCount'] = getWordCount(sentStr)
    featList['commaCount']= getCommaCount(sentStr)
    featList['semicolonCount']= getSemicolonCount(sentStr)
    featList['uppercount']=getUpperCount(sentStr)
    featList['digitcount']=getDigitCount(sentStr)
    featList['exclaimCount'] = getExclaimCount(sentStr)


    # feature for presence of top words
    featList.update(getReviewDict(sentStr))


    return featList



# feature extraction methods
def getReviewDict(sent):

    # print parsedata[:5]
    contain_features = {}
    global top_words
    print top_words
    for word in top_words:
        contain_features['contains(%s)' % (word)] = (word in set(sent))

    return contain_features



def getCharCount(sent):
    return int(len(sent))


def getWordCount(sent):
    return len(word_tokenize(sent))

def getCommaCount(sent):
    commaRegEx = re.compile(',')

    numoccur = len([a.start() for a in commaRegEx.finditer(sent)])

    return numoccur


def getExclaimCount(sent):
    exclaimRegEx = re.compile('!')

    numoccur = len([a.start() for a in exclaimRegEx.finditer(sent)])

    return numoccur

def getSemicolonCount(sent):
    semicolonRegEx = re.compile(';')

    numoccur = len([a.start() for a in semicolonRegEx.finditer(sent)])

    return numoccur

def getUpperCount(sent):
    numoccur=0
    for i in range(len(sent)):
        i=str(i)
        if i.isupper==True:
            numoccur+=1
    return numoccur

def getDigitCount(sent):
    numoccur=0
    for i in range(len(sent)):
        i=str(i)
        if i.isdigit==True:
            numoccur+=1
    return numoccur





def main():
    userInput = parser.getInput()
    fileList = parser.getFiles(userInput['train'])
    pdata = parser.parseFiles(fileList)


    allsent = ''
    for f in pdata:
        allsent += f[3]

    all_words = FreqDist(w.lower()
                    for w in word_tokenize(allsent)
                        if w not in stopwords.words('english') )

    global top_words
    top_words = all_words.keys()[:500]

    # pdata = getParseData()
    featdata = featureAggregator(pdata)







    print featdata[:10]

    # print parsedata[:20]
    # print len(parsedata)

if __name__ == '__main__':
    main()
