#!/usr/bin/env python
# -*- coding: utf-8 -*-

class DownloadError(Exception):
    def __init__(self, value, systemErrorValue=""):
        self.systemErrorValue = systemErrorValue
        self.value = value

    def __str__(self):
        return str(self.systemErrorValue) + " " + str(self.value)

