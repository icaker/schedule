#! /usr/bin/python2.7
#! -*-coding:utf-8 -*-
#Program:
#    simulation process with
#    3 types of bandwidth(10Mbps,1Mbps,0.1Mbps),
#    5 servers (Max Rate:100Mbps)
#Usage:
#    $ ./simulate.py [simulate date file]
#Date:
#    2014.07.17

import sys
import commands
# from operator import itemgetter
from math import ceil

Rmax=[100]*5

type=[10.0,1.0,0.1]                     #rate type
qnew=[[] for t in range(3)]
qtemp=[[] for t in range(3)]
qwait=[[] for t in range(3)]
qloadlen=[0,0,0]                        #queue length for different rate type

logfile=open(sys.argv[1])
req=logfile.readline().split()
req[0]=int(req[0])                      #timestamp
req[1]=float(req[1])                    #file size
req[2]=int(req[2])                      #type flag
for second in range(3600):
    ra=Rmax                             #rate available
    print "second %d" % second
    #calculate waiting queue to be scheduled
    #each item in waiting queue is an integer,indicating time slot required
    qwait[0]=qtemp[0]+qnew[0]
    qwait[1]=qtemp[1]+qnew[1]
    qwait[2]=qtemp[2]+qnew[2]
    qloadlen=[sum(i) for i in qwait]
    num=[len(i) for i in qwait]         #task number

    print "qloadlen"
    print qloadlen
    print "qloadnum"
    print num

    #bandwidth allocation using GLPK,results = [1,2,3,...,13,14,15]
    shell="solve_preemptive/solve %d %d %d %d %d %d 100" % (qloadlen[0],qloadlen[1],qloadlen[2],num[0],num[1],num[2])
    temp_results=commands.getoutput(shell).split("\n")[-1].split(",")
    results=[int(i) for i in temp_results]
    summary=[0,0,0]                     #different type of bandwidth allocation summary
    for i in range(3):
        for j in range(5):
            summary[i]=summary[i]+results[i+j*3]

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
    while(req[0]==second):
        qnew[req[2]].append(int(ceil(req[1]/type[req[2]])))
        req=logfile.readline().split()
        if not len(req):
            break
        req[0]=int(req[0])                      #timestamp
        req[1]=float(req[1])                    #file size
        req[2]=int(req[2])                      #type flag

    throughput=summary[0]*type[0]+summary[1]*type[1]+summary[2]*type[2]
    #output print
    print results
    print summary
    print "throughput %f" % throughput

    if not len(req):
        break

logfile.close()
