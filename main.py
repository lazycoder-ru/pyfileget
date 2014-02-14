#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Just for test file download module

import os
import lib.pyfileget

def main():
    home = os.path.expanduser("~")
    lib.pyfileget.download("http://mirror.yandex.ru/ubuntu-releases/13.10/ubuntu-13.10-desktop-i386.iso", home)
    return 0

if __name__ == '__main__':
    main()

