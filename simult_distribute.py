#! /usr/bin/python2.7
#! -*-coding:utf-8 -*-
#Program:
#    simulation process with
#    3 types of bandwidth(10Mbps,1Mbps,0.1Mbps),
#    5 servers (Max Rate:100Mbps)
#Usage:
#    $ ./simult_distribute.py [simulate date file] [request detail record file]
#Date:
#    2014.07.29

import sys
import commands
from math import ceil
from operator import itemgetter

class Request:
    def __init__(self,req):
        req=req.split()
        a=int(req[0])
        b=float(req[1])
        c=int(req[2])
        rt=[10,1,0.1]                   #used to get initial ttl
        self.request_time=a             #timestamp
        self.size=b                     #file size
        self.rtype=c                    #type flag
        self.complete=0                 #complete time
        self.ttl=int(ceil(b/rt[c]))
        self.server=0                  #server id scheduled
        self.schedule_time=0

Rmax=[100]*5

type=[10.0,1.0,0.1]                     #rate type
qwait= [[[],[],[]] for i in range(5)]   #request length to be scheduled
qloadlen=[0,0,0]                        #queue length for different rate type
req_on_server = [[[],[],[]] for i in range(5)]      #requests pushed but not finished
req_wait = [[[],[],[]] for i in range(5)]           #new requests waiting list
summary=[[0,0,0] for i in range(5)]                 #number of different request on server

logfile=open(sys.argv[1])
logdetail=open(sys.argv[2],'w')         #write schedule detail to it
req=logfile.readline()
req_next = Request(req)

ra = Rmax
for second in range(7200):
    print "second %d" % second
    #calculate waiting queue to be scheduled
    #each item in waiting queue is an integer,indicating time slot required
    for i in range(5):
        qloadlen=map(sum,qwait[i])
        num=map(len,qwait[i])           #task number
       # print 'i,num:%d'%i
       # print 'num:%d,%d,%d'%(num[0],num[1],num[2])
        #bandwidth allocation using GLPK,results = [1,2,3]
        shell="solve_distribute/solve %d %d %d %d %d %d %f" % (qloadlen[0],qloadlen[1],qloadlen[2],num[0],num[1],num[2],ra[i])
        temp_results=commands.getoutput(shell).split("\n")[-1].split(",")
        results=[int(j) for j in temp_results]
      #  print shell
       # print results
        summary[i][0]+=results[0]
        summary[i][1]+=results[1]
        summary[i][2]+=results[2]

        #update Requests info about time scheduled
        for j in range(3):
            f=0
            x = results[j]
            for k in range(x):
                req_wait[i][j][k-f].schedule_time=second
                req_on_server[i][j].append(req_wait[i][j][k-f])
                ra[i]-=type[j]
                del req_wait[i][j][k-f]
                del qwait[i][j][k-f]
                f+=1

        #then update each Request ttl on server
        for j in range(3):
            f=0
            for k in range(summary[i][j]):
                req_on_server[i][j][k-f].ttl -= 1
                if req_on_server[i][j][k-f].ttl==0:
                    #print its detail to file [logdetail] and req departure
                    req_on_server[i][j][k-f].complete = second
                    depart = req_on_server[i][j][k-f]     #just for short
                    detail = "%d\t%f\t%d\t%d\t%d\t%d\n"%(depart.request_time,depart.size,depart.rtype,depart.complete,depart.server_id,depart.schedule_time)
                    logdetail.write(detail)
                    #departure
                    ra[i]+=type[j]
                    summary[i][j]-=1
                    del req_on_server[i][j][k-f]
                    f=f+1

    #new request coming
    while(req_next.request_time==second):
        itstype = req_next.rtype
        theirque =map(itemgetter(itstype),qwait)
        theirlen =map(sum,theirque)
        sid = min(enumerate(theirlen),key=itemgetter(1))[0]
        req_next.server_id = sid
        qwait[sid][req_next.rtype].append(req_next.ttl)
        req_wait[sid][req_next.rtype].append(req_next)
        req=logfile.readline()
        if not bool(req):
            break
        req_next=Request(req)

logfile.close()
logdetail.close()
