#!/usr/bin/python
# -*- coding: utf-8 -*- 

import os,sys,urllib2,platform,time
from pynetspeed import NetSpeed

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

def download(remoteFile, localFile, bytesReaded, remoteLen):
    #TODO: add try except
    cols = get_console_width()
    speed = NetSpeed(bytesReaded)
    try:
        for line in remoteFile:
            bytesReaded += len(line)
            display_download_info(bytesReaded, remoteLen, speed.get_speed(bytesReaded), cols)
            localFile.write(line)
    finally:
        remoteFile.close()
        localFile.close()
    rename_downloaded(newPath) 

def get_remote_file_info(url):
    try:
        reply = urllib2.urlopen(url)
        fileLen = int(reply.info().getheader("Content-Length"))
        code = reply.getcode()
        fileType = reply.info().getheader("Content-Type")
    except (urllib2.HTTPError, urllib2.URLError), e:
        print e
        print "Download aborted.\n"
        return None
    except TypeError:
        #TODO: make ability to download web pages (they have None in Length)
        print "Content-Length is None. Nothing to download.\n"
        return None
    return fileLen, code, fileType

def get_local_file_length(path):
    currentDlPath = path+DL_EXT
    if os.path.exists(currentDlPath):
        return int(os.path.getsize(currentDlPath))
    else:
        return 0
    
def get_remote_file_handle(url, bytesOffset=0):
    req = urllib2.Request(url)
    req.headers['Range'] = 'bytes='+str(bytesOffset)+'-'
    try:
        fileObj = urllib2.urlopen(req)
    except (urllib2.HTTPError, urllib2.URLError), e:
        print e
        return None
    return fileObj
        
def get_local_file_handle(path):
    try:
        fileObj = open(path+DL_EXT, "ab")    
    except (IOError, OSError), e:
        print e
        print "Download aborted.\n"
        return None
    return fileObj

def download_file(url, localpath=None):
    #requesting file and getting info of remote file
    print "Sending request..."
    remoteLen, returnCode, remoteType = get_remote_file_info(url)
    if not remoteLen: return
    #print info
    print "Received code:", returnCode
    print "Length: %d (%.02fM) [%s]" % (
        remoteLen,
        remoteLen/1024.0/1024.0,
        remoteType)
    #getting local path
    newPath = get_new_path(url, localpath)
    print "Saving to:", newPath
    if os.path.exists(newPath):
        print "File exists. Download aborted.\n"
        return
    localLen = get_local_file_length(newPath)
    if localLen == remoteLen:
        print "File has downloaded already.\n"
        rename_downloaded(newPath)
        return
    #getting local file handle
    localFile = get_local_file_handle(newPath)
    if not localFile: return
    #getting remote file handle
    remoteFile = get_remote_file_handle(url, localLen)
    if not remoteFile: return
    #downloading
    print "Downloading:", remoteFile.url
    download(remoteFile, localFile, float(localLen), float(remoteLen))
    print "\nFile [%s] has been downloaded.\n" % newPath
    return
