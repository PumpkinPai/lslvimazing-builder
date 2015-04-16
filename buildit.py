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
        txtFilename = name + '.txt'
        ignore  = conf['scraper']['ignore'] 
        url     = conf['scraper']['url'] + page 
        begin   = conf['scraper']['pageBegin']
        end     = conf['scraper']['pageEnd']
        search  = conf['scraper']['searchTerm']
        delim   = conf['scraper']['delim']
        founds, pages = spidey.crawl(url, begin, end, search, delim, txtFilename)
        print('Found: ' + str(founds) + ' results on ' + str(pages) + ' pages')
        print('Cleaning ' + txtFilename)
        total, first, last = spidey.cleanResults(txtFilename, rules, replace, ignore)
        print('Captured ' + str(total) + ' results from ' + first + ' to ' + last)
        print('Done!')

# Deprecated Functions
def scrapeDeps():
    print('Sorting deprecations...')
    depFilename = 'LSL_Deprecated.txt'
    try:
        pass
        # os.remove(depFilename)
    except:
        pass
    searchTerm = '<s>'
    pageBegin = 'title="LlAbs"'
    pageEnd = 'id="footnote_1"'
    delim = ['>','<']
    url = 'http://wiki.secondlife.com/w/index.php?title=Category:LSL_Functions'
    spidey.crawl(url, pageBegin, pageEnd, searchTerm, delim, depFilename)
    spidey.cleanResults(depFilename, ['firstLower'], [False], [False])

    # Remove deps from captured result files
    depFile = open(depFilename, 'r')
    for r in conf['scraper']['queries']:
        srcFilename = r['name'] + '.txt'
        srcFile = open(srcFilename, 'r')
        src = []
        for line in srcFile:
            src.append(line.strip('\n')) 
        for dep in depFile:
            dep = dep.strip('\n')
            try:
                src.remove(dep)
            except: pass
            print('Removing deprecation: ' + dep)

        srcTxt = '\n'.join(src)
        srcFile.close
        srcFile = open(srcFilename, 'w')
        srcFile.write(srcTxt)
        srcFile.close

    depFile.close

    print('Done!')

# Generate main syntax file
def generateSyntax():
    syntaxFile = open('plug-syntax.txt', 'w')

    # Simple types will be manual
    # LSL_Manual.txt also forms the main template and holds the pain in the
    # butt regex stuff and vim syntax references
    manualFile    = open('LSL_Manual.txt', 'r')
    manualTxt     = manualFile.read()
    manualFile.close
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

    syntaxTxt = manualTxt 
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


    # Create directories and cp plug-* files to proper files and locations 
    for r in conf['structure']:
        # todo
        # print(r)
        pass

    generateSyntax()

    print('All done!  Enjoy your day!')
