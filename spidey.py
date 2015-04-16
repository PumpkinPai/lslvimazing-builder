#!/usr/bin/python3

# go to 'targeturl' looking for 'searchterm' and return all of the values within 
# 'delim' immediately following the beginning of 'searchterm'

import urllib.request
import os

# Crawl url, look for searchTerm, grab thing within delim, put it in txtFile
def crawl(url, pageBegin, pageEnd, searchTerm, delim, txtFile):
    # temp- we now have decent files to play with
    # return ('x', 'x')

    multi = True
    multiQuery = ''
    # clear text file
    try:
        os.remove(txtFile)
    except: pass

    pageCount = 0
    findCount = 0

    try:
        while multi:
            pageCount += 1
            print('Going to: ' + url+multiQuery)
            response = urllib.request.urlopen(url+multiQuery)
            html = str(response.read())

            # PAGEBEGIN TO PAGEEND
            # Make it just the nectar within pageBegin and pageEnd
            startHtml = html.find(pageBegin)
            endHtml   = html.find(pageEnd)
            html = html[startHtml:endHtml]

            # MULTI
            # If the category spans multiple pages, cry
            multi = html.find('pagefrom=')
            # we need this link for the next time around
            startMulti = html.find('=', multi) + 1
            endMulti   = html.find('"', startMulti + 1)
            multiQuery = html[startMulti:endMulti]

            if multi > 0: multi = True
            else: multi = False

            # PROCESS HTML and save
            foundList = []
            saveFile = open(txtFile, 'a')
            while True:
                startFind  = html.find(searchTerm) + len(searchTerm)
                startFound = html.find(delim[0], startFind)
                endFound   = html.find(delim[1], startFound + 1)
                found      = html[startFound + 1 : endFound]
                html       = html[endFound:]

                if found:
                    findCount += 1 
                    foundList.append(found)
                else:
                    foundTxt = '\n'.join(foundList) + '\n'
                    saveFile.write(foundTxt)
                    saveFile.close
                    break
        return (str(findCount), str(pageCount))
                     
    except Exception as e:
        print(str(e))
        return (0, 0) 

def cleanResults(dirtyFilename, specialRules, replace, ignoreList):
    try:
        readFile = open(dirtyFilename, 'r')
    except Exception as e:
        print(str(e))
        return

    resultList = []
    for line in readFile:
        resultList.append(line.strip('\n'))

    # Round 1 for specialRules
    cleanList = []
    for rule in specialRules:
        # print(rule) # debug
        for txt in resultList:
            if rule == 'caps':
                txt = txt.upper()
            elif rule  == 'lower':
                txt = txt.lower()
            elif rule  == 'firstLower':
                txt = txt[0].lower() + txt[1:] 
            cleanList.append(txt)

    # Round 2, replicants and ignorables
    resultList = cleanList
    cleanList = []
    for txt in resultList:
        # Assume they took a bath
        dirty = ''
        if txt in cleanList: 
            # She's a replicant
            dirty = ' a replicant'   
        if txt.lower() in ignoreList: 
            dirty = ' in the ignoreList' 
        if dirty == '':
            cleanList.append(txt)
        else:
            pass
            # print('Removed: ' + txt + ' because it was' + dirty) 

    # Round 3, replacements
    if replace[0]:
        resultList = cleanList
        cleanList = []
        for txt in resultList:
            txt = txt.replace(replace[0], replace[1])
            cleanList.append(txt)

    readFile.close
    resultTxt = '\n'.join(cleanList)
    writeFile = open(dirtyFilename, 'w')
    writeFile.write(resultTxt)
    writeFile.close
    
    # return number, first and last
    return (str(len(resultList)), resultList[0], resultList[-1])


if __name__ == "__main__":
    print('The main file is "buildit.py" Run that instead.')
