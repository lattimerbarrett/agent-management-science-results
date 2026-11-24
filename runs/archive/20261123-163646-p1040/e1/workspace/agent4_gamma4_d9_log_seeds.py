import sys,time,json
import numpy as np
from pathlib import Path
from scipy.sparse import load_npz
sys.path.insert(0,'workspace')
from agent4_tensor_d9_log import deriv,logseed,M
from agent4_gamma3_d9_tensor_seeds import expand
from agent3_magnus import K,C,auto_commutator
f=np.load('workspace/agent4_gamma3_d9_log_seeds.npz')['seeds'].astype(np.int16)
flat=f.reshape(729,-1)
G=[]
for i in range(1,4):
 for j in range(1,4):
  if i!=j:G.append(K(3,i,j))
 other=[j for j in range(1,4) if j!=i];G.append(C(3,i,*other))
si=int(np.where(np.any(flat,axis=1))[0][0]);aa,cc=divmod(si,9);a,b=divmod(aa,9)
A,Ai=G[a];B,Bi=G[b];C0,Ci=G[cc]
AB=auto_commutator(A,Ai,B,Bi);ABi=auto_commutator(B,Bi,A,Ai)
F=auto_commutator(AB,ABi,C0,Ci);Fi=auto_commutator(C0,Ci,AB,ABi)
for k,(g,gi) in enumerate(G):
 t=time.time();N=load_npz(f'workspace/agent4_tensor_d9_N_{k}.npz')
 nf=(N@flat.T).T.reshape(729,3,M)%3
 comm=(-nf-2*(deriv(f,nf)-deriv(nf,f)))%3
 assert not comm[:,:,:81].any()
 out=comm[:,:,81:].astype(np.int8)
 # LiteralAut/freeword check of selectedactualseed, noBCHinferredsign.
 h=auto_commutator(F,Fi,gi,g)
 hf=[]
 for i,w in enumerate(h):
  P=expand(w,d=9,p=3);P[0]-=1;P[i+1]-=1;P%=3
  assert not P[:40].any();hf.append(P[40:])
 check=logseed(np.array(hf)[None,:,:])[0,:,81:]
 assert np.array_equal(check,out[si]),(k,si)
 np.savez_compressed(f'workspace/agent4_gamma4_d9_log_seeds_{k}.npz',seeds=out)
 print('saved generator',k,'nonzero',np.any(out,axis=(1,2)).sum(),'seconds',round(time.time()-t,2),flush=True)
