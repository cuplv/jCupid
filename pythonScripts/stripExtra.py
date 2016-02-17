#! /usr/bin/env python

"""
this file will run the degbugJavac and debugJava on the given file name, with the -XX:+TraceBytecodes flag and save output in a file. It will then strip all the output outside the 
desired function (second input to this script). Finally it will remove the process ID and first numbers on a line. 

The script assumes a number of arguments:

The first is the location of the java file to compile.
The second is the class we are interested in.
The third is the name of the method we are interested in.
The fourth (if entered) is the input file to read inputs from.
The fifth (if entered) is the output file to write results to.
"""


import subprocess
import sys
import re

debugJavac = "/usr/local/OpenJDK8/build/linux-x86_64-normal-server-fastdebug/jdk/bin/javac"
debugJava = "/usr/local/OpenJDK8/build/linux-x86_64-normal-server-fastdebug/jdk/bin/java"

def compileAndRun(fileName,className,inputFile):
    """This function will handle the compilation and will run the file with any inputs"""
    # first we compile the program with the debug compiler
    # we need to add the -d flag and the "." so that we create the .class file in the local directory. will be cleaned up later
    p1 = subprocess.Popen([debugJavac,"-d","/tmp/",fileName],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p1.communicate()

    # now we run the debug JVM with the flags in order to get the bytecode trace

    # first we extract the class name. We find the last / and the .java, everything between should be the className
    p2 = subprocess.Popen([debugJava,"-classpath","/tmp/","-XX:+TraceBytecodes","-Xint",className],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for i in inputFile:
        p2.stdin.write(i); # this line may need + "\n" if input isn't accepted

    so, se = p2.communicate()
    if se:
        se = se.split("\n")
        # there is something in the stdError output. Report this to the user and attempt to continue.
        print("There was an error running your code: ")
        for e in se:
            print(e)
        print("Script will continue, but depending on error may have unexpected results")
    # make the output have one line per element

    return so.split("\n")

def stripLines(so,phrase):
    """This function will strip lines before the function is called and after the function is run."""

    # search the output for the phrase className.methodName
    enum = list(enumerate(so))
    # data will be all the lines we care about.
    data = []
    try:
        first = next(i for i,v in enum if re.match(r'.*'+phrase,v))
        # for the second we will assume there is only one line after the phrase, probably a bad assumption
        second = next(i for i,v in reversed(enum) if re.match(r'.*' + phrase,v))
    except StopIteration:
        print("Could not find " + phrase + " in the output, are you sure the function is called?")
    else:
        try:
            stop = so[second:].index("")
        except ValueError:
            print("Weird error, could not find an empty string after last return")
        else:
            data = so[first:stop+second]

    return data

def cleanData(data):
    """This function will clean up the data to remove process id and overall bytecodes run"""

    # now we format the output: first remove process id -
    data = [re.sub(r'\[[0-9]*\]','',s,1) for s in data]

    # now remove overall bytecodes run:
    data = [re.sub(r'\s+[0-9]+','',s,1) for s in data]

    return data

def main():
    """This function will handle all command-line arguments and call other functions"""
    if(len(sys.argv) < 2):
        print("Must have a first argument - java file to compile");
        sys.exit()

    if(len(sys.argv) < 3):
        print("Must have a second argument, class name to look for.")
        sys.exit()

    if(len(sys.argv) < 4):
        print("Must have a third argument, method name to look for.")
        sys.exit()

    iFile = []
    if(len(sys.argv) < 5):
        print("No input file given, no input given to program.")
    else:
        try:
            iFile = open(sys.argv[4],"r").readlines()
        except IOError as e:
            print("Couldn't open file: "+sys.argv[4])
            print("Got this error:")
            print(e)
            print("Script will continue as if there were no input file")
            iFile = []

    if (len(sys.argv) < 6):
        oFile = open("output","w")
    else:
        oFile = open(sys.argv[5],"w")

    className= sys.argv[1][sys.argv[1].rfind("/")+1:sys.argv[1].find(".java")]
    output = compileAndRun(sys.argv[1],className,iFile)

    # output now needs to be formatted
    phrase = sys.argv[2] + "." + sys.argv[3]
    data = stripLines(output,phrase)

    # now we have the lines we need, we want to remove [####] and ######  from them:

    data = cleanData(data)

    # now that data is clean... write it to file:
    for i in data:
        oFile.write(i+"\n")


if __name__ == "__main__":
    main()
