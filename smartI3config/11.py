import fcntl,sys,os,time

fp=open("/var/tmp/lf",'w')
try:
    fcntl.lockf(fp,fcntl.LOCK_EX|fcntl.LOCK_NB)
except:
    os._exit(0)
time.sleep(20)
