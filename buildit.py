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


if __name__ == "__main__":

    confFile = open('config.yaml', 'r')
    conf = yaml.load(confFile)

    # Go get 'em!
    # todo- loop through the conf['scraper','queries']

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

    # Create the plugin tree and put files where they go
    for txt in conf['structure']:
        print(txt['name'])


