#! /usr/bin/env python
import time
import sys
import subprocess
import random
import string

def main():
    args = sys.argv
    fileName = args[1]
    className = args[2]
    length = int(args[3])
    its = int(args[4])
    method = args[5]
    inp = ''.join(random.choice(string.ascii_letters+ string.digits + string.punctuation) for _ in range(length))

    javaTotal = 0
    jCupidTotal = 0
    for i in range(5):
        # subprocess.call(["javac", fileName])
        # start = time.time()
        # for j in range(its):
            # p = subprocess.Popen(["java",className],stdin=subprocess.PIPE)
            # p.stdin.write(inp+"\n")
            # p.communicate()
        # stop = time.time()

        # javaTotal += (stop - start)

        print("after java, run " + str(i+1))
        start = time.time()
        
        p = subprocess.Popen(["./jCupid.py", "-l", str(length), "-i", str(its), "-c", className, "-f", fileName, "-m", method, "-k", inp])
        p.communicate()
        stop = time.time()

        jCupidTotal += (stop - start)

    print("java run time: " + str(javaTotal))
    print("jCupid run time: " + str(jCupidTotal)) 



if __name__ == "__main__":
    main()
