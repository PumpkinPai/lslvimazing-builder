#!/usr/bin/python3

##############################################################################
#
# This little gem scrapes the official LSL wiki and builds a vim plugin with
# that data.  Syntax definitions are added from the text files afterwards.
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
    url     = 'http://wiki.secondlife.com/wiki/Category:'
    pageBegin = 'Pages in category'
    pageEnd = 'class="printfooter"'
    searchTerm = '<li><a href="/wiki/'
    delim = ['>','<']

    # Get Functions
    page    = 'LSL_Functions'
    targetFile = page + '.txt'
    spidey.wikiCrawl(url+page, pageBegin, pageEnd, searchTerm, delim, targetFile)
    spidey.cleanFunctions(targetFile)
    exit()

    # Get Events
    page = 'LSL_Events'
    targetFile = page + '.txt'
    spidey.wikiCrawl(url+page, pageBegin, pageEnd, searchTerm, delim, targetFile)
    spidey.cleanEvents(targetFile)

    # Get Constants
    # Constants are complicated as they span multiple pages.  We must start
    # with a fresh txt file and append to it as we go
    page = 'LSL_Constants'
    targetFile = page + '.txt'
    spidey.wikiCrawl(url+page, pageBegin, pageEnd, searchTerm, delim, targetFile)
    spidey.cleanConstants(targetFile)

    # getOperators()
