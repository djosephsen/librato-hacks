#!/usr/bin/python
import argparse
import librato
import numpy
dataPoints=[]
measurements=[]
#TODO: add reading creds from the environment
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

for d in dataPoints:
	print "%s:%s" % (d['time'],d['value'])

print "%s Total dataPoints across %s Pages" % (len(dataPoints),page)

for p in [75,80,85,90,95,99]:
	print "%sth percentile: %s" % (p,numpy.percentile(measurements,p))
