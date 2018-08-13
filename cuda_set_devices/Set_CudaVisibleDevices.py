'''

To install the hook: 
1. Copy to the Set_CudaVisibleDevices.py to the current directory
2. Install the hook by running the below commands

qmgr -c "c h set_cuda event='execjob_end,execjob_launch,exechost_periodic'"
qmgr -c "i h set_cuda application/x-python default  Set_CudaVisibleDevices.py"

To disable the hook:
qmgr -c  "set hook set_cuda enabled=false"

To delete the hook:
qmgr -c "delete hook set_cuda"



qmgr -c "l h"
Hook set_cuda
     type = site
     enabled = true
     event = execjob_end,execjob_launch,exechost_periodic
     user = pbsadmin
     alarm = 30
     freq = 120
     order = 1
     debug = true
     fail_action = none


'''


#!/usr/bin/python
import os
import sys
import pbs
import string
import time
import re
import subprocess

# Define PBS_CONF_FILE variable

if sys.platform == 'win32':
    os.environ['PBS_CONF_FILE'] = 'C:\Program Files\PBS Pro\pbs.conf'
else:
    os.environ['PBS_CONF_FILE'] = '/etc/pbs.conf'

if os.path.isfile(os.environ['PBS_CONF_FILE']):
    pbs_conf = open(os.environ['PBS_CONF_FILE'], 'r')
    for line in pbs_conf:
        if '=' in line:
            os.environ[line.split('=')[0]] = line.split('=')[1].strip('\n')
    pbs_conf.close()
else:
    print 'Unable to find PBS_CONF_FILE ... ' + os.environ['PBS_CONF_FILE']
    sys.exit(1)

pbsExec = os.environ['PBS_EXEC']
pbsHome = os.environ['PBS_HOME']

def OpenFile(suspJobsPath, mode): 
    myFile = open(suspJobsPath, mode)
    return myFile

def numGpusOnHost():
    ngpus = 0
    try:
      output = subprocess.check_output( [ "/usr/bin/nvidia-smi", "-L" ] )
      l = output.split("\n")
      for ll in l:
         if "GPU" in ll:
           ngpus = ngpus + 1
      pbs.logmsg(pbs.LOG_DEBUG, "Host has %d GPUs" %( ngpus, ) )
      return ngpus
    except:
      return 0

def UpdateGpuJobs(job,cuda_visible_devices, GpuJobsPath, add):
    if not os.path.exists(hook_storage_path):
        try:
            os.makedirs(hook_storage_path)
        except OSError:
            pass
    if add:
        cuda_visible_devices = cuda_visible_devices.replace('\\','')
        csd = cuda_visible_devices.strip()
        if csd != "":
            f = OpenFile(GpuJobsPath, 'a')
            f.write('%s=%s\n' % ( job.strip(),csd ) )
            f.close()

    else:
        #Remove the entry from file after resuming
        if os.path.exists(GpuJobsPath):
            f = open(GpuJobsPath, 'r')
            lines = f.readlines()
            f.close()
            if lines:
              for line in lines:
                  data = line.split('=')
                  if data[0] == job:
                    lines.remove(line)
              f = OpenFile(GpuJobsPath, 'w')
              for line in lines:
                  f.write('%s\n' % line.strip())
              f.close()

def GetUsedGpus(GpuJobsPath):
    GpuJobs = []
    lines = []
    lst = []
    if os.path.exists(GpuJobsPath):
        f = open(GpuJobsPath, 'r')
        lines = f.readlines()
        f.close()
    for line in lines:
        lst = [ int(x.replace('\'','')) for x in line.split('=')[1].split(',') ]
        GpuJobs = GpuJobs + lst
        GpuJobs.sort()
    return GpuJobs

def GetJobsInFile(GpuJobsPath):
    Jobs = []
    lines = []
    if not os.path.exists(GpuJobsPath):
        pbs.logmsg(pbs.LOG_DEBUG,"GPU job file %s does not exist!" %(GpuJobsPath,))
    if os.path.exists(GpuJobsPath):
        f = open(GpuJobsPath, 'r')
        lines = f.readlines()
        f.close()
    for line in lines:
        lst = line.split('=')[0]
        Jobs.append(lst)
    return Jobs

def GetReqGpus():
    sel = repr(pbs.event().job.schedselect)
    req_gpus = 0
    for chunk in sel.split('+'):
        for c in chunk.split(":"):
            kv = c.split("=")
            if ( kv[0] == "ngpus" ) :
                req_gpus = kv[1]
                pbs.logmsg(pbs.LOG_DEBUG,"Selected ngpus = value=%s" % (str(kv[1])))
    return req_gpus

def getJobs():
    job_lst = []
    jobs = {}
    s = pbs.server()
    if s.vnode(local_node).jobs:
        job_lst = s.vnode(local_node).jobs.split(',')
        for job in job_lst:
            job = re.sub('/\d+','',job)
            job = job.replace(" ","")
            jobs[job] = 1
    return jobs


def execjob_launch():

    try:
      if pbs.event().env["PBS_TASKNUM"] != "1":
        pbs.logmsg(pbs.LOG_DEBUG, "Not the first task, so not setting CUDA_VISIBLE_DEVICES" )
        return
    except:
      pbs.logmsg(pbs.LOG_DEBUG, "Exception in getting PBS_TASKNUM from env")

    job = pbs.event().job.id 
    vn=pbs.event().vnode_list
    req_gpus = GetReqGpus() 



    if req_gpus:
        cuda_visible_devices = ""
        available_gpus = [ i for i in range(0, numGpusOnHost() ) ] # pbs.server().vnode(local_node).resources_available['ngpus']) ]
        ## Check the gpus already assigned on the node
        used_gpus = GetUsedGpus(GpuJobsPath)
        pbs.logmsg(pbs.LOG_DEBUG,"Used GPUs = %s" %(used_gpus))
        if used_gpus:
            available_gpus = [item for item in available_gpus if item not in used_gpus] 
            pbs.logmsg(pbs.LOG_DEBUG,"GPUs available for assignment %s" %(available_gpus))
        for i in range(int(req_gpus)):
           if cuda_visible_devices != "":
             cuda_visible_devices += "\\,"
           cuda_visible_devices += str(available_gpus.pop(0))
        value = cuda_visible_devices
        pbs.logmsg(pbs.LOG_DEBUG,"The Cuda visible devices is  ==> %s" % (value))
        pbs.event().env['CUDA_VISIBLE_DEVICES'] = str(value)
        UpdateGpuJobs(job,value, GpuJobsPath, add=True)

def execjob_end():

    pbs.logmsg(pbs.LOG_DEBUG, "Removing any GPUs assigned to the job" )
    job = pbs.event().job.id
    vn=pbs.event().vnode_list
    # does not matter what the value is just remove the job from file after completion
    value = ""
    UpdateGpuJobs(job,value, GpuJobsPath, add=False)

def exechost_periodic():
    vn=pbs.event().vnode_list
    JobsOnNode = getJobs() 
    JobsOnFile = GetJobsInFile(GpuJobsPath)
    pbs.logmsg(pbs.LOG_DEBUG,"Jobs in File %s" %(JobsOnFile))
    for job in JobsOnFile: 
        if not (str(job) in JobsOnNode.keys()):
            # Remove this job
            value = ""
            UpdateGpuJobs(job,value, GpuJobsPath, add=False)
            pbs.logmsg(pbs.LOG_DEBUG, "Removing Job %s from file %s --> The job is not running on the node" %(job, GpuJobsPath))
        
try:
    pbs.logmsg(pbs.LOG_DEBUG, 'Starting %s, event %s' % (pbs.event().hook_name, pbs.event().type))
    hook_storage_path = '/var/spool/PBS/spool/'
    GpuUsingJobs = 'jobs_using_gpus'
    GpuJobsPath = os.path.join(hook_storage_path, GpuUsingJobs)
    local_node = pbs.get_local_nodename()

    if pbs.event().type == pbs.EXECJOB_LAUNCH:
        execjob_launch()
    if pbs.event().type == pbs.EXECJOB_END:
        execjob_end()
    if ( pbs.event().type == pbs.EXECHOST_PERIODIC ):
#        s = pbs.server()
#        if ('ngpus' in s.vnode(local_node).resources_available.keys()) :
#          if str( s.vnode(local_node).resources_available["ngpus"] ) != "0":
        if (numGpusOnHost() > 0):
              pbs.logmsg(pbs.LOG_DEBUG, 'Running set_cuda_visible_devices periodic hook' )
              exechost_periodic()
        else:
              pbs.logmsg(pbs.LOG_DEBUG, 'Not running set_cuda_visible_devices periodic hook - no GPUs' )

except : 
    import traceback
    
    log_buffer = traceback.format_exc()
    pbs.logmsg(pbs.LOG_DEBUG, 'Hook exception:')
    for line in log_buffer.split('\n'):
        pbs.logmsg(pbs.LOG_DEBUG, line)
#    pbs.event().reject("Exception trapped in %s:\n %s" % (pbs.event().hook_name, log_buffer))
    pbs.event().accept()

