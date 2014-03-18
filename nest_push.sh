#!/bin/sh
#use nest.py to gather interesting metrics, and push them to librato

NP="/home/dave/tmp/nest.py" # the location of the nest.py script
source ${SBHOME}/shellbrato.sh #the librato shell library


${NP} | egrep -w 'current_humidity|current_temperature|hvac_heater_state|target_temperature' | sed -e 's/\.\+: /:/'| while read METRIC
do
	read NAME VALUE <<< $(echo ${METRIC} | tr ':' ' ')
	[ "${VALUE}" == "True" ] && VALUE=1
	[ "${VALUE}" == "False" ] && VALUE=0
	queueGauge "$(date +%s)||${NAME}||${VALUE}" #queue up each metric
done

sendMetrics  #send them to librato
