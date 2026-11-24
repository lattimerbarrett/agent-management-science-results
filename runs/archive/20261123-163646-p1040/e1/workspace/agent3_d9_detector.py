"""Exact mod3 tensor wordlength9 detector using GAP CVEC rowspaces.
Uses actual gamma4 logarithm seeds and proven class2 logarithm arithmetic.
Queue rows are original independent generators, not reduced basis vectors.
"""
import sys,os,json,time,gc
from pathlib import Path
import numpy as np
from scipy.sparse import load_npz
sys.path.insert(0,'workspace')
from agent3_cvec_basis import CVecBasis,libgap
NCO=88209;CAP=16000;BATCH=128
ix=np.array([i*29484+j for i in range(3) for j in range(81,29484)])
Ns=[load_npz(f'workspace/agent4_tensor_d9_N_{j}.npz')[ix,:][:,ix] for j in range(9)]

def insert(B,Q,n,row):
 if not np.any(row):return n
 if B.insert(row):
  if n>=CAP:raise RuntimeError('queue capacity exceeded')
  Q[n]=row;n+=1
 return n

def finish(Q,n,c):
 Q.flush();del Q
 filename=f'workspace/agent3_d9_gamma{c}_queue.raw'
 with open(filename,'r+b') as f:f.truncate(n*NCO)
 json.dump({'rows':n,'cols':NCO},open(filename+'.json','w'))
 return np.memmap(filename,dtype=np.uint8,mode='r',shape=(n,NCO))

def initqueue(c):
 return np.memmap(f'workspace/agent3_d9_gamma{c}_queue.raw',dtype=np.uint8,mode='w+',shape=(CAP,NCO))

def gamma4():
 t=time.time();B=CVecBasis(NCO);Q=initqueue(4);n=0
 for j in range(9):
  A=np.load(f'workspace/agent4_gamma4_d9_log_seeds_{j}.npz')['seeds'].reshape(729,NCO)
  for row in A:n=insert(B,Q,n,row)
  print('D9 gamma4 seedblock',j,'rank',n,'elapsed',time.time()-t,flush=True)
 del A
 cur=0
 while cur<n:
  end=min(cur+BATCH,n);A=np.array(Q[cur:end])
  for N in Ns:
   C=((N@A.T).T%3).astype(np.uint8)
   for row in C:n=insert(B,Q,n,row)
  cur=end
  if cur%1024==0 or cur==n:print('D9 gamma4 closurequeue',cur,'/',n,'elapsed',time.time()-t,flush=True)
 print('D9 GAMMA4 FINAL',n,'elapsed',time.time()-t,flush=True)
 out=finish(Q,n,4);del B;gc.collect();libgap.GASMAN('collect')
 return out

def nextgamma(A,c):
 t=time.time();B=CVecBasis(NCO);Q=initqueue(c);n=0
 for start in range(0,len(A),BATCH):
  V=np.array(A[start:start+BATCH])
  for N in Ns:
   C=((N@V.T).T%3).astype(np.uint8)
   for row in C:n=insert(B,Q,n,row)
  if start%1024==0:print('D9 gamma',c,'input',start,'rank',n,'elapsed',time.time()-t,flush=True)
 print('D9 GAMMA',c,'FINAL',n,'elapsed',time.time()-t,flush=True)
 out=finish(Q,n,c);del B;gc.collect();libgap.GASMAN('collect')
 return out

def leadingrank(A,c):
 starts=[(3**k-1)//2 for k in range(11)]
 cols=[i*29403+j for i in range(3) for j in range(starts[c+1]-starts[5],starts[c+2]-starts[5])]
 B=CVecBasis(len(cols))
 for start in range(0,len(A),BATCH):
  V=A[start:start+BATCH,cols]
  for row in V:
   if np.any(row):B.insert(row)
 r=B.info()[0];del B;gc.collect();libgap.GASMAN('collect');return r

if __name__=='__main__':
 A=gamma4()
 for c in (5,6,7):
  A=nextgamma(A,c);print('D9 leading rank',c,leadingrank(A,c),flush=True)
