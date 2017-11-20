def get_group_membership()
	import pbs
	import sys

	PBS_EXEC = '/opt/pbs/default'
	GETENT_CMD = '/bin/getent'

	# Main
	sys.path.append(PBS_EXEC + '/python/lib/python2.7')
	sys.path.append(PBS_EXEC + '/python/lib/python2.7/lib-dynload')
	from subprocess import Popen, PIPE
	from sets import Set

	e = pbs.event()
	j = e.job

	# Get the username
	who = str(e.requestor)

	# Build a list of users from all permitted groups
	users = Set([])
	for g in permitted_groups:
  	  output = Popen([GETENT_CMD , "group", g], stdout=PIPE).communicate()[0].strip()
    	output = output.split(':')[-1].split(',')
    	users = users.union(output)

	return users

