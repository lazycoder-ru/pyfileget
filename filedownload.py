#!/usr/bin/python
# -*- coding: utf-8 -*- 

import os,sys,urllib2,platform,time
import pynetspeed

APPENDMODE = "ab"
REWRITEMODE = "wb"

def getConsoleWidth():
    columns = 80 #for windows and others
    if platform.system() == "Linux":
        columns = os.popen('stty size', 'r').read().split()[1]
    return int(columns)
    
def getLoadingBar(ln, percent=100, bracket="[]", fillch="#", emptych="-"):
    sumln = ln-2 #2 brackets
    filled = int(percent*sumln/100)
    return "%s%s%s%s" % (bracket[0], fillch*filled, emptych*(sumln-filled), bracket[1])

def getNewPath(url, name=None, folderpath=None):
    if not name: name = url.split("/")[-1] #if name is empty  
    if folderpath: 
        folderpath = folderpath.rstrip(os.sep)
        if not os.path.exists(folderpath): os.makedirs(folderpath)
    else:
        folderpath=os.getcwd() # from curdir to absolute path
    return "%s%s%s" % (folderpath, os.sep, name)

def displayDownloadInfo(bytesRead, remoteLen, speed, conWidth):
    #TODO: make templated output
    percent = 100*bytesRead/remoteLen
    curInfo = "\rProgress: %.02f/%.02f KB (%d%%) %.02f KB/s" % (
        bytesRead/1024.0,
        remoteLen/1024.0,
        percent,
        speed)
    loadbar = getLoadingBar(conWidth-len(curInfo), percent)
    curInfo = curInfo[:11] + loadbar + curInfo[10:] #after progress
    sys.stdout.write(curInfo)
    sys.stdout.flush()    

def downloadfile(url, newName=None, folderpath=None):
    print "Sending request..."
    try:
        res = urllib2.urlopen(url)
        remoteLen = float(res.info().getheader("Content-Length"))
    except (urllib2.HTTPError, urllib2.URLError), e:
        print e
        print "Download aborted.\n"
        return
    except TypeError:
        #TODO: download web pages (they have None in Length)
        print "Content-Length is None. Nothing to download.\n"
        return
        
    print "Received code:", res.getcode()
    print "Length: %d (%.02fM) [%s]" % (
        remoteLen,
        remoteLen/1024.0/1024.0,
        res.info().getheader("Content-Type"))
    newPath = getNewPath(url, newName, folderpath)
    print "Saving to:", newPath
    
    if os.path.exists(newPath): 
        localLen = int(os.path.getsize(newPath))  
        if localLen == remoteLen:
            print "File has downloaded already.\n"
            return
        mode = APPENDMODE
    else: 
        localLen = 0
        mode = REWRITEMODE

    try:
        localFile = open(newPath, mode)    
    except (IOError, OSError), e:
        print e
        print "Download aborted.\n"
        return

    req = urllib2.Request(url)
    req.headers['Range'] = 'bytes='+str(localLen)+'-'
    try:
        remoteFile = urllib2.urlopen(req)
    except (urllib2.HTTPError, urllib2.URLError), e:
        print e
        return
        
    cols = getConsoleWidth()
    print "Downloading:", remoteFile.url
    bytesRead = float(localLen)
    pynetspeed.initMeter(bytesRead)
    for line in remoteFile:
        bytesRead += len(line)
        displayDownloadInfo(bytesRead, remoteLen, pynetspeed.getNetSpeed(bytesRead), cols)
        localFile.write(line)
    remoteFile.close()
    localFile.close()
    print "\nFile [%s] has been downloaded.\n" % newPath
    return
