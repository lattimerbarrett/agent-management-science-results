import numpy as np,time
from pathlib import Path
D=9;LO=4
starts={d:sum(3**k for k in range(LO,d)) for d in range(LO,D+2)}
M=starts[D+1]
def deriv(A,B):
 # A,B shape(batch,3,M), output derivative D_A(B), truncated through9.
 A=np.asarray(A,dtype=np.int16);B=np.asarray(B,dtype=np.int16)
 n=len(A);out=np.zeros_like(A,dtype=np.int16)
 for d in range(4,7):
  for i in range(3):
   PP=B[:,i,starts[d]:starts[d+1]]
   if not PP.any():continue
   for pos in range(d):
    P=PP.reshape(n,3**pos,3,3**(d-pos-1))
    for j in range(3):
     R=P[:,:,j,:]
     if not R.any():continue
     for e in range(4,min(6,10-d)+1):
      Q=A[:,j,starts[e]:starts[e+1]]
      if not Q.any():continue
      out[:,i,starts[d+e-1]:starts[d+e]]+=np.einsum('nab,nc->nacb',R,Q,optimize=False).reshape(n,3**(d+e-1))
 return out%3

def logseed(f):return (np.asarray(f,dtype=np.int16)-2*deriv(f,f))%3
if __name__=='__main__':
 f=np.load('workspace/agent4_gamma3_d9_tensor_seeds.npz')['seeds']
 t=time.time();logs=logseed(f)
 assert np.array_equal(f,(logs+2*deriv(logs,logs))%3)
 np.savez_compressed('workspace/agent4_gamma3_d9_log_seeds.npz',seeds=logs.astype(np.int8))
 print('PASS log-exp inverse for all729 actualgamma3seeds; seconds',time.time()-t,flush=True)
