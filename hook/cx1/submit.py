#
# Submit hook
# CX1
# HPC - Imperial College London
#

import sys
import pbs

list_of_resources = ["ncpus","ngpus","mem","mpiprocs","ompthreads","arch","host","switchgroup","icib","avx","avx2","westmere","sandyb","ivyb","haswell","broadwell","skylake","fauxqueue","tmpspace","viz","has_magma","gpu_type","proxied","jupyter","using_ht","cpumodel"]

try:
#
# Verify user requested walltime
   if ( pbs.event().job.Resource_List["walltime"] == None ):
      pbs.event().reject("Walltime must be specified, jobs cannot be scheduled without a runtime estimate!")
#
# Verify a select statement was used
   if ( pbs.event().job.Resource_List["select"] == None ):
      pbs.event().reject("All jobs must specify a select statement, jobs cannot be allocated proper resources without this!\n\n      Your select statment has to be of the form:\n\n      #PBS -l select=[X:ncpus=Y:mem=M[mb|MB|gb|GB]:[mpiprocs:Z[:ompthreads=T[:<extra_node_resources>]]]]\n\n      where X is the number of nodes, Y the number of cores per node, M the memory per node,\n      Z the number of ranks per nodes in a parallel job and T the threads per node in a multithreaded application.\n")
#
# Go over the select statement to verify resources are correct and count the number of nodes used.
   accel = 0
   nodect = 0
   for chunk in repr(pbs.event().job.Resource_List["select"]).split("+"):
      nodect+=int(chunk.split(":")[0])
      for rs in chunk.split(":")[1:]:
         kw = rs.split("=")[0]
         if kw not in list_of_resources:
            pbs.event().reject("Select statements can only contain the resources: "+", ".join(list_of_resources))
         if kw in ["ngpus"]:
            accel=1
#
# If we are in multinode make sure we use scatter and exclusive hosts
   if ( nodect > 1 and not accel ):
      pbs.event().job.Resource_List["place"]=pbs.place("scatter:exclhost")
#
# Queue
   queue_name=""
   if ( pbs.event().job.queue != "" ):
      queue_name=pbs.event().job.queue.name
#
# Because the interactive queue is accessible by everyone check that only interactive jobs go there
   if ( ( not pbs.event().job.interactive ) and ( queue_name == "interactive" ) ):
      pbs.event().reject("You can only submit interactive jobs to the interactive queue!")
#
# All interactive jobs except the ones for the viz queue should go to the interactive queue 
   if ( ( pbs.event().job.interactive ) and ( queue_name not in ["viz","debug","build"] ) and ( queue_name[0:2] != "pq" ) ):
      pbs.event().job.queue=pbs.server().queue("interactive")
#
# If we request accelerators but we are not on a private queue, or gpgpu then redirect
   if ( accel and ( queue_name != "gpgpu" ) and ( queue_name[0:2] != "pq" ) ):
      pbs.event().job.queue=pbs.server().queue("gpgpu")   
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
