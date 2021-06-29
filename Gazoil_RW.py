
##### Chunk Parsers #####

def matrix(fobj):
    mtx = struct.unpack('<16f', fobj.read(64))
    MMatrix = om.MMatrix((
        mtx[0] , mtx[1] , mtx[2] , mtx[3] ,
        mtx[4] , mtx[5] , mtx[6] , mtx[7] ,
        mtx[8] , mtx[9] , mtx[10], mtx[11],
        mtx[12], mtx[13], mtx[14], mtx[15]
    ))

    objects[-1][mat].append(MMatrix)

def positions(fobj):
    MPositions = om.MPointArray()
    positions = struct.unpack("<I", fobj.read(4))[0]

    for i in range(positions):
        x , y , z = struct.unpack("<3f", fobj.read(12))
        MPositions.append((x , y , z))

    objects[-1][pos].append(MPositions)

def normals(fobj):
    MNormals = om.MVectorArray()
    normals = struct.unpack("<I", fobj.read(4))[0]
    
    for i in range(normals):
        nx , ny , nz = struct.unpack("<3f", fobj.read(12))
        MNormals.append(( nx , ny , nz ))

    objects[-1][nor].append(MNormals)

def textcoords(fobj):
    MTextcoords = om.MFloatArray()
    textcoords = struct.unpack("<I", fobj.read(4))[0]
    iter = textcoords * 3

    for i in range(iter):    
        MTextcoords.append(struct.unpack("f", fobj.read(4))[0])
       
    objects[-1][txt].append(MTextcoords)

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
    objects[-1][nam].append(str(name))
    objects[-1][par].append(str(parent))
    objects[-1][pidx].append(parentidx)

def meta1(fobj):
    namelen = struct.unpack("<I", fobj.read(4))[0]
    name = fobj.read(namelen)
    print(objectstr % (str(name)))
    parentidx = struct.unpack("<I", fobj.read(4))[0]
    parentlen = struct.unpack("<I", fobj.read(4))[0]
    parent = fobj.read(parentlen)
    objects[-1][nam].append(str(name))
    objects[-1][par].append(str(parent))
    objects[-1][pidx].append(parentidx)


##### Parsing Jumps #####

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

###### Standards modules #####

import io
import os
import sys
import struct
from enum import IntEnum

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

objects = []

##### Classes #####

class Array:

    def config(self):
        self.append([])
        for j in range(len(List)):
            self[-1].append([])

    def extend(self):
        print("extending array")
        self.append([])
        for j in range(len(List)):
            self[-1].append([])

    def log(self):
        print("logging array")
        for j in range(len(self)):
            print(self[j])

# Enums

class Index(IntEnum): ## Same name on arrays => 2nd funcdecl overwrites the 1st => 

    name = 0
    parent = 1
    parentidx = 2
    matrix = 3
    positions = 4
    normals = 5
    tangents = 6
    textcoords = 7
    textcoords2 = 8
    vertexindices = 9
    facesindices = 10
    blendvertices = 11
    
    
# Aliases

nam  = Index.name
par  = Index.parent
pidx = Index.parentidx 
mat  = Index.matrix
pos  = Index.positions
nor  = Index.normals
tan  = Index.tangents
txt  = Index.textcoords
txt2 = Index.textcoords2
vind = Index.vertexindices
find = Index.facesindices
bvtx = Index.blendvertices


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

########################################################################
##### code instructions #####

print(title)
elu = openfile()
headerargs = header(elu)
Array.config(objects)

for i in range(headerargs[1]):
    if(headerargs[0] == "0x5011"):
        meta0(elu)
        import_5011(elu)
        Array.extend(objects)
    elif(headerargs[0] == "0x5012"):
        meta0(elu)
        import_5012(elu)
        Array.extend(objects)
    elif(headerargs[0] == "0x5013"):
        meta1(elu)
        import_5013(elu)
        Array.extend(objects)
    elif(headerargs[0] == "0x5014"):
        meta1(elu)
        import_5014(elu)
        Array.extend(objects)
    else:
        print(err)

print("EOF")

Array.log(objects)
elu.close()
print("EOS")

########################################################################