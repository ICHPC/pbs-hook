#
# Submit hook
# CX2
# HPC - Imperial College London
#

import sys
import pbs

list_of_resources = ["ncpus","mem","mpiprocs","ompthreads"]

geometries = {16:range(1,5),24:range(1,21),28:range(1,16)}

try:
#
# Verify user requested walltime
   if ( pbs.event().job.Resource_List["walltime"] == None ):
      pbs.event().reject("Walltime must be specified, jobs cannot be scheduled without a runtime estimate!")
#
# Verify a select statement was used
   if ( pbs.event().job.Resource_List["select"] == None ):
      pbs.event().reject("All jobs must specify a select statement, jobs cannot be allocated proper resources without this!")
# Queue
   queue_name="X"
   if ( pbs.event().job.queue != "" ):
      queue_name=pbs.event().job.queue.name
#
# Verify resources requested, count the number of nodes used, the ncpus requested and compute the number of IRUs
   if queue_name[0] != "R":
      nodect = 0
      chunks = repr(pbs.event().job.Resource_List["select"]).split("+")
      if ( len(chunks) != 1 ):
         pbs.event().reject("You can only request one chunk of the form #PBS -l select=X:ncpus=Y:mpiprocs=Z:ompthreads=T.")
      for chunk in chunks:
         nodect+=int(chunk.split(":")[0])
         for rs in chunk.split(":")[1:]:
            kw = rs.split("=")[0]
            if ( kw not in list_of_resources ):
               pbs.event().reject("Select statements can only contain the resources: "+", ".join(list_of_resources))
            if ( kw == "ncpus" ):
               node_size=int(rs.split("=")[1])
      iru = nodect/18.0  
      if ( ( node_size == 24 ) and ( nodect < 18 ) ):
         model=":cpumodel=24s"
         pbs.event().job.queue=pbs.server().queue("short")
      elif ( ( node_size == 16 ) and ( iru in geometries[16] ) ):
         model=":cpumodel=16"
         pbs.event().job.queue=pbs.server().queue("general")
      elif ( ( node_size == 24 ) and ( iru in geometries[24] ) ):
         model=":cpumodel=24"
         pbs.event().job.queue=pbs.server().queue("general")
      elif ( ( node_size == 28 ) and ( iru in geometries[28] ) ):
         model=":cpumodel=28"
         pbs.event().job.queue=pbs.server().queue("general")
      else:
         pbs.event().reject("Unsupported geometry. Please read https://wiki.imperial.ac.uk/display/HPC/Job+sizing+on+cx2")
      pbs.event().job.Resource_List["select"]=pbs.select(chunk+model)
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
