#!/usr/bin/python
# -*- coding: utf-8 -*- 

import os,sys,urllib2,platform,time
from pynetspeed import NetSpeed

APPENDMODE = "ab"
REWRITEMODE = "wb"
DL_EXT = ".download"

def get_console_width():
    columns = 80 #for windows and others
    if platform.system() == "Linux":
        columns = os.popen('stty size', 'r').read().split()[1]
    return int(columns)
    
def get_loading_bar(totalLen, percent=100, bracket="[]", fillch="#", emptych="-"):
    barLen = totalLen-2 #2 brackets
    filled = int(percent*barLen/100)
    return "%s%s%s%s" % (bracket[0], fillch*filled, emptych*(barLen-filled), bracket[1])

def get_new_path(url, localpath=None):
    filename = url.split("/")[-1]
    folderpath = os.getcwd()
    if localpath:
        if os.path.isdir(localpath) or localpath[-1] == os.sep:
            folderpath = os.path.abspath(localpath)
        else:
            filename = os.path.basename(localpath)
            folderpath = os.path.abspath(os.path.dirname(localpath))
        try:
            if not os.path.exists(folderpath): os.makedirs(folderpath)
        except (IOError, OSError), e:
            folderpath = os.getcwd()
            print e, "\nUsing working directory:", folderpath
    return "%s%s%s" % (folderpath, os.sep, filename)

def rename_downloaded(path):
    try:
        os.rename(path+DL_EXT, path)
    except (IOError, OSError), e:
        print e
        print "Error while renaming file. Renaming aborted."        

def display_download_info(bytesRead, remoteLen, speed, conWidth):
    #TODO: make templated output
    percent = 100*bytesRead/remoteLen
    curInfo = "\rProgress: %.02f/%.02f KB (%d%%) %s" % (
        bytesRead/1024.0,
        remoteLen/1024.0,
        percent,
        speed)
    loadbar = get_loading_bar(conWidth-len(curInfo), percent)
    curInfo = curInfo[:11] + loadbar + curInfo[10:] #after progress
    sys.stdout.write(curInfo)
    sys.stdout.flush()    

def download_file(url, localpath=None):
    #requesting file and getting length of remote file
    print "Sending request..."
    try:
        res = urllib2.urlopen(url)
        remoteLen = float(res.info().getheader("Content-Length"))
    except (urllib2.HTTPError, urllib2.URLError), e:
        print e
        print "Download aborted.\n"
        return
    except TypeError:
        #TODO: make ability to download web pages (they have None in Length)
        print "Content-Length is None. Nothing to download.\n"
        return
    #print info
    print "Received code:", res.getcode()
    print "Length: %d (%.02fM) [%s]" % (
        remoteLen,
        remoteLen/1024.0/1024.0,
        res.info().getheader("Content-Type"))
    #getting local path
    newPath = get_new_path(url, localpath)
    print "Saving to:", newPath
    #getting length of local file
    currentDlPath = newPath+DL_EXT
    if os.path.exists(currentDlPath):
        localLen = int(os.path.getsize(currentDlPath))
        if localLen == remoteLen:
            print "File has downloaded already.\n"
            rename_downloaded(newPath)
            return
        mode = APPENDMODE
    else:
        localLen = 0
        mode = REWRITEMODE
    #getting local file handle
    try:
        localFile = open(currentDlPath, mode)    
    except (IOError, OSError), e:
        print e
        print "Download aborted.\n"
        return
    #getting remote file handle
    req = urllib2.Request(url)
    req.headers['Range'] = 'bytes='+str(localLen)+'-'
    try:
        remoteFile = urllib2.urlopen(req)
    except (urllib2.HTTPError, urllib2.URLError), e:
        print e
        return
    #downloading
    cols = get_console_width()
    print "Downloading:", remoteFile.url
    bytesReaded = float(localLen)
    speed = NetSpeed(bytesReaded)
    for line in remoteFile:
        bytesReaded += len(line)
        display_download_info(bytesReaded, remoteLen, speed.get_speed(bytesReaded), cols)
        localFile.write(line)
    remoteFile.close()
    localFile.close()
    rename_downloaded(newPath)
    print "\nFile [%s] has been downloaded.\n" % newPath
    return
