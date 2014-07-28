#! /usr/bin/python2.7
#! -*-coding:utf-8 -*-
#Program:
#    calculate actual throuthput on each server,
#    according to request detail log
#Usage:
#    $ ./throughput.py [request detail log] [output file]
#Date:
#    2014.07.26

import sys
input =open(sys.argv[1])
output=open(sys.argv[2],'w')

type=[10,1.0,0.1]
MAX_DURATION_TIME = 3660+1
#each element in this represensts acutal throughput of each time slot
throughput = [[0,0,0,0,0] for i in range(MAX_DURATION_TIME)]

for record in input:
    record = record.split()   #timestamp,size,type,complete_time,server_id,schedule_time
    size = float(record[1])
    rt = int(record[2])
    server_id = [int(i) for i in record[4].split('|')]
    schedule_time = [int(i) for i in record[5].split('|')]
    n = len(server_id)        #time slot required
    for i in range(n-1):
        sid = server_id[i]
        t = schedule_time[i]
        throughput[t][sid]+=type[rt]
    lastid = server_id[-1]
    lastime =schedule_time[-1]
    throughput[lastime][lastid]+=size-(n-1)*type[rt]

for data in throughput:
    output.write(("  ".join([str(i) for i in data]))+'\n')

input.close()
output.close()
