#!/usr/bin/python
# -*- coding: utf-8 -*- 

import os,sys,urllib2,platform,time
from pynetspeed import NetSpeed
from downloaderror import DownloadError

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

def display_download_info(bytesRead=1, remoteLen=1, speed="", conWidth=80):
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

def download(remoteFile, localFile, remoteLen, bytesReaded):
    cols = get_console_width()
    speed = NetSpeed(bytesReaded)
    print "Downloading:", remoteFile.url
    try:
        for line in remoteFile:
            bytesReaded += len(line)
            display_download_info(bytesReaded, remoteLen, speed.get_speed(bytesReaded), cols)
            localFile.write(line)
    except (OSError, urllib2.HTTPError, urllib2.URLError), e:
        raise DownloadError(systemErrorValue=e)
    finally:
        remoteFile.close()
        localFile.close()

def get_remote_file_info(url):
    try:
        reply = urllib2.urlopen(url)
        fileLen = int(reply.info().getheader("Content-Length"))
        code = reply.getcode()
        fileType = reply.info().getheader("Content-Type")
    except (urllib2.HTTPError, urllib2.URLError, ValueError), e:
        raise DownloadError("", e)
    except TypeError:
        #TODO: make ability to download web pages (they have None in Length)
        raise DownloadError("Content-Length is None.")
    return fileLen, code, fileType

def get_local_file_length(path):
    currentDlPath = path+DL_EXT
    if os.path.exists(currentDlPath):
        return int(os.path.getsize(currentDlPath))
    else:
        return 0
    
def get_remote_file_handler(url, bytesOffset=0):
    req = urllib2.Request(url)
    req.headers['Range'] = 'bytes='+str(bytesOffset)+'-'
    try:
        fileObj = urllib2.urlopen(req)
    except (urllib2.HTTPError, urllib2.URLError), e:
        raise DownloadError("Cant open remote file", e)
    return fileObj
        
def get_local_file_handler(path):
    try:
        fileObj = open(path+DL_EXT, "ab")    
    except (IOError, OSError), e:
        raise DownloadError("Cant open local file:"+path+DL_ext,e)
    return fileObj

def download_file(url, localpath=None):
    #requesting file and getting info of remote file
    print "Sending request..."
    remoteLen, returnCode, remoteType = get_remote_file_info(url)
    #print info
    print "Received code:", returnCode
    print "Length: %d (%.02fM) [%s]" % (remoteLen, remoteLen/1024.0/1024.0, remoteType)
    #getting local path
    newPath = get_new_path(url, localpath)
    print "Saving to:", newPath
    if os.path.exists(newPath):
        raise DownloadError("File %s exists." % newPath)
    localLen = get_local_file_length(newPath)
    if localLen == remoteLen:
        rename_downloaded(newPath)
        raise DownloadError("File %s has downloaded already." % newPath)
    download(get_remote_file_handler(url, localLen),
             get_local_file_handler(newPath),
             float(remoteLen), float(localLen))
    rename_downloaded(newPath)
    return newPath

def pyget(url, localpath):
    try:
        newPath = download_file(url, localpath)
    except DownloadError, e:
        print e, "Download aborted.\n"
    else:
        print "\nFile [%s] has been downloaded.\n" % newPath
