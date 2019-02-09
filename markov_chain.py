#!/usr/bin/python2.7

import getch
import bisect
import random
import numpy as np
import math

#------------------------------Functions start-------------------------------------------------
def Prefix_Suffix_Pairs(prefix_length, essay_list):
    prefix_dict={}
    for essay in essay_list:
        essay_words=essay.split()

        #Prepend some empty strings so we can start with a correct length prefix
        essay_words=["" for i in range(prefix_length)]+essay_words
        
        for i in range(len(essay_words)-prefix_length):
            this_prefix=tuple(essay_words[i:i+prefix_length])
            this_suffix=essay_words[i+prefix_length]

            #If needed, add the prefix to the dict and the suffix to the prefix's dict, then increment the occurences counter
            if tuple(this_prefix) not in prefix_dict: prefix_dict[this_prefix]={}
            if this_suffix not in prefix_dict[this_prefix]: prefix_dict[this_prefix][this_suffix]=0
            prefix_dict[this_prefix][this_suffix]+=1

    #Now we need to convert raw occurences into a probability weighting for each prefix
    for key1 in prefix_dict.keys():
        suffix_dict=prefix_dict[key1]
        total_occurences=sum([x for x in suffix_dict.values()])

        #Each suffix should get a weighting between 0 and 1        
        for key2 in suffix_dict.keys():
            this_occurences=suffix_dict[key2]
            weight=float(this_occurences) / float(total_occurences)
            suffix_dict[key2]=weight

        #Now turn the suffix dict into a list of tuples, analagous to a dictionary with repeated keys, where the keys
        #are the weights and the values are the words. We were hitting a problem keeping it as a dictionary as words
        #with the same weight were overwriting eachother.        
        prefix_dict[key1]=[(item[1],item[0]) for item in suffix_dict.items()]
                
    return prefix_dict

def Next_Word(prefix_dict, this_prefix):
    #Look for the prefix in the dict - if it's not there, return 0
    if this_prefix not in prefix_dict: return 0

    #The weights are the 0th tuple values (analagous to keys) of the prefix's suffix list. Make
    #the weighted choice, and then return the chosen word.
    weights=[item[0] for item in prefix_dict[this_prefix]]

    #Numpy produces arrays of the given length, so grab the first element to get a number rather than a 1 element array.
    chosen_index=np.random.choice(len(weights), 1, p=weights)[0]
    
    chosen_item=prefix_dict[this_prefix][chosen_index]
    chosen_word=chosen_item[1]
    
    return chosen_word

def Generate_Text(prefix_length, max_length, prefix_dict):
    max_length+=prefix_length #We don't want to count the initial empty strings

    #Initialize the text with a long enough blank prefix
    text=["" for i in range(prefix_length)]

    #In each loop we add one word, until we get to the desired length
    while True:
        this_prefix=tuple(text[-prefix_length:]) #Tuple for hashing
        next_word=Next_Word(prefix_dict, this_prefix)
        if not next_word: break #We failed to find a suffix for the prefix
        text.append(next_word)

        if len(text) >= max_length: break

    #Get rid of the initial empty strings, and join up with spaces
    text=" ".join(text[prefix_length:])

    #If there were no full stops, retry with the generation
    if '.' not in text: return Generate_Text(prefix_length, max_length-prefix_length, prefix_dict)
    
    #We want to finish on a full stop, so find the pos of the last one, and grab everything up to and including it
    last_stop_pos=len(text)-text[::-1].find('.')-1    
    return text[:last_stop_pos+1]
    
#------------------------------Functions end-----------------------------------------------------

corpus_path="corpus/parsed_essays"

#The essays are separated by 10 newlines, so split the file by that, and then strip each chunk of leading & ending whitespace.
essay_list=[s.strip() for s in open(corpus_path,'r').read().split("\n"*10) if len(s.strip())]

#print str(len(essay_list))+" essays found."

intro="\nHi! This is the Common App Markov Text Generator. We tried hard to find a lot of essays for our corpus, but so far \
we've only found 137 top-of-the-line pieces. While this gives us a dataset of just over 400KB, Markov-vy Madness would ideally \
prefer quite a bit more. As such, we recommend that your Markov chunks are of length 1 or 2, as anything more will likely \
fail to produce a sizeable text.\n\nPlease enter your settings now, and enjoy.\n"

print intro


#Ask for the prefix_length: the length of the chunk we consider when calling next_word
try:
    prefix_length=int(raw_input("Markov chunk size: "))
    if prefix_length < 1: raise Exception()
except:
    print "Markov chunk size must be a positive integer"
    quit()

#Ask for the word_length: the minimum word length of the text we want to generate
try:
    words_length=int(raw_input("Max word count: "))
    if prefix_length < 1: raise Exception()
except:
    print "Max word count must be a positive integer"
    quit()
    
min_length = int(math.ceil(float(words_length) / float(prefix_length)))
prefix_dict = Prefix_Suffix_Pairs(prefix_length, essay_list)


while True:
    text=Generate_Text(prefix_length, min_length, prefix_dict)
    print "\n\n\n"+text

    #If we like it, append it to a file
    good_products=open('good_products','a+')
    print "\n\nSave it to file? (y / n): "
    while True:
        ans=getch.getch()
        if not(ans in ['y','n']):
            print 'Please input \'y\' or \'n\''
            continue
    
        if ans == 'y': good_products.write("\n\n\n"+text+"\n\n\n")
        break

    #Then ask if we want another one
    print "Another text? (y / n): "
    while True:
        ans=getch.getch()
        if not(ans in ['y','n']):
            print 'Please input \'y\' or \'n\''
            continue
    
        if ans == 'n': quit()
        break
        
