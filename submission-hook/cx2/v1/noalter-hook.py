import pbs
e = pbs.event()
j = e.job
who = e.requestor
pbs.logmsg(pbs.LOG_DEBUG, "move/modify requestor=%s" % (who,))
admin_ulist = ["PBS_Server", "Scheduler", "pbs_mom", "root", "apache", "rcregan", "mjharvey"]
if who not in admin_ulist:
  e.reject("Normal users are not allowed to modify their jobs")
