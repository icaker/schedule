#! /usr/bin/python2.7
#! -*-coding:utf-8 -*-
#Program:
#    simulation process with
#    3 types of bandwidth(10Mbps,1Mbps,0.1Mbps),
#    5 servers (Max Rate:100Mbps)
#Usage:
#    $ ./simult_non_preempt.py [simulate date file] [request detail record file]
#Date:
#    2014.07.27

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
        self.server=0                  #server id scheduled
        self.schedule_time=0

Rmax=[100]*5

type=[10.0,1.0,0.1]                     #rate type
qnew=[[] for i in range(3)]             #new requests coming
qloadlen=[0,0,0]                        #queue length for different rate type
req_on_server = [[],[],[]]              #Requests pushed but not finished
req_new = [[],[],[]]                    #Requests new coming
summary=[0,0,0]                         #different type of bandwidth allocation summary
logfile=open(sys.argv[1])
logdetail=open(sys.argv[2],'w')         #write schedule detail to it
req=logfile.readline()
req_next = Request(req)

ra=Rmax                                 #rate available
for second in range(7200):
    print "second %d" % second
    #calculate new queue to be scheduled
    #each item in new queue is an integer,indicating time slot required
    qloadlen=[sum(i) for i in qnew]
    num=[len(i) for i in qnew]          #task number

    #print 'qloadlen :'
    #print qloadlen
    #print 'num :'
    #print num

    #bandwidth allocation using GLPK,results = [1,2,3,...,13,14,15]
    shell="solve_non_preemptive/solve %d %d %d %d %d %d %d %d %d %d %d" % (qloadlen[0],qloadlen[1],qloadlen[2],num[0],num[1],num[2],ra[0],ra[1],ra[2],ra[3],ra[4])
    temp_results=commands.getoutput(shell).split("\n")[-1].split(",")
    results=[int(i) for i in temp_results]
    #print 'results :'
    #print results

    #current server status
    new_allo=[0,0,0]                     #different type of bandwidth new allocation
    for i in range(3):
        for j in range(5):
            new_allo[i]=new_allo[i]+results[i+j*3]
    summary[0]=summary[0]+new_allo[0]
    summary[1]=summary[1]+new_allo[1]
    summary[2]=summary[2]+new_allo[2]
    #print "new_allo :"
    #print  new_allo
    #print "summary :"
    #print summary

    #update Requests info about server id and time scheduled
    #firstly,get server id for requests to be scheduled
    server_id = [[] for i in range(3)]
    for i in range(3):
        for j in range(5):
            x = results[j*3+i]
            if x:
                server_id[i].extend([j]*x)
    #print "server_id :"
    #print server_id

    #then push each new Request to server,
    #i.e. write server id and scheduled time to Request info
    req_todo=[[],[],[]]
    for i in range(3):
        f=0
        for j in range(new_allo[i]):
            id = server_id[i][j]
            req_new[i][j-f].server = id
            req_new[i][j-f].schedule_time = second
            ra[id]-=type[i]
            req_todo[i].append(req_new[i][j-f])
            del req_new[i][j-f]
     #       print "i,j,f,second"
      #      print i,j,f,second
            f=f+1
        req_on_server[i].extend(req_todo[i])

    #update each Request info
    #i.e. reduce ttl and del finished ones
    for i in range(3):
        f=0
        for j in range(summary[i]):
            req_on_server[i][j-f].ttl -= 1
            if req_on_server[i][j-f].ttl==0:
                #print its detail to file [logdetail] and req departure
                req_on_server[i][j-f].complete = second
                depart = req_on_server[i][j-f]     #just for short
                detail = "%d\t%f\t%d\t%d\t%d\t%d\n"%(depart.request_time,depart.size,depart.rtype,depart.complete,depart.server,depart.schedule_time)
                logdetail.write(detail)
                #resource released
                ra[depart.server]+=type[depart.rtype]
                #departure
                del req_on_server[i][j-f]
                summary[i]-=1
                f=f+1
   # print "ra :"
    #print ra

    #new request coming
    qnew=[[],[],[]]
    while(req_next.request_time==second):
        qnew[req_next.rtype].append(req_next.ttl)
        req_new[req_next.rtype].append(req_next)
        req=logfile.readline()
        if not bool(req):
            break
        req_next=Request(req)
   # print 'qnew :'
   # print qnew
    #bandwidth availiable
    throughput=summary[0]*type[0]+summary[1]*type[1]+summary[2]*type[2]

logfile.close()
logdetail.close()
