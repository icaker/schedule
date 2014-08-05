#! /usr/bin/python2.7
#! -*-coding:utf-8 -*-
#Program:
#    calculate average throuthput within a minute,
#    according to throughput data of each second
#Usage:
#    $ ./average_throughput.py [input file] [output file]
#Date:
#    2014.08.02

import sys
input =open(sys.argv[1])
output=open(sys.argv[2],'w')
input.readline()                        #the first line is useless
line = input.readline()
temp=[0 for i in range(5)]
n=1
while(line):
    line = line.split()
    for i in range(5):
        temp[i]+=float(line[i])
    if (n%60 == 0):
        info = ' '.join([str(i/60) for i in temp])
        output.write(info+'\n')
        temp = [0 for i in range(5)]
    line = input.readline()
    n+=1;

input.close()
output.close()
