corpus_path="corpus/parsed_essays"

#The essays are separated by 10 newlines, so split the file by that, and then strip each chunk of leading & ending whitespace.
essay_list=[s.strip() for s in open(corpus_path,'r').read().split("\n"*10) if len(s.strip())]


intro="\nHi! This is the Common App Phrase Frequency Analyser.\n\nPlease enter your settings now, and enjoy.\n"

print intro


#Ask for the phrase_length:
try:
    phrase_length=int(raw_input("Phrase length: "))
    if phrase_length < 1: raise Exception()
except:
    print "Phrase length must be a positive integer"
    quit()

#Ask for the num_phrases
try:
    num_phrases=int(raw_input("Number of phrases to print: "))
    if num_phrases < 1: raise Exception()
except:
    print "Number of phrases must be a positive integer"
    quit()

phrases={}
import re

#For each essay, grab every phrase of the target length and toss it in the dict
for e in essay_list:

    #Remove '.' and ',' from  the essay - we want "dog." and "the dog is good." both to add to the dog count. Remember to escape the '.'
    re.sub('\.|,','',e)
    e=e.split() #Split into words

    
    for i in range(len(e)-phrase_length):
        phrase=tuple(e[i:i+phrase_length])
        
        if phrase not in phrases: phrases[phrase]=0
        phrases[phrase]+=1

#Sort the dict by value
ranked_phrases=sorted([(k,v) for k,v in phrases.items()], key=lambda x: x[1], reverse=True)

to_print=min(num_phrases,len(ranked_phrases))

print "\n\n"+"-"*20
for i in range(to_print):
    this_phrase=" ".join(ranked_phrases[i][0])
    this_occurences=ranked_phrases[i][1]
    print this_phrase+" : "+str(this_occurences)
