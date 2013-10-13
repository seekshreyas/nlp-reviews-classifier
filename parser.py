#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Parser
========
Parse the txt files for collecting reviews

author = "Shreyas"
email = "shreyas@ischool.berkeley.edu"
python_version = "Python 2.7.5 :: Anaconda 1.6.1 (x86_64)"
"""
from __future__ import division
from optparse import OptionParser

import os
import re



def getInput():
    parser = OptionParser()

    parser.add_option('-t', '--train', dest='train')

    (option, args) = parser.parse_args()

    if not option.train:
        return parser.error('data not provided.\n Usage: --data="path.to.data"')

    return { 'train' : option.train }


def getFiles(dir):
    # os.lisdir(dir)
    os.chdir(dir)
    datafiles = [f for f in os.listdir('.') if f.endswith('.txt')]
    return datafiles


def parseFiles(fList):
    allSents = []

    for f in fList:
        fileObj = open(f)

        for l in fileObj:
            if not l.startswith('*') and not l.startswith('[t]'):

                #find all occurrence of ## in the sentence
                delimPos = [(a.start(), a.end()) for a in list(re.finditer('##', l))]

                if len(delimPos) == 0:
                    # no reviews in a sentence
                    feat = 'None'
                    rev = 'N.A.'
                    print l
                elif len(delimPos) == 1:
                    #simple case of only 1 sentence
                    feat = l.split('##')[0]
                    vote = getVotes(feat)
                    rev = l.split('##')[1]
                    allSents.append((vote, rev))



                else:
                    # more than 1 reviews in a sentence
                    feat1 = l.split('##')[0]
                    rev2_raw = l.split('##')[2]
                    rev1_feat2 = l.split('##')[1]

                    rev2 = cleanReview(rev2_raw)
                    vote1 = getVotes(feat1)
                    vote2 = getVotes(rev1_feat2)

                    # print l
                    # print vote1, vote2


        fileObj.close()

    return allSents



def cleanReview(revstr):
    """
    return the cleaned up review after getting a raw string
    """
    eolregEx = '/[\.|\?]'
    eol = re.compile(eolregEx)

    m = eol.match(revstr)

    # print m







def getVotes(rawstr):
    voteRegEx = '\[[\+\-][0-3]?\]'

    vote = re.compile(voteRegEx)
    vote_raw = vote.findall(rawstr)

    if len(vote_raw) == 0:
        # rev1 = rawstr
        # feat2 = 0
        meanvote = 0.0

    else:
        votes = []
        for vote in vote_raw:
            v = vote[1:-1]
            if v == '+':
                vt = 1
            elif v == '-':
                vt = -1
            else:
                vt = int(v)

            votes.append(vt)

        meanvote = sum(votes)/len(votes)

    return meanvote



def main():
    userInput = getInput()
    fileList = getFiles(userInput['train'])
    sents = parseFiles(fileList)

    # print fileList

    print "-" * 79
    print "No. of files parsed: %d" % (len(fileList))
    print sents[:20]
    print "Total No of sentences: %d" % (len(sents))


if __name__ == "__main__":
    main()

