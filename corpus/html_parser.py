import html

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

def RemoveTag(essay,tag):
    return essay.replace("<"+tag+">"," ").replace("</"+tag+">"," ")

parsed_essays=splitter.join(raw_essays)

#Translate HTML entities
parsed_essays=html.unescape(parsed_essays)

#Remove tags
tags=["em","strong","br","span","u","p","sup","a","ul","li"]
for t in tags: parsed_essays=RemoveTag(parsed_essays,t)
parsed_essays=parsed_essays.replace("<br/>"," ") #Damn those self closers


#Strip these two odd '-' and '_' that have appeared
stripped=""
bad=[160,173]
for c in parsed_essays:
    if ord(c) in bad: stripped+=' '        
    else: stripped+=c
parsed_essays=stripped

#Remove extra spaces
import re
parsed_essays=re.sub(' +',' ', parsed_essays)

#Then write the parsed_essays
open("parsed_essays",'w').write(parsed_essays+splitter)

