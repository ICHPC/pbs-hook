#
# This code is provided "as is" without any warranty, express or implied, or 
# indemnification of any kind. All other terms and conditions are as specified
# in the Altair PBS EULA.
#
# Author: Alexander Franke, <franke@altair.de>
#
# --- Description ---
#
# This hooks enables you to set restrictions for certain secondary groups at
# queue level. This way jobs of users which don't belong to the list of groups set at
# the queue will be rejected.
#
# The hook is using 'getent group <group_name>' to determine the users which are members
# of group <group_name>. 
#
# In case a user is not permitted to submit to a certain queue the user will get a
# message like
#
# qsub: You are not permitted to submit jobs to queue admin.
#
# --- Configuration ---
#
# First we need to introduce a new custom resource to allow you to set a list
# of permitted groups at queue level. You can put the following line in
# $PBS_HOME/server_priv/resourcedef
#
# permitted_groups type=string_array 
#
# To make PBS aware of this new resource you have to restart PBS with
#
# qterm -t quick;/etc/init.d/pbs start
#
# Now we can set the permitted groups at queue level like this:
#
# qmgr -c 'set queue workq resources_available.permitted_groups += group_a'
# qmgr -c 'set queue workq resources_available.permitted_groups += group_c'
#
# Later this PBS hook will look at this setting to accept or reject the jobs.
#
# To install the hook copy it to some directory on the PBS server host, e.g. to
# 
# /opt/pbs/custom/hooks
#
# and change to that directory.
#
# Next you have to set the variable PBS_EXEC and GETENT_CMD below in the hook code
# to the correct path, e.g.
#
# PBS_EXEC = '/opt/pbs/default'
# GETENT_CMD = '/usr/bin/getent'
#
# Now we can create the hook with
#
# qmgr -c 'create hook group_acl event="queuejob"' 
#
# Now we can import the hook with 
#
# qmgr -c 'import hook group_acl application/x-python default group_acl.py'
#
#
# In case of trouble you can disable the hook with
#
# qmgr -c 'set hook group_acl enabled = false'
#
# and file a support request.
#
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

# Get queue
if j.queue == '':
    q = pbs.server().default_queue.name
else:
    q = j.queue.name

# Get permitted_groups or accept the job

permitted_groups = pbs.server().queue(q).resources_available['permitted_groups']
if permitted_groups == None:
    e.accept()
else:
    permitted_groups = permitted_groups.split(',')

# Build a list of users from all permitted groups
users = Set([])
for g in permitted_groups:
    output = Popen([GETENT_CMD , "group", g], stdout=PIPE).communicate()[0].strip()
    output = output.split(':')[-1].split(',')
    users = users.union(output)

# Check if job submitter is in the list of users
if who in users:
    e.accept()
else:
    e.reject('You are not permitted to submit jobs to queue %s.' % q)

e.accept()

