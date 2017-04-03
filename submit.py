#
# Submit hook
# CX1
# HPC - Imperial College London
#

import sys
import pbs

list_of_resources = ["ncpus","ngpus","mem","mpiprocs","ompthreads"]

try:
#
# Verify user requested walltime
   if ( pbs.event().job.Resource_List["walltime"] == None ):
      pbs.event().reject("Walltime must be specified, jobs cannot be scheduled without a runtime estimate!")
#
# Verify a select statement was used
   if ( pbs.event().job.Resource_List["select"] == None ):
      pbs.event().reject("All jobs must specify a select statement, jobs cannot be allocated proper resources without this!")
#
# Go over the select statement to verify resources are correct and count the number of nodes used.
   nodect = 0
   for chunk in repr(pbs.event().job.Resource_List["select"]).split("+"):
      nodect+=int(chunk.split(":")[0])
      for rs in chunk.split(":")[1:]:
         kw = rs.split("=")[0]
         if kw not in list_of_resources:
            pbs.event().reject("Select statements can only contain the resources: "+", ".join(list_of_resources))
#
# If we are in multinode make sure we use scatter and exclusive hosts
   if ( nodect > 1 ):
      pbs.event().job.Resource_List["place"]=pbs.place("scatter:exclhost")
#
# Because the interactive queue is accessible by everyone check that only interactive jobs go there
   if ( ( not pbs.event().job.interactive ) and ( pbs.event().job.queue != "" ) and ( pbs.event().job.queue.name == "interactive" ) ):
      pbs.event().reject("You can only submit interactive jobs to the interactive queue!")
#
# All interactive jobs except the ones for the viz queue should go to the interactive queue 
   if ( ( pbs.event().job.interactive ) and ( ( pbs.event().job.queue == "" ) or ( pbs.event().job.queue.name != "viz" ) ) ):
      pbs.event().job.queue=pbs.server().queue("interactive")
#
# If we accept or reject we are done
except SystemExit:
   pass
#
# If an error was generated then stop the job submission
except:
   e=sys.exc_info()
   pbs.logmsg(pbs.LOG_DEBUG, "Error - type:  %s"%(e[0]))
   pbs.logmsg(pbs.LOG_DEBUG, "Error - value:  %s"%(e[1]))
   pbs.logmsg(pbs.LOG_DEBUG, "Error - traceback:  %s"%(e[2]))
   pbs.event().reject("Error submitting job! Contact hpc-support@imperial.ac.uk")

#
# pbs.logmsg(pbs.LOG_DEBUG, "Jobid = %s"%(pbs.event().job.id))
#
