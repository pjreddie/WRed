import ctypes
import numpy as N
# Defined ctypes
from ctypes import c_void_p, c_int, c_long, c_char, c_char_p,c_double
from ctypes import byref as _ref
c_void_pp = ctypes.POINTER(c_void_p)
c_int_p = ctypes.POINTER(c_int)
c_double_p=ctypes.POINTER(c_double)


#def convert_array(arr):
#    arr


class fiduc(ctypes.Structure):
    _fields_=[("Y",c_void_pp),
            ("Z",c_void_pp)]
#slab_offset.ctypes.data_as(c_int_p) 
pt=fiduc()
zdata=N.zeros((4,4),dtype='float64')
ydata=N.ones((4,4),dtype='float64')
pt.Y=ydata.ctypes.data_as(c_void_pp)
pt.Z=zdata.ctypes.data_as(c_void_pp)




#lib=ctypes.cdll['pb.dll']
#lib.correct(ctypes.byref(pt))  #by reference
#lib.correct((pt)) #actually will change value in c code

foo = N.ctypeslib.load_library('pb.dll', '.')
foo.correct(pt.Y,pt.Z)
s=''
print zdata

#x = N.array([[10,20,30], [40,50,60], [80,90,100]], 'f4')
#f4ptr = POINTER(c_float)
#data = (f4ptr*len(x))(*[row.ctypes.data_as(f4ptr) for row in x])