#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time

startTime = None
bytesReaded = 0.0
speed = 0.0

def initMeter(startSize=0.0):
	global bytesReaded, startTime
	startTime = time()
	
	bytesReaded = startSize
	
def getNetSpeed(_bytesReaded):
	global bytesReaded, startTime, speed
	if time()-startTime >= 1.0:
		startTime = time()
		speed = (_bytesReaded-bytesReaded)/1024.0
		bytesReaded = _bytesReaded
	return speed

