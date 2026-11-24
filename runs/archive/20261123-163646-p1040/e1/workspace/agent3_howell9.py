"""Exact module generators and cardinality over Z/9, dense Sage BLAS.
No saturation or division by nonunits is assumed.
"""
from sage.all import *
import numpy as np,gc,time
_fun,_args=matrix(GF(3),[[1]]).__reduce__()
def fastmat(A,p=3):
 a=list(_args);a[1]=MatrixSpace(Integers(p),*A.shape);a[4]=(1,True,A.astype(np.uint8,copy=False).tobytes());return _fun(*a)
def tonumpy(M):return np.frombuffer(M.__reduce__()[1][4][2],dtype=np.uint8).reshape(M.nrows(),M.ncols())
def module9(A,verbose=True):
 t=time.time();A=np.asarray(A,dtype=np.uint8)%9
 P=fastmat(A%3);PT=P.transpose();rows=list(PT.pivots());del PT
 cols=list(P.pivots());r=len(cols);del P;gc.collect()
 if verbose:print('module9 mod3rank',r,'elapsed',time.time()-t,flush=True)
 if not r:
  assert not (A%3).any();E=fastmat(A//3);E.echelonize();s=E.rank();B=3*tonumpy(E[:s,:]);return B,(0,s)
 C=A[rows,:];U=C[:,cols]
 V=fastmat(U%3).inverse();V9=fastmat(tonumpy(V),9);del V
 U9=fastmat(U,9)
 V9=V9*(2*identity_matrix(Integers(9),r)-U9*V9);del U9
 C9=V9*fastmat(C,9);del V9,C,U;gc.collect()
 assert C9.matrix_from_columns(cols)==identity_matrix(Integers(9),r)
 if verbose:print('module9 normalized','elapsed',time.time()-t,flush=True)
 R9=fastmat(A,9)-fastmat(A[:,cols],9)*C9;del A;gc.collect()
 RR=tonumpy(R9);assert not (RR%3).any()
 E=fastmat(RR//3);del R9,RR;gc.collect()
 E.echelonize();s=E.rank();Earr=tonumpy(E[:s,:]);del E
 B=np.vstack((tonumpy(C9),3*Earr)).astype(np.uint8);del C9;gc.collect()
 if verbose:print('module9 ranks',r,s,'log3size',2*r+s,'elapsed',time.time()-t,flush=True)
 return B,(r,s)
