from threading import Thread
import subprocess
from queue import Queue
import time

start = time.time()
num_threads=20
ips = [f"192.168.20.{i}" for i in range(1, 101)]
if ips:
    num_threads = len(ips)
q=Queue()
def pingme(i,queue):
    while True:
        ip=queue.get()
        print ('Thread %s pinging %s' %(i,ip))
        ret=subprocess.call('ping %s' % ip,shell=True,stdout=open('D:/null','w'),stderr=subprocess.STDOUT)
        if ret==0:
            print ('%s 活着!' %ip)
        elif ret==1:
            print ('%s 挂了...'%ip)
        queue.task_done()

#start num_threads threads
for i in range(num_threads):
    t=Thread(target=pingme,args=(i,q))
    t.setDaemon(True)
    t.start()

for ip in ips:
    q.put(ip)
print ('main thread waiting...')
q.join();
end = time.time()
running_time = end-start
print('time cost : %.3f sec' %running_time)
print ('完成')