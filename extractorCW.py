#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Extractor
=========
After parsing, given a list of tuples of the format:
[(filename, linenumber, aggregatevote, sentence)]

output a list of tuples with
[(filename, linenumber, aggregatevote, sentence, {feat1, feat2, ..})]

author = "Shreyas" and "Charles"
email = "shreyas@ischool.berkeley.edu"
python_version = "Python 2.7.5 :: Anaconda 1.6.1 (x86_64)"
"""
from __future__ import division
from nltk.tokenize import word_tokenize

#using my parser.py file for getting the input
import os, sys, re
test_folder = os.path.abspath(os.getcwd())
sys.path.append(test_folder)
import parseReview
import nltk



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
        outputLineTuple = inputLineList

        # calculate new aggregatevote based on feature returned values
        outputLineTuple = tuple(featureCalculator(outputLineTuple))
        
        outputdata.append(outputLineTuple)

    return outputdata


def featureExtractor(sentStr):
    featList = {}
    #featList['charCount'] = getCharCount(sentStr)
    #featList['wordCount'] = getWordCount(sentStr)
    featList['upperCount'] = getUpperCount(sentStr)
    featList['postiveWordCount'] = getPostiveWordCount(sentStr)
    featList['negativeWordCount'] = getNegativeWordCount(sentStr)
    featList['bigramBeginWithNotCount'] = getBigramBeginWithNotCount(sentStr)

    return featList

def featureCalculator(sentTuple):
    sentTuple_update = sentTuple
    featureDir = sentTuple[4]
    current_vote = sentTuple_update[2] 
    new_vote = current_vote - featureDir['upperCount'] - featureDir['negativeWordCount'] + featureDir['postiveWordCount'] + 2 * featureDir['bigramBeginWithNotCount']
    sentTuple_update[2] = new_vote
    return sentTuple_update


# feature extraction methods
def getCharCount(sent):
    return int(len(sent))


def getWordCount(sent):
    return len(word_tokenize(sent))

def getUpperCount(sent):
    uppercase_meaningless_words = ["A", "I", "IPOD", "USB", "MP3", "CD", "FM", "GB", "PC", "LCD", "MP-3", "WMA", "WMP",
                               "AC/DC", "PDA", "PXC250", "XP", "LED", "AC", "AGK", "DVD", "SD", "MB"]
    upperCount = 0
    for word in sent.split(" "): 
        word = word.replace(".","").replace(",","").replace("!","").replace("?","").replace("##","").replace("(","").replace(")","").replace("**","")
        for letter in word:
            if letter.isdigit():
                word = word.replace(letter, "")
            else:
                break
        if word.isupper() and len(word) != 1 and not word in uppercase_meaningless_words:
            upperCount += 1
    return upperCount

def getPostiveWordCount(sent):
    positive_keywords = ["good", "happy", "love", "great", "reasonable", "glad", "simple", "outstanding", "easy",
                     "wonderful", "cool", "remarkably", "remarkable", "enjoy", "nice", "thoughtful", "pretty",
                     "responsive", "comforatable", "favorite", "desire", "best", "solid", "cool", "impressed",
                     "sleek", "appealing", "rocks", "blazing", "amazing", "plus", "blessing", "awesome", "loved",
                        "enjoyed", "desired", "impressive", "impress", "rocked", "bless", "positive", "fabulous"]
    postiveCount = 0
    for word in sent.split(" "): 
        word = word.replace(".","").replace(",","").replace("!","").replace("?","").replace("##","").replace("(","").replace(")","").replace("**","")
        if word.lower() in positive_keywords:
            postiveCount += 1
    return postiveCount

def getNegativeWordCount(sent):
    negative_keywords = ["bad", "sad", "don't", "could not", "crappy", "unfortunately", "remove", "why", "poor",
                     "bothersome", "terrible", "although", "complaints", "outrageous", "isn't", "poorly",
                     "drawback", "annoying", "against", "irritating", "wouldn't", "won't", "wasn't", "couldn't",
                     "awful", "didn't", "hasn't", "difficult", "hate", "incorrect", "junk", "trash", "removed",
                         "complain", "complained", "hated", "negative"]
    negativeCount = 0
    for word in sent.split(" "): 
        word = word.replace(".","").replace(",","").replace("!","").replace("?","").replace("##","").replace("(","").replace(")","").replace("**","")
        if word.lower() in negative_keywords:
            negativeCount += 1
    return negativeCount

def getBigramBeginWithNotCount(sent):
    negative_keywords = ["bad", "sad", "don't", "could not", "crappy", "unfortunately", "remove", "why", "poor",
                     "bothersome", "terrible", "although", "complaints", "outrageous", "isn't", "poorly",
                     "drawback", "annoying", "against", "irritating", "wouldn't", "won't", "wasn't", "couldn't",
                     "awful", "didn't", "hasn't", "difficult", "hate", "incorrect", "junk", "trash", "removed",
                         "complain", "complained", "hated", "negative"]
    bigramPostiveCount = 0
    '''
    from nltk.corpus import brown
    brown_tagged_sents = brown.tagged_sents(categories='news')
    brown_sents = brown.sents(categories='news')
    unigram_tagger = nltk.UnigramTagger(brown_tagged_sents)
      
    for bigram in nltk.bigrams(word_tokenize(sent)):
        if bigram[0].lower() == "not" and bigram[1].lower() in negative_keywords:
            print sent
            print bigram
            print unigram_tagger.tag(word_tokenize(sent))
            bigramNotCount += 1
    '''
    for i, word in enumerate(word_tokenize(sent)): 
        if word.lower() == "not":
            if word_tokenize(sent)[i + 1] in negative_keywords : # e.g. NOT bad
                bigramPostiveCount += 1
            if i < len(word_tokenize(sent)) - 2 and word_tokenize(sent)[i + 2] in negative_keywords: # e.g. NOT too bad
                bigramPostiveCount += 1
            else:                                                # e.g. NOT good
                bigramPostiveCount -= 1
    return bigramPostiveCount        


def main():
    parser = parseReview
    #userInput = parser.getInput()
    fileList = parser.getFiles("data/raw/charles")
    parsedata = parser.parseFiles(fileList)

    featdata = featureAggregator(parsedata)

    print featdata[:10]

    # print parsedata[:20]
    # print len(parsedata)

if __name__ == '__main__':
    main()
