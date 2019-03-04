#!/usr/bin/env python

from __future__ import print_function

queue_array_variant = {
	"throughput24" : "throughput2a",
	"general24"    : "general24a"
}

private_queue_restrictions = {
	"pqmedbio-thoughput"  : [ {
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


    "largemem72"     : [ ],
#			# NB - largemem72 has additional options that are machine-generated below - for all ncpus in multiples of 10, mem in multiples of 120
     "throughput24" : [{
      "nodect"   : [1,1],
			"ncpus"    : [1,8],
      "ngpus"    : [0,0],
      "walltime" : [ 0.5000001, 24 ],
			"mem"      : [ 1, 96 ],
			"interactive" : False,
			"express"  : False,
			"avx"      : True,
			"avx2"     : False,
			"avx512"   : False
		} ],
		"short2": [{
			"nodect"   : [1,17],
			"ncpus"    : [[24,24],[48,48]],
			"ngpus"    : [0,0],
			"walltime" : [0,2.],
			"mem"      : [1, 120],
			"interactive": False,
			"express"  : False
		}],
		"interactive2": [{
			"nodect"   : [1,17],
			"ncpus"    : [[24,24],[48,48]],
			"ngpus"    : [0,0],
			"walltime" : [0,2.],
			"mem"      : [1, 120],
			"interactive": True,
			"express"  : False
		}],

		"general72":[ {
			"nodect"   : [2,18],
			"ncpus"    : [[16,16],[32,32]],
			"ngpus"    : [0,0],
			"walltime" : [0, 72],
			"mem"      : [1, 62],
			"interactive": False,
			"express"  : False
		}],

		"large48":[ {
			"nodect"   : [18,72],
			"ncpus"    : [[24,24],[48,48]],
			"ngpus"    : [0,0],
			"walltime" : [2.,48], 
			"mem"      : [1, 120],
			"interactive": False,
			"express"  : False
		}],

		"capability24": [{
			"nodect"   : [72,265],
			"ncpus"    : [[28,28],[56,56]],
			"ngpus"    : [0,0],
			"walltime" : [0,24],
			"mem"      : [1, 120],
			"interactive": False,
			"express"  : False
		}],

		"exp_24_128_ib":[ {
			"nodect"   : [1,265],
			"ncpus"    : [ [24,24], [48,48] ],
			"ngpus"    : [0,0],
			"walltime" : [1, 240.],
			"mem"      : [1, 120],
			"interactive": False,
			"express"  : True
		} ],
}

def expand_classifications():
	# machine-generate extra classes
	c = []  

	for n in range(1, 100 ):
		ncpus =  10 * n
		mem   = 120 * n
		c.append(	
		{ "nodect"   : [1,1],
			"ncpus"    : [ ncpus, ncpus ],
      "ngpus"    : [0,0],
      "walltime" : [ 0.5000001, 72 ],
			"mem"      : [ mem, mem ],
			"interactive" : False,
			"express"  : False,
			"avx"      : True,
			"avx2"     : False,
		} 
		)
	classifications["largemem72"] = c;

	# Same as largemem, just 
	private_queue_restrictions["pqmedbio-large"]    = c;
		
	
expand_classifications()

config = {
 "queue_array_variant"        : queue_array_variant,
 "private_queue_restrictions" : private_queue_restrictions,
 "classifications"            : classifications
}

import json
f  = json.dumps( config, sort_keys=True, indent=2, separators=(',', ': ') )
ff = open("configuration.json", "w" )
print( f, file=ff )
ff.close()
