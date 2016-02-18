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

import difflib
import os
import subprocess
import sys



def runProgram(jFile,cName,mName,inp,run):
    """This function will handle calling the stripExtra script once and provide input (if given) then return results"""
    if inp:
        p = subprocess.Popen(["./stripExtra.py",jFile,cName,mName,inp,"out{:d}".format(run)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        so, se = p.communicate()
    else:
        p = subprocess.Popen(["./stripExtra.py",jFile,cName,mName,"fake","out{:d}".format(run)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        so, se = p.communicate()

    if se:
        se = se.split("\n")
        sys.stderr.write("There were errors running the stripExtra script:\n")
        for e in se:
            sys.stderr.write(e)
            sys.stderr.write("\n")

        sys.stderr.write("This script will continue as if everything is fine, this may lead to unexpected results\n")

    return so.split("\n")


def findDiffs(toDo):
    """This program will diff the various entries of toDo, and remove any entries that are the same as
    previous runs."""
    curr = 0 
    toSkip= []
    while curr < len(toDo):
        for i in [j for j in range(curr+1,len(toDo)) if j not in toSkip]:
            sys.stderr.write("diffing {:d} and {:d}\n".format(curr,i))
            # now we diff curr and toDo[i]
            p = subprocess.Popen(["diff","out{:d}".format(curr),"out{:d}".format(i)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            so,se = p.communicate()
            if se:
                sys.stderr.write("There was an error diffing those files:\n")
                for e in se:
                    sys.stderr.write(e)
                    sys.stderr.write("\n")


            if so: # there was a difference, so write it to a file
                so = so.split("\n")
                f = open("diff{:d}-{:d}".format(curr,i),"w")
                sys.stderr.write("There was a difference between runs {:d} and {:d}, saving the diff\n".format(curr,i))
                f.write(so)
                f.write("\n")
                f.close()
            else: # there was no error, so skip it
                toSkip.append(i)
                sys.stderr.write("Run {:d} is the same as run {:d} removing extra file\n".format(curr,i))
                os.remove("out{:d}".format(i))

        # update curr
        toSkip.append(curr)
        while curr in toSkip:
            curr += 1 


def main():
    """This function will handle all user input, and call other functions"""
    runs = 20
    program = "stripExtra.py"
    if len(sys.argv) < 2:
        sys.stderr.write("You must provide a file to compile, it must be a .java file\n")
        sys.exit()
    if len(sys.argv) < 3:
        sys.stderr.write("You must provide a class name to look for\n")
        sys.exit()
    if len(sys.argv) < 4:
        sys.stderr.write("You must provide a method name to look for\n")
        sys.exit()
    if len(sys.argv) < 5:
        sys.stderr.write("You did not provide a number of times to run the script, will use the default value of 20\n")
    else:
        runs = int(sys.argv[4])
    if len(sys.argv) < 6:
        sys.stderr.write("You did not provide a file for input to program, assumes program takes no input.\n")
        numFiles = 0
    else:
        numFiles = len(sys.argv) - 5

    # out will be the output from alllllll the runs, each entry is a different run
    out = []
    files = [] 
    if numFiles == 0:
        numFiles += 1
        f.append(None)
    else:
        for i in range(5,5+numFiles):
            files.append(sys.argv[i])
    for i in range(numFiles*runs):
        f = files[i / runs]
        out.append(runProgram(sys.argv[1],sys.argv[2],sys.argv[3],f,i))

    # at this point we have all the output files, now we need to diff them, instead of diffing only consecutive pairs
    # we diff every different pair. The first will diff everything, then we go to the first difference from the first
    # and diff with everything after (everything before is same as first) and continue.
    # instead of using diff (since we don't have files) we will use difflib
    findDiffs(out)

if __name__ == "__main__":
    main()
