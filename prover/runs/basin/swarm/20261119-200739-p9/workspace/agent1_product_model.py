import numpy as np
from scipy.sparse.linalg import LinearOperator, svds

def leaves(N,t,phi,mode=0):
 d=np.diag(np.exp([t,-t])); di=np.linalg.inv(d)
 def rot(a): return np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]])
 A=d@rot(phi); B=di@rot(-phi if mode==0 else phi)
 S=np.eye(2)[None,:,:]
 for j in range(N):
  S=np.stack([S@A,S@B],axis=1).reshape(-1,2,2)
 return S.transpose(0,2,1)
def haar(x,signs):
 y=x.copy(); m=len(y); levels=[]
 while m>1:
  a=(y[:m:2]+y[1:m:2])/np.sqrt(2)
  b=(y[:m:2]-y[1:m:2])/np.sqrt(2)
  levels.append(b); y[:m//2]=a; m//=2
 out=np.zeros_like(y[:1])
 for j,b in reversed(list(enumerate(levels))):
  if len(b)>1:
   bb=b.copy(); bb[::2]=b[1::2]; bb[1::2]=-b[::2]
  else: bb=np.zeros_like(b)
  out=np.stack([(out+signs[j]*bb)/np.sqrt(2),(out-signs[j]*bb)/np.sqrt(2)],axis=1).reshape(-1,2)
 return out
def calc(N,t,phi,mode=0):
 M=leaves(N,t,phi,mode); Mi=np.linalg.inv(M); n=len(M)
 signs=np.array([(-1)**j for j in range(N)])
 def mv(x):return np.einsum('nij,nj->ni',M,haar(np.einsum('nij,nj->ni',Mi,x.reshape(n,2)),signs)).ravel()
 def rmv(x):return -np.einsum('nji,nj->ni',Mi,haar(np.einsum('nji,nj->ni',M,x.reshape(n,2)),signs)).ravel()
 op=LinearOperator((2*n,2*n),matvec=mv,rmatvec=rmv)
 norm=svds(op,k=1,return_singular_vectors=False,tol=1e-6)[0]
 Q=np.cosh(2*t)**(2*N)
 return Q,norm
for N in [5,8,11]:
 for t in [.1,.3,.5]:
  for phi in [.1,.5,1.]:
   Q,v=calc(N,t,phi)
   print(N,t,phi,'Q',round(Q,3),'norm',round(v,3),'power',round(np.log(v)/np.log(Q),3),flush=True)
open('workspace/agent1_product_model.py','w').write(open('scratchpad.py').read())
