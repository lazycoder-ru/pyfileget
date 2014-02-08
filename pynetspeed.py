#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time

startTime = None
bytesReaded = 0.0

def initMeter(startSize=0.0):
	startTime = time()
	global bytesReaded
	bytesReaded = startSize
	
def getNetSpeed(_bytesReaded):
	if time()-starTime >= 1.0:
		startTime = time()
		global bytesReaded
		speed = (_bytesReaded-byteReaded)/1024.0
		bytesReaded = _bytesReaded
		return speed

