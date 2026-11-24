from sage.all import *
import numpy as np,gc,time
from agent3_howell9 import fastmat,tonumpy,module9

def normalize27(C,cols=None):
 if cols is None:cols=list(fastmat(C%3).pivots())
 r=len(C);assert len(cols)==r
 U=C[:,cols];V=fastmat(U%3).inverse();V27=fastmat(tonumpy(V),27);del V
 U27=fastmat(U,27);I=identity_matrix(Integers(27),r)
 for _ in range(2):V27=V27*(2*I-U27*V27)
 C27=V27*fastmat(C,27)
 assert C27.matrix_from_columns(cols)==I
 return tonumpy(C27),cols

def module27(A,verbose=True):
 t=time.time();A=np.asarray(A,dtype=np.uint8)%27
 P=fastmat(A%3);PT=P.transpose();rows=list(PT.pivots());del PT
 cols=list(P.pivots());r=len(cols);del P;gc.collect()
 if verbose:print('module27 mod3rank',r,'elapsed',time.time()-t,flush=True)
 if not r:
  assert not (A%3).any();E,inv=module9(A//3,False);return 3*E,(0,)+inv
 U,cols=normalize27(A[rows,:],cols);U27=fastmat(U,27)
 if verbose:print('module27 normalized','elapsed',time.time()-t,flush=True)
 R27=fastmat(A,27)-fastmat(A[:,cols],27)*U27
 RR=tonumpy(R27);assert not (RR%3).any()
 E,inv=module9(RR//3,False)
 B=np.vstack((U,3*E)).astype(np.uint8)
 if verbose:print('module27 ranks',(r,)+inv,'elapsed',time.time()-t,flush=True)
 return B,(r,)+inv
