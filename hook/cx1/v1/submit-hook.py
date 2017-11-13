
#
# Submit hook
# CX1
# HPC - Imperial College London
#

import sys
import pbs

list_of_resources = ["ncpus","ngpus","mem","mpiprocs","ompthreads","arch","host","switchgroup","avx","avx2","avx512","tmpspace","has_magma","gpu_type","cpumodel","using_ht"]

	# 
# This is prepended to any target_queue name to allow for future versioning in place

queue_config_version = "v1_"

classifications = {
		"interactive": {
			"nodect"   : [1,1],
			"ncpus"    : [1,20],
			"ngpus"    : [0,1],
			"walltime" : [0,8],
			"mem"      : [1, 128],
			"interactive": True,
		},
		"debug": {
			"nodect"   : [1,1],
			"ncpus"    : [1,20],
			"ngpus"    : [0,1],
			"walltime" : [0,0.5], # Up to 3 mins
			"mem"      : [1, 128],
			"interactive": False,
		},

		"throughput24": {
			"nodect"   : [1,1],
			"ncpus"    : [1,16],
			"ngpus"    : [0,0],
			"walltime" : [0,24],
			"mem"      : [1, 128],
			"interactive": False,
		},

		"throughput72": {
			"nodect"   : [1,1],
			"ncpus"    : [1,16],
			"ngpus"    : [0,0],
			"walltime" : [24.001, 72],
			"mem"      : [1, 128],
			"interactive": False,
		},

		"turnaround24": {
			"nodect"   : [1,16],
			"ncpus"    : [ [16,16], [32,32] ],
			"ngpus"    : [0,0],
			"walltime" : [1,24.],
			"mem"      : [1, 128],
			"interactive": False,
		},

		"turnaround72": {
			"nodect"   : [1,16],
			"ncpus"    : [ [16,16], [32,32] ],
			"ngpus"    : [0,0],
			"walltime" : [24.001, 72.],
			"mem"      : [1, 128],
			"interactive": False,
		},
		"singlenode24": {
			"nodect"   : [1,1],
			"ncpus"    : [ [24,24], [48,48] ],
			"ngpus"    : [0,0],
			"walltime" : [1,24.],
			"mem"      : [1, 256],
			"interactive": False,
		},

		"multinode24": {
			"nodect"   : [ 2, 20 ],
			"ncpus"    : [ 12, 12 ],
			"ngpus"    : [0,0],
			"walltime" : [ 0., 24. ],
			"mem"      : [1, 48],
			"interactive": False,
		},

		"multinode72": {
			"nodect"   : [ 2, 20 ],
			"ncpus"    : [ 12, 12 ],
			"ngpus"    : [0,0],
			"walltime" : [ 0., 24. ],
			"mem"      : [1, 48],
			"interactive": False,
		},

		"largemem48": {
			"nodect"   : [ 1, 1 ],
			"ncpus"    : [ 1, 24 ],
			"ngpus"    : [0,0],
			"walltime" : [ 0., 48. ],
			"mem"      : [128, 256],
			"interactive": False,
		},

		"gpu48": {
			"nodect"   : [ 1, 1 ],
			"ncpus"    : [ 1, 24 ],
			"ngpus"    : [1,8],
			"walltime" : [ 0., 48. ],
			"mem"      : [1, 128],
			"interactive": False,
		},

}

def match_class(selection, walltime, clss ):
	# Compare walltime
	if (walltime < clss["walltime"][0])  or ( walltime > clss["walltime"][1] ):
		return False

	if clss["interactive"] != selection["interactive"]:
		return False

	for minmax in ["walltime", "mem", "nodect", "ngpus"]:
		if ( selection[minmax] < clss[minmax][0] ) or ( selection[minmax] > clss[minmax][1] ):
			return False

	if not isinstance( clss["ncpus"], list ):
		clss["ncpus"] = [ clss["ncpus"] ]

	for c in range(len(clss["ncpus"])):
		if ( selection["ncpus"] < clss["ncpus"][c][0] ) or ( selection["ncpus"] > clss["ncpus"][c][1] ):
			return False
	# Classification matches
	return True


# Match job to class. Error out if it matches more than one class
def classify_job( selection, walltime ):
	names = ""
	ret=[];

	for clssname  in classifications.keys():
		clss = classifications[clssname]
		if match_class( selection, walltime, clss ):
			clss["target_queue"] = clssname
			ret.append( clss )
			names = names + clssname + " "

	if len(ret) > 1:
		pbs.event().reject( "Job matches multiple classes: [ " + names.strip() + "]" )

	if len(ret):
		return ret[0]
	else:
		pbs.event().reject( "Job resource selection does not match any permitted configuration. Please review the CX1 Job Sizing page on https://www.imperial.ac.uk/ict/rcs" )


# Returns the type of the submission queue "common", "private" or "express"
# Errors out is anything other than a pq*, med-bio or e* is specified
def extract_queue_type():

	if pbs.event().job.queue == "" or pbs.event().job.queue == None:
		return "common"

	if ( pbs.event().job.queue != "" ):
		queue_name=pbs.event().job.queue.name

	if len(queue_name)>0 and queue_name[0] == "e":
		return "express"
	elif len(queue_name)>0 and ( queue_name[0] == "p"  or queue_name == "med-bio" ):
		return "private"
	else:
		pbs.event().reject("Invalid queue name.")

# Returns a float of the # of hours requested for the job
# Errors out if not specified or the format is wrong 
def extract_walltime():
	hrs=0;
	if ( pbs.event().job.Resource_List["walltime"] == None ):
		pbs.event().reject("You must specify a walltime.")
	try:
		wt = pbs.event().job.Resource_List["walltime"].split(":")
		if len(wt) != 3:
			pbs.event().reject("The walltime must be in the format -lwalltime=hh:mm:ss" )
		hrs =  float(wt[0]) + float(wt[1])/60. + float(wt[2])/3600. 
		return hrs
	except:
		pbs.event().reject("The walltime must be in the format -lwalltime=hh:mm:ss" )
#  

# Return the amount of requested memory in gb as an int, rounded down (min 1gb)
def canoncical_mem( mem ):
	# Canonicalise "mem"
	mem = mem.lower()
	factor = 1./ (1024*1024*1024) # scale down from bytes to gb

	if re.search("^[1234567890]+kb$", mem) or re.search("^[1234567890]+k$", mem ):
		factor = 1. / (1024. * 1024.) # scale from kb to gb
	elif re.search("^[1234567890]+mb$", mem) or re.search("^[1234567890]+m$", mem ):
		factor = 1. /1024. # scale from mb to gb
	elif re.search("^[1234567890]+gb$", mem) or re.search("^[1234567890]+g$", mem ):
		factor = 1. # scale from gb to gb
	elif re.search("^[1234567890]+tb$", mem) or re.search("^[1234567890]+t$", mem ):
		factor = 1024. # scale from tb to gb

	mem = re.sub( "[tkmgb]+", "", mem )
	mem = int(float(mem) * factor)
	if mem<=0:
		mem = 1


# Return a dict of the job selection
# Errors out if mandatory values are not set
def extract_selection():
	if ("select" not in pbs.event().job.Resource_List) or ( pbs.event().job.Resource_List["select"] == None ):
		pbs.event().reject("You must specify a resource selection." )

	select = pbs.event().job.Resource_List["select"]
	select = select.split("+")

	if len(select) > 1:
		pbs.event().reject("Only one -lselect is permitted.")

	chunk = select[0]

	ret= dict()
	try:
		nodect = 0
		chunk.split(":")
		nodect = int(	 chunk[0] )

		ret["nodect"] = nodect

		selects = chunk[1].split(":")
		for rs in selects:
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
		pbs.event().reject("Invalid -lselect syntax." )

	if "ncpus" not in ret:
			pbs.event().reject("[ncpus] must be in the -lselect")
	if "ngpus" not in ret:
			ret["ngpus"] = 0	
	if "mem" not in ret:
			pbs.event().reject("[mem] must be in the -lselect")

	ret["mem"] = canconical_mem( ret["mem"] )

	# Not part of the select, but smuggle it in here
	ret["interactive"] = pbs.event().job.interactive

	return ret
	


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



	clss = classify_job( selection, walltime )

	# Move the job into the right queue
	pbs.event().job.queue = pbs.server().queue( clss["target_queue"] )
	 	
except SystemExit:
	pass
#
# If an error was generated then stop the job submission
except:
	e=sys.exc_info()
	pbs.logmsg(pbs.LOG_DEBUG, "Error - type:  %s"%(e[0]))
	pbs.logmsg(pbs.LOG_DEBUG, "Error - value:  %s"%(e[1]))
	pbs.logmsg(pbs.LOG_DEBUG, "Error - traceback:  %s"%(e[2]))
	pbs.event().reject("Internal error submitting job. Please report this to rcs-support@imperial.ac.uk")

