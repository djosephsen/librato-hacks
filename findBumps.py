#!/usr/bin/python
# iterate through metric names on stdin and check the last 24 hours worth of data for 95th percentile bumps. 

import argparse
import librato
import numpy
import os
dataPoints=[]
measurements=[]
lbUser=os.environ['LBUSER']
lbToken=os.environ['LBTOKEN']
api=librato.connect(lbUser,lbToken )
page=0

parser = argparse.ArgumentParser()
parser.add_argument("mName", type=str, help="The metric name")
parser.add_argument("sTime", type=int, help="The start time in epoc seconds")
args = parser.parse_args()


def getMetric(mName, sTime):
#recursive function to page through results
	global page,measurements,dataPoints
	page+=1
	metric=api.get(mName, start_time=sTime , resolution=1)

	for host in metric.measurements:
		h=metric.measurements[host][0]
		mDict={'host':host, 'time':h["measure_time"], 'value':h['value']}
		dataPoints.append(mDict)
		measurements.append(h['value'])
		#print "%s :: %s : %s" % (host, h["measure_time"], h["value"])

	if 'next_time' in metric.query:
		getMetric(mName,metric.query['next_time'])


##### Lets kick this pig
getMetric(args.mName,args.sTime)

#what's the difference between the 90th and 95th?
eighty=numpy.percentile(measurements,80)
ninety=numpy.percentile(measurements,90)
ninetyfive=numpy.percentile(measurements,95)
lower_dif=ninety-eighty
upper_dif=ninetyfive-ninety

print "%s, (%s vs %s)" % (args.mName, upper_dif, lower_dif)
for p in [75,80,85,90,95,99]:
	print "%sth percentile: %s" % (p,numpy.percentile(measurements,p))

if (lower_dif > 0):
	if (upper_dif > lower_dif):
		outFile='/home/dave/tmp/librato_data/%s' % args.mName
		print 'found one!! %s, (%s vs %s)' % (args.mName, upper_dif, lower_dif)
		for p in [75,80,85,90,95,99]:
			print "%sth percentile: %s" % (p,numpy.percentile(measurements,p))
		f = open(outFile, 'w')
		f.write('%s'%dataPoints)
		f.close()
