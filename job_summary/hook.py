import pbs
import datetime

try:
	e=pbs.event()
	j = e.job
	ji=j.id
	path=j._stdout_file


	try:
		if(j.in_ms_mom()):
			w=open('%s' % (path), 'a')
			w.write( "\n")
			w.write( "=====================================\n" )
			w.write( "" )  
			w.write( "       Job resource use summary " )  
			w.write( "" )  
			w.write( "                 Memory        NCPUs\n" )
			w.write( " Requested:      %s            %d\n" % ( str(Resource_List.mem), int(Resource_List.ncpus), ) )
			w.write( " Used     :      %s            %.2f\n" % ( str(resources_used.mem), float(resources_used.cpupercent) / 100., ) )
			w.write( "" )  
			w.write( "=====================================\n" )
			w.close()

	except IOError :
		pbs.logmsg(pbs.LOG_DEBUG,"File open error occured : %s ====>>> " % (path))

    
except:
	import traceback
	log_buffer = traceback.format_exc()
	pbs.logmsg(pbs.LOG_DEBUG, 'Hook exception:')
	for line in log_buffer.split('\n'):
		pbs.logmsg(pbs.LOG_DEBUG, line)
		pbs.event().reject("Exception trapped in %s:\n %s" % (pbs.event().hook_name, log_buffer))
