#
# Makefile
# ian, 2016-01-26 14:07
#

compilelucky13: Lucky13.java
	javac Lucky13.java

debugCompileLucky13: Lucky13.java
	debugJavac Lucky13.java

debugRunLucky13: Lucky13.class
	debugJava -XX:+CountBytecodes Lucky13

runlucky13: Lucky13.class
	java Lucky13

# vim:ft=make
#
