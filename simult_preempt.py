#! /usr/bin/python2.7
#! -*-coding:utf-8 -*-
#Program:
#    simulation process with
#    3 types of bandwidth(10Mbps,1Mbps,0.1Mbps),
#    5 servers (Max Rate:100Mbps)
#Usage:
#    $ ./simult_preempt.py [simulate date file] [request detail record file]
#Date:
#    2014.07.17

import sys
import commands
from math import ceil

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
        self.server=[]                  #server id scheduled
        self.schedule_time=[]

Rmax=[100]*5

type=[10.0,1.0,0.1]                     #rate type
qnew=[[] for i in range(3)]
qtemp=[[] for i in range(3)]
qwait=[[] for i in range(3)]
qloadlen=[0,0,0]                        #queue length for different rate type
req_todo = [[],[],[]]                   #requests pushed but not finished
logfile=open(sys.argv[1])
logdetail=open(sys.argv[2],'w')         #write schedule detail to it
req=logfile.readline()
req_next = Request(req)

for second in range(7200):
    ra=Rmax                             #rate available
    print "second %d" % second
    #calculate waiting queue to be scheduled
    #each item in waiting queue is an integer,indicating time slot required
    qwait[0]=qtemp[0]+qnew[0]
    qwait[1]=qtemp[1]+qnew[1]
    qwait[2]=qtemp[2]+qnew[2]
    qloadlen=[sum(i) for i in qwait]
    num=[len(i) for i in qwait]         #task number

    #bandwidth allocation using GLPK,results = [1,2,3,...,13,14,15]
    shell="solve_preemptive/solve %f %f %f %d %d %d 100" % (qloadlen[0],qloadlen[1],qloadlen[2],num[0],num[1],num[2])
    temp_results=commands.getoutput(shell).split("\n")[-1].split(",")
    results=[int(i) for i in temp_results]
    summary=[0,0,0]                     #different type of bandwidth allocation summary
    for i in range(3):
        for j in range(5):
            summary[i]=summary[i]+results[i+j*3]

    #update Requests info about server id and time scheduled
    #firstly,get server id for requests to be scheduled
    server_id = [[] for i in range(3)]
    for i in range(3):
        for j in range(5):
            x = results[j*3+i]
            if x:
                server_id[i].extend([j]*x)
    #then update each Request info
    for i in range(3):
        f=0
        for j in range(summary[i]):
            id = server_id[i][j]
            req_todo[i][j-f].server.append(id)
            req_todo[i][j-f].schedule_time.append(second)
            req_todo[i][j-f].ttl -= 1
            if req_todo[i][j-f].ttl==0:
                #print its detail to file [logdetail] and req departure
                req_todo[i][j-f].complete = second
                depart = req_todo[i][j-f]     #just for short
                s_id = "|".join([str(t) for t in depart.server])
                s_id_time = "|".join([str(t) for t in depart.schedule_time])
                detail = "%d\t%f\t%d\t%d\t%s\t%s\n"%(depart.request_time,depart.size,depart.rtype,depart.complete,s_id,s_id_time)
                logdetail.write(detail)
                #departure
                del req_todo[i][j-f]
                f=f+1


    #request scheduled,reduce the load in waiting queue
    for i in range(3):
        f=0
        for j in range(summary[i]):
            qwait[i][j-f]=qwait[i][j-f]-1
            if qwait[i][j-f]==0:
                del qwait[i][j-f]
                f=f+1


    #request to be moved back
    qtemp=qwait

    #new request coming
    qnew=[[],[],[]]
    while(req_next.request_time==second):
        qnew[req_next.rtype].append(req_next.ttl)
        req_todo[req_next.rtype].append(req_next)
        req=logfile.readline()
        if not bool(req):
            break
        req_next=Request(req)

    throughput=summary[0]*type[0]+summary[1]*type[1]+summary[2]*type[2]
    #output print
#    print results
 #   print summary
  #  print "throughput %f" % throughput


logfile.close()
logdetail.close()
