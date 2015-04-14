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

    depFile = conf['scraper']['depFile']
    try:
        os.remove(depFile)
    except:
        pass

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
        spidey.crawl(url, begin, end, search, delim, txtFile, depFile)
        print('Cleaning ' + txtFile)
        # count, first, last = spidey.cleanResults(txtFile, rules, ignore)
        spidey.cleanResults(txtFile, rules, replace, ignore)
        # print('Captured ' + str(count) + ' results from ' + first + ' to ' + last)
        print('Done!')


    # Simple types will be manual
    manualFile = open('LSL_Manual.txt', 'r')

    # Create directories and cp plug-* files to proper files and locations 
    for r in conf['structure']:
        # todo
        print(r)


    # Generate lsl.vim syntax file
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

    exit()
