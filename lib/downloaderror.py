# -*- coding: utf-8 -*-
#
# Simple user-exceptions class for download problems.
# 3nd argument in constructor is for system exceptions text that may
# caused by downloading process.  


class DownloadError(Exception):
    def __init__(self, value, sysErrorValue=None):
        self.sysErrorValue = sysErrorValue
        self.value = value

    def __str__(self):
        if self.sysErrorValue:
            return str(self.sysErrorValue) + " " + self.value.encode("utf-8")
        return self.value.encode("utf-8")

