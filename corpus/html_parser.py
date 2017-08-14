import html
import re

raw_pages=open("raw_pages","r").read()

#Now we need to extract the essays from the bodies full of html rubbish
start_indicator="<div class=\"body\"><p>"
end_indicator="</div>"
splitter="\n"*10

raw_essays=[]
start_index=0

#Search forward the essay start indicator, increment it, and repeat until we can't find any more
while True:
    start_index=raw_pages.find(start_indicator, start_index) #Index of the '<' that starts <div class=...>
    if start_index == -1: break

    start_index+=len(start_indicator) #Index of the first letter in the essay
    
    end_index=raw_pages.find(end_indicator, start_index) #Index of the letter after the end of the essay
    if end_index == -1: break
    
    essay_chunk=raw_pages[start_index:end_index]
    raw_essays.append(essay_chunk)
    start_index=end_index
        
print(str(len(raw_essays))+" essays extracted")

#Replace weird whitespace with simple spaces
for i in range(len(raw_essays)): raw_essays=[' '.join(e.split()) for e in raw_essays]

#Join up into a single string
parsed_essays=splitter.join(raw_essays)

#Translate HTML entities
parsed_essays=html.unescape(parsed_essays)

#Remove residual tags - make sure to do non-greedy matching (the '?') so that we don't consume the whole essay.
parsed_essays=re.sub("<.*?>"," ", parsed_essays)

#Strip these two odd '-' and '_' that have appeared
stripped=""
bad=[160,173]
for c in parsed_essays:
    if ord(c) in bad: stripped+=' '        
    else: stripped+=c
parsed_essays=stripped

#Remove extra spaces
parsed_essays=re.sub(' +',' ', parsed_essays)

#And kill the irritating SAT score thing at the end of some seemingly random subset of the essays. It's denoted by a "--- SAT", so scan
#that and kill everything after it up to the newline.
parsed_essays=re.sub("--- SAT.*\n",'\n',parsed_essays)

#Then write the parsed_essays
open("parsed_essays",'w').write(parsed_essays+splitter)

