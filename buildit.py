#!/usr/bin/python3

##############################################################################
#
# This little gem scrapes the official LSL wiki and builds a vim plugin with
# that data.  Syntax definitions are added from the text files afterwards.
#
# It will eventually use beautifulsoup4 but I needed the exercise.
# Hence, spidey.py
#
##############################################################################

import spidey
import os
import yaml


def getConf():
    confFile = open('config.yaml', 'r')
    conf = yaml.load(confFile)
    return conf

# Main Scrapes
def scrapeMain():
    for r in conf['scraper']['queries']:
        name    = r['name']
        page    = r['page']
        rules   = r['rules']
        replace = r['replace']
        txtFile = name + '.txt'
        ignore  = conf['scraper']['ignore'] 
        url     = conf['scraper']['url'] + page 
        begin   = conf['scraper']['pageBegin']
        end     = conf['scraper']['pageEnd']
        search  = conf['scraper']['searchTerm']
        delim   = conf['scraper']['delim']
        # print('Getting ' + url)
        foundCount = 0
        pageCount = 0
        foundCount, pageCount = spidey.crawl(url, begin, end, search, delim, txtFile)
        print('Found: ' + str(foundCount) + ' results on ' + str(pageCount) + 'pages') # debug
        print('Cleaning ' + txtFile)
        # count, first, last = spidey.cleanResults(txtFile, rules, ignore)
        success = spidey.cleanResults(txtFile, rules, replace, ignore)
        print('Clean success: ' + str(success)) # debug
        # print('Captured ' + str(count) + ' results from ' + first + ' to ' + last)
        print('Done!')

# Deprecated Functions
def scrapeDeps():
    depFile = 'LSL_Deprecated.txt'
    try:
        os.remove(depFile)
    except:
        pass
    searchTerm = '<s>'
    pageBegin = 'title="LlAbs"'
    pageEnd = 'id="footnote_1"'
    delim = ['>','<']
    url = 'http://wiki.secondlife.com/w/index.php?title=Category:LSL_Functions'
    spidey.crawl(url, pageBegin, pageEnd, searchTerm, delim, depFile)
    spidey.cleanResults(depFile, ['firstLower'], [False], [False])
    # Remove deps from captured result files
    depsTxt = open(depFile, 'r')
    for r in conf['scraper']['queries']:
        txtFile = r['name'] + '.txt'
        txt = open(txtFile, 'r')
        for line in depsTxt:
            txt = txt.replace(line, '')
        txtFile.close
        txtFile.open(txtFile, 'w')
        txtFile.write(txt)
        txtFile.close
    depFile.close

    print('Done!')

# Generate main syntax file
def generateSyntax():
    syntaxFile = open('plug-syntax.txt', 'w')
    syntaxTxt  = manualFile.read()

    functionsFile = open('LSL_Functions.txt', 'r')
    functionsTxt  = functionsFile.read()
    functionsTxt  = functionsTxt.replace('\n', '\n\ ')
    functionsFile.close
    eventsFile    = open('LSL_Events.txt', 'r')
    eventsTxt     = eventsFile.read()
    eventsTxt     = eventsTxt.replace('\n', '\n\ ')
    eventsFile.close
    constantsFile = open('LSL_Constants.txt', 'r')
    constantsTxt  = constantsFile.read()
    constantsTxt  = constantsTxt.replace('\n', '\n\ ')
    constantsFile.close
    deprecatedFile = open('LSL_Deprecated.txt', 'r')
    deprecatedTxt  = deprecatedFile.read()
    deprecatedTxt  = deprecatedTxt.replace('\n', '\n\ ')
    deprecatedFile.close

    syntaxTxt = syntaxTxt.replace('*FUNCTIONS*', functionsTxt)
    syntaxTxt = syntaxTxt.replace('*EVENTS*', eventsTxt)
    syntaxTxt = syntaxTxt.replace('*CONSTANTS*', constantsTxt)
    syntaxTxt = syntaxTxt.replace('*DEPRECATED*', deprecatedTxt)

    syntaxFile.write(syntaxTxt)
    syntaxFile.close

if __name__ == "__main__":

    conf = getConf()

    scrapeMain()

    scrapeDeps()

    # Simple types will be manual
    manualFile = open('LSL_Manual.txt', 'r')

    # Create directories and cp plug-* files to proper files and locations 
    for r in conf['structure']:
        # todo
        # print(r)
        pass

    generateSyntax()
