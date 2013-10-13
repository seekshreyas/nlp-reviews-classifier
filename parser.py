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
                voteRegEx = '\[[\+\-][0-3]?\]'

                vote = re.compile(voteRegEx)

                # if len(delimPos) != 1:
                #     print l, delimPos
                # else:
                #     print delimPos

                if len(delimPos) == 0:
                    # no reviews in a sentence
                    feat = 'None'
                    rev = 'N.A.'
                elif len(delimPos) == 1:
                    #simple case of only 1 sentence
                    feat = l.split('##')[0]
                    rev = l.split('##')[1]
                    allSents.append((feat, rev))

                else:
                    # more than 1 reviews in a sentence
                    feat1 = l.split('##')[0]
                    rev2 = l.split('##')[2]
                    rev1_feat2 = l.split('##')[1]

                    # print l

                    print vote.findall(rev1_feat2)
                    # print list(re.finditer(voteRegEx, rev1_feat2))

                    # print [(v.start(), v.end()) for v in list(re.finditer(voteRegEx, rev1_feat2))]



        fileObj.close()

    return allSents


def main():
    userInput = getInput()
    fileList = getFiles(userInput['train'])
    sents = parseFiles(fileList)

    # print fileList

    print "-" * 79
    print "No. of files parsed: %d" % (len(fileList))
    # print sents[:20]
    print "Total No of sentences: %d" % (len(sents))


if __name__ == "__main__":
    main()

