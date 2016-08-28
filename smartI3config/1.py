import fcntl,sys,os

fp=open("/var/tmp/lf",'w')
try:
    fcntl.lockf(fp,fcntl.LOCK_EX|fcntl.LOCK_NB)
except:
    print("other prog is running")
    os._exit(0)
    

