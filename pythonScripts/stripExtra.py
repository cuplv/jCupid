#! /usr/bin/env python

"""
this file will run the degbugJavac and debugJava on the given file name, with the -XX:+TraceBytecodes flag and save output in a file. It will then strip all the output outside the 
desired function (second input to this script). Finally it will remove the process ID and first numbers on a line. After this is done it 
will do the whole process 99 more times and will diff consecutive runs to see differences (save output?) and count number of bytecodes.
"""

import subprocess
import sys

debugJavac = "/usr/local/OpenJDK8/build/linux-x86_64-normal-server-fastdebug/jdk/bin/javac"
debugJava = "/usr/local/OpenJDK8/build/linux-x86_64-normal-server-fastdebug/jdk/bin/java"
p1 = subprocess.Popen([debugJavac,sys.argv[1]],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
p1.communicate()

p2 = subprocess.Popen([debugJava,"-XX:+TraceBytecodes","-Xint","Test"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

so = p2.communicate()[0]

print(len(so))


