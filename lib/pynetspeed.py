# -*- coding: utf-8 -*-

from time import time

class NetSpeed(object):
    startTime = None
    bytesReaded = 0.0
    speed = 0.0
    measure = "KB"
    measures = {"B":1, "KB":1024.0, "MB":1024.0*1024.0}

    def __init__(self, bytesReaded, measure="KB"):
        self.bytesReaded = bytesReaded
        if not measure in self.measures.keys():
            measure = "KB"
        self.measure = measure
        self.startTime = time()

    def get_speed(self, bytesReaded):
        if time()-self.startTime >= 1.0:
            self.startTime = time()
            self.speed = (bytesReaded-self.bytesReaded)/self.measures[self.measure]
            self.bytesReaded = bytesReaded
        return "%.02f %s/s" % (self.speed, self.measure)
