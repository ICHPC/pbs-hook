#!/usr/bin/env python

from __future__ import print_function
import re
import subprocess

f=open("tests_good.txt", "r" )
tests_good = f.readlines()
f.close()
f=open("tests_bad.txt", "r" ) 
tests_bad = f.readlines()
f.close()

for test  in tests_good:
	test = test.split("|" )
	queue = test[0].strip()
	test  = test[1].strip()
	test = test.split()
#	print(test)
	test.extend(["jobscript"])
#	print(test)
	r=["qsub"]
	r.extend(test)	
	test = r 
	print("TEST: [%s][%s]" %( queue, test ) )
	out = subprocess.check_output( test )
	jobid = out
	if not re.match("^[1234567890]+", jobid ):
		print("\tERROR: JOB SUBMISSION FAILED: " + jobid.strip() )
	else:
		try:
			ret = subprocess.check_output( ["qstat", jobid.strip() ] )
			ret = ret.split("\n")
			ret = ret[2]
			ret = ret.split()
			ret = ret[5]
			if ret == queue:
				print("\tSUCCESS")
			else:
				print("\tERROR: WRONG QUEUE: expected " + queue + " got " + ret.strip() )
			subprocess.check_output( ["qdel" , jobid.strip() ] )	
		except:
			print("\tERROR: JOB QSTAT FAILED")

		

for test  in tests_bad:
	test = test.split("|" )
	queue = test[0].strip()
	test  = test[1].strip()
	test = test.split()
#	print(test)
	test.extend(["jobscript"])
#	print(test)
	r=["qsub"]
	r.extend(test)	
	test = r 
	print("TEST: [%s][%s]" %( queue, test ) )
	out = subprocess.check_output( test )
	jobid = out
	if not re.match("^[1234567890]+", jobid ):
		print("\tSUCCESS: JOB SUBMISSION FAILED: " + jobid.strip() )
	else:
		print("\tERROR: JOB ACCEPTED" )
		subprocess.check_output( ["qdel" , jobid.strip() ] )	

