
#
# Submit hook
# CX1
# HPC - Imperial College London
# Home: github ICHPC/pbs-hook

# To install
# qmgr -c "import hook submit application/x-python default submit-hook.py"

import sys
import pbs
import traceback
import re

list_of_resources = ["ncpus","ngpus","mem","mpiprocs","ompthreads", "avx", "avx2", "avx512", "gpu_type","cpumodel" ]

	# 
# This is prepended to any target_queue name to allow for future versioning in place

queue_config_version = "v1_"

queue_array_variant = {
	"throughput24" : "throughput2a",
	"general24"    : "general24a"
}

private_queue_restrictions = {
	"med-bio"  : [ {
		"nodect"     : [1,20],
		"ncpus"      : [1,40],
		"ngpus"      : [0,0],
		"walltime"   : [0,150.],
		"mem"        : [1,128],
		"avx512"     : False,
	} ],
	"pqaam"  : [ {
		"nodect"     : [1,12],
		"ncpus"      : [1,32],
		"ngpus"      : [0,0],
		"walltime"   : [0,168.],
		"mem"        : [1,64],
		"avx512"     : False,
		},
		{
		"nodect"     : [1,4],
		"ncpus"      : [1,48],
		"ngpus"      : [0,0],
		"walltime"   : [0,168.],
		"mem"        : [1,128],
		"avx512"     : False,
		} ],
	"pqaero"  : [ {
		"nodect"     : [1,12],
		"ncpus"      : [1,32],
		"ngpus"      : [0,0],
		"walltime"   : [0,168.],
		"mem"        : [1,64],
		"avx512"     : False,
		},
		{
		"nodect"     : [1,4],
		"ncpus"      : [1,48],
		"ngpus"      : [0,0],
		"walltime"   : [0,168.],
		"mem"        : [1,128],
		"avx512"     : False,
		} ],
	"pqaerogpu" : [ {
		"nodect"     : [1,4],
		"ncpus"      : [1,32],
		"ngpus"      : [0,8],
		"walltime"   : [0,168.],
		"mem"        : [1,32],
		"avx512"     : False,
		}, ],
	"pqaeromg" : [ {
		"nodect"     : [1,4],
		"ncpus"      : [1,40],
		"ngpus"      : [0,0],
		"walltime"   : [0,168.],
		"mem"        : [1,128],
		"avx512"     : False,
	} ],
	"pqaeromorph" : [ {
		"nodect"    : [1,10],
		"ncpus"     : [1,32],
		"ngpus"     : [0,2],
		"walltime"  : [0,168.],
		"mem"       : [1,64],
		"avx512"     : False,
	} ],
	"pqastro" : [ {
		"nodect"    : [1,4],
		"ncpus"     : [1,32],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,64],
		"avx512"     : False,
	} ],
	"pqalwalsh" : [ {
		"nodect"    : [1,6],
		"ncpus"     : [1,48],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,256],
		"avx512"     : False,
	} ],
	"pqberloff" : [ {
		"nodect"    : [1,3],
		"ncpus"     : [1,32],
		"ngpus"     : [0,0],
		"walltime"  : [0,2400.],
		"mem"       : [1,64],
		"avx512"     : False,
	} ],
	"pqcdt" : [ {
		"nodect"    : [1,20],
		"ncpus"     : [1,40],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,64],
		"avx512"     : False,
	} ],
	"pqcgi" : [ {
		"nodect"    : [1,16],
		"ncpus"     : [1,32],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqchem" : [ {
		"nodect"    : [1,10],
		"ncpus"     : [1,40],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqchemeng" : [ {
		"nodect"    : [1,8],
		"ncpus"     : [1,40],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqcivstruct" : [ {
		"nodect"    : [1,4],
		"ncpus"     : [1,40],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqcvcsm" : [ {
		"nodect"    : [1,12],
		"ncpus"     : [1,40],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqeboek" : [ {
		"nodect"    : [1,7],
		"ncpus"     : [1,12],
		"ngpus"     : [0,8],
		"walltime"  : [0,168.],
		"mem"       : [1,256],
		"gpu_type"  : [ "P100", "K80" ],
		"avx512"     : False,
	} ],
	"pqeboekcpu" : [ {
		"nodect"    : [1,20],
		"ncpus"     : [1,32],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,64],
		"avx512"     : False,
	} ],
	"pqeelab" : [ {
		"nodect"    : [1,8],
		"ncpus"     : [1,40],
		"ngpus"     : [0,0],
		"walltime"  : [0,1000.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqeph" : [ {
		"nodect"    : [1,8],
		"ncpus"     : [1,40],
		"ngpus"     : [0,0],
		"walltime"  : [0,2400.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqexss" : [ {
		"nodect"    : [1,4],
		"ncpus"     : [1,40],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqfano" : [ {
		"nodect"    : [1,1],
		"ncpus"     : [1,48],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqfogim" : [ {
		"nodect"    : [1,4],
		"ncpus"     : [1,48],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqgrimes" : [ {
		"nodect"    : [1,4],
		"ncpus"     : [1,40],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqigould" : [ {
		"nodect"    : [1,1],
		"ncpus"     : [1,8],
		"ngpus"     : [0,4],
		"walltime"  : [0,168.],
		"mem"       : [1,16],
		"gpu_type"  : ["GTX980", "GTX1080" ],
		"avx512"     : False,
	} ],
	"pqjferrer" : [ {
		"nodect"    : [1,8],
		"ncpus"     : [1,40],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqjpritcha" : [ {
		"nodect"    : [1,4],
		"ncpus"     : [1,48],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,256],
		"avx512"     : False,
	} ],
	"pqkjelfs" : [ {
		"nodect"    : [1,2],
		"ncpus"     : [1,48],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqlaser" : [ {
		"nodect"    : [1,12],
		"ncpus"     : [1,40],
		"ngpus"     : [0,0],
		"walltime"  : [0,2400.],
		"mem"       : [1,256],
		"avx512"     : False,
	} ],
	"pqmaterials" : [ {
		"nodect"    : [1,10],
		"ncpus"     : [1,40],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqmb" : [ {
		"nodect"    : [1,8],
		"ncpus"     : [1,48],
		"ngpus"     : [0,0],
		"walltime"  : [0,2400.],
		"mem"       : [1,256],
		"avx512"     : False,
	} ],
	"pqmedyn" : [ {
		"nodect"    : [1,40],
		"ncpus"     : [1,48],
		"ngpus"     : [0,0],
		"walltime"  : [0,2400.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqmemphis" : [ {
		"nodect"    : [1,36],
		"ncpus"     : [1,56],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqmeneg" : [ {
		"nodect"    : [1,20],
		"ncpus"     : [1,48],
		"ngpus"     : [0,0],
		"walltime"  : [0,2400.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqmrwarn" : [ {
		"nodect"    : [1,72],
		"ncpus"     : [1,48],
		"ngpus"     : [0,0],
		"walltime"  : [0,2400.],
		"mem"       : [1,384],
	} ],
	"pqmrwarn2" : [ {
		"nodect"    : [1,4],
		"ncpus"     : [1,40],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,128],
	} ],
	"pqmultiflow" : [ {
		"nodect"    : [1,40],
		"ncpus"     : [1,40],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqmultiflowib" : [ {
		"nodect"    : [1,20],
		"ncpus"     : [1,40],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,64],
		"avx512"     : False,
	} ],
	"pqndenuc" : [ {
		"nodect"    : [1,1],
		"ncpus"     : [1,32],
		"ngpus"     : [0,16],
		"walltime"  : [0,168.],
		"mem"       : [1,512],
		"avx512"     : False,
	} ],
	"pqnmh" : [ {
		"nodect"    : [1,16],
		"ncpus"     : [1,48],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqpcsmith" : [ {
		"nodect"    : [1,3],
		"ncpus"     : [1,24],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,192],
		"avx512"     : False,
	} ],
	"pqph" : [ {
		"nodect"    : [1,4],
		"ncpus"     : [1,48],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,256],
		"avx512"     : False,
	} ],

	"pqpdh" : [ {
		"nodect"    : [1,8],
		"ncpus"     : [1,48],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqplasma2" : [ 
		{
		"nodect"    : [1,5],
		"ncpus"     : [1,48],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,128],
		"avx512"     : False,
		},
		{
		"nodect"    : [1,72],
		"ncpus"     : [1,24],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,48],
		"avx512"     : False,
	} ],
	"pqplinds" : [ {
		"nodect"    : [1,20],
		"ncpus"     : [1,40],
		"ngpus"     : [0,0],
		"walltime"  : [0,2400.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqrrng" : [ {
		"nodect"    : [1,100],
		"ncpus"     : [1,48],
		"ngpus"     : [0,0],
		"walltime"  : [0,2400.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqsc03" : [ {
		"nodect"    : [1,12],
		"ncpus"     : [1,40],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqstokes" : [ {
		"nodect"    : [1,28],
		"ncpus"     : [1,32],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqstorm" : [ {
		"nodect"    : [1,4],
		"ncpus"     : [1,48],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,256],
		"avx512"     : False,
	} ],
	"pqtimm" : [ {
		"nodect"    : [1,4],
		"ncpus"     : [1,40],
		"ngpus"     : [0,0],
		"walltime"  : [0,2400.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqtouldrid" : [ {
		"nodect"    : [1,4],
		"ncpus"     : [1,48],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqtribo" : [ {
		"nodect"    : [1,10],
		"ncpus"     : [1,48],
		"ngpus"     : [0,0],
		"walltime"  : [0,168.],
		"mem"       : [1,128],
		"avx512"     : False,
	} ],
	"pqturbo" : [ {
		"nodect"    : [1,4],
		"ncpus"     : [1,48],
		"ngpus"     : [0,0],
		"walltime"  : [0,2400.],
		"mem"       : [1,256],
		"avx512"     : False,
	} ],

}


	


classifications = {
		"interactive": [{
			"nodect"   : [1,1],
			"ncpus"    : [1,8],
			"ngpus"    : [0,1], 
			"walltime" : [0,8.],
			"mem"      : [1, 96],
			"interactive": True,
			"express"  : False,
			"gpu_type" : [ "P1000"  ],
			"avx"      : True,
			"avx2"     : False,
			"avx512"   : False
		}],
		"debug": [{
			"nodect"   : [1,1],
			"ncpus"    : [1,8],
			"ngpus"    : [0,1],
			"walltime" : [0,0.5], # Up to 30 mins
			"mem"      : [1, 96],
			"interactive": False,
			"express"  : False,
			"gpu_type" : [ "P1000" ],
			"avx"      : True,
			"avx2"     : False,
			"avx512"   : False
		}],

		"long1000" : [{
			"nodect"   : [1,1],
			"ncpus"    : [1,8],
			"ngpus"    : [0,0],
			"walltime" : [72.00001,1000],
			"mem"      : [1, 96],
			"interactive": False,
			"express"  : False,
			"avx"      : True,
			"avx2"     : False,
			"avx512"   : False
		}],
		"throughput24": [{
			"nodect"   : [1,1],
			"ncpus"    : [1,8],
			"ngpus"    : [0,0],
			"walltime" : [0.500001,24],
			"mem"      : [1, 96],
			"interactive": False,
			"express"  : False,
			"avx"      : True,
			"avx2"     : False,
			"avx512"   : False
		}],

		"throughput72": [{
			"nodect"   : [1,1],
			"ncpus"    : [1,8],
			"ngpus"    : [0,0],
			"walltime" : [24.00001, 72],
			"mem"      : [1, 96],
			"interactive": False,
			"express"  : False,
			"avx"      : True,
			"avx2"     : False,
			"avx512"   : False
		}],

		"general24": [{
			"nodect"   : [1,16],
			"ncpus"    : [ [16,16], [32,32] ],
			"ngpus"    : [0,0],
			"walltime" : [0.50001,24.],
			"mem"      : [1, 124],
			"interactive": False,
			"express"  : False,
			"avx"      : True,
			"avx2"     : False,
			"avx512"   : False
		}],

		"general72": [{
			"nodect"   : [1,16],
			"ncpus"    : [ [16,16], [32,32] ],
			"ngpus"    : [0,0],
			"walltime" : [24.00001, 72.],
			"mem"      : [1, 124],
			"interactive": False,
			"express"  : False,
			"avx"      : True,
			"avx2"     : False,
			"avx512"   : False
		}],

		"singlenode24": [{
			"nodect"   : [1,1],
			"ncpus"    : [ [24,24], [48,48] ],
			"ngpus"    : [0,0],
			"walltime" : [1,24.],
			"mem"      : [1, 250],
			"interactive": False,
			"express"  : False,
			"avx"      : True,
			"avx2"     : True,
			"avx512"   : False
		}],

		"multinode24": [{
			"nodect"   : [ 3, 20 ],
			"ncpus"    : [ 12, 12 ],
			"ngpus"    : [0,0],
			"walltime" : [ 0., 24. ],
			"mem"      : [1, 46],
			"interactive": False,
			"express"  : False,
			"avx"      : False,
			"avx2"     : False,
			"avx512"   : False
		}],

		"multinode48": [{
			"nodect"   : [ 3, 20 ],
			"ncpus"    : [ 12, 12 ],
			"ngpus"    : [0,0],
			"walltime" : [ 24.00001, 48.00 ],
			"mem"      : [1, 46],
			"interactive": False,
			"express"  : False,
			"avx"      : False,
			"avx2"     : False,
			"avx512"   : False
		}],

		"largemem24": [{
			"nodect"   : [ 1, 1 ],
			"ncpus"    : [ [ 12, 12 ], [24, 24] ],
			"ngpus"    : [0,0],
			"walltime" : [ 0.5, 24. ],
			"mem"      : [128, 380],
			"interactive": False,
			"express"  : False,
			"avx"      : False,
			"avx2"     : False,
			"avx512"   : False
		}],



		"largemem48": [{
			"nodect"   : [ 1, 1 ],
			"ncpus"    : [ [ 12, 12 ], [24, 24] ],
			"ngpus"    : [0,0],
			"walltime" : [ 24.00001, 48. ],
			"mem"      : [128, 380],
			"interactive": False,
			"express"  : False,
			"avx"      : False,
			"avx2"     : False,
			"avx512"   : False
		}],

		"gpu24": [{
			"nodect"   : [ 1, 1 ],
			"ncpus"    : [ 1, 8 ],
			"ngpus"    : [1,2],
			"walltime" : [ 0.5, 24. ],
			"mem"      : [1, 32],
			"interactive": False,
			"express"  : False,
			"gpu_type" : [ "P100", "K80", "GTXTITAN" ],
			"avx"      : True,
			"avx2"     : False,
			"avx512"   : False
		},
		{
			"nodect"   : [ 1, 1 ],
			"ncpus"    : [ 1, 8 ],
			"ngpus"    : [1,1],
			"walltime" : [ 0.5, 24. ],
			"mem"      : [1, 32],
			"interactive": False,
			"express"  : False,
			"gpu_type" : [ "P1000" ],
			"avx"      : True,
			"avx2"     : False,
			"avx512"   : False
		}],

		"gpu48": [{
			"nodect"   : [ 1, 1 ],
			"ncpus"    : [ 1, 8 ],
			"ngpus"    : [1,2],
			"walltime" : [ 24.00001, 48. ],
			"mem"      : [1, 32],
			"interactive": False,
			"express"  : False,
			"gpu_type" : [ "P100", "K80", "GTXTITAN", "P1000"  ],
			"avx"      : True,
			"avx2"     : False,
			"avx512"   : False
		},
		{
			"nodect"   : [ 1, 1 ],
			"ncpus"    : [ 1, 8 ],
			"ngpus"    : [1,1],
			"walltime" : [ 24.00001, 48. ],
			"mem"      : [1, 32],
			"interactive": False,
			"express"  : False,
			"gpu_type" : [ "P1000"  ],
			"avx"      : True,
			"avx2"     : False,
			"avx512"   : False
		}],




		"exp_48_128_72": [{
			"nodect"   : [1,16],
			"ncpus"    : [ [24,24], [48,48] ],
			"ngpus"    : [0,0],
			"walltime" : [1, 240.],
			"mem"      : [1, 252],
			"interactive": False,
			"express"  : True,
			"avx"      : True,
			"avx2"     : True,
			"avx512"   : False
		}],
		"exp_32_64_72": [{
			"nodect"   : [1,16],
			"ncpus"    : [ [16,16], [32,32] ],
			"ngpus"    : [0,0],
			"walltime" : [1, 240.],
			"mem"      : [1, 62 ],
			"interactive": False,
			"express"  : True,
			"avx"      : True,
			"avx2"     : False,
			"avx512"   : False
		}],




}


def queue_name():
	if pbs.event().job.queue == None:
		return ""
	if isinstance ( pbs.event().job.queue, str ):
		return pbs.event().job.queue
	else:
		return pbs.event().job.queue.name
		
	
def set_topjob_ineligible( ):
	pbs.event().job.topjob_ineligible = True

def check_express_project_code():
	project = pbs.event().job.project
	if not project:
		pbs.event().reject( "You must specify an express code with -P when submitting express jobs" )
	
	project = repr(project)
	if not re.match("^exp-[a-z0-9]+$", project ):
		pbs.event().reject( "Invalid express code: these have the format 'exp-XXXX'" )
	if not test_group_membership( [ project ] ):
		pbs.event().reject( "You are not authorised to use this express code" )

	r = None
	try:
		import requests
		r = requests.get( "https://api.rcs.imperial.ac.uk/v1.0/express/%s/enabled" % ( project, ) )
	except :#
		pass

	if r:
		pbs.logmsg( pbs.LOG_ERROR, str(r.status_code) )
		pbs.logmsg(pbs.LOG_ERROR,  str(r.text) )
		if (r.status_code == 200) and (r.text != "1"):
			pbs.event().reject("This express code is not enabled. Please contact rcs-support@imperial.ac.uk" )
	else:
		pbs.event().reject("This express code cannot be used at this time. Please try later or contact rcs-support@imperial.ac.uk" )

	return project

def match_class(selection, walltime, clssname, clss, express ):
	# Compare walltime
	if (walltime < clss["walltime"][0])  or ( walltime > clss["walltime"][1] ):
#		pbs.logmsg( pbs.LOG_ERROR, "CLASS [" + clssname +"] failed walltime ("+str(walltime) + "in range " + str(clss["walltime"][0]) + " " + str(clss["walltime"][1]) )
		return False

	if "interactive" in clss:
		if clss["interactive"] != selection["interactive"]:
#		pbs.logmsg( pbs.LOG_ERROR, "CLASS [" + clssname +"] failed interactive " + str(clss["interactive"] ) + " " + str(selection["interactive"]) )
			return False

	for minmax in [ "nodect", "ngpus" ]:
		if ( selection[minmax] < clss[minmax][0] ) or ( selection[minmax] > clss[minmax][1] ):

#			pbs.logmsg( pbs.LOG_ERROR, "CLASS [" + clssname +"] failed " + minmax )
			return False

	if ( pbs.size(selection["mem"]) < pbs.size(str(clss["mem"][0])+"gb") ) or ( pbs.size(selection["mem"]) > pbs.size(str(clss["mem"][1])+"gb") ):
#		pbs.logmsg( pbs.LOG_ERROR, "CLASS [" + clssname +"] failed mem" )
		return False

	if not isinstance( clss["ncpus"][0], list ):
		clss["ncpus"] = [ clss["ncpus"] ]

	ncpus_match = False
	for c in clss["ncpus"]:
		if ( selection["ncpus"] >= c[0] ) and ( selection["ncpus"] <= c[1] ):
			ncpus_match = True

	if not ncpus_match:
#			pbs.logmsg( pbs.LOG_ERROR, "CLASS [" + clssname +"] failed ncpus" )
			return False

	if "express" in clss:
		if clss["express"] != express:
#			pbs.logmsg( pbs.LOG_ERROR, "CLASS [" + clssname +"] doesn't match express" )
			return False
	# Classification matches
#	pbs.logmsg( pbs.LOG_ERROR, " CLASS  " + clssname + " matched" )

	# Check to see if the gpu_type is present and permitted for this class
	if "gpu_type" in selection:
		if "gpu_type" not in clss:
			return False
		if selection["gpu_type"] not in clss["gpu_type"]:
			return False


	for pcap in [ "avx", "avx2", "avx512" ]:
		if pcap in clss and pcap in selection:
			if selection[pcap] != clss[ pcap ]:
				return False

	return True


def check_pq_restriction( selection, walltime, queue ):
	if queue not in private_queue_restrictions:
		# There wasn't a restriction for this pq, so accept it
		return

	clss = private_queue_restrictions[ queue ]
	for c in clss:
			if match_class( selection, walltime, queue, c, False ):
				return True
	pbs.event().reject( "The private queue has insufficient resources for a job this size.\nPlease consult https://selfservice.rcs.imperial.ac.uk/pqs/nodes/%s to see what's available.\nFor any queries please contact us via rcs-support@imperial.ac.uk" % ( queue ) )


# Match job to class. Error out if it matches more than one class
def classify_job( selection, walltime, express= False, queue = None ):
	names = ""
	ret=[];

	for clssname  in sorted(classifications.keys()):
		clssset = classifications[clssname]
		for clss in clssset:
			if ( queue == None ) or clssname == queue:
				if match_class( selection, walltime, clssname, clss, express ):
					clss["target_queue"] = clssname
					ret.append( clss )
					names = names + clssname + " "

# Always go with the first if more than one class has matched. Lexical order of classname
#	if len(ret) > 1:
#		pbs.event().reject( "Job matches multiple classes: [ " + names.strip() + "]" )

	if len(ret):
		return ret[0]
	else:
		pbs.logmsg( pbs.LOG_ERROR, "FAILED TO MATCH A JOB:"  +  repr(pbs.event().job.Resource_List["select"])  + " walltime " + repr(pbs.event().job.Resource_List["walltime"]) )
		pbs.event().reject( "Job resource selection does not match any permitted configuration.\n      Please review the CX1 Job Sizing guidance on:\n       https://bit.ly/2AInEIj\n")


# Returns the type of the submission queue "common", "private" or "express"
# Errors out is anything other than a pq*, med-bio or e* is specified
def extract_queue_type():

	if pbs.event().job.queue == "" or pbs.event().job.queue == None:
		return "common"

	if ( pbs.event().job.queue != "" ):
		queue_name=pbs.event().job.queue.name

	if queue_name == "express": # len(queue_name)>0 and queue_name[0] == "e":
		return "express"
	elif len(queue_name)>0 and ( queue_name[0] == "p"  or queue_name == "med-bio" or queue_name == "viz"):
		return "private"
	elif queue_name.startswith(queue_config_version):
		queue_name = re.sub("^" + queue_config_version, "", queue_name )
		return "common:" + queue_name
	elif queue_name == "gpgpu":
		pbs.event().reject("-q gpgpu no longer required. Please submit without a queue qualification")
	else:
		pbs.event().reject("Unknown queue name.")

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
		pbs.event().reject("Invalid -lselect syntax. :" + str(select) + "\n     The correct format is -lselect=N:ncpus=X:mem=Ygb , optionally including ompthreads=A:mpiprocs=B" )

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
	exempt = False
	try:
		qn = pbs.event().job.queue.name
		if qn in [ "pqmrwarn", "pqmrwarn2" ]:
			exempt = True
	except:
		pass

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
				if not exempt:
					pbs.event().reject( "mpiprocs * ompthreads must equal ncpus" )
			
# Returns a list of all the groups the requestor is a member of
def test_group_membership( permitted_groups ):
  import pbs
  import sys

#  PBS_EXEC = '/opt/pbs/default'
  GETENT_CMD = '/bin/getent'

  # Main
#  sys.path.append(PBS_EXEC + '/python/lib/python2.7')
#  sys.path.append(PBS_EXEC + '/python/lib/python2.7/lib-dynload')
  from subprocess import Popen, PIPE
  from sets import Set

  e = pbs.event()
  j = e.job

  # Get the username
  who = str(e.requestor)

  # Build a list of users from all permitted groups
  for g in permitted_groups:
      output = Popen([GETENT_CMD , "group", g], stdout=PIPE).communicate()[0].strip()
      output = output.split(':')[-1].split(',')
      if who in output:
        return True

  return False


# MAIN LOGIC BEGIN
try:
	queue_type = extract_queue_type()

	walltime   = extract_walltime()
	selection  = extract_selection()

	if queue_type == "private":
		if pbs.event().job.project:
			pbs.event().reject( "Express project codes can not be used with private queues" )

		queue = pbs.server().queue(pbs.event().job.queue.name)
		if not queue:
			pbs.event().reject("Invalid queue name")

		permitted_groups =  queue.resources_available['permitted_groups']
		if permitted_groups:
			permitted_groups = permitted_groups.split(',')
			if not test_group_membership( permitted_groups ):
				pbs.event().reject( "You are not authorised to use this private queue" )

		fixup_mpiprocs_ompthreads( selection )
		# PQs are small and offline resources may preent jobs running
		# Prevent them becoming topjobs
		# Exclude med-bio, they can be top jobs, this lets largemem jobs compete against tiny ones
		if queue_name() != "med-bio":
			set_topjob_ineligible( )

		# Check that geometry is smaller than maximum that pq resources can accommodate
		check_pq_restriction( selection, walltime, pbs.event().job.queue.name )
		pbs.event().accept()


	# Express version 0 - accept anything provided the user is in an exp-XXX group
	express = False
	if queue_type == "express":
		check_express_project_code()
		express = True

	if queue_type != "express" and pbs.event().job.project:
			pbs.event().reject( "Express project codes can only be used if submitting express jobs with -q express" )

	
	if queue_type == "common" or queue_type == "express":
		clss = classify_job( selection, walltime, express )

		# Array jobs are never top jobs
		# As a matter of policy, are low-prio throughput
		if str(pbs.event().job.array_indices_submitted) != "None":
			# Exclude med-bio, they can be top jobs, this lets largemem jobs compete against tiny ones
			if queue_name() != "med-bio":
				set_topjob_ineligible()
		
	else:
		# If the user submitted to a specific queue, test against the config for that alone
		queue_type = queue_type.split(":")
		clss = classify_job( selection, walltime, express, queue = queue_type[1] )
		

	dest_queue = clss["target_queue" ]

	# If the job is an array job, check to see if this class has an "array variant"
	# These are used for preemption
	if str(pbs.event().job.array_indices_submitted) != "None":
		if dest_queue in queue_array_variant:
			dest_queue = queue_array_variant[ dest_queue ]

	# Move the job into the right queue
	if queue_type == "express":
		pbs.event().job.queue = pbs.server().queue( dest_queue ) #  clss["target_queue"] )
	else:
		pbs.event().job.queue = pbs.server().queue( queue_config_version + dest_queue ) # clss["target_queue"] )

	pbs.logmsg( pbs.LOG_ERROR, "MOVING JOB TO QUEUE: " + dest_queue ) # clss["target_queue"] )
#	pbs.logmsg( pbs.LOG_ERROR, "MOVING JOB TO QUEUE: " + repr( pbs.event().job.queue.name )  )

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

