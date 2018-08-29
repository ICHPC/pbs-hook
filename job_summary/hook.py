import pbs
import datetime
import re
import math
try:
	e=pbs.event()
	j = e.job
	ji=j.id
	path=j._stdout_file


	if(j.in_ms_mom()):
			mem_rq  = str(j.Resource_List.mem)
			mem_used= str(j.resources_used.mem)
			mem_rq = mem_rq.lower()
			mem_rq = re.sub("mb", "000", mem_rq )
			mem_rq = re.sub("gb", "000000", mem_rq )
			mem_rq = re.sub("tb", "000000000", mem_rq )
			mem_used = re.sub( "kb", "", mem_used )

			mem_rq  = int(mem_rq) / 1000000 # to gb
			mem_used= int(mem_used ) / 1000000 # to gb

			best_ncpu = math.ceil( float(j.resources_used.cpupercent) / 100.)
			if best_ncpu < 1.0:
				best_ncpu = 1.0		

			best_mem = mem_used * 1.1
			if best_mem < 1.0:
				best_mem = 1.0

			w=open('%s' % (path), 'a')
			w.write( "\n")
			w.write( "============================================\n" )
			w.write( "\n" )  
			w.write( "        Job resource usage summary \n" )  
			w.write( "\n" )  
			w.write( "                 Memory (GB)    NCPUs\n" )
			w.write( " Requested  :    %6s        %6d\n" % ( str(mem_rq), int(j.Resource_List.ncpus), ) )
			w.write( " Used       :    %6s (peak) %6.2f (ave)\n" % ( str(mem_used), float(j.resources_used.cpupercent) / 100., ) )
			w.write( "\n" )  
#			w.write( " Recommended:    %6d        %6d\n" % ( int(best_mem), int(best_ncpu), ) )
#			w.write( "\n" )  
			w.write( "============================================\n" )
			w.close()


    
except:
	pbs.logmsg( pbs.LOG_DEBUG, "MJH: Exception in job_summary hook" );

pbs.event().accept()

#	import traceback
#	log_buffer = traceback.format_exc()
#	pbs.logmsg(pbs.LOG_DEBUG, 'Hook exception:')
#	for line in log_buffer.split('\n'):
#		pbs.logmsg(pbs.LOG_DEBUG, line)
#		pbs.event().reject("Exception trapped in %s:\n %s" % (pbs.event().hook_name, log_buffer))
