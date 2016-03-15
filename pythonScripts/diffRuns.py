#! /usr/bin/env python
"""
    This file will run the stripExtra script on a given file, with method name and given number of times
    and will diff the outputs and save them to files. This file assumes it is run from the same directory
    as stripExtra.py, that is it will call the program as ./stripExtra.py

    This script takes numerous command line inputs:

    First - java file to run through stripExtra
    Second - class name to give to stripExtra
    Third - method name to give to stripExtra
    Fourth (optional) - file to read input from
    Fifth (optional) - number of times to run stripExtra

    If no input file is given then it is assumed the program doesn't take any input
"""

from optparse import OptionParser
import os
import re
import subprocess
import sys

options={}
def runProgram(jFile,cName,mName,inp,run):
    """This function will handle calling the stripExtra script once and provide input (if given) then return results"""
    if inp:
        if run == 0:
            p = subprocess.Popen(["./stripExtra.py","-f",jFile,"-n",cName,"-m",mName,"-i",inp,"-c"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        else:
            p = subprocess.Popen(["./stripExtra.py","-f",jFile,"-n",cName,"-m",mName,"-i",inp],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        so, se = p.communicate()
    else:
        if run == 0:
            p = subprocess.Popen(["./stripExtra.py","-f",jFile,"-n",cName,"-m",mName,"-c"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        else:
            p = subprocess.Popen(["./stripExtra.py","-f",jFile,"-n",cName,"-m",mName],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        so, se = p.communicate()

    if se:
        se = se.split("\n")
        sys.stderr.write("There were errors running the stripExtra script:\n")
        for e in se:
            sys.stderr.write(e)
            sys.stderr.write("\n")

        sys.stderr.write("This script will continue as if everything is fine, this may lead to unexpected results\n")

    return so.split("\n")

def getLineNumber(bigList,first,second,line):
    """This function is called when there is a difference between two outputs. The diff is written to the file diff{first}-{second} so we will open that file and find the first
    difference and find the line number by referencing javap."""
    global options

    classLineNbr = next(i for i,v in reversed(list(enumerate(bigList[first][:line]))) if options.className in v)
    classLine = bigList[first][classLineNbr]

    lastLineNbr = next((i for i,v in enumerate(bigList[first][classLineNbr:line]) if v == ""),line-classLineNbr)-1
    lastLineNbr += classLineNbr
    lastLine = bigList[first][lastLineNbr]
    relative = int(lastLine.split()[0])

    methodName = classLine[classLine.find(options.className) + len(options.className)+1:classLine.find("(")] 

    p = subprocess.Popen(["javap","-l","/tmp/"+options.filename[options.filename.rfind("/")+1:].replace("java","class")],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    so, se = p.communicate()

    if se:
        se = se.split("\n")
        sys.stderr.write("There were errors running the javap utility:\n")
        for e in se:
            sys.stderr.write(e)
            sys.stderr.write("\n")

        sys.stderr.write("This script will continue as if everything is fine, this may lead to unexpected results\n")


    so = so.split("\n")

    methodTrace = so[next(i for i,v in enumerate(so) if methodName in v):]


    for i in range(len(methodTrace)):
        if ": " not in methodTrace[i]:
            continue
        
        if int(methodTrace[i][methodTrace[i].find(": ")+2:]) < relative:
            continue
        else:
            break

    print ("Divergence happens at: " + methodTrace[i-1].strip()[:methodTrace[i-1].strip().find(":")])



    


 


def findDiffs(toDo):
    """This program will diff the various entries of toDo, and remove any entries that are the same as
    previous runs."""
    curr = 0 
    toSkip= []
    filesWritten=[]
    while curr < len(toDo):
        for i in [j for j in range(curr+1,len(toDo)) if j not in toSkip]:
            sys.stderr.write("diffing {:d} and {:d}\n".format(curr,i))
            # now loop through the curr output and the i output
            
            foundDiff = False
            for k in range(max(len(toDo[curr]),len(toDo[i]))):
                try:
                    if toDo[curr][k] == toDo[i][k]:
                        continue
                    else:
                        # there is a difference at the kth entry!
                        foundDiff = True
                        break
                except IndexError:
                    # can't index into one of these, so the one we can index
                    # into will tell us the place of the difference.
                    foundDiff = True
                    break

            # at this point k is the first difference, or k = max(lens) 
            if not foundDiff:
                # there was no difference so the ith and the currth entries are the same!
                toSkip.append(i)
            else:
                # there is a difference! so write the output files!
                sys.stderr.write("There was a difference between runs " + str(curr) + " and " + str(i) + " saving output files\n")
                if curr not in filesWritten:
                    f = open("out"+str(curr),"w")
                    for line in toDo[curr]:
                        f.write(line)
                        f.write("\n")
                    f.close()
                    filesWritten.append(curr)
                if i not in filesWritten:
                    f = open("out"+str(i),"w")
                    for line in toDo[i]:
                        f.write(line)
                        f.write("\n")
                    f.close()
                    filesWritten.append(i)

                getLineNumber(toDo,curr,i,k)

            
            # now we diff curr and toDo[i]
            # p = subprocess.Popen(["diff","out{:d}".format(curr),"out{:d}".format(i)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            # so,se = p.communicate()
            # if se:
                # sys.stderr.write("There was an error diffing those files:\n")
                # for e in se:
                    # sys.stderr.write(e)
                    # sys.stderr.write("\n")


            # if so: # there was a difference, so write it to a file
                # p = subprocess.Popen(["diff","--side-by-side","out{:d}".format(curr),"out{:d}".format(i)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                # so,se = p.communicate()
                # so = so.split("\n")
                # f = open("diff{:d}-{:d}".format(curr,i),"w")
                # sys.stderr.write("There was a difference between runs {:d} and {:d}, saving the diff\n".format(curr,i))
                # for s in so:
                    # f.write(s)
                    # f.write("\n")
                # f.close()
                # getLineNumber(curr,i)
            # else: # there was no error, so skip it
                # toSkip.append(i)
                # sys.stderr.write("Run {:d} is the same as run {:d} removing extra file\n".format(curr,i))
                # os.remove("out{:d}".format(i))

        # update curr
        toSkip.append(curr)
        while curr in toSkip:
            curr += 1 


def main():
    """This function will handle all user input, and call other functions"""
    runs = 20
    program = "stripExtra.py"

    parser = OptionParser()

    parser.add_option("-f", "--file", dest="filename",help="Must have java file to compile", metavar="FILE")
    parser.add_option("-r", "--runs", dest="runs",help="How many runs to give to each input file. 20 by default", metavar="RUNS")
    parser.add_option("-n", "--class", dest="className",help="class name to strip around", metavar="CLASS")
    parser.add_option("-m", "--method", dest="method",help="Method name to strip around", metavar="METHOD")
    parser.add_option("-i", "--input", action="append",dest="inputFiles",help="input file to read from", metavar="INPUT")
    parser.add_option("-o", "--output", dest="outputFile",help="output file to write output to", metavar="OUTPUT")

    global options
    (options,args) = parser.parse_args()

    if options.filename == None:
        sys.stderr.write("You must provide a file to compile, it must be a .java file, following the -f flag\n")
        sys.exit()
    if options.className == None:
        sys.stderr.write("You must provide a class name to look for, following the -n flag\n")
        sys.exit()
    if options.method == None:
        sys.stderr.write("You must provide a method name to look for, following the -m flag\n")
        sys.exit()
    if options.runs == None:
        sys.stderr.write("You did not provide a number of times to run the script, will use the default value of 20\n")
    else:
        runs = int(options.runs)
    if options.inputFiles == None:
        sys.stderr.write("You did not provide a file for input to program, assumes program takes no input.\n")
        numFiles = 0
    else:
        numFiles = len(options.inputFiles) 

    # out will be the output from alllllll the runs, each entry is a different run
    out = []
    files = [] 
    if numFiles == 0:
        numFiles += 1
        f.append(None)
    else:
        for i in range(numFiles):
            files.append(options.inputFiles[i])

    for i in range(numFiles*runs):
        f = files[i / runs]
        out.append(runProgram(options.filename,options.className,options.method,f,i))

    # at this point we have all the output files, now we need to diff them, instead of diffing only consecutive pairs
    # we diff every different pair. The first will diff everything, then we go to the first difference from the first
    # and diff with everything after (everything before is same as first) and continue.
    findDiffs(out)

if __name__ == "__main__":
    main()
