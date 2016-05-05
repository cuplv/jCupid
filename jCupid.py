#! /usr/bin/env python


import itertools
from optparse import OptionParser
import random
import shutil
import string
import subprocess
import sys

"""This script is the main user interaction for the tool. They will provide a class name, a path to the .java file and a method name. Using this we will call jCute to determine what inputs reach different paths. Then using those inputs on the modified jdk to determine their hash value. If there is ever two different hashes then run those inputs looking for the first difference in bytecode and backtrack to a line number."""

# JCUTEDIR = "/home/ian/Documents/jcute/"
OPENJDKDIR = "/home/ian/Documents/OpenJDK-fork/build/linux-x86_64-normal-server-fastdebug/jdk/bin/"
TOOLDIR = "/home/ian/Documents/bytecode-tool/"


# def jcute(path,fileName, className):
    # """This function will call jcutec and jcute to determine which inputs will lead down different paths."""

    # if path[-1] != "/":
        # path += "/"
    # p = subprocess.Popen([JCUTEDIR+"jcutec",path,fileName,className,"-sequential"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    # (out,err) = p.communicate()
    # ret = p.returncode

    # if err:
        # sys.stderr.write("An error occurred running jcutec:\n")
        # sys.stderr.write(err)
        # sys.stderr.write("\n")
        # sys.stderr.write("Please fix these errors first\n")
        # sys.exit()
    # else:
        # sys.stderr.write(out)
        # sys.stderr.write("\n")

    # p = subprocess.Popen([JCUTEDIR+"jcute",className,"-i","100"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    # (out,err) = p.communicate()
    # ret = p.returncode

    # sys.stderr.write("Error output from jcute, these might be jcute providing input that causes your program to error\n")
    # sys.stderr.write(err)
    # sys.stderr.write("\nRest of the output of jcute:\n")
    # sys.stderr.write(out)
    # sys.stderr.write("\n")


def hasDifference(someList):
    """returns the indices where list has differences, if there are, if there are no differences then returns None"""

    for i,j in itertools.combinations(someList,2):
       if i != j and i is not None and j is not None:
           return (someList.index(i),someList.index(j))

    return None

def randomString(size,chars=string.letters + string.digits):
    """This will create a random string of given size."""
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

def hashJDK(fileName,mainClassName,stripClassName,methodName,strLen, its):
    """This function will run the modified openJDK fork with the inputs from jcute."""

    # f = open(JCUTEDIR+"tmpjcute/cuteInputLog","r")
    # data = f.readlines()
    # f.close()

    #compile the file

    p = subprocess.Popen([OPENJDKDIR+"javac", fileName],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (out,err) = p.communicate()

    if err:
        sys.stderr.write("Error compiling code:\n")
        sys.stderr.write(err)

    if out:
        sys.stderr.write("Output from compilation:\n")
        sys.stderr.write(out)

    hashes = [None]*its
    inputs = [None]*its
    ret = None
    for i in range(its):
        inputs[i] = randomString(strLen)
        print("input = " + inputs[i])
        p = subprocess.Popen([OPENJDKDIR+"java","-XX:+TraceBytecodes","-Xint","-hashClass="+stripClassName,"-hashMethod="+methodName, mainClassName],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        p.stdin.write(inputs[i]+ "\n")
        (out,err) = p.communicate()

        if err:
            sys.stderr.write("Had errors:\n")
            sys.stderr.write(err)

        if out:
            sys.stderr.write("output: \n")
            sys.stderr.write(out)
            outList = out.split("\n")
            # need to find the line containing final has is #########
            for line in outList:
                if "final hash is" not in line:
                    continue

                hashes[i] = int(line[13:])

            diffs = hasDifference(hashes)

            if diffs:
                ret = (inputs[diffs[0]],inputs[diffs[1]])
                break


    return ret

def traceJDK(mainClassName,stripClassName,methodName,inps):
    """This method will run the modified jdk to get the traces of each input, around the given stripClass and method and save the outputs to files."""


    p = subprocess.Popen([OPENJDKDIR+"java","-XX:+TraceBytecodes","-Xint","-traceClass="+stripClassName,"-traceMethod="+methodName, mainClassName],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.stdin.write(inps[0])

    (out1,err1) = p.communicate()

    if err1:
        sys.stderr.write("There was an error running the program with -traceClass and traceMethod")
        sys.exit()

    if out1:
        f = open(TOOLDIR+"out1","w")
        f.write(out1)
        f.close()

    p = subprocess.Popen([OPENJDKDIR+"java","-XX:+TraceBytecodes","-Xint","-traceClass="+stripClassName,"-traceMethod="+methodName, mainClassName],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.stdin.write(inps[1])

    (out2,err2) = p.communicate()

    if err2:
        sys.stderr.write("There was an error running the program with -traceClass and traceMethod")
        sys.exit()

    if out2:
        f = open(TOOLDIR+"out2","w")
        f.write(out2)
        f.close()


    return out1,out2

def findFirstDiff(outputs,className,methodName):
    """This will find the source code line with that corresponds to the first difference in bytecodes."""

    first = None
    for i,j in zip(enumerate(outputs[0]),enumerate(outputs[1])):
        if i != j:
            divLine = i[0]
            break
    
    # now we have the first place they differ, need to back trace to find last place the given class.method is referenced.

    searchString = className + "." + methodName
    searchStringLine = next(i for i,v in reversed(list(enumerate(outputs[0][:divLine]))) if className in v)

    # now we see if there is a blank line between these lines, if not then the first line we found is the line to compare to javap, if there is we need to take the line before the first blank line

    lineDist = next((i for i,v in enumerate(outputs[0][searchStringLine:divLine]) if v == ""),divLine-searchStringLine)-1

    return outputs[0][searchStringLine + lineDist]
    # if importantLine == 0:
        # return outputs[0][divLine]
    # else:
        # return ouputs[0][divLine + importantLine]


def crossRef(mainClassName,stripClassName,methodName,relByte):
    """This function will call javap and get a list of the line numbers with the relative bytecodes and then print the line number corresponding to the first difference."""

    p = subprocess.Popen([OPENJDKDIR+"javap", "-l",mainClassName+".class"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    (out,err) = p.communicate()

    if err:
        sys.stderr.write("There was an error running the javap utility:\n")
        sys.stderr.write(err)
        sys.exit()

    if out:
        out = out.split("\n")

        methodTrace = out[next(i for i,v in enumerate(out) if methodName in v):]

        for i in range(len(methodTrace)):
            if ": " not in methodTrace[i]:
                continue

            if int(methodTrace[i][methodTrace[i].find(": ") +2:]) < relByte:
                continue
            else:
                break


        print("Divergence happens at: " + methodTrace[i-1].strip()[:methodTrace[i-1].strip().find(":")])
                


def main():
    """This will handle all of the flags and then execute jcute and the jdk"""

    parser = OptionParser()
    # parser.add_option("-p", "--path", dest="path",help="Must have the source path to the .java file to compile",metavar="PATH")
    parser.add_option("-f", "--filename", dest="filename",help="Must have the full path including the .java file",metavar="FILE")
    parser.add_option("-c", "--mainclass", dest="mainClassName",help="class name that contains main method", metavar="MAINCLASS")
    parser.add_option("-n", "--stripclass", dest="stripClassName", help="class name that contains method to hash around, if not included uses mainclass input",metavar="STRIPCLASS")
    parser.add_option("-m", "--methodname", dest="methodName", help="method name to hash around",metavar="METHODNAME")
    parser.add_option("-l", "--length", dest="stringLength",type="int",help="length of input strings to program",metavar="STRINGLENGTH")
    parser.add_option("-i", "--iterations", dest="iterations",type="int",help="maximum number of iterations to try",metavar="MAXITERATIONS")

    (options,args) = parser.parse_args()

    if options.filename == None:
        sys.stderr.write("You must provide the name of the .java file, with full path, with the -f (--filename) option.\n")
        sys.exit()
    if options.mainClassName == None:
        sys.stderr.write("You must provide a class name with -c (--mainclass) of the class that contains the main method.\n")
        sys.exit()
    if options.methodName == None:
        sys.stderr.write("You must provide a method name to hash around with -m (--methodname).\n")
        sys.exit()
    if options.stringLength == None:
        sys.stderr.write("You must provide a length of strings to generate with -l (--length).\n")
        sys.exit()
    if options.iterations == None:
        options.iterations = 100;

    if options.stripClassName == None:
        # was not used, so make it the mainClassName
        options.stripClassName = options.mainClassName


    # jcute(options.path,options.filename,options.mainClassName)

    r = hashJDK(options.filename,options.mainClassName,options.stripClassName,options.methodName,options.stringLength,options.iterations)
    if r:
        sys.stderr.write("inputs that produce different hashes: " + str(r) + "\n")
        outs = traceJDK(options.mainClassName,options.stripClassName,options.methodName,r)

        outs = (outs[0].split("\n"),outs[1].split("\n"))
        diffLine = findFirstDiff(outs,options.stripClassName,options.methodName)
        sys.stderr.write("diffLine = " + diffLine + "\n")

        relativeByte = int(diffLine.split()[0])
        # now we get the cross reference material from javap
        crossRef(options.mainClassName,options.stripClassName,options.methodName, relativeByte)
    else:
        print("jCupid could not find inputs to cause different executed bytecodes")

        

        
    

    

if __name__ == "__main__":
    main()
