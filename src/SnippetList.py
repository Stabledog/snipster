#!/usr/bin/env python3

import os
import csv
from Snippet import Snippet
from tabulate import tabulate

snippetList = []
sourceDir = str(os.path.expanduser("~/.snipster"))
snippetListFile = "__snipster__.csv"


def lookupSnippetPath(id):
    print("looking up")
    openSnippetList()
    return findSnippet(id)

def showSnippetList(filters):
    print("show snippets")
    openSnippetList()
    if filters != []:
        filterSnippets(filters)
    printSnippets()

def sourceSnippets():
    print("Sourcing snippets")
    walkDirectories(sourceDir)
    saveSnippetList(sourceDir)


def filterSnippets(filters):
    print(str(filters))

def printSnippets():
    headers = ["ID", "Title", "Language", "Tags", "Filename"]
    table = []
    for snippet in snippetList:
        filePathIndex = len(snippet)-1
        snippet[filePathIndex] = snippet[filePathIndex][len(sourceDir):]
        table.append(snippet)
    print(tabulate(snippetList, headers=headers, tablefmt="pipe"))
    print("Snippets")

def walkDirectories(basePath):
    allTheFiles = []
    subDirectories = []
    for(dirpath, dirnames, filename) in os.walk(basePath):
        allTheFiles.extend(filename)
        subDirectories.extend(dirnames)
        break

    for file in allTheFiles:
        if file[0:2] != "__":
            print(str(file))
            try:
                snippetList.append(Snippet(basePath + file))
            except Exception:
                print("Snippet " + str(file) + " not added to list.")
    for directory in subDirectories:
        walkDirectories(basePath + "/" + directory)


# formatting: id;title;lang;tag1,tag2;filepath
def saveSnippetList(sourceDir):
    listFile = open(sourceDir + "/" + snippetListFile, "w")
    for snippet in snippetList:
        listFile.write(snippet.id + ";")
        listFile.write(snippet.title + ";")
        listFile.write(snippet.language + ";")
        taglist = ""
        for tag in snippet.tags:
            taglist += tag + ","
        listFile.write(taglist.rstrip(",") + ";")
        listFile.write(snippet.path + "\n")

def openSnippetList():
    print("opening file")
    try:
        with open(sourceDir + "/" + snippetListFile) as snippetCSV:
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
