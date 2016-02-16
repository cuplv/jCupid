#! /usr/bin/env python

"""
this file will run the degbugJavac and debugJava on the given file name, with the -XX:+TraceBytecodes flag and save output in a file. It will then strip all the output outside the 
desired function (second input to this script). Finally it will remove the process ID and first numbers on a line. After this is done it 
will do the whole process 99 more times and will diff consecutive runs to see differences (save output?) and count number of bytecodes.
"""

import subprocess
import sys
import re

debugJavac = "/usr/local/OpenJDK8/build/linux-x86_64-normal-server-fastdebug/jdk/bin/javac"
debugJava = "/usr/local/OpenJDK8/build/linux-x86_64-normal-server-fastdebug/jdk/bin/java"

if(len(sys.argv) < 2):
    print("Must have a first argument - java file to compile");
    sys.exit()

# first we compile the program with the debug compiler
# we need to add the -d flag and the "." so that we create the .class file in the local directory. will be cleaned up later
p1 = subprocess.Popen([debugJavac,"-d","/tmp/",sys.argv[1]],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
p1.communicate()

# now we run the debug JVM with the flags in order to get the bytecode trace

# first we extract the class name. We find the last / and the .java, everything between should be the className
className= sys.argv[1][sys.argv[1].rfind("/")+1:sys.argv[1].find(".java")]
p2 = subprocess.Popen([debugJava,"-classpath","/tmp/","-XX:+TraceBytecodes","-Xint",className],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
so, se = p2.communicate()
if se:
    se = se.split("\n")
    # there is something in the stdError output. Report this to the user and attempt to continue.
    print("There was an error running your code: ")
    for e in se:
        print(e)
    print("Script will continue, but depending on error may have unexpected results")
# make the output have one line per element

so = so.split("\n")

if(len(sys.argv) < 3):
    print("Must have a second argument, method name to look for.")
    sys.exit()

# search the output for the phrase className.methodName
phrase = className + "." + sys.argv[2]
# phrase = "UnixFileSystem"
enum = list(enumerate(so))
try:
    first = next(i for i,v in enum if re.match(r'.*'+phrase,v))
    # for the second we will assume there is only one line after the phrase, probably a bad assumption
    second = next(i for i,v in reversed(enum) if re.match(r'.*' + phrase,v))
except StopIteration:
    print("Could not find " + phrase + " in the output, are you sure the function is called?")
else:
    # data will be all the lines we care about.
    data = []
    try:
        stop = so[second:].index("")
    except ValueError:
        print("Weird error, could not find an empty string after last return")
    else:
        data = so[first:stop+second]
    
    f = open("/tmp/out",'w')
    for item in data:
        f.writelines("%s\n" %item)
    f.close()

    # now we format the output
    outFile = open("/tmp/out1","w")
    p3 = subprocess.Popen(["sed","s/\[[0-9]*\]//","/tmp/out"],stdin=subprocess.PIPE,stdout=outFile,stderr=subprocess.PIPE)
    sedo1,sede1 = p3.communicate()
    outFile.close()
    if sede1:
        sede1=sede1.split("\n")
        # we're in here if something went wrong with sed
        print("There was an error running sed on your output: ")
        for e in sede1:
            print(e)
        printf("Script will continue, but depending on error may have unexpected results")

    # if the user supplies 3 arguments then the last is assumed to be the file name to save results to.
    if (len(sys.argv) >= 4):
        outFile = open(sys.argv[3],"w")
    else:
        outFile = open("output","w")

    p4 = subprocess.Popen(["sed","s/\s\+[0-9]\+//","/tmp/out1"],stdin=subprocess.PIPE,stdout=outFile,stderr=subprocess.PIPE)
    sedo2,sede2 = p4.communicate()
    outFile.close()
    if sede2:
        sede2=sede2.split("\n")
        # we're in here if something went wrong with sed
        print("There was an error running sed on your output: ")
        for e in sede2:
            print(e)


# now add sed commands, in particular "sed/\[[0-9]*\]//" <tmp > tmp1
# then another sed to remove numbers: "sed/\s+[0-9]*//" <tmp1 > tmp

