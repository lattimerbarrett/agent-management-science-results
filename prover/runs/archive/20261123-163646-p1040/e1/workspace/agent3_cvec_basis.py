"""Memory-efficient exact F3 rowspace via GAP CVEC (3 bits/coefficient).
NumPy exchange uses portable CVEC external packed32-bit words, 10coeffs/word.
Binary IO uses GAP IO_Write, not PrintTo (which strips NULs).
"""
from sage.all import *
from sage.libs.gap.libgap import libgap
import numpy as np
libgap.eval('LoadPackage("cvec",false:OnlyNeeded:=true)')
libgap.eval('LoadPackage("io",false:OnlyNeeded:=true)')
EXPORT=libgap.eval('''function(B,filename) local f,v,s; f:=IO_File(filename,"w"); for v in B!.vectors do s:=""; CVEC_CVEC_TO_EXTREP(v,s); IO_Write(f,s); od; IO_Close(f); return B!.pivots;end''')
INFO=libgap.eval('function(B)return [Length(B!.vectors),B!.pivots];end')
ESCAPES=['\\%03o'%b for b in range(256)]
class CVecBasis:
 def __init__(self,n):
  self.n=n;self.cl=libgap.CVecClass(3,1,n)
  self.basis=libgap.EmptySemiEchelonBasis(libgap.CMat([],self.cl))
 def insert(self,row):
  a=np.asarray(row,dtype=np.uint32)%3
  if len(a)!=self.n:raise ValueError('wrong length')
  a=np.pad(a,(0,(-len(a))%10))
  packed=(a.reshape(-1,10)<<np.arange(0,30,3,dtype=np.uint32)).sum(axis=1,dtype=np.uint32).astype('<u4').tobytes()
  s=libgap.eval('"'+''.join(ESCAPES[b] for b in packed)+'"')
  v=libgap.CVec(self.cl);libgap.CVEC_EXTREP_TO_CVEC(s,v)
  return not bool(libgap.CleanRow(self.basis,v,True,libgap.fail))
 def info(self):return INFO(self.basis).sage()
 def export(self,filename):
  piv=EXPORT(self.basis,filename).sage();return piv
 def numpy(self,filename):
  piv=self.export(filename);raw=np.fromfile(filename,dtype='<u4').reshape(len(piv),-1)
  A=((raw[:,:,None]>>np.arange(0,30,3,dtype=np.uint32))&7).astype(np.uint8).reshape(len(piv),-1)[:,:self.n]
  assert np.all(A<3)
  return A,piv
