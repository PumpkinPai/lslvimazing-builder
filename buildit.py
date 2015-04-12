#!/usr/bin/python3

##############################################################################
#
# This little gem scrapes the official LSL wiki and builds a vim plugin with
# that data.  Syntax definitions are added from the text files afterwards.
#
##############################################################################

import scrapeit

# Gets the list of lsl functions
def getFunctions():
    txtFile = 'lslFunctions.txt'
    url = 'http://wiki.secondlife.com/wiki/Category:LSL_Functions'
    scrapeit.getUrl(url)
    scrapeit.filterit('title="Ll', ['>','<'], txtFile)
    scrapeit.cleanFunctions(txtFile)

def getEvents():
    txtFile = 'lslEvents.txt'
    url = 'http://wiki.secondlife.com/wiki/Category:LSL_Events'
    # scrapeit.getUrl(url)
    scrapeit.filterit('<li><a href="/wiki/', ['>','<'], txtFile)
    scrapeit.cleanEvents(txtFile)

def getConstants():
    txtFile = 'lslConstants.txt'
    url = 'http://wiki.secondlife.com/wiki/Category:LSL_Constants'
    scrapeit.getUrl(url)
    scrapeit.filterit('<li><a href="/wiki/', ['>','<'], txtFile)
    scrapeit.cleanEvents(txtFile)

def getOperators():
# todo
    # operators and other things are simple enough to be loaded from a manually
    # created text file
    pass



if __name__ == "__main__":

    # Go get 'em!
    # getFunctions()
    #getEvents()
    getConstants()
    getOperators()
