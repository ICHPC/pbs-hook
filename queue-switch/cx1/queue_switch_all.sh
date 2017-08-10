#!/bin/sh

for Q in $(qstat -q | grep pq | awk '{print $1}'); do 
	./queue_switch $T serial24,singlenode24,multinode24 
done
