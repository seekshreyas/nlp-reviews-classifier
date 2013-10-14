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

from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures as BAM
from itertools import chain


from nltk import FreqDist

#using my parser.py file for getting the input
import parser
import re, nltk




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

    sentwords = getWordsFromSent(sentStr)

    featList = {}

    featList['charCount'] = getCharCount(sentStr)
    # featList['wordCount'] = getWordCount(sentStr)
    # featList['commaCount']= getCommaCount(sentStr)
    # featList['semicolonCount']= getSemicolonCount(sentStr)
    # featList['uppercount']=getUpperCount(sentStr)
    # featList['digitcount']=getDigitCount(sentStr)
    # featList['exclaimCount'] = getExclaimCount(sentStr)
    # featList['whiteSpaceCount'] = getWhiteSpaceCount(sentStr)
    # featList['tabCount'] = getTabCount(sentStr)
    # featList['percentCount'] = getPercentCount(sentStr)    
    # featList['etcCount'] = getEtcCount(sentStr)
    # featList['dollarCount'] = getDollarCount(sentStr)
    # featList["avgWordLen"]= getAvgWordLen(sentStr)
    # featList["wordLen6"]= getWordLen6(sentStr)
    #featList["uniqueWords"]= getUniqueWords(sentStr)
    # featList["countJJ"]=getCountJJ(sentStr)
    # featList["countCC"]=getCountCC(sentStr)
    #featList.update(getReviewDict(sentStr))
    # featList["countIN"]=getCountIN(sentStr)
    # featList["countRB"]=getCountRB(sentStr)
    # featList["countPRP"]=getCountPRP(sentStr)
    # featList["countTO"]=getCountTO(sentStr)
    # featList["countVBD"]=getCountVBD(sentStr)
    # featList["countJJR"]=getCountJJR(sentStr)
    # featList["countNN"]=getCountNN(sentStr)
    # featList["countNNS"]=getCountNNS(sentStr)
    # featList["countNNP"]=getCountNNP(sentStr)
    # featList["countRB"]=getCountRB(sentStr)
    # featList["countVBG"]=getCountVBG(sentStr)
    # featList["countVBZ"]=getCountVBZ(sentStr)
    # featList["countVBP"]=getCountVBP(sentStr)
    # featList["countVBN"]=getCountVBN(sentStr)
    # featList["countMD"]=getCountMD(sentStr)
    # featList["countWDT"]=getCountWDT(sentStr)
    # featList["countPRPA"]=getCountPRPA(sentStr)
    # featList["countJN"]=getCountJN(sentStr)
    # featList["countRJ"]=getCountRJ(sentStr)
    # featList["countJJC"]=getCountJJC(sentStr)
    # featList["countNJ"]=getCountNJ(sentStr)
    # featList["countRV"]=getCountRV(sentStr)

    featList.update(getUnigramWordFeatures(sentStr, sentwords))
    #featList.update(getBigramWordFeatures(sentStr, sentwords))


    return featList



def getWordsFromSent(sent):
    words = [w.lower() for w in word_tokenize(sent)
                if w
                    not in stopwords.words('english')
                    # and len(w) > 1
            ]
    return words



# feature extraction methods
def getReviewDict(sent):

    # print parsedata[:5]
    contain_features = {}
    global top_words
    for word in top_words:
        contain_features['contains(%s)' % (word)] = (word in set(sent))

    return contain_features


def getUnigramWordFeatures(sent, words):

    return dict((word, True) for word in words)


def getBigramWordFeatures(sent, words, score_fn=BAM.chi_sq, n=200):

    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)

    return dict((bg, True) for bg in chain(words, bigrams))




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

def getWhiteSpaceCount(sent):
    whitespaceRegEx = re.compile(' ')

    numoccur = len([a.start() for a in whitespaceRegEx.finditer(sent)])

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

def getTabCount(sent):
    tabRegEx = re.compile('    ')

    numoccur = len([a.start() for a in tabRegEx.finditer(sent)])

    return numoccur

def getPercentCount(sent):
    numoccur=0
    for i in sent:
        i=str(i)
        if i== '%':
            numoccur+=1
    return numoccur

def getEtcCount(sent):
    numoccur=0
    for i in sent:
        i=str(i)
        if i== 'etc.':
            numoccur+=1
    return numoccur

def getDollarCount(sent):
    numoccur=0
    for i in sent:
        i=str(i)
        if i== '$':
            numoccur+=1
    return numoccur

def getAvgWordLen(sent):
    avg, total = 0,0
    sent=sent.split(" ")
    ln= len(sent)
    if ln>0:
        for i in sent:
            i=str(i)
            lnword=len(i)
            total=total+lnword
        avg=total/ln
    return avg 

def getWordLen6(sent):
    numoccur = 0
    for i in sent:
        if len(i)>= 6:
            numoccur+=1
    return numoccur

def getUniqueWords(sent):
    word=[]
    wunique=0
    for item in sent:
        if item not in word:
            wunique+=1
    return wunique

def getCountJJ(sent):
    countjj= 0 
    sent= nltk.word_tokenize(sent)
    text=nltk.pos_tag(sent)
    for i in range(len(sent)):
        if text[i][1]=="JJ":
            countjj+=1
    return countjj

def getCountCC(sent):
    countcc= 0 
    sent= nltk.word_tokenize(sent)
    text=nltk.pos_tag(sent)
    for i in range(len(sent)):
        if text[i][1]=="CC":
            countcc+=1
    return countcc

def getCountIN(sent):
    countin= 0 
    sent= nltk.word_tokenize(sent)
    text=nltk.pos_tag(sent)
    for i in range(len(sent)):
        if text[i][1]=="IN":
            countin+=1
    return countin

def getCountRB(sent):
    countrb= 0 
    sent= nltk.word_tokenize(sent)
    text=nltk.pos_tag(sent)
    for i in range(len(sent)):
        if text[i][1]=="RB":
            countrb+=1
    return countrb

def getCountPRP(sent):
    countprp= 0 
    sent= nltk.word_tokenize(sent)
    text=nltk.pos_tag(sent)
    for i in range(len(sent)):
        if text[i][1]=="PRP":
            countprp+=1
    return countprp

def getCountTO(sent):
    countto= 0 
    sent= nltk.word_tokenize(sent)
    text=nltk.pos_tag(sent)
    for i in range(len(sent)):
        if text[i][1]=="TO":
            countto+=1
    return countto

def getCountVBD(sent):
    countvbd= 0 
    sent= nltk.word_tokenize(sent)
    text=nltk.pos_tag(sent)
    for i in range(len(sent)):
        if text[i][1]=="VBD":
            countvbd+=1
    return countvbd


def getCountJJR(sent):
    countjjr= 0 
    sent= nltk.word_tokenize(sent)
    text=nltk.pos_tag(sent)
    for i in range(len(sent)):
        if text[i][1]=="JJR":
            countjjr+=1
    return countjjr

def getCountNN(sent):
    countnn= 0 
    sent= nltk.word_tokenize(sent)
    text=nltk.pos_tag(sent)
    for i in range(len(sent)):
        if text[i][1]=="NN":
            countnn+=1
    return countnn

def getCountNNS(sent):
    countnns= 0 
    sent= nltk.word_tokenize(sent)
    text=nltk.pos_tag(sent)
    for i in range(len(sent)):
        if text[i][1]=="NNS":
            countnns+=1
    return countnns

def getCountNNP(sent):
    countnnp= 0 
    sent= nltk.word_tokenize(sent)
    text=nltk.pos_tag(sent)
    for i in range(len(sent)):
        if text[i][1]=="NNP":
            countnnp+=1
    return countnnp

def getCountRBR(sent):
    countrbr= 0 
    sent= nltk.word_tokenize(sent)
    text=nltk.pos_tag(sent)
    for i in range(len(sent)):
        if text[i][1]=="RBR":
            countrbr+=1
    return countrbr

def getCountVB(sent):
    countvb= 0 
    sent= nltk.word_tokenize(sent)
    text=nltk.pos_tag(sent)
    for i in range(len(sent)):
        if text[i][1]=="VB":
            countvb+=1
    return countvb

def getCountVBP(sent):
    countvbp= 0 
    sent= nltk.word_tokenize(sent)
    text=nltk.pos_tag(sent)
    for i in range(len(sent)):
        if text[i][1]=="VBP":
            countvbp+=1
    return countvbp

def getCountVBZ(sent):
    countvbz= 0 
    sent= nltk.word_tokenize(sent)
    text=nltk.pos_tag(sent)
    for i in range(len(sent)):
        if text[i][1]=="VBZ":
            countvbz+=1
    return countvbz

def getCountVBG(sent):
    countvbg= 0 
    sent= nltk.word_tokenize(sent)
    text=nltk.pos_tag(sent)
    for i in range(len(sent)):
        if text[i][1]=="VBG":
            countvbg+=1
    return countvbg

def getCountVBN(sent):
    countvbn= 0 
    sent= nltk.word_tokenize(sent)
    text=nltk.pos_tag(sent)
    for i in range(len(sent)):
        if text[i][1]=="VBN":
            countvbn+=1
    return countvbn

def getCountMD(sent):
    countmd= 0 
    sent= nltk.word_tokenize(sent)
    text=nltk.pos_tag(sent)
    for i in range(len(sent)):
        if text[i][1]=="MD":
            countmd+=1
    return countmd

def getCountWDT(sent):
    countwdt= 0 
    sent= nltk.word_tokenize(sent)
    text=nltk.pos_tag(sent)
    for i in range(len(sent)):
        if text[i][1]=="WDT":
            countwdt+=1
    return countwdt

def getCountPRPA(sent):
    countprpa= 0 
    sent= nltk.word_tokenize(sent)
    text=nltk.pos_tag(sent)
    for i in range(len(sent)):
        if text[i][1]=="PRP$":
            countprpa+=1
    return countprpa

def getCountJN(sent):
    countjn= 0 
    sent= nltk.word_tokenize(sent)
    text=nltk.pos_tag(sent)
    for i in range(len(text)):
        if text[i][1]=="JJ" and text[i+1][1]=="NN": countjn+=1
        if x[i][1]=="JJ" and x[i+1][1]=="NNS": countjn+=1
    return countjn

def getCountRJ(sent):
    countrj= 0 
    sent= nltk.word_tokenize(sent)
    text=nltk.pos_tag(sent)
    for i in range(len(text)):
        if x[i][1]=="RB" and x[i+1][1]=="JJ": countrj+=1
        if x[i][1]=="RBR" and x[i+1][1]=="JJ": countrj+=1
        if x[i][1]=="RBS" and x[i+1][1]=="JJ": countrj+=1
    return countrj

def getCountJJC(sent):
    countjjc= 0 
    sent= nltk.word_tokenize(sent)
    text=nltk.pos_tag(sent)
    for i in range(len(text)):
        if x[i][1]=="JJ" and x[i+1][1]=="JJ": countjjc +=1
    return countjjc

def getCountNJ(sent):
    countnj= 0 
    sent= nltk.word_tokenize(sent)
    text=nltk.pos_tag(sent)
    for i in range(len(text)):
        if x[i][1]=="NNS" and x[i+1][1]=="jj": countnj+=1
    return countnj

def getCountRV(sent):
    countrv= 0 
    sent= nltk.word_tokenize(sent)
    text=nltk.pos_tag(sent)
    for i in range(len(text)):
        if x[i][1]=="RR" and x[i+1][1]=="VB": countrv+=1
        if x[i][1]=="RBS" and x[i+1][1]=="VBN": countrv+=1
        if x[i][1]=="RBR" and x[i+1][1]=="VBD": countrv+=1
        if x[i][1]=="RR" and x[i+1][1]=="VB": countrv+=1
        if x[i][1]=="RBR" and x[i+1][1]=="VBN": countrv+=1
        if x[i][1]=="RBS" and x[i+1][1]=="VBD": countrv+=1
        if x[i][1]=="RR" and x[i+1][1]=="VB": countrv+=1
        if x[i][1]=="RBR" and x[i+1][1]=="VBN": countrv+=1
        if x[i][1]=="RBS" and x[i+1][1]=="VBD": countrv+=1
        if x[i][1]=="RR" and x[i+1][1]=="VBG": countrv+=1
        if x[i][1]=="RBR" and x[i+1][1]=="VBG": countrv+=1
        if x[i][1]=="RBS" and x[i+1][1]=="VBG": countrv+=1
    return countrv



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
