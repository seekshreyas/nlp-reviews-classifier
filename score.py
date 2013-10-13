from __future__ import division

''' Info 256 Group Assignment '''
''' 10/12 Charles Wang '''
''' @Objective: assign each sentence in given input file a sentiment score '''
''' @Note: the default input.txt is copied from training/MicroMP3.txt '''

import re

f = open('data/raw/training/Diaper Champ.txt', 'r')
f1 = open('output.txt', 'w')

''' @Summary: Review MicroMP3.txt as reference '''

''' @Fearure 1: Decide sentence sentiment based on its words. Starting from the first
word of the sentence, if we encounter a word that is in the bag of words which defined
in advance, we then catergorize it to that category, either positive (+1) or negative (-1).
If after looping all the words in the sentence, we still couldn't find a corresponding
sentiment keywords, we mark the sentence as neutral (0) '''

''' @Feature 2: If within a sentence, there's a word that's all capitalized, we mark it
as negative (-1), except if the words are meaningless like A, I, IPOD, or USB... '''

''' @Feature 3: Remove punctuations entailing a word '''

''' @Feature 4: Remove intial digits in a word. To do this, we convert each letter to
unicode and check with isnumeric() '''

''' @Feature 5: Extrat product feature score xxxx[+|-n], adjust overall score
according to this value (positive or negative)'''

''' @Feature 6: If we encounter the word NOT, we minus 2 because we may have plused 1 for
the postive adjective entailed'''

'''@Validation step: Check if the score we computed has the same (+/-) sign as the user
evaluation of the product feature '''

positive_keywords = ["good", "happy", "love", "great", "reasonable", "glad", "simple", "outstanding", "easy",
                     "wonderful", "cool", "remarkably", "remarkable", "enjoy", "nice", "thoughtful", "pretty",
                     "responsive", "comforatable", "favorite", "desire", "best", "solid", "cool", "impressed",
                     "sleek", "appealing", "rocks", "blazing", "amazing", "plus", "blessing", "awesome"]
negative_keywords = ["bad", "sad", "don't", "could not", "crappy", "unfortunately", "remove", "why", "poor",
                     "bothersome", "terrible", "although", "complaints", "outrageous", "isn't", "not", "poorly",
                     "drawback", "annoying", "against", "irritating", "wouldn't", "won't", "wasn't", "couldn't",
                     "awful", "didn't", "hasn't", "difficult", "hate", "hated", "incorrect", "junk", "trash"]
uppercase_meaningless_words = ["A", "I", "IPOD", "USB", "MP3", "CD", "FM", "GB", "PC", "LCD", "MP-3", "WMA", "WMP",
                               "AC/DC", "PDA", "PXC250", "XP", "LED", "AC", "AGK"]

accuracy = 0
correct_count = 0
total_count = 0
for i, line in enumerate(f):
    score = 0
    mood = 0 # +/- toward product feature
    print("line " + str(i))
    for word in line.split(" "): 
        word = word.replace(".","").replace(",","").replace("!","").replace("?","").replace("##","").replace("(","").replace(")","").replace("**","") # Feature 3
        for letter in word:
            if unicode(letter).isnumeric():
                word = word.replace(letter, "") # Feature 4
            else:
                break
        if re.search("\w+\[\W\d\]", word): # Feature 5
            numeric = word[word.index("[")+1:-1]
            if numeric[0] == '+':
                #score += int(numeric[1])
                mood += int(numeric[1])
            else:
                #score -= int(numeric[1])
                mood -= int(numeric[1])
            print ">>> product feature: " + word + ", value " + numeric[0:2]
        elif word.isupper() and not word in uppercase_meaningless_words: # Feature 2
            score -= 1
            print ">>> uppercase keywords: " + word + ", value -1"
        elif word.lower() in positive_keywords: # Feature 1
            score += 1
            print ">>> positive keywords: " + word + ", value +1"
        elif word.lower() in negative_keywords: # Feature 1
            score -= 1
            print ">>> negative keywords: " + word + ", value -2"
        elif word.lower() == "not": # Feature 6
            score -= 2
            print ">>> encounter a NOT" + ", value -2"
    sensitivity = "neutral"
    if score > 0:
        sensitivity = "positive"
    elif score < 0:
        sensitivity = "negative"
    correctness = "correct!"
    if score * mood < 0: # negative result suggests the signs of the numbers are different
        correctness = "ooooooooops!"
    else:
        correct_count += 1
    total_count += 1
    f1.write("line " + str(i) + " [" + str(score) + ": " + "(" + sensitivity + ") " + correctness +"]: " + line + "\n")
print "############################################"
print "total line: " + str(total_count)
print "correct line: " + str(correct_count)
print "overall accuracy: " + str(float(correct_count/total_count))
f.close()
f1.close()
