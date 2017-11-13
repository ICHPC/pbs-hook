#!/usr/bin/env python

f=open("tests_good.txt", "r" )
tests_good = f.readlines()
f.close()
f=open("tests_bad.txt", "r" ) 
tests_bad = f.readlines()
f.close()
