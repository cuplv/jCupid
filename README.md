# bytecode-tool

## Necessary tools:
### OpenJDK

#### Obtaining source code:
===
This will require building OpenJDK with certain flags, thus you must obtain the code, this is done with Mercurial:

```
hg clone http://hg.openjdk.java.net/jdk8/jdk8 YourOpenJDK 
cd _YourOpenJDK_ 
bash ./get_source.sh
```

#### Configuring
===
After the source code is obtained we need to configure the build. For building OpenJDK8 we will need a version of JDK7 that is Update 7 or newer. You can go [here](http://www.oracle.com/technetwork/java/javase/downloads/index.html) to obtain JDK 7. 

Now we can configure:
<pre>
cd <i>YourOpenJDK</i>
bash ./configure --enable-debug --with-target-bits=64
</pre>

#### Making
===
Easiest part:

```
make all
```

pythonScripts contains just those.
    flagVariance.py is a script to test the effect of different flags on number of bytecodes executed
    stripExtra.py is a script that will run a given program (command line arg) and will use the print the executed bytecodes and strip off info surounding given method name (commandline arg)
    diffRuns.py a script to call stripExtra a given number of times and diff the output bytecodes

HelloWorld.java - just that

Lucky13.java - code that will implement a lucky13 attack (length of input makes MAC run longer or shorter)

SumBytes.java - takes a string and sums those bytes, value determines whether to hash once or twice.

SumRandomBytes.java - Takes a string and sums those bytes, that determines how many bytes to read from /dev/random, hashes that resulting string of bytes.
