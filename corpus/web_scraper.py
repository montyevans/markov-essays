#A drop of 'wget' got us the homepage, which contains the links to all the essays
base_file=open("index.html",'r').read()

#We're going to scan through the homepage, looking for the indicator for an essay link, until we can't find any  more
hrefs=[]
div_indicator="<div class=\"entry\">"
href_indicator="href=\""

start_index=0
while True:
    #Look for the entry in the list, only looking forward from the last index    
    start_index=base_file.find(div_indicator, start_index)
    if start_index == -1: break #No more to be found

    #Now look forward for the href to which the entry points    
    start_index=base_file.find(href_indicator,start_index)

    start_index+=len(href_indicator) #This is now pointing to the first char in the href
    end_index=base_file.find("\"", start_index)

    hrefs.append(base_file[start_index:end_index]) 


#Build a list with the full urls - the hrefs we scraped are relative to the site's root, so we need to sellotape the root on the front
root_url="https://www.apstudynotes.org"
urls=[root_url+x for x in hrefs]

#Tell the console how many we scored - should be 150
print(str(len(urls))+" urls scraped")

#Now we have to make requests to these urls - after a bit of fiddling, we can get them going through at 1/sec
import requests
raw_pages=open("raw_pages",'w')
count=0
for url in urls:
    #In Python 2.7 the request returns a string, but in 3.5 it's a bytes-object you have to decode. Annoying.
    page=requests.get(url).content.decode("utf-8") 
    raw_pages.write(page)
    count+=1; print (count)    
    
#Dump the pages to a file and deal with them in another program, so if we screw up we don't have to make a load of slow requests again
