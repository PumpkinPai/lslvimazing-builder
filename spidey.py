#!/usr/bin/python3

# go to 'targeturl' looking for 'searchterm' and return all of the values within 
# 'delim' immediately following the beginning of 'searchterm'

import urllib.request
# Crawl url, look for searchTerm, grab thing within delim, put it in txtFile
def wikiCrawl(url, pageBegin, pageEnd, searchTerm, delim, txtFile):
    print('Like sands through the hourglass, so are the bytes of our hives...')
    multi = True
    multiQuery = ''
    try:
        while multi:
            response = urllib.request.urlopen(url+multiQuery)
            html = str(response.read())
            # Make it just the nectar within pageBegin and pageEnd
            startHtml = html.find(pageBegin)
            endHtml   = html.find(pageEnd)
            html = html[startHtml:endHtml]
            # Some wiki pages are silly and put spaces and junk between tags
            # Lets fix that... todo- do it with regex to allow for more junk
            html = html.replace('<s>', '')
            html = html.replace('> <', '><')

            # If the category spans multiple pages, cry
            multi = html.find('&pagefrom=')
            if multi > 0: multi = True
            else: multi = False

            saveFile = open(txtFile, 'a')
            while html:
                startFind  = html.find(searchTerm) + len(searchTerm)
                startFound = html.find(delim[0], startFind)
                endFound   = html.find(delim[1], startFound + 1)
                found      = html[startFound + 1 : endFound]
                html       = html[endFound:]
                if found:
                    saveFile.write(found + '\n')
                else:
                    saveFile.close
                    if multi: multiQuery = '&pagefrom=' + found
                    return True 

    except Exception as e:
        print(str(e))
        return False


# todo- use this function to replace all of the following (might be more
# trouble than it's worth
def cleanup(dirtyFile, startsWith):
    pass

def cleanFunctions(dirtyFile):
    print('Cleaning lsl functon results...')
    readFile = open(dirtyFile, 'r')
    txt = ''
    additions = 0
    firstAddition = ''
    lastAddition = ''
    for line in readFile:
        if True: # (line[0].islower()):
            txt = txt + line
            additions += 1
            if firstAddition == '': firstAddition = line.replace('\n','')
            lastAddition = line.replace('\n','')
    
    readFile.close
    writeFile = open(dirtyFile, 'w')
    writeFile.write(txt)
    writeFile.close
    print('Finished getting ' + str(additions) + ' functions!')
    print('From ' + firstAddition + ' to ' + lastAddition)


def cleanEvents(dirtyFile):
    print('Cleaning lsl event results...')
    readFile = open(dirtyFile, 'r')
    txt = ''
    additions = 0
    firstAddition = ''
    lastAddition = ''
    for line in readFile:
        if (line[0:3] != 'LSL'):
            line = line.replace(' ', '_')
            txt = txt + line.lower()
            additions += 1
            if firstAddition == '': firstAddition = line.replace('\n', '')
            lastAddition = line.replace('\n', '')
        if line.lower() == 'transaction_result\n':
            break
    
    readFile.close
    writeFile = open(dirtyFile, 'w')
    writeFile.write(txt)
    writeFile.close
    print('Finished getting ' + str(additions) + ' events!')
    print('From ' + firstAddition + ' to ' + lastAddition)


def cleanConstants(dirtyFile):
    pass

if __name__ == "__main__":
    print('The main file is "buildit.py" Run that instead.')
