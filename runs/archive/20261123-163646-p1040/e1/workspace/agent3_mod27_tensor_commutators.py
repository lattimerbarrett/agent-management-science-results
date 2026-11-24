"""Exact F3 commutator corrections for F in A3, truncation wordlength8.
Input f displacement output-major degrees4..8; Lg is action g^-1 F g linear part.
Returns [F,g^-1] displacement in degrees5..8 (a true gamma4 element).
"""
import numpy as np

def quad_g(f4,index):
 # generator ordering K(i,j) jascending followed C(i;j,k), i=0,1,2.
 i=index//3;t=index%3;others=[j for j in range(3) if j!=i]
 if t<2:
  j=others[t];a,b=f4[j],f4[i]
 else:
  j,k=others;a,b=f4[j],f4[k]
 Q=np.zeros((3,6561),dtype=np.int16)
 Q[i]=(np.outer(a,b)-np.outer(b,a)).reshape(-1)%27
 return Q

def directional_5_on_4(direction5,f4):
 # derivative direction applied to f4, homogeneous wordlength8
 out=np.zeros((3,6561),dtype=np.int16)
 for i in range(3):
  H=f4[i].reshape((3,)*4)
  for pos in range(4):
   for j in range(3):
    h=np.take(H,j,axis=pos)
    v=direction5[j].reshape((3,)*5)
    C=np.tensordot(h,v,axes=0)
    perm=list(range(pos))+list(range(3,8))+list(range(pos,3))
    out[i]+=C.transpose(perm).reshape(-1)
 return out%27

def commutator_seed(f,linear_h,index):
 f=f.reshape(3,9801).astype(np.int16)
 h=linear_h.reshape(3,9801).astype(np.int16).copy()%27
 f4=f[:,:81]
 h[:,-6561:]=(h[:,-6561:]+quad_g(f4,index))%27
 direction5=(h[:,81:324]-f[:,81:324])%27
 corr=directional_5_on_4(direction5,f4)
 out=(f-h)%27
 out[:,-6561:]=(out[:,-6561:]+corr)%27
 assert not out[:,:81].any()
 return out[:,81:].astype(np.int8)
