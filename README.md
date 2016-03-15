# bytecode-tool

## Necessary tools:

### OpenJDK

### Obtaining source code:
This will require building OpenJDK with certain flags, thus you must obtain the code, this is done with Mercurial:

Note that `get_source.sh`, and `configure` may not be executable by default. OpenJDK recommends simply directly calling `bash` instead of making them executable.

```bash
hg clone http://hg.openjdk.java.net/jdk8/jdk8 YourOpenJDK 
cd YourOpenJDK
bash ./get_source.sh
```

#### Configuring
After the source code is obtained we need to configure the build. For building OpenJDK8 we will need a version of JDK7 that is Update 7 or newer. You can go [here](http://www.oracle.com/technetwork/java/javase/downloads/index.html) to obtain JDK 7. It is also necessary that the JDK 7 be accessible through your `PATH`. If that is not desirable or not an option then the following configure call will need an additional flag: `--with-boot-jdk=`*path*, where *path* is the path to your JDK 7.


Now we can configure:

```bash
cd YourOpenJDK
bash ./configure --enable-debug --with-target-bits=64
```

#### Making
Easiest part:

```bash
make all
```

#### Modifying tool:

In the file `stripExtra.py` in the `pythonScripts` directory the first two lines are the absolute path to the newly made debug versions of `java` and `javac`. These lines should be modified to be the path to YOUR copy.

## How to use tool:

Main use is through the diffRuns.py script. It has a number of necessary flags: 

```
-f  -   path to java file to run, can be relative.
-n  -   class name to find a difference around.
-m  -   method name to find a difference around.
-r  -   number of times to run each file, this is not  necessary but encouraged, without it each file will be run 20 times!
-i  -   designates a file to read input from, this flag is needed before each filename!
```

With this we can run our tool:
`./diffRuns.py -f ../SumRandomBytes.java -n SumRandomBytes -m main -r 1 -i inp -i inp1`

We assume for the above that we are in the pythonScripts folder, and that inp and inp1 exist. If inp contains `hello` and inp1 contains `inp1` then the output of the script should be: 
```
diffing 0 and 1
There was a difference between runs 0 and 1 saving output files
Divergence happens at: line 57
```

## Contents
pythonScripts contains just those.

`flagVariance.py` is a script to test the effect of different flags on number of bytecodes executed

`stripExtra.py` is a script that will run a given program (command line arg) and will use the print the executed bytecodes and strip off info surounding given method name (commandline arg)

`diffRuns.py` a script to call stripExtra a given number of times and diff the output bytecodes

`HelloWorld.java` - just that

`Lucky13.java` - code that will implement a lucky13 attack (length of input makes MAC run longer or shorter)

`SumBytes.java` - takes a string and sums those bytes, value determines whether to hash once or twice.

`SumRandomBytes.java` - Takes a string and sums those bytes, that determines how many bytes to read from /dev/random, hashes that resulting string of bytes.
