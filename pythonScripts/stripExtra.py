#! /usr/bin/env python

"""
this file will run the degbugJavac and debugJava on the given file name, with the -XX:+TraceBytecodes flag and save output in a file. It will then strip all the output outside the 
desired function (second input to this script). Finally it will remove the process ID and first numbers on a line. 

The script assumes a number of arguments:

The first is the name (including path to it) of the java file to compile.
The second is the class we are interested in.
The third is the name of the method we are interested in.
The fourth (if entered) is the input file to read inputs from.
The fifth (if entered) is the output file to write results to, if none given then prints to stdout
"""


from optparse import OptionParser
import subprocess
import sys
import re

debugJavac = "/usr/local/OpenJDK8/build/linux-x86_64-normal-server-fastdebug/jdk/bin/javac"
debugJava = "/usr/local/OpenJDK8/build/linux-x86_64-normal-server-fastdebug/jdk/bin/java"

def compileProg(fileName):
    """This function will handle the compilation of the given file with the debugJavac, but only if this script is called with
    the -c flag."""
    # first we compile the program with the debug compiler
    # we need to add the -d flag and the "." so that we create the .class file in the local directory. will be cleaned up later
    p1 = subprocess.Popen([debugJavac,"-d","/tmp/",fileName],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p1.communicate()

def runProg(className,inputFile):
    """This function will run the file with any inputs"""

    # we run the debug JVM with the flags in order to get the bytecode trace

    p2 = subprocess.Popen([debugJava,"-classpath","/tmp/","-XX:+TraceBytecodes","-Xint",className],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for i in inputFile:
        p2.stdin.write(i); # this line may need + "\n" if input isn't accepted

    so, se = p2.communicate()
    if se:
        se = se.split("\n")
        # there is something in the stdError output. Report this to the user and attempt to continue.
        sys.stderr.write("There was an error running your code:\n")
        for e in se:
            sys.stderr.write(e)
            sys.stderr.write("\n")
        sys.stderr.write("Are you sure it was compiled?\n")
        sys.stderr.write("Script will continue, but depending on error may have unexpected results\n")
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
        second = next(i for i,v in reversed(enum) if re.match(r'.*' + phrase,v))
    except StopIteration:
        sys.stderr.write("Could not find " + phrase + " in the output, are you sure the function is called?\n")
    else:
        try:
            stop = so[second:].index("")
        except ValueError:
            sys.stderr.write("Weird error, could not find an empty string after last return\n")
        else:
            data = so[first:stop+second]

    return data

def cleanData(data):
    """This function will clean up the data to remove process id and overall bytecodes run"""

    # now we format the output: first remove process id -
    data = [re.sub(r'\[[0-9]*\]\s+[0-9]*','',s) for s in data]

    # now remove overall bytecodes run:
    # data = [re.sub(r'\s+[0-9]+','',s,1) for s in data]

    return data


def main():
    """This function will handle all command-line arguments and call other functions"""
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",help="Must have java file to compile", metavar="FILE")
    parser.add_option("-c", "--compile", action="store_true",dest="toCompile",help="Determines whether to compile the program or not", metavar="COMPILE")
    parser.add_option("-n", "--class", dest="className",help="class name to strip around", metavar="CLASS")
    parser.add_option("-m", "--method", dest="method",help="Method name to strip around", metavar="METHOD")
    parser.add_option("-i", "--input", dest="inputFile",help="input file to read from", metavar="INPUT")
    parser.add_option("-o", "--output", dest="outputFile",help="output file to write output to", metavar="OUTPUT")

    (options,args) = parser.parse_args()

    if(options.filename == None):
        print("Must have a java file to compile, written after the -f flag.");
        sys.exit()

    if(options.className == None):
        print("Must have a class name to look for, written after the -n flag.")
        sys.exit()

    if(options.method == None):
        print("Must have a method name to look for, written after the -m flag.")
        sys.exit()
    
    iFile = []
    if(options.inputFile == None):
        sys.stderr.write("No input file provided, must be added after -i flag.")
    else:
        try:
            iFile = open(options.inputFile,"r").readlines()
        except IOError as e:
            sys.stderr.write("Couldn't open file: "+sys.argv[4]+ "\n")
            sys.stderr.write("Got this error:\n")
            sys.stderr.write("\t"+str(e))
            sys.stderr.write("\n")
            sys.stderr.write("Script will continue as if there were no input file\n")

    if (options.outputFile == None):
        oFile = sys.stdout 
    else:
        oFile = open(options.outputFile,"w")

    # we find the className from the file provided for the running. The className on the commandline
    # is for stripping input around, but may not be the "main" class of the file
    className= options.filename[options.filename.rfind("/")+1:options.filename.find(".java")]
    if options.toCompile:
        compileProg(options.filename)
    output = runProg(className,iFile)

    # output now needs to be formatted
    phrase = options.className + "." + options.method 
    data = stripLines(output,phrase)

    # now we have the lines we need, we want to remove [####] and ######  from them:

    data = cleanData(data)

    # now that data is clean... write it to file:
    for i in data:
        oFile.write(i+"\n")

    oFile.close()


if __name__ == "__main__":
    main()
