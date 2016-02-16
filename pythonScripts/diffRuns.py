#! /usr/bin/env python
"""
    This file will run the stripExtra script on a given file (argument 1), with method name (argument 2) an given number of times (argument 3)
    and will diff the consecutive outputs and save them to files. This file assumes it is run from the same directory
    as stripExtra.py
"""

import subprocess
import sys

runs = 100
program = "stripExtra.py"
if len(sys.argv) < 2:
    print("You must provide a file to compile, it must be a .java file")
    sys.exit()
if len(sys.argv) < 3:
    print("You must provide a method name to look for")
    sys.exit()
if len(sys.argv) < 4:
    printf("You did not provide a number of times to run the script, will use the default value of 100")
else:
    runs = int(sys.argv[3])


diffValue=[]
for i in range(runs):
    diffValue.append([])
    p = subprocess.Popen(["./stripExtra.py",sys.argv[1],sys.argv[2],"out{:d}".format(i)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    so, se = p.communicate()

    if se:
        se = se.split("\n")
        print("There were errors running the stripExtra script:")
        for e in se:
            print(e)

        print("This script will continue as if everything is fine, this may lead to unexpected results")

# at this point we have all the output files, now we need to diff them, instead of diffing only consecutive pairs
# we diff every different pair. The first will diff everything, then we go to the first difference from the first
# and diff with everything after (everything before is same as first) and continue.

toDo = range(runs)
curr = 0
while toDo:
    # removed = []
    # we only want to loop over values that are in toDo, but I modify toDo, so can't loop through toDo directly
    for i in [j for j in range(curr+1,runs) if j in toDo]:
        # if i in removed:
            # continue;
        p = subprocess.Popen(["diff","out{:d}".format(curr),"out{:d}".format(i)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        so,se = p.communicate()

        if se:
            se = se.split("\n")
            print("There was an error running diff on files: ")
            for e in se:
                print(e)

        if so: # there was a difference, so write it to a file
            so = so.split("\n")
            f = open("diff{:d}-{:d}".format(curr,i),"w")
            print("There was a difference between runs {:d} and {:d}, saving the diff".format(curr,i))
            for o in se:
                f.write(o)
                f.write("\n")
            f.close()
        else: # there was no error, so remove it from toDo
            toDo.remove(i)
            # removed.append(i)

    # update curr
    toDo.remove(curr)
    if toDo:
        curr = toDo[0]


