#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Just for test file download module

import os
from filedownload import pyget

def main():
	home = os.path.expanduser("~")
	pyget("http://mirror.yandex.ru/ubuntu-releases/13.10/ubuntu-13.10-desktop-i386.iso", home)
	#http://mirror.yandex.ru/ubuntu-releases/13.10/ubuntu-13.10-desktop-i386.iso
	
	return 0

if __name__ == '__main__':
	main()

