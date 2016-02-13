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
p1 = subprocess.Popen([debugJavac,"-d",".",sys.argv[1]],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
p1.communicate()

# now we run the debug JVM with the flags in order to get the bytecode trace

# first we extract the class name. We find the last / and the .java, everything between should be the className
className= sys.argv[1][sys.argv[1].rfind("/")+1:sys.argv[1].find(".java")]
p2 = subprocess.Popen([debugJava,"-XX:+TraceBytecodes","-Xint",className],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
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
    print("Must have a third argument, method name to look for.")
    sys.exit()

f = open("tmp",'w')
for item in so:
    f.writelines("%s\n" %item)
f.close()

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
    data = so[first:second+2]
    print("first = " + str(first))
    print("so[first] = " + so[first])
    print("data[0] = " + data[0])
    print("second = " + str(second))
    print("data[-1] = " + data[-1])
    print("so[second+1] = " + so[second+1])
    print("data[-3] = " + data[-3])
    print("len(data[-3]) = " + str(len(data[-3])))
    print("len(data) = " + str(len(data)))
    print("data.count('') = " + str(data.count("")))
