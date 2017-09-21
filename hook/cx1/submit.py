#
# Submit hook
# CX1
# HPC - Imperial College London
#

import sys
import pbs

list_of_resources = ["ncpus","ngpus","mem","mpiprocs","ompthreads","arch","host","switchgroup","icib","avx","avx2","westmere","sandyb","ivyb","haswell","broadwell","skylake","nphis","fauxqueue","tmpspace","viz","has_magma","gpu_type","proxied","jupyter","using_ht","cpumodel"]

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
         if kw in ["ngpus","nmics","nphi"]:
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
   if ( ( pbs.event().job.interactive ) and ( queue_name not in ["viz","debug","build"] ) and ( queue_name[0:2] != "pq" ) and ( queue_name[0] != "e" ) ):
      pbs.event().job.queue=pbs.server().queue("interactive")
#
# If we request accelerators but we are not on a private queue, or gpgpu then redirect
   if ( accel and ( queue_name != "gpgpu" ) and ( queue_name[0:2] != "pq" ) ):
      pbs.event().job.queue=pbs.server().queue("gpgpu")   

# Check expedited queue config. Only allow certain configs, and force node exclusivity
   if queue_name[0] == "e":
      pbs.event().job.Resource_List["place"]=pbs.place("pack:exclhost")

      nodect = 0
      chunks = repr(pbs.event().job.Resource_List["select"]).split("+")
      if ( len(chunks) != 1 ):
         pbs.event().reject("You can only request one chunk of the form #PBS -l select=N:ncpus=X:mem=Ygb:mpiprocs=Z:ompthreads=W")
      for chunk in chunks:
         nodect+=int(chunk.split(":")[0])
         for rs in chunk.split(":")[1:]:
            kw = rs.split("=")[0]
            if ( kw not in list_of_resources ):
               pbs.event().reject("Select statements can only contain the resources: "+", ".join(list_of_resources))
            if ( kw == "ncpus" ):
               ncpus=int(rs.split("=")[1])
      matched = False
      if ncpus == 32: 
          matched = True

      if not matched:
           pbs.event().reject("Unsupported geometry: Please read https://wiki.imperial.ac.uk/display/HPC/Job+sizing+on+cx1")


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
