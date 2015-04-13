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

# Gets the list of lsl functions
def getFunctions():
    targetFile = 'lslFunctions.txt'
    url = 'http://wiki.secondlife.com/wiki/Category:LSL_Functions'
    searchTerm = '<li><a href="/wiki/'
    delim = ['>','<']
    spidey.crawl(url, searchTerm, delim, targetFile)
    spidey.cleanFunctions(targetFile)


if __name__ == "__main__":

    # Go get 'em!
    url     = 'http://wiki.secondlife.com/w/index.php?title=Category:'
    pageBegin = 'Pages in category'
    pageEnd = 'class="printfooter"'
    searchTerm = '<li><a href="/wiki/'
    delim = ['>','<']

    # Get Functions
    page    = 'LSL_Functions&pagefrom='
    functionsFile = page.strip('&pagefrom=') + '.txt'
    spidey.wikiCrawl(url+page, pageBegin, pageEnd, searchTerm, delim, functionsFile)
    spidey.cleanFunctions(functionsFile)

    # Get Events
    page = 'LSL_Events&pagefrom='
    eventsFile = page.strip('&pagefrom=') + '.txt'
    spidey.wikiCrawl(url+page, pageBegin, pageEnd, searchTerm, delim, eventsFile)
    spidey.cleanEvents(eventsFile)

    # Get Constants
    page = 'LSL_Constants&pagefrom='
    constantsFile = page.strip('&pagefrom=') + '.txt'
    spidey.wikiCrawl(url+page, pageBegin, pageEnd, searchTerm, delim, constantsFile)
    spidey.cleanConstants(constantsFile)

    # Simple files will be manual
    operatorsFile   = 'LSL_Operators.txt'
    typesFile       = 'LSL_Types.txt'
    flowFile        = 'LSL_Flow.txt'


