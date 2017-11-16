#
# Submit hook
# CX2
# HPC - Imperial College London
#

import sys
import pbs

list_of_resources = ["ncpus","mem","mpiprocs","ompthreads", "cpumodel"]

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
    nodect = int(  chunk[0] )

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
      ret[key] = val
  except:
    pass
  return ret
  

def fixup_mpiprocs_ompthreads( sel ):
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
        pbs.event().reject( "mpiprocs * ompthreads must equal ncpus" )


try:
#
# Verify user requested walltime
   if ( pbs.event().job.Resource_List["walltime"] == None ):
      pbs.event().reject("Walltime must be specified, jobs cannot be scheduled without a runtime estimate!")

   walltime = pbs.event().job.Resource_List["walltime"] 
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
   if queue_name[0] != "R" and queue_name[0] != "e": # Anything goes in a Reservation or expedited queue
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
      if nodect <= 18 and ncpus==24 and walltime <= pbs.duration("2:0:0"):
          pbs.event().job.queue=pbs.server().queue("short")
          matched = True 
      if not matched and nodect>=2 and nodect <=18 and ncpus == 16 and walltime <= pbs.duration("72:0:0"):
          pbs.event().job.queue=pbs.server().queue("general")
          matched = True 
      if not matched and nodect>=72 and nodect <=270 and ncpus in [28] and walltime <= pbs.duration("24:0:0"):
          pbs.event().job.queue=pbs.server().queue("capability")
          matched = True 
      if not matched and nodect>=18 and nodect <=72 and ncpus in [24,28] and walltime <= pbs.duration("48:0:0"):
          pbs.event().job.queue=pbs.server().queue("large")
          matched = True 

      if not matched:
           pbs.event().reject("Unsupported geometry: Please read https://wiki.imperial.ac.uk/display/HPC/Job+sizing+on+cx2")

# Logic for expedited queues
# Only allow 24 core jobs
   if queue_name[0] == "e":
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
      if ncpus == 24 and nodect <= 270:
          matched = True 

      if not matched:
           pbs.event().reject("Unsupported geometry: Please read https://wiki.imperial.ac.uk/display/HPC/Job+sizing+on+cx2")

   sel = extract_selection()
   fixup_mpiprocs_ompthreads(sel)
      

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
