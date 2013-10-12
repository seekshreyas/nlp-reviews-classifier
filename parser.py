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

        allSents.extend(l for l in fileObj if not l.startswith('*') and not l.startswith('[t]'))

    return allSents


def main():
    userInput = getInput()
    fileList = getFiles(userInput['train'])
    sents = parseFiles(fileList)

    print fileList
    print sents[:20]


if __name__ == "__main__":
    main()

