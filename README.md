#### pyfileget v0.2dev - simple console download module
**Language:** Python

**Features:** continue downloading, statusbar, speedmetre, safe(local files will not be overwritten)

**Description:** Simple file download module for using in your scripts with console output. Pyfileget uses only standart python2 libs(urllib and urllib2 for connections and downloading). 

**Usage:**

    from pyfileget import download
    path = "path/to/save"
    download("http://mirror.yandex.ru/ubuntu-releases/13.10/ubuntu-13.10-desktop-i386.iso", path)
Where `path` may be path to folder or file, if `path` is empty file will be saved to the current working directory. If localfile exists then downloading will be aborting.

**Notice:** I dont give a shit how it works on Windows. I even didnt try this.

**Author:** Dmitriy Kalinin (dem.mort@gmail.com)

