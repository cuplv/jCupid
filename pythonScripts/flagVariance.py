#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 ian <ian@ian-HP-Mini-210-2000>
#
# Distributed under terms of the MIT license.

"""
This file will run my Test java program 1000 times and read the output of bytecodes 
executed and see what the range is
"""

import numpy
import subprocess

debugJVM = "/home/ian/Downloads/YourOpenJDK/build/linux-x86-normal-server-fastdebug/images/j2sdk-image/bin/java"

# output = []
# for i in range(100):
    # p1 = subprocess.Popen([debugJVM,"-XX:+CountBytecodes","-XX:-UseCompiler","Test"],stdin=subprocess.PIPE,
        # stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # output.append(int(p1.communicate()[0][12:18]))
    # if i % 20 == 0:
        # print("i = " + str(i));


# print("median -UseCompiler = " + str(numpy.median(output)))
# print("average -UseCompiler = " + str(numpy.average(output)))
# print("range -UseCompiler = " + str(max(output) - min(output)))

output = []
for i in range(100):
    p1 = subprocess.Popen([debugJVM,"-XX:+CountBytecodes","-Xint","Lucky13"],stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p1.stdin.write("n\n")
    output.append(int(p1.communicate()[0][-10:-2]))
    if i % 20 == 0:
        print("i = " + str(i));


print("median -Xint = " + str(numpy.median(output)))
print("average -Xint = " + str(numpy.average(output)))
print("range -Xint = " + str(max(output) - min(output)))

output = []
for i in range(100):
    p1 = subprocess.Popen([debugJVM,"-XX:+CountBytecodes","-XX:-UseCompiler","Lucky13"],stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p1.stdin.write("n\n")
    output.append(int(p1.communicate()[0][-10:-2]))
    if i % 20 == 0:
        print("i = " + str(i));


print("median -XX:-UseCompiler = " + str(numpy.median(output)))
print("average -XX:-UseCompiler = " + str(numpy.average(output)))
print("range -XX:-UseCompiler = " + str(max(output) - min(output)))

output = []
for i in range(100):
    p1 = subprocess.Popen([debugJVM,"-XX:+CountBytecodes","-Xint","Lucky13"],stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p1.stdin.write("y\n")
    p1.stdin.write("12345678901234567890123456789012\n")
    output.append(int(p1.communicate()[0][-10:-2]))
    if i % 20 == 0:
        print("i = " + str(i));


print("median -Xint new input = " + str(numpy.median(output)))
print("average -Xint new input = " + str(numpy.average(output)))
print("range -Xint new input = " + str(max(output) - min(output)))

output = []
for i in range(100):
    p1 = subprocess.Popen([debugJVM,"-XX:+CountBytecodes","-XX:-UseCompiler","Lucky13"],stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p1.stdin.write("y\n")
    p1.stdin.write("12345678901234567890123456789012\n")
    output.append(int(p1.communicate()[0][-10:-2]))
    if i % 20 == 0:
        print("i = " + str(i));


print("median -XX:-UseCompiler new input = " + str(numpy.median(output)))
print("average -XX:-UseCompiler new input = " + str(numpy.average(output)))
print("range -XX:-UseCompiler new input = " + str(max(output) - min(output)))
