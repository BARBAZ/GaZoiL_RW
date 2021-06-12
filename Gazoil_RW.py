
###### Python Builtin modules #####

import io
import os
import sys
import struct


##### Autodesk Maya's API Modules #####

import maya.cmds as cmds
import maya.api.OpenMaya as om

# Strings

ffilters = "RS3 Models Files (*.elu) ;; All Files (*.*)"
title = "\n\t\t\t\t\t\t##### GaZoiL #####\n"
exterr = "Incorrect or corrupted file format ! Please select a correct .elu file \nProgram will stop !"
eluversion = "Elu Version : %s"

# Constants

Objects = []

# Functions definitions 

def openfile():
    fullpath = cmds.fileDialog2(fileMode=1, ff=ffilters)
    fullpath = str(fullpath[0])
    cnt = fullpath.count("/")
    splitpath = fullpath.split("/")
    filename = splitpath[cnt]
    realpath = fullpath.replace(filename,"")
    os.chdir(realpath)
    file_object = io.open(filename,'r+b')
    print ("Opening file : %s \nFrom : %s " % (filename, realpath))
    return file_object

def header(fobj):
    magic = struct.unpack("<I", fobj.read(4))[0]
    if(magic != 17297504):
        print(exterr)
        sys.exit()
    version = hex(struct.unpack("<I", fobj.read(4))[0])
    print(eluversion % (version))
    fobj.seek(4, os.SEEK_CUR)
    objcount = struct.unpack("<I", fobj.read(4))[0]
    return version, objcount 

def meta0(fobj):
    print "meta0 init"
    namelen = struct.unpack("<I", fobj.read(4))[0]
    name = fobj.read(namelen)
    parentlen = struct.unpack("<I", fobj.read(4))[0]
    parent = fobj.read(parentlen)
    parentidx = struct.unpack("<I", fobj.read(4))[0]
    return name, parent, parentidx

def meta1(fobj):
    print "meta1 init"
    namelen = struct.unpack("<I", fobj.read(4))[0]
    name = fobj.read(namelen)
    parentidx = struct.unpack("<I", fobj.read(4))[0]
    parentlen = struct.unpack("<I", fobj.read(4))[0]
    parent = fobj.read(parentlen) 
    return name, parent, parentidx

###############################################################################

print(title)
elu = openfile()
headerargs = header(elu)

if(headerargs[0] == "0x5011" or headerargs[0] == "0x5012"):
    metaargs = meta0(elu)
else:
    metaargs = meta1(elu)

elu.close()

###############################################################################