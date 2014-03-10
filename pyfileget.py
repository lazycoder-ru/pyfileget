# -*- coding: utf-8 -*- 

import os,sys,urllib,urllib2,time
from lib import NetSpeed, DownloadError

DL_EXT = ".pyflget"

#returns width of current console
def get_console_width():
    try:
        columns = int(os.popen('stty size', 'r').read().split()[1])
    except:
        columns = 40 #for windows and others
    return columns

#returns loading bar
def get_loading_bar(totalLen, percent=100, bracket="[]", fillch="#", emptych="-"):
    barLen = totalLen-2 #2 brackets
    filled = int(percent*barLen/100)
    return "%s%s%s%s" % (bracket[0], fillch*filled, emptych*(barLen-filled), bracket[1])

#get resulting local path
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
            raise DownloadError("Cant create folder(s).",e)
    return "%s%s%s" % (folderpath, os.sep, filename)

#renames downloaded file by removing .pyflget extension
def rename_downloaded(path):
    if os.path.exists(path): raise DownloadError("File %s exists." % path)    
    try:
        os.rename(path+DL_EXT, urllib.unquote(path))
    except (IOError, OSError), e:
        raise DownloadError("Error while renaming file.", e)

def display_download_info(passed=1, total=1, speed="", conWidth=80):
    #TODO: make templated output
    percent = 100*passed/total
    curInfo = "\rProgress: %.02f/%.02f KB (%d%%) %s" % (
        passed/1024.0,
        total/1024.0,
        percent,
        speed)
    loadbar = get_loading_bar(conWidth-len(curInfo), percent)
    curInfo = curInfo[:11] + loadbar + curInfo[10:] #after progress
    sys.stdout.write(curInfo)
    sys.stdout.flush()    

def download_process(remoteFile, localFile, remoteLen, bytesReaded):
    cols = get_console_width()
    speed = NetSpeed(bytesReaded)
    try:
        for line in remoteFile:
            bytesReaded += len(line)
            display_download_info(bytesReaded, remoteLen, speed.get_speed(bytesReaded), cols)
            localFile.write(line)
    except (OSError, urllib2.HTTPError, urllib2.URLError), e:
        raise DownloadError(sysErrorValue=e)
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
    if os.path.exists(path): raise DownloadError("File %s exists." % path)
    #TODO: actions for renaming downloading file or something
    if os.path.exists(path+DL_EXT): return os.path.getsize(path+DL_EXT)
    return 0
    
def get_remote_file_handle(url, bytesOffset=0):
    req = urllib2.Request(url)
    req.headers['Range'] = 'bytes='+str(bytesOffset)+'-'
    try:
        fileObj = urllib2.urlopen(req)
    except (urllib2.HTTPError, urllib2.URLError), e:
        raise DownloadError("Cant open remote file:"+fileObj.url, e)
    return fileObj
        
def get_local_file_handle(path):
    try:
        fileObj = open(path+DL_EXT, "ab")    
    except (IOError, OSError), e:
        raise DownloadError("Cant open local file:"+path+DL_ext,e)
    return fileObj

def download(url, localpath=None):
    #requesting file and getting info of remote file
    print "Sending request..."
    remoteLen, returnCode, remoteType = get_remote_file_info(url)
    #print info
    print "Received code:", returnCode
    print "Length: %d (%.02fM) [%s]" % (remoteLen, remoteLen/1024.0/1024.0, remoteType)
    #getting local path
    newPath = get_new_path(url, localpath)
    print "Saving to:", newPath
    #getting length of localfile
    localLen = get_local_file_length(newPath)
    if localLen == remoteLen:
        rename_downloaded(newPath)
        raise DownloadError("File %s has downloaded already." % newPath)
    print "Downloading:", url #maybe need to use remoteFile.url
    #actual process itself
    download_process(get_remote_file_handle(url, localLen),
        get_local_file_handle(newPath), float(remoteLen), float(localLen))
    rename_downloaded(newPath)
    return newPath