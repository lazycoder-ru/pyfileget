#!/usr/bin/python
# -*- coding: utf-8 -*- 

import os,sys,urllib2,platform,time

def getConsoleWeight():
    columns = 80 #for windows and others
    if platform.system() == "Linux":
        columns = os.popen('stty size', 'r').read().split()[1]
    return int(columns)
    
def getLoadingBar(ln, percent=100, bracket="[]", fillch="#", emptych="-"):
    sumln = ln-2 #2 brackets
    filled = int(percent*sumln/100)
    bar = "%s%s%s%s" % (bracket[0], fillch*filled, emptych*(sumln-filled), bracket[1])
    return bar

def getNewPath(url, name=None, directory=None):
    if directory==None: directory=os.curdir
    if not os.path.exists(directory): os.makedirs(directory)
    if name==None:
        path="%s%s%s" % (
            directory,
            os.sep,
            url.split("/")[-1])
    else:
        path="%s%s%s" % (
            directory,
            os.sep,
            name)
    return path

def downloadfile(url, newName=None, dir=None):
    newPath = getNewPath(url, newName, dir)
    
    if not os.path.exists(newPath):
        localLen = 0
    else:
        localLen = os.path.getsize(newPath)
        
    req = urllib2.Request(url)
    req.headers['Range'] = 'bytes='+str(localLen)+'-'
    
    print "Sending request..."
    remoteLen = 0
    try:
        res = urllib2.urlopen(url)
        remoteLen = int(res.info().getheader("Content-Length"))
    except urllib2.HTTPError, e:
        print e
        return
    except urllib2.URLError, e:
        print e
        return
        
    print "Received code:", res.getcode()

    print "Length: %d (%.02fM) [%s]" % (
        remoteLen,
        remoteLen/1024.0/1024.0,
        res.info().getheader("Content-Type"))
    
    print "Saving to:", newPath
        
    if localLen == 0:
        localFile = open(newPath, "wb")
        isNewDownload = True
    elif localLen < remoteLen:
        localFile = open(newPath, "ab")
        isNewDownload = False
    elif localLen >= remoteLen:
        print "File has downloaded already.\n"
        return

    try:
        remoteFile = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e
        return
    except urllib2.URLError, e:
        print e
        return
        
    cols = getConsoleWeight()
    if isNewDownload: print "Downloading: %s" % (remoteFile.url)
    else: print "Continue downloading: %s" % (remoteFile.url)
    if remoteLen == 0: raise urllib2.HTTPError("Content-Length is 0")
    remoteLen = float(remoteLen)
    bytesRead = float(localLen)
    for line in remoteFile:
        bytesRead += len(line)
        percent = 100*bytesRead/remoteLen
        curInfo = "\rProgress: %.02f/%.02f kb (%d%%)" % (
            bytesRead/1024.0,
            remoteLen/1024.0,
            percent)
        loadbar = getLoadingBar(cols-len(curInfo), percent)
        curInfo = curInfo[:11] + loadbar + curInfo[10:]
        sys.stdout.write(curInfo)
        sys.stdout.flush()
        localFile.write(line)
    remoteFile.close()
    localFile.close()
    print "\nFile [%s] has been downloaded.\n" % newPath
