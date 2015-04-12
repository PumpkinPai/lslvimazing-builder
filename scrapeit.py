#!/usr/bin/python3

# go to 'targeturl' looking for 'searchterm' and return all of the values within 
# 'delim' immediately following the beginning of 'searchterm'

import urllib.request

# grab a url and save as text to avoid hammering pages
def getUrl(targetUrl):
    try:
        print('Attempting to save ' + targetUrl)
        response = urllib.request.urlopen(targetUrl)
        html = str(response.read())
        
        saveFile = open('temp.html', 'w')
        saveFile.write(html)
        saveFile.close
        print('Success!')
    except Exception as e:
        print(str(e))

def filterit(searchTerm, delim, targetFile):
    print('Processing html...')

    readFile = open('temp.html', 'r')
    page = readFile.read()
    saveFile = open(targetFile, 'w')
    while page:
        startFind  = page.find(searchTerm) + len(searchTerm)
        startFound = page.find(delim[0], startFind)
        endFound   = page.find(delim[1], startFound + 1)
        found      = page[startFound + 1 : endFound]
        page       = page[endFound:]
        if found:
            saveFile.write(found + '\n')
        else:
            readFile.close
            saveFile.close
            return

def cleanFunctions(dirtyFile):
    print('Cleaning lsl functon results...')
    readFile = open(dirtyFile, 'r')
    txt = ''
    for line in readFile:
        if (line[0].islower()):
            txt = txt + line
    
    readFile.close
    writeFile = open(dirtyFile, 'w')
    writeFile.write(txt)
    writeFile.close

def cleanEvents(dirtyFile):
    print('Cleaning lsl event results...')
    readFile = open(dirtyFile, 'r')
    txt = ''
    for line in readFile:
        if (line[0:3] != 'LSL'):
            line = line.replace(' ', '_')
            txt = txt + line.lower()
        if line.lower() == 'transaction_result\n':
            break
    
    readFile.close
    writeFile = open(dirtyFile, 'w')
    writeFile.write(txt)
    writeFile.close



def cleanOperators(dirtyFile):
    # todo
    pass

if __name__ == "__main__":
    print('The main file is "buildit.py" Run that instead.')
