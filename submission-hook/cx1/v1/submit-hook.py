
#
# Submit hook
# CX1
# HPC - Imperial College London
# Home: github ICHPC/pbs-hook

import sys
import pbs
import traceback
import re

list_of_resources = ["ncpus","ngpus","mem","mpiprocs","ompthreads","host","switchgroup","avx","avx2","avx512","tmpspace","has_magma","gpu_type","cpumodel","using_ht"]

	# 
# This is prepended to any target_queue name to allow for future versioning in place

queue_config_version = "v1_"

classifications = {
		"interactive": {
			"nodect"   : [1,1],
			"ncpus"    : [1,8],
			"ngpus"    : [0,1],
			"walltime" : [0,8.],
			"mem"      : [1, 96],
			"interactive": True,
		},
		"debug": {
			"nodect"   : [1,1],
			"ncpus"    : [1,8],
			"ngpus"    : [0,1],
			"walltime" : [0,0.5], # Up to 30 mins
			"mem"      : [1, 96],
			"interactive": False,
		},

		"throughput24": {
			"nodect"   : [1,1],
			"ncpus"    : [1,8],
			"ngpus"    : [0,0],
			"walltime" : [0.500001,24],
			"mem"      : [1, 96],
			"interactive": False,
		},

		"throughput72": {
			"nodect"   : [1,1],
			"ncpus"    : [1,8],
			"ngpus"    : [0,0],
			"walltime" : [24.00001, 72],
			"mem"      : [1, 96],
			"interactive": False,
		},

		"general24": {
			"nodect"   : [1,16],
			"ncpus"    : [ [16,16], [32,32] ],
			"ngpus"    : [0,0],
			"walltime" : [0.50001,24.],
			"mem"      : [1, 124],
			"interactive": False,
		},

		"general72": {
			"nodect"   : [1,16],
			"ncpus"    : [ [16,16], [32,32] ],
			"ngpus"    : [0,0],
			"walltime" : [24.00001, 72.],
			"mem"      : [1, 124],
			"interactive": False,
		},
		"singlenode24": {
			"nodect"   : [1,1],
			"ncpus"    : [ [24,24], [48,48] ],
			"ngpus"    : [0,0],
			"walltime" : [1,24.],
			"mem"      : [1, 250],
			"interactive": False,
		},

		"multinode24": {
			"nodect"   : [ 2, 20 ],
			"ncpus"    : [ 12, 12 ],
			"ngpus"    : [0,0],
			"walltime" : [ 0., 24. ],
			"mem"      : [1, 46],
			"interactive": False,
		},

		"multinode48": {
			"nodect"   : [ 2, 20 ],
			"ncpus"    : [ 12, 12 ],
			"ngpus"    : [0,0],
			"walltime" : [ 24.00001, 48.00 ],
			"mem"      : [1, 46],
			"interactive": False,
		},

		"largemem24": {
			"nodect"   : [ 1, 1 ],
			"ncpus"    : [ 12, 12 ],
			"ngpus"    : [0,0],
			"walltime" : [ 0.5, 24. ],
			"mem"      : [127, 252],
			"interactive": False,
		},



		"largemem48": {
			"nodect"   : [ 1, 1 ],
			"ncpus"    : [ 12, 12 ],
			"ngpus"    : [0,0],
			"walltime" : [ 24.00001, 48. ],
			"mem"      : [127, 252],
			"interactive": False,
		},

		"gpu24": {
			"nodect"   : [ 1, 1 ],
			"ncpus"    : [ 1, 4 ],
			"ngpus"    : [1,1],
			"walltime" : [ 0.1, 24. ],
			"mem"      : [1, 16],
			"interactive": False,
		},
		"gpu48": {
			"nodect"   : [ 1, 1 ],
			"ncpus"    : [ 1, 4 ],
			"ngpus"    : [1,1],
			"walltime" : [ 24.00001, 48. ],
			"mem"      : [1, 16],
			"interactive": False,
		},



}

def match_class(selection, walltime, clssname, clss ):
	# Compare walltime
	if (walltime < clss["walltime"][0])  or ( walltime > clss["walltime"][1] ):
		pbs.logmsg( pbs.LOG_ERROR, "CLASS [" + clssname +"] failed walltime ("+str(walltime) + "in range " + str(clss["walltime"][0]) + " " + str(clss["walltime"][1]) )
		return False

	if clss["interactive"] != selection["interactive"]:
		pbs.logmsg( pbs.LOG_ERROR, "CLASS [" + clssname +"] failed interactive " + str(clss["interactive"] ) + " " + str(selection["interactive"]) )
		return False

	for minmax in [ "nodect", "ngpus" ]:
		if ( selection[minmax] < clss[minmax][0] ) or ( selection[minmax] > clss[minmax][1] ):

			pbs.logmsg( pbs.LOG_ERROR, "CLASS [" + clssname +"] failed " + minmax )
			return False

	if ( pbs.size(selection["mem"]) < pbs.size(str(clss["mem"][0])+"gb") ) or ( pbs.size(selection["mem"]) > pbs.size(str(clss["mem"][1])+"gb") ):
		pbs.logmsg( pbs.LOG_ERROR, "CLASS [" + clssname +"] failed mem" )
		return False

	if not isinstance( clss["ncpus"][0], list ):
		clss["ncpus"] = [ clss["ncpus"] ]

	ncpus_match = False
	for c in clss["ncpus"]:
		if ( selection["ncpus"] >= c[0] ) and ( selection["ncpus"] <= c[1] ):
			ncpus_match = True

	if not ncpus_match:
			pbs.logmsg( pbs.LOG_ERROR, "CLASS [" + clssname +"] failed ncpus" )
			return False

	# Classification matches
	pbs.logmsg( pbs.LOG_ERROR, " CLASS  " + clssname + " matched" )
	return True


# Match job to class. Error out if it matches more than one class
def classify_job( selection, walltime, queue = None ):
	names = ""
	ret=[];

	for clssname  in sorted(classifications.keys()):
		clss = classifications[clssname]
		if ( queue == None ) or clssname == queue:
			if match_class( selection, walltime, clssname, clss ):
				clss["target_queue"] = clssname
				ret.append( clss )
				names = names + clssname + " "

	if len(ret) > 1:
		pbs.event().reject( "Job matches multiple classes: [ " + names.strip() + "]" )

	if len(ret):
		return ret[0]
	else:
		pbs.event().reject( "Job resource selection does not match any permitted configuration.\n      Please review the CX1 Job Sizing guidance on:\n       https://bit.ly/2AInEIj\n")


# Returns the type of the submission queue "common", "private" or "express"
# Errors out is anything other than a pq*, med-bio or e* is specified
def extract_queue_type():

	if pbs.event().job.queue == "" or pbs.event().job.queue == None:
		return "common"

	if ( pbs.event().job.queue != "" ):
		queue_name=pbs.event().job.queue.name

	if len(queue_name)>0 and queue_name[0] == "e":
		return "express"
	elif len(queue_name)>0 and ( queue_name[0] == "p"  or queue_name == "med-bio" or queue_name == "viz"):
		return "private"
	elif queue_name.startswith(queue_config_version):
		queue_name = re.sub("^" + queue_config_version, "", queue_name )
		return "common:" + queue_name
	else:
		pbs.event().reject("Invalid queue name.")

# Returns a float of the # of hours requested for the job
# Errors out if not specified or the format is wrong 
def extract_walltime():
	hrs=0;
	if ( pbs.event().job.Resource_List["walltime"] == None ):
		pbs.event().reject("You must specify a walltime using the format\n      -lwalltime=HH:MM:00")
	
	wt = pbs.event().job.Resource_List["walltime"]
	wt = float(wt)/ 3600.
	return wt


# Return a dict of the job selection
# Errors out if mandatory values are not set
def extract_selection():
	if ("select" not in pbs.event().job.Resource_List) or ( pbs.event().job.Resource_List["select"] == None ):
		pbs.event().reject("You must specify a resource selection using the format\n      -lselect=N:ncpus=X:mem=Ygb" )

	select = repr(pbs.event().job.Resource_List["select"])
	select = select.split("+")

	if len(select) > 1:
		pbs.event().reject("Only one -lselect is permitted.")

	chunk = select[0]

	ret= dict()
	try:
		nodect = 0
		chunk=chunk.split(":")
		nodect = int(	 chunk[0] )

		ret["nodect"] = nodect

		for rs in chunk[1:]:
			key = rs.split("=")[0]
			val = rs.split("=")[1]
			if key not in list_of_resources:
				pbs.event().reject("Resource ["+key+"] not permitted in -lselect.")
	
			# Try converting the value to an integer if it happens to be one
			try:
				val=int(val)
			except:	
				pass

			# if the value is plausibly boolean, convert it to a bool
			if isinstance( val, str ):
				t = val.lower()
				if t == "true" :	val = True
				if t == "false":  val = False

			ret[key] = val
	except:
		pbs.event().reject("Invalid -lselect syntax. :" + str(select) + "\n     The corrcet format is -lselect=N:ncpus=X:mem=Ygb" )

	if "ncpus" not in ret:
			pbs.event().reject("[ncpus] must be in the -lselect")
	if "ngpus" not in ret:
			ret["ngpus"] = 0	
	if "mem" not in ret:
			pbs.event().reject("[mem] must be in the -lselect")


	# Not part of the select, but smuggle it in here
	ret["interactive"] = pbs.event().job.interactive
	if ret["interactive"] == None:
		ret["interactive"] = False
	else:
		ret["interactive"] = True	

	return ret
	

def fixup_icib( queue, sel ):
	if "multinode" in queue:
		selstr = repr(pbs.event().job.Resource_List["select"])
		selstr = selstr + ":icib=true"
		pbs.event().job.Resource_List["select"] = pbs.select( selstr )

def fixup_mpiprocs_ompthreads( sel ):
	selstr = repr(pbs.event().job.Resource_List["select"])

	if "mpiprocs" not in sel and "ompthreads" not in sel:
		mpiprocs   = int(sel["ncpus"])
		ompthreads = 1
		pbs.event().job.Resource_List["select"] = pbs.select( selstr + ":mpiprocs=" + str(mpiprocs ) + ":ompthreads=" + str(ompthreads) )
	elif "mpiprocs" not in sel and "ompthreads" in sel:
		ompthreads = int(sel["ompthreads"])
		mpiprocs   = ( sel["ncpus"] / ompthreads )
		if mpiprocs < 1:
			mpiprocs = 1
		pbs.event().job.Resource_List["select"] = pbs.select( selstr + ":mpiprocs=" + str(mpiprocs ) )
		# Add mpiprocs = ncpus / ompthreads
	elif "mpiprocs" in sel and "ompthreads" not in sel:
		mpiprocs   = int( sel["mpiprocs"] )
		ompthreads = int( sel["ncpus"] ) / mpiprocs 
		if ompthreads < 1:
			ompthreads =1
		pbs.event().job.Resource_List["select"] = pbs.select( selstr + ":ompthreads=" + str(ompthreads ) )
	else:
			mpiprocs  = int(sel["mpiprocs"])
			ompthreads= int(sel["ompthreads"])
			if (mpiprocs * ompthreads) != int(sel["ncpus"]):
				pbs.event().reject( "mpiprocs * ompthreads must equal ncpus" )
			


# MAIN LOGIC BEGIN
try:
	queue_type = extract_queue_type()

	# Anything goes in private queues
	# so exit at this point, to prevent walltime and select parsing raising a reject()
	if queue_type == "private":
		pbs.event().accept()

	walltime   = extract_walltime()
	selection  = extract_selection()

	# 
	if queue_type == "express":
		pbs.event().reject("Express queue functionality not available yet")

	
	if queue_type == "common":
		clss = classify_job( selection, walltime )
	else:
		# If the user submitted to a specific queue, test against the config for that alone
		queue_type = queue_type.split(":")
		clss = classify_job( selection, walltime, queue = queue_type[1] )
		

	# Move the job into the right queue
	pbs.event().job.queue = pbs.server().queue( queue_config_version + clss["target_queue"] )

	pbs.logmsg( pbs.LOG_ERROR, "MOVING JOB TO QUEUE: " + clss["target_queue"] )
	pbs.logmsg( pbs.LOG_ERROR, "MOVING JOB TO QUEUE: " + repr( pbs.event().job.queue.name )  )

	fixup_mpiprocs_ompthreads( selection )

	pbs.event().accept()


	 	
except SystemExit:
	pass
#
# If an error was generated then stop the job submission
except:
	e=sys.exc_info()
	pbs.logmsg(pbs.LOG_ERROR, "Error - type:  %s"%(e[0]))
	pbs.logmsg(pbs.LOG_ERROR, "Error - value:  %s"%(e[1]))
	pbs.logmsg(pbs.LOG_ERROR, "Error - traceback:  %s"%(e[2]))
	pbs.event().reject("Internal error submitting job.\n     Please report the following information to rcs-support@imperial.ac.uk, including a copy of your jobscript:\n" + traceback.format_exc())

