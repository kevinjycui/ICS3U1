#########################
# Commenter by Kevin Cui
#########################

import os
import time

print("Hello USER. This is Commenter for Python, created by Kevin Cui 2019-06-04")
while True:
    currFileName= input("Input current file name (*.py)\n>>> ")
    currFileName = currFileName.replace('.py', '')
    if os.path.isfile(currFileName+".py"):
        break
    else:
        print("File does not exist")
getOverride = False
runCheck = True
while runCheck:
    checkOver = input("Override current file or create new file? (O)verride, (N)ew file\n>>> ").upper()
    if checkOver == 'O':
        getOverride = True
        fileName = 'temp'
        runCheck = False
    elif checkOver == 'N':
        getOverride = False
        fileName = input("Input file name, Commenter will automatically set file name to follow PEP-8 naming conventions (*.py, Leave blank to set to '"+currFileName+"_commented.py')\n>>> ").lower().replace(" ", "_")
        fileName = fileName.replace('.py', '')
        if len(fileName)==0:
            fileName = currFileName+"_commented"
        if os.path.isfile(fileName+".py"):
            confirm = ""
            while True:
                confirm = input("The file '"+fileName+".py' already exists. Are you sure you want to replace it? (Y)es, (C)ancel\n>>> ").upper()
                if confirm == 'Y':
                    runCheck = False
                    break
                elif confirm == 'C':
                    runCheck = False
                    break
                else:
                    print("Invalid input")
        else:
            runCheck = False
    else:
        print("Invalid input")
programmerName = input("Input developer name (Leave blank to set to 'Kevin Cui')\n>>> ")
if len(programmerName)==0:
    programmerName = "Kevin Cui"
programTime = input("Input time (Leave blank to set to current time)\n>>> ")
if len(programTime)==0:
    programTime = time.ctime()
programDesc = input("Input description (Leave blank to set to '"+currFileName+"')\n>>> ")
if len(programDesc)==0:
    programDesc = currFileName

file = open(fileName+".py", 'w+')
currFile = open(currFileName+".py", 'r')

file.write("#"*max(len(programmerName), len(programTime), len(programDesc), len("Description:"))+"\n")
file.write("# Programmer:\n# "+programmerName+"\n# Date:\n# "+programTime+"\n# Description:\n# "+programDesc+"\n")
file.write("#"*max(len(programmerName), len(programTime), len(programDesc), len("Description:"))+"\n\n")

commentDict = {'for':'iterate', 'while':'run until', 'in':'through', '=':'to', 'import':'add module', 'def':'define',
               'if':'check if', 'def':'define a function for', 'class':'create the class', 'init':'initialize', 'range':'the range',
               '[':'a list of', '{':'a dictionary of',']':'', '}':'', 'int':'integer of', 'float':'float of', 'str':'string of', 'list':'list of', 'bool':'boolean of',
               'round':'rounded', 'max':'maximum of', 'abs':'absolute value of', ':':'do', 'elif':'else check if', 'else':'else check', 'print':'output',
               'input':'input', 'return':'return', 'break':'break out of loop', 'continue':'go back to beginning of loop', '+=':'increment by', '-=':'reduce by',
                '*=':'multiply self by', '/=':'divide self by', '//=':'integer divide self by'}
placeHold = ['in', 'if', '=', 'import', 'while', 'def', 'class', 'init', 'range', 'int', 'float',' str', 'list', 'bool', 'round', 'max', 'abs',
             'elif', 'else', 'input', 'print', 'return', '+=', '-=', '*=', '/=', '//=']
operatorDict = {'and':'and', 'or':'or', 'not':'not', '+':'plus', '-':'minus', '**':'to the power of', '*':'multiply',
               '//':'integer divide', '/':'divide', '==':'is equal to', '>=':'is greater than or equal to', '<=':'is less than or equal to',
               '>':'is greater than', '<':'is less than', '(':'', ')':'', ':':'', 'len':'length'}

tripleQuotes = 0
for line in currFile:
    keyWords = line.split(" ")
    comment = ""
    referenced = ""
    singleQuotes = 0
    doubleQuotes = 0
    for key in range(len(keyWords)):
        for i in range(keyWords[key].count("'")):
            singleQuotes = 1-singleQuotes
        for j in range(keyWords[key].count('"')):
            doubleQuotes = 1-doubleQuotes
        for k in range(keyWords[key].count('"""')):
            tripleQuotes = 1-tripleQuotes
        if singleQuotes==0 and doubleQuotes==0 and tripleQuotes==0:
            if keyWords[key]=='=' and key-1>=0:
                comment += "assign "+keyWords[key-1]+" "
            if keyWords[key] in commentDict:
                comment += commentDict[keyWords[key]]+" "
            if keyWords[key] in placeHold:
                index = 1
                while key+index<len(keyWords):
                    if keyWords[key+index] in operatorDict:
                        referenced += operatorDict[keyWords[key+index]]+" "
                    else:
                        referenced += keyWords[key+index]+" "
                    index+=1
    comment = comment.replace("(", " of ").replace(")", "").replace(":", "")
    referenced = referenced.replace("(", " of ").replace(")", "").replace(":", "")
    if len(comment)>0:
        newLine = line[:-1]+" #"+(comment+referenced)[:-1]
    else:
        newLine = line
    file.write(newLine)

currFile.close()
file.close()

if getOverride:
    newFile = open('temp.py', 'r')
    origFile = open(currFileName+'.py', 'w')
    for line in newFile.read():
        origFile.write(line)
    origFile.close()
    newFile.close()
    os.remove('temp.py')

print("Comments added successfully")
