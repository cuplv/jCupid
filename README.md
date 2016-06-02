# jCupid 

## Necessary tools:

In order to use jCupid you must download and compile the modified OpenJDK. This is taken care of by the setup script. It will clone our modified OpenJDK
from `https://github.com/cuplv/OpenJDK` and configure and compile for you.

Thus after cloning this repository, you simply need to run `./setup`

## Requirements:

In order to install OpenJDK you will need a version of Oracles JDK 7. You can acquire that [here](http://www.oracle.com/technetwork/java/javase/downloads/index.html), this version should be in your `PATH` variable, or if it is not you should add the line `--with-boot-jdk=`*path* to the configures line in the `setup` script.

Additional system requirements are `alsa`, `freetype`, `cups`, and `xrender`, these are required to build the OpenJDK and can be installed with:

If any of the above are missing the configure step will and it will suggest how to install missing dependencies.

The script assumes you are on a 64-bit machine, if you are on a 32-bit machine you must delete part of one line of this script. The line containing `./configure --enable-debug --with-target-bits=64`, simply remove the whole `--with-target-bits flag`

## How to use tool:

Main use is through the jCupid.py script. It has a number of necessary flags: 

`./jCupid -f fileName -c mainClass [-n stripClass] -m methodName -l length [-i its] [-k input]`

```
-f  -   path to java file to run, can be relative.
-c  -   name of the class which contains the main method.
-n  -   class name to find a difference around, if ommitted the main class is used.
-m  -   method name to find a difference around.
-l  -   the length of inputs to be randomly generated, this must be an integer
-i  -   the number of iterations for jCupid to try different inputs, must be and integer. If ommitted jCupid uses 100 iterations.
-k  -   allows the user to supply the input, generally used for debugging.
```

With this we can run our tool:
`./jCupid.py -l 5 -i 20 -c repeatedSquaring -f Examples/repeatedSquaring.java -m repeatedSquare`

This will run the jCupid tool, fuzzing at most 20 inputs of length 5. jCupid will compile the file `Examples/repeatedSquaring.java`, the main method is in the class `repeatedSquaring` and jCupid will trace around the method `repeatedSquare`.

The `Examples` directory contains a few examples. You can test the tool is finding differences on any of these
examples.
