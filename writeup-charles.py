'''
Assignment for 10/14
Charles Wang
INFO 256
'''

###################################################
#####################    i    #####################
###################################################

### feature 1 ###
''' @description: If within a sentence, there's a word that's all capitalized, we mark it
as negative (-1), except if the words are meaningless like A, I, IPOD, or USB... '''

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

### feature 2 ###
''' @description: Decide sentence sentiment based on its words. Starting from the first
word of the sentence, if we encounter a word that is in the bag of words which defined
in advance, we then catergorize it to that category, either positive (+1) or negative (-1).
If after looping all the words in the sentence, we still couldn't find a corresponding
sentiment keywords, we mark the sentence as neutral (0) '''

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

### feature 3 ###
''' @descripion: we first compute all the bigrams within a sentence. If we encounter the word
NOT, we minus 2 because we may have plused 1 for the postive adjective entailed. Similary,
we plus 2 if the word after NOT is in the negative bag of words (e.g. NOT bad) '''

def getBigramBeginWithNotCount(sent):
    negative_keywords = ["bad", "sad", "don't", "could not", "crappy", "unfortunately", "remove", "why", "poor",
                     "bothersome", "terrible", "although", "complaints", "outrageous", "isn't", "poorly",
                     "drawback", "annoying", "against", "irritating", "wouldn't", "won't", "wasn't", "couldn't",
                     "awful", "didn't", "hasn't", "difficult", "hate", "incorrect", "junk", "trash", "removed",
                         "complain", "complained", "hated", "negative"]
    bigramPostiveCount = 0
    for i, word in enumerate(word_tokenize(sent)): 
        if word.lower() == "not":
            if word_tokenize(sent)[i + 1] in negative_keywords : # e.g. NOT bad
                bigramPostiveCount += 1
            if i < len(word_tokenize(sent)) - 2 and word_tokenize(sent)[i + 2] in negative_keywords: # e.g. NOT too bad
                bigramPostiveCount += 1
            else:                                                # e.g. NOT good
                bigramPostiveCount -= 1
    return bigramPostiveCount

#####################################################
#####################    ii    ######################
#####################################################
''' @answer: the agreed upon format for feature functions is to return a numerical score (float or int) that can later
be weighted in the calculation of aggegated vote. after the feature extraction step, the output is  a list of tuples with
[(filename, linenumber, aggregatevote, sentence, {feat1, feat2, ..})], where the inital aggregatevote for each sentence
is 0, and the last item in the tuple is a dictionary that stores the return value for each features we defined. Finally,
we send each tuple to a featureCalculator that calculates the updated aggregatevote based on our initial assumption: '''

def featureCalculator(sentTuple):
    sentTuple_update = sentTuple
    featureDir = sentTuple[4]
    current_vote = sentTuple_update[2] 
    new_vote = current_vote - featureDir['upperCount'] - featureDir['negativeWordCount'] + featureDir['postiveWordCount'] + 2 * featureDir['bigramBeginWithNotCount']
    sentTuple_update[2] = new_vote
    return sentTuple_update

#####################################################
#####################    iii    #####################
#####################################################
''' @optimization for feature 1: we remove punctuations entailing a word. we also remove intial or ending digits in a word.
this feature seems to be quite accurate as most sentences with alot of capitalized words tend to be more negative than positve.
however, we must exclude words that are commonly capitalized, such as PDA, MP3, or IPOD. '''
 
''' @optimization for feature 2: as we processed the training set, we prepared a bag of positive and negative emotional words,
according to two of the training product files. for most sentence, this approach correctly tag sentiments. but in the case when
there's a NOT preceding an adjective, the polarity of the sentence would be reversed. and that's how we've come up with feature 3'''

''' @optimization for feature 3: we've tried the nltk.bigrams() function but it takes too much time to process all the sentences
given the input files. we've also considered nltk.UnigramTagger to train and classify the POS tag after the NOT, but after a few trial
and error we concluded that in most situations when there's a NOT in a sentence, it's polarity is negative, except it's entailed by a
negative word (e.g. NOT bad). thus, we do not care much what the POS tag is after the word NOT, whether is JJ, NN, or WDT '''

####################################################
#####################    iv   ######################
####################################################
''' @classification result:  we randomize, shuffle and split the data into tranining and test dataset. then we apply the 10-fold
cross classification with naive bayes classifier '''
''' classifier accuracy on training data: 69% '''
''' classifier accuracy on held-out data: 74% '''















