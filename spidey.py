#!/usr/bin/python3

# go to 'targeturl' looking for 'searchterm' and return all of the values within 
# 'delim' immediately following the beginning of 'searchterm'

import urllib.request
import os

# Crawl url, look for searchTerm, grab thing within delim, put it in txtFile
def crawl(url, pageBegin, pageEnd, searchTerm, delim, txtFile):
    # temp- we now have decent files to play with
    return

    multi = True
    multiQuery = ''
    # clear text file
    try:
        os.remove(txtFile)
    except: pass

    try:
        while multi:
            print('Going to: ' + url+multiQuery)
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
            multi = html.find('pagefrom=')
            # we need this link for the next time around
            startMulti = html.find('=', multi) + 1
            endMulti   = html.find('"', startMulti + 1)
            multiQuery = html[startMulti:endMulti]

            if multi > 0: multi = True
            else: multi = False

            foundList = []
            saveFile = open(txtFile, 'a')
            while True:
                startFind  = html.find(searchTerm) + len(searchTerm)
                startFound = html.find(delim[0], startFind)
                endFound   = html.find(delim[1], startFound + 1)
                found      = html[startFound + 1 : endFound]
                html       = html[endFound:]
                if found:
                    foundList.append(found)
                else:
                    foundTxt = '\n'.join(foundList) + '\n'
                    saveFile.write(foundTxt)
                    saveFile.close
                    break
                     
    except Exception as e:
        print(str(e))
        return False

def cleanResults(dirtyFile, specialRules, ignoreList):
    try:
        readFile = open(dirtyFile, 'r')
    except Exception as e:
        print(str(e))
        return
    resultList = []
    for line in readFile:
        resultList.append(line.strip('\n'))

    # Round 1, replicants and ignorables
    cleanList = []
    for txt in resultList:
        dirty = False                       # Assume they took a bath
        if txt in cleanList: dirty = True   # She's a replicant
        if txt.lower() in ignoreList: dirty = True
        if dirty == False:
            cleanList.append(txt)

    # Round 2 for specialRules
    resultList = cleanList
    cleanList = []
    for rule in specialRules:
        for txt in resultList:
            if rule == 'caps':
                txt = txt.upper()
            elif rule == 'lower':
                txt = txt.lower()
            elif rule == 'firstLower':
                txt = txt[0].lower() + txt[1:] 
            elif rule == 'replace':
                txt = txt.replace(rule['find'], rule['replacement'])
            cleanList.append(txt)

    readFile.close
    resultTxt = '\n'.join(cleanList)
    writeFile = open(txtFile, 'w')
    writeFile.write(resultTxt)
    writeFile.close
    
    # return number, first and last
    return str(len(resultList)), resultList[0], resultList[1]


def cleanFunctions(dirtyFile):
    print('Cleaning lsl functon results...')
    try:
        readFile = open(dirtyFile, 'r')
    except Exception as e:
        print(str(e))
        return
    # make a list out of the file
    resultList = []
    for line in readFile:
        # make it 'll' instead of 'Ll'
        line = line[0].lower() + line[1:]
        resultList.append(line.strip('\n'))
    
    resultList = cleanList(resultList)
    
    readFile.close
    resultTxt = '\n'.join(resultList)
    writeFile = open(dirtyFile, 'w')
    writeFile.write(resultTxt)
    writeFile.close
    print('Finished getting ' + str(len(resultList)) + ' functions!')
    print('From ' + resultList[0] + ' to ' + resultList[-1])


def cleanEvents(dirtyFile):
    print('Cleaning lsl event results...')
    try:
        readFile = open(dirtyFile, 'r')
    except Exception as e: 
        print(str(e))
        return

    # Make a list of the file
    resultList = []
    for line in readFile:
        resultList.append(line.strip('\n'))

    resultList = cleanList(resultList)
    # 'state_entry' vs 'state entry'
    for i in range(len(resultList)):
        resultList[i] = resultList[i].replace(' ', '_')
        resultList[i] = resultList[i].lower()

    readFile.close
    resultTxt = '\n'.join(resultList)
    writeFile = open(dirtyFile, 'w')
    writeFile.write(resultTxt)
    writeFile.close
    print('Finished getting ' + str(len(resultList)) + ' events!')
    print('From ' + resultList[0] + ' to ' + resultList[-1])


def cleanConstants(dirtyFile):
    print('Cleaning lsl constant results...')
    try:
        readFile = open(dirtyFile, 'r')
    except Exception as e: 
        print(str(e))
        return

    # Make a list of the file
    resultList = []
    for line in readFile:
       resultList.append(line.strip('\n'))

    resultList = cleanList(resultList)
    # 'LINK_ROOT' vs 'LINK ROOT'
    for i in range(len(resultList)):
        resultList[i] = resultList[i].replace(' ', '_')
        resultList[i] = resultList[i].upper()

    readFile.close
    resultTxt = '\n'.join(resultList)
    writeFile = open(dirtyFile, 'w')
    writeFile.write(resultTxt)
    writeFile.close
    print('Finished getting ' + str(len(resultList)) + ' constants!')
    print('From ' + resultList[0] + ' to ' + resultList[-1])


# Removes duplicates and garbage lines
def cleanList(dirtyList):
    cleanList = []
    ignoreList = ['\\n', '(', '(previous 200) (', 'next 200', 'previous 200', 
                  '(previous 200) (next 200)\\n'] 
    for txt in dirtyList:
        dirty = False
        if txt in cleanList:  dirty = True
        if txt.lower() in ignoreList: dirty = True
        if dirty == False:
            cleanList.append(txt)

    return cleanList



if __name__ == "__main__":
    print('The main file is "buildit.py" Run that instead.')
