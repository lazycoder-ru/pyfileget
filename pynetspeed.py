#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time

class NetSpeed(object):
	startTime = None
	bytesReaded = 0.0
	speed = 0.0	

	def __init__(self, bytesReaded):
		self.bytesReaded = bytesReaded
		self.startTime = time()

	def get_speed(self, bytesReaded):
		if time()-self.startTime >= 1.0:
			self.startTime = time()
			self.speed = (bytesReaded-self.bytesReaded)/1024.0
			self.bytesReaded = bytesReaded
		return self.speed
