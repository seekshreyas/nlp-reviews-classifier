#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Writeup
==========
My tasks were:
    Project Scaffolding + Parsing + Feature Extraction

author = "Shreyas"
email = "shreyas@ischool.berkeley.edu"
python_version = "Python 2.7.5 :: Anaconda 1.6.1 (x86_64)"
"""

from __future__ import division
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures as BAM
from nltk.metrics import TrigramAssocMeasures as TAM

from itertools import chain


from nltk import FreqDist

#using my parser.py file for getting the input
import parser

import re
import os
import nltk




def scaffolding():
    """
    Scaffolding
    =============
    The project was organized into 3 separate files:
    @files:
        - parser.py
        - extractor.py
        - classifier.py

    Each file was treated as an independent COMPOSABLE part, which could
    be run independently as well as imported into other programs to pass
    the output. Hence all of those files were written so as to handle
    userinput from the command line via flags.

    This helped us checking errors separately as well as a whole.
    For eg,
    we could run

        - $python extractor.py --train="<path.to.datafolder>"

    to check just our feature extraction

    whereas we could also run

        - $python classifier.py --train="<path.to.datafolder>"

    to check our overall classification
    """
    print scaffolding.__doc__




    # helper methods
    def getWordsFromSent(sent):
        """
        Get words from a sentence with/without stopwords, by quickly
        modifying this method for different varations of words
        """
        words = [w.lower() for w in word_tokenize(sent)
                    if w
                        not in stopwords.words('english')
                        # and len(w) > 1
                ]
        return words




    def getTaggedSents(sentWords):
        """
        Get POS tagged words from a sentence
        """
        return nltk.pos_tag(sentWords)



    def parseOpinionLexicon():
        """
        Get a list of 'positive' and 'negative' words from lexicon
        maintained by Bing Liu

        url: http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html
        """

        # print os.getcwd()
        opinionLexPath = '../../../lexicon/opinionwords/'

        posfileObj = open(opinionLexPath + 'positive-words.txt')
        negfileObj = open(opinionLexPath + 'negative-words.txt')

        lexWords = {}
        lexWords['positive'] = [l[:-2] for l in posfileObj if not l.startswith(';') and l[:-2] is not '']
        lexWords['negative'] = [l[:-2] for l in negfileObj if not l.startswith(';') and l[:-2] is not '']

        posfileObj.close()
        negfileObj.close()

        return lexWords



    ##
    ## My FEATURE EXTRACTION METHODS
    ##

    def getReviewDict(sent):
        """
        Constructed a list of top 200 words from all the review sentences,
        and then given a new sentence checked for the presence of those
        top words.
        Format:
            contains('<word>') : True/False

        Note: turned this feature off because of computation expense and
        in favor of simple unigram feature
        """

        # print parsedata[:5]
        contain_features = {}
        global top_words
        for word in top_words:
            contain_features['contains(%s)' % (word)] = (word in set(sent))

        return contain_features



    def getUnigramWordFeatures(sent, words):
        """
        Simple unigram presence/absence feature
        """
        return dict(('contains("%s")' % word, True) for word in words)



    def getBigramWordFeatures(sent, words, score_fn=BAM.pmi, n=200):
        """
        Bigram Feature : True/False
        """

        bigram_finder = BigramCollocationFinder.from_words(words)
        # score = bigram_finder.score_ngrams(BAM.jaccard)

        bigrams = bigram_finder.nbest(score_fn, n)

        return dict((bg, True) for bg in chain(words, bigrams))


    def getSentOverallOpinion(sent, words, opinioncorpus):
        """
        Score of a sentence from Bing Liu's Opinion lexicon,
        normalized by length of a sentence
        """
        score = 0.0

        if len(words) != 0:
            for w in words:
                if w in opinioncorpus['positive']:
                    score += 1.0
                elif w in opinioncorpus['negative']:
                    score -= 1.0

            return score/len(words)
        else:
            return score


    def getCharCount(sent):
        """
        Total Chars : <num>
        Normalization toggle-able
        """
        # return int(len(sent))/len(sent)
        return int(len(sent))


    def getWordCount(sent):
        """
        Total Words: <num>
        Normalization toggle-able
        """
        # return len(word_tokenize(sent))/len(sent)
        return len(word_tokenize(sent))

    def getCommaCount(sent):
        """
        Total Comma counts : <num>
        Normalization toggle-able
        """
        commaRegEx = re.compile(',')
        numoccur = len([a.start() for a in commaRegEx.finditer(sent)])
        # return numoccur/len(sent)
        return numoccur


    def getExclaimCount(sent):
        """
        Total ! counts : <num>
        Normalization toggle-able
        """
        exclaimRegEx = re.compile('!')
        numoccur = len([a.start() for a in exclaimRegEx.finditer(sent)])
        # return numoccur/len(sent)
        return numoccur



    def getAdjOpinionScore(tagSent, opinioncorpus):
        """
        Adj Score (using opinion corpus) : num
        """
        score = 0
        for (word, tag) in tagSent:

            if tag == 'JJ' or tag == 'ADV' or tag == 'VBG' or tag == 'RB' or tag == 'VBZ' or tag == 'JJS':

                if word in opinioncorpus['positive']:
                    print word
                    score += 1
                if word in opinioncorpus['negative']:
                    score -= 1

        return score


    # Print Methods and Method names
    # Print Methods and Method names
    print "My Helper Methods"
    print "-" * 79
    print "\n\n"

    print ">>>", getWordsFromSent.__name__,'()', getWordsFromSent.__doc__
    print ">>>", getTaggedSents.__name__,'()', getTaggedSents.__doc__
    print ">>>", parseOpinionLexicon.__name__,'()',parseOpinionLexicon.__doc__
    print ">>>", getReviewDict.__name__,'()', getReviewDict.__doc__


    print "My FeatureExtraction Methods"
    print "-" * 79
    print "\n\n"

    print ">>>", getReviewDict.__name__,'()', getReviewDict.__doc__
    print ">>>", getUnigramWordFeatures.__name__,'()', getUnigramWordFeatures.__doc__
    print ">>>", getBigramWordFeatures.__name__,'()', getBigramWordFeatures.__doc__
    print ">>>", getSentOverallOpinion.__name__,'()', getSentOverallOpinion.__doc__
    print ">>>", getCharCount.__name__,'()', getCharCount.__doc__
    print ">>>", getWordCount.__name__,'()', getWordCount.__doc__
    print ">>>", getCommaCount.__name__,'()', getCommaCount.__doc__
    print ">>>", getExclaimCount.__name__,'()', getExclaimCount.__doc__
    print ">>>", getAdjOpinionScore.__name__,'()', getAdjOpinionScore.__doc__


def parsing():
    """
    Parsing
    =========
    @file: parser.py

    Given a folder (supplied via a flag on command line), it looks for
    all the *.txt files in the folder, reads each line looking for '##'
    tagged lines, parses and organizes them into a list of tuples of
    the format:
        [(filename, linenumber, aggregatevote, sentence)]


    Error handling:
    - line with no '##' tags:           REJECTED
    - line with 2 '##' tags:            ACCEPTED

    """
    print parsing.__doc__



def extraction():
    """
    Extraction
    ==================
    @file: extractor.py


    Given a list of tuples of the format:
        [(filename, linenumber, aggregatevote, sentence)]

    returned from parser.py, each tuple is expanded to contain a dictionary
    of features, now represented as:
        [(
            filename, linenumber, aggregatevote, sentence,
            {
                feat[key1]:val1,
                feat[key2]:val2,
                ...
            }
        )]

    features are returned via separate methods in featureExtractor() that
    works on every sentence and those features are then aggregated in
    featureAggregator()

    This is the format that was agreed in the group. This kind of modularity
    allowed us to develop and assimilate each other's feature easily, and
    quickly check how each feature is performing on our classifier by
    simply commenting out other feature return values

    Methods below are features that I developed for classification, pasted
    here for evaluation. The overall features of our group can be found in
    extractor.py
    """
    print extraction.__doc__



def classification():
    """
    Classification
    ================
    @file: classifier.py

    Given a list of tuples containing sentence and feature, it reclassifies
    aggregatevote value in the dataset to:
        - positive
        - neutral
        - negative

    This forms our consolidated dataset for classification. This list is then
        - randomly shuffled
        - partitioned into K-folds
        - trained on (K-1) K-folds
        - tested on 1 fold
        - cross-validated on all K-folds
        - accuracy is average of accuracy on all folds separately.
        - most informative features is printed for classification on each-fold


    K(default) = 10

    Current Accuracy Report (At time of submission):
        - Training Data : ~ 50.9 %
        - Held Out Data : ~ 52 %

    """
    print classification.__doc__


def main():

    print __doc__


    scaffolding()
    parsing()
    extraction()
    classification()


if __name__ == '__main__':
    main()
