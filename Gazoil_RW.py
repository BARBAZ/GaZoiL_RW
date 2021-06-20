
##### Chunk Parsers #####

def matrix(fobj):
    mtx = struct.unpack('<16f', fobj.read(64))
    matrix = om.MMatrix((
        mtx[0] , mtx[1] , mtx[2] , mtx[3] ,
        mtx[4] , mtx[5] , mtx[6] , mtx[7] ,
        mtx[8] , mtx[9] , mtx[10], mtx[11],
        mtx[12], mtx[13], mtx[14], mtx[15]
    ))

    return matrix

def positions(fobj):
    positions = []
    positions = struct.unpack("<I", fobj.read(4))[0]

    for i in range(positions):
        x , y , z = struct.unpack("<3f", fobj.read(12))

    return positions

def normals(fobj):
    normals = []
    normals = struct.unpack("<I", fobj.read(4))[0]
    
    for i in range(normals):
        nx , ny , nz = struct.unpack("<3f", fobj.read(12))

    return normals

def textcoords(fobj):
    textcoords = []
    textcoords = struct.unpack("<I", fobj.read(4))[0]
    
    for i in range(textcoords):
        tx , ty , tz = struct.unpack("<3f", fobj.read(12))
    
    return textcoords

def faces(fobj):
    faces = []
    faces = struct.unpack("<I", fobj.read(4))[0]

    if(faces):
        seek(8, fobj)
        for i in range(faces):
            faces_idx = struct.unpack("<I", fobj.read(4))[0]
            for j in range(faces_idx):
                faces_ord, textcoords = struct.unpack("<2H", fobj.read(4))
                seek(8, fobj)
            seek(2, fobj)

def faces14(fobj):
    faces = []
    faces = struct.unpack("<I", fobj.read(4))[0]

    if(faces):
        seek(8, fobj)
        for i in range(faces):
            faces_idx = struct.unpack("<I", fobj.read(4))[0]
            for j in range(faces_idx):
                faces_ord, textcoords = struct.unpack("<2H", fobj.read(4))
                seek(10, fobj)
            seek(2, fobj)

def binds(fobj):
    binds = []
    binds = struct.unpack("<I", fobj.read(4))[0]
    
    for i in range(binds):
        influences = struct.unpack("<I", fobj.read(4))[0]
        for j in range(influences):
            seek(2, fobj)
            bone = struct.unpack("<H", fobj.read(2))[0] # bone idx
            weight = struct.unpack("f", fobj.read(4))   # bone to vtx weight

def vertex(fobj):
    vertex = []
    vertex = struct.unpack("<I", fobj.read(4))[0]

    for i in range(vertex):
        vtx_idx = 0
        nrm_idx = 0
        txt_idx = 0
        vtx_idx, nrm_idx, txt_idx = struct.unpack('<3H', fobj.read(6))
        seek(6, fobj)

def vertex14(fobj):
    vertex = []
    vertex = struct.unpack("<I", fobj.read(4))[0]

    for i in range(vertex):
        vtx_idx = 0
        nrm_idx = 0
        txt_idx = 0
        vtx_idx, nrm_idx, txt_idx = struct.unpack('<3H', fobj.read(6))
        seek(8, fobj)

def face(fobj):
    face = []
    face = struct.unpack("<I", fobj.read(4))[0]

    for i in range(face):
        seek(2, fobj)    



##### Parsing Routines #####

def seek(size, fobj):
    fobj.seek(size, os.SEEK_CUR)

def ukn12(fobj):
    ukn_cnt = struct.unpack("<I", fobj.read(4))[0]
    for i in range(ukn_cnt):
        seek(12, fobj)

def ukn16(fobj):
    ukn_cnt = struct.unpack("<I", fobj.read(4))[0]
    for i in range(ukn_cnt):
        seek(16, fobj)

def ukn64(fobj):
    ukn_cnt = struct.unpack("<I", fobj.read(4))[0]
    for i in range(ukn_cnt):
        seek(64, fobj)
    for i in range(ukn_cnt):
        seek(2, fobj)

##### Objects Parsers #####

def import_5011(fobj): # functional for parsing
    seek(8, fobj)
    matrix(fobj)
    seek(4, fobj)
    positions(fobj)
    normals(fobj)
    ukn16(fobj)
    ukn12(fobj)
    textcoords(fobj)
    ukn12(fobj)
    faces(fobj)
    ukn12(fobj)
    seek(4, fobj)
    binds(fobj)
    ukn64(fobj)
    vertex(fobj)
    seek(4, fobj)
    face(fobj)
    ukn12(fobj)
    seek(24, fobj)

def import_5012(fobj):
    seek(8, fobj)
    matrix(fobj)
    seek(8, fobj)
    positions(fobj)
    normals(fobj)
    ukn16(fobj)
    ukn12(fobj)
    textcoords(fobj)
    ukn12(fobj)
    faces(fobj)
    ukn12(fobj)
    seek(4, fobj)
    binds(fobj)
    ukn64(fobj)
    vertex(fobj)
    seek(4, fobj)
    face(fobj)
    ukn12(fobj)
    seek(24, fobj)

def import_5013(fobj):
    matrix(fobj)
    seek(16, fobj)
    positions(fobj)
    textcoords(fobj)
    ukn12(fobj)
    normals(fobj)
    ukn16(fobj)
    ukn12(fobj)
    faces(fobj)
    ukn12(fobj)
    seek(4, fobj)
    binds(fobj)
    seek(4, fobj)
    vertex(fobj)
    ukn64(fobj)
    ukn12(fobj)
    face(fobj)
    seek(24, fobj) 

def import_5014(fobj):
    matrix(fobj)
    seek(16, fobj)
    positions(fobj)
    seek(2, fobj)
    textcoords(fobj)
    ukn12(fobj)
    ukn12(fobj)
    normals(fobj)
    ukn16(fobj)
    ukn12(fobj)
    faces14(fobj)
    ukn12(fobj)
    seek(4, fobj)
    binds(fobj)
    seek(4, fobj)
    vertex14(fobj)
    ukn64(fobj)
    ukn12(fobj)
    face(fobj)
    seek(24, fobj)

#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################





#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################

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
err = "Internal error ! Contact admin"
eluversion = "Elu Version : %s"
objectstr = "Object : %s"
curpos = 'Done ! file curpos at %x'
comperr = "no support for this version of elu format yet !"

# Arrays

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
    namelen = struct.unpack("<I", fobj.read(4))[0]
    name = fobj.read(namelen)
    print(objectstr % (str(name)))
    parentlen = struct.unpack("<I", fobj.read(4))[0]
    parent = fobj.read(parentlen)
    parentidx = struct.unpack("<I", fobj.read(4))[0]
    return name, parent, parentidx

def meta1(fobj):
    namelen = struct.unpack("<I", fobj.read(4))[0]
    name = fobj.read(namelen)
    print(objectstr % (str(name)))
    parentidx = struct.unpack("<I", fobj.read(4))[0]
    parentlen = struct.unpack("<I", fobj.read(4))[0]
    parent = fobj.read(parentlen)
    return name, parent, parentidx

########################################################################

print(title)
elu = openfile()
headerargs = header(elu)

for i in range(headerargs[1]):
    if(headerargs[0] == "0x5011"):
        meta0(elu)
        import_5011(elu)
    elif(headerargs[0] == "0x5012"):
        meta0(elu)
        import_5012(elu)
    elif(headerargs[0] == "0x5013"):
        meta1(elu)
        import_5013(elu)
    elif(headerargs[0] == "0x5014"):
        meta1(elu)
        import_5014(elu)
    else:
        print(err)

print("EOF")
print("EOS")
elu.close()

########################################################################