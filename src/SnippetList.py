#!/usr/bin/env python3

import os
import csv
from Snippet import Snippet
from tabulate import tabulate

snippetList = []
sourceDir = str(os.path.expanduser("~/.snipster/"))
snippetListFile = "__snipster__.csv"

tags = []
keywords = []
languages = []
filteredSnippetList = []

def lookupSnippetPath(id):
    print("looking up")
    openSnippetList()
    return findSnippet(id)

def showSnippetList(filters):
    print("show snippets")
    global filteredSnippetList
    openSnippetList()
    if filters != []:
        filterSnippets(filters)
        setUpFilters(filters)
        filterSnippets()
    else:
        filteredSnippetList = snippetList
    printSnippets()

def sourceSnippets():
    print("Sourcing snippets")
    walkDirectories(sourceDir)
    saveSnippetList(sourceDir)

def filterSnippets():
    print("Filtering")


def setUpFilters(filters):
    for value in filters:
        if value == "-t":
            filterType = "tags"
            continue
        elif value == "-k":
            filterType = "keywords"
            continue
        elif value == "-l":
            filterType = "language"
            continue

        if filterType == "tags":
            tags.append(value)
        if filterType == "keywords":
            keywords.append(value)
        if filterType == "language":
            languages.append(value)
    print("Tags: " + str(tags))
    print("Keywords: " + str(keywords))
    print("Langs: " + str(languages))

def printSnippets():
    headers = ["ID", "Title", "Language", "Tags", "Filename"]
    table = []
    for snippet in filteredSnippetList:
        filePathIndex = len(snippet)-1
        snippet[filePathIndex] = snippet[filePathIndex][len(sourceDir):]
        table.append(snippet)
    print("Snippets")
    print(tabulate(filteredSnippetList, headers=headers, tablefmt="pipe"))

def walkDirectories(basePath):
    allTheFiles = []
    subDirectories = []
    for(dirpath, dirnames, filename) in os.walk(basePath):
        allTheFiles.extend(filename)
        subDirectories.extend(dirnames)
        break

    addSnippetsToList(allTheFiles, basePath)
    for directory in subDirectories:
        walkDirectories(basePath + directory + "/")



def addSnippetsToList(allTheFiles, basePath):
    newSnippets = []
    for file in allTheFiles:
        if file[0:2] == "__":
            continue
        try:
            snippet = Snippet(basePath + file)
            if int(snippet.id) == 0:
                newSnippets.append(snippet)
            else:
                snippetList.append(snippet)
        except Exception as e:
            print("Snippet " + str(file) + " not added to list: " + str(e))

    for snippet in newSnippets:
        newIndex = len(snippetList)+1
        while existsSnippet(newIndex):
            newIndex += 1
        assignId(snippet, newIndex)

def assignId(snippet, newIndex):
    print(str(snippet.path))
    snippet.setId(newIndex)
    snippetList.append(snippet)

# formatting: id;title;lang;tag1,tag2;filepath
def saveSnippetList(sourceDir):
    listFile = open(sourceDir + snippetListFile, "w")
    for snippet in snippetList:
        listFile.write(str(snippet.id) + ";")
        listFile.write(snippet.title + ";")
        listFile.write(snippet.language + ";")
        taglist = ""
        for tag in snippet.tags:
            taglist += tag + ", "
        listFile.write(taglist.rstrip(", ") + ";")
        listFile.write(snippet.path + "\n")

def openSnippetList():
    print("opening file")
    try:
        with open(sourceDir + snippetListFile) as snippetCSV:
            snippetListCSVFile = csv.reader(snippetCSV, delimiter= ";")
            for row in snippetListCSVFile:
                snippetList.append(row)
    except FileNotFoundError:
        print("Didn't find a snippet list file. You can create one by using the source command ('snipster source')")
        exit(1)



def findSnippet(id):
    for snippet in snippetList:
        print(str(snippet))
        if int(snippet[0]) == int(id):
            return snippet[len(snippet)-1]

    print("No snippet with id " + id + " found.")
    exit(1)

def existsSnippet(id):
    for snippet in snippetList:
        if int(snippet.id) == id:
            return True
    return False

