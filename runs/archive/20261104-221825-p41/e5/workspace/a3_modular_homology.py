"""Exact modular reduced homology, with explicit cycle/cochain witnesses."""
import numpy as np

def rref(A,p):
 A=np.array(A,dtype=np.int64,copy=True)%p;m,n=A.shape;r=0;piv=[]
 for j in range(n):
  ii=np.flatnonzero(A[r:,j])
  if not len(ii):continue
  i=r+int(ii[0]);A[[i,r]]=A[[r,i]];A[r]=A[r]*pow(int(A[r,j]),-1,p)%p
  ii=np.flatnonzero(A[:,j]);ii=ii[ii!=r]
  A[ii]=(A[ii]-A[ii,j,None]*A[r])%p
  piv.append(j);r+=1
  if r==m:break
 return A,piv

def kernel(A,p):
 R,pp=rref(A,p);n=A.shape[1];free=[j for j in range(n) if j not in pp]
 Z=np.zeros((n,len(free)),dtype=np.int64)
 for k,j in enumerate(free):
  Z[j,k]=1
  for i,v in enumerate(pp):Z[v,k]=-R[i,j]%p
 assert not np.any((A@Z)%p)
 return Z

def boundary(lower,higher):
 ix={g:i for i,g in enumerate(lower)};A=np.zeros((len(lower),len(higher)),dtype=np.int64)
 for j,g in enumerate(higher):
  vv=[v for v in range(g.bit_length()) if g>>v&1]
  for k,v in enumerate(vv):A[ix[g^(1<<v)],j]=(-1)**k
 return A

def witness(C,i,p):
 """Returns cycle z and cochain u dicts with <u,z>!=0, or None."""
 cells=sorted(g for g in C if g.bit_count()==i+1)
 low=sorted(g for g in C if g.bit_count()==i)
 high=sorted(g for g in C if g.bit_count()==i+2)
 A=boundary(low,cells);B=boundary(cells,high)
 assert not np.any(A@B)
 Z=kernel(A,p);U=kernel(B.T,p)
 pairing=(U.T@Z)%p
 nz=np.argwhere(pairing)
 if not len(nz):return None
 a,b=map(int,nz[0]);z=Z[:,b];u=U[:,a]
 assert not np.any(A@z%p) and not np.any(B.T@u%p) and int(u@z)%p
 return ({g:int(z[k]) for k,g in enumerate(cells) if z[k]}, {g:int(u[k]) for k,g in enumerate(cells) if u[k]})
