#! /usr/bin/python2.7
#! -*-coding:utf-8 -*-
#Program:
#    calculate average delay of all requests
#    according to request detail log
#Usage:
#    $ ./delay [request detail log] [ouput with delay info]
#Date:
#    2014.07.31

from sys import argv
from math import ceil

input = open(argv[1])
output = open(argv[2],'w')
type=[10.0,1.0,0.1]
for req in input:
    line=req.split()
    request_time = int(line[0])
    complete_time =int(line[3])
    require_slot = int(ceil(float(line[1])/type[int(line[2])]))
    delay =complete_time-request_time-require_slot
    output.write("%s\t%d" %(req,delay))

input.close()
output.close()
