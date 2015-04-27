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
from datetime import date


def getConf():
    confFile = open('config.yaml', 'r')
    conf = yaml.load(confFile)
    confFile.close
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
        squash  = conf['scraper']['squash']
        founds, pages = spidey.crawl(url, begin, end, search, delim, squash, txtFilename)
        print('Found: ' + str(founds) + ' results on ' + str(pages) + ' pages')
        print('Cleaning ' + txtFilename)
        total, first, last = spidey.cleanResults(txtFilename, rules, replace, ignore)
        print('Captured ' + str(total) + ' results from ' + first + ' to ' + last)
        print('Done!')

# DEPRECATED FUNCTIONS
def scrapeDeps():
    print('Sorting deprecations...')
    depFilename = 'LSL_DEPRECATED.txt'
    depFilename2 = 'LSL_DEPRECATED2.txt'
    try:
         os.remove(depFilename)
         os.remove(depFilename2)
    except:
        pass
    # First search, on LSL_FUNCTIONS page
    searchTerm = '<s>'
    pageBegin = 'title="LlAbs"'
    pageEnd = 'id="footnote_1"'
    delim = ['>','<']
    ignore = ['\n', '(', '(previous 200) (', 'next 200', 'previous 200', '(previous 200) (next 200)\n']
    url = 'http://wiki.secondlife.com/w/index.php?title=Category:LSL_Functions'
    spidey.crawl(url, pageBegin, pageEnd, searchTerm, delim, [], depFilename)
    spidey.cleanResults(depFilename, ['firstLower'], [False], ignore)
    
    # Second search, on the ill-maintained LSL_DEPRECATED page
    url = 'http://wiki.secondlife.com/w/index.php?title=Category:LSL_Deprecated'
    pageBegin = 'Pages in category'
    pageEnd = 'class="printfooter"'
    searchTerm = '<li><a href="/wiki/'
    ignore = ['\n', '(', '(previous 200) (', 'next 200', 'previous 200', '(previous 200) (next 200)\n']
    spidey.crawl(url, pageBegin, pageEnd, searchTerm, delim, [], depFilename2)
    spidey.cleanResults(depFilename, [False], [' ','_'], ignore)

    # Merge the two dep files
    depFile1 = open(depFilename, 'r')
    depFile2 = open(depFilename2, 'r')
    deps1 = depFile1.read().splitlines()
    # debug- print(str(deps1))
    deps2 = []
    for line in depFile2:
        line = line.strip('\n')
        if line[0:2] == 'Ll':
            line = 'll' + line[2:]
        if not line in deps1:
            if line != '\\n':
                deps2.append(line.strip('\n'))
    deps2Txt = '\n'.join(deps2)
    depFile1.close
    depFile2.close
    depFile1 = open(depFilename, 'a')
    depFile1.write(deps2Txt)
    depFile1.close


    # Remove deps from captured result files case insensitively
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
            print('Removing deprecation from' + srcFilename + ': ' + dep)

        srcTxt = '\n'.join(src)
        srcFile.close
        srcFile = open(srcFilename, 'w')
        srcFile.write(srcTxt)
        srcFile.close

    depFile.close

    print('Done!')

# Search txt for stuff between delim, return list
def getReplacements(txt, delim):
    results = []
    while txt: 
        startFind   = txt.find(delim[0]) + len(delim[0])
        endFind     = txt.find(delim[1], startFind)
        if endFind == -1: break
        found = txt[startFind:endFind]
        results.append(found)
        txt = txt[endFind + len(delim[1]):]
        print(found)

    return results

# Generate main syntax file
def generateSyntax():

    # Simple types will be manual
    # LSL_Manual.txt also forms the main template and holds the pain in the
    # butt regex stuff and vim syntax references
    manualFile    = open('LSL_Manual.txt', 'r')
    manualTxt     = manualFile.read()
    manualFile.close
    delim = ['!!', '!!']

    replacements = getReplacements(manualTxt, delim)

    for replacement in replacements:
        srcFile = open(replacement + '.txt', 'r')
        srcTxt  = srcFile.read()
        srcFile.close
        srcTxt  = srcTxt.replace('\n', '\n\ ')
        manualTxt = manualTxt.replace(delim[0] + replacement + delim[1], srcTxt)

    manualTxt = manualTxt.replace('LASTUPDATE', str(date.today()))
    # todo- insert last update into README.md file
    readmeFile = open('plug-README.md', 'r')
    readmeTxt = readmeFile.read()
    readmeTxt = readmeTxt.replace('LASTUPDATE', str(date.today()))
    readmeFile.close
    readmeFile = open('plug-README.md', 'w')
    readmeFile.write(readmeTxt)
    readmeFile.close


    syntaxFile = open('plug-syntax.txt', 'w')
    syntaxFile.write(manualTxt)
    syntaxFile.close

# Create directories and cp plug-* files to proper files and locations 
def stuffFiles():
    for r in conf['structure']:
        directory = r['directory']
        filename    = r['filename']
        source      = r['source']

        print('Stuffing: ' + directory + filename)
        try:
            os.mkdir(directory)
        except:
            pass
        srcFile   = open(source, 'r')
        dstFile   = open(directory+filename, 'w+')
        srcTxt = srcFile.read()
        dstFile.write(srcTxt)
        srcFile.close
        dstFile.close


if __name__ == "__main__":

    conf = getConf()

    scrapeMain()

    scrapeDeps()

    generateSyntax()

    stuffFiles()

    print('All done!  Enjoy your day!')
