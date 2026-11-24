"""Self-contained NumPy/SciPy finite-Magnus certificate.
All IA3 images, scalar substitutions, conjugation operators and witnesses
are constructed here. No stored matrices, precomputed ranks, Sage or GAP.
"""
import numpy as np
from scipy.sparse import coo_matrix,csr_matrix,kron,eye,vstack
from itertools import product
from collections import defaultdict
import time

def inv(w):return tuple(-a for a in reversed(w))
def comm(u,v):return u+v+inv(u)+inv(v)
def gens():
 G={}
 for i in range(1,4):
  for j in range(1,4):
   if i==j:continue
   a=[(k,) for k in range(1,4)];b=a.copy()
   a[i-1]=(j,i,-j);b[i-1]=(-j,i,j)
   n=len(G)//2+1;G[n]=a;G[-n]=b
  j,k=[k for k in range(1,4) if k!=i]
  a=[(k,) for k in range(1,4)];b=a.copy()
  a[i-1]=(i,j,k,-j,-k);b[i-1]=(i,k,j,-k,-j)
  n=len(G)//2+1;G[n]=a;G[-n]=b
 return G

def scalar(D,p):
 words=[w for d in range(1,D+1) for w in product(range(3),repeat=d)]
 IX={w:j for j,w in enumerate(words)};M=len(words)
 def clean(P):return {w:(c%p if p else c) for w,c in P.items() if (c%p if p else c)}
 def mul(P,Q):
  R=defaultdict(int)
  for u,c in P.items():
   for v,e in Q.items():
    if len(u)+len(v)<=D:R[u+v]+=c*e
  return clean(R)
 def magnus(w):
  P={():1}
  for a in w:
   i=abs(a)-1
   Q={():1,(i,):1} if a>0 else {(i,)*k:(-1)**k for k in range(D+1)}
   P=mul(P,Q)
  P.pop((),None);return P
 S={}
 for a,g in gens().items():
  G=[magnus(w) for w in g]
  cache={():{():1}};rr=[];cc=[];vv=[]
  for j,w in enumerate(words):
   P=mul(cache[w[:-1]],G[w[-1]]);cache[w]=P
   for v,c in P.items():rr.append(IX[v]);cc.append(j);vv.append(c)
  S[a]=coo_matrix((np.array(vv,dtype=np.int64),(rr,cc)),shape=(M,M)).tocsr()
 E=np.zeros((M,3),dtype=np.int64);E[:3]=np.eye(3,dtype=np.int64)
 return S,E,words

def evaluate(word,S,E,p):
 V=E.copy()
 for a in reversed(word):
  V=S[a]@V
  if p:V%=p
 return V-E

def adjoints(S,words):
 D=max(map(len,words));inds=[j for j,w in enumerate(words) if len(w)>=5]
 ws=[words[j] for j in inds];IX={w:j for j,w in enumerate(ws)};m=len(ws)
 degree=np.array([len(w) for w in ws]*3)
 N=[]
 for g in range(1,10):
  Sinv=S[-g][inds,:][:,inds];rr=[];cc=[];vv=[]
  for i in range(3):
   P=S[g][:,i].tocoo()
   for a,c in zip(P.row,P.data):
    v=words[a]
    for pos,j in enumerate(v):
     for w in ws:
      if len(v)+len(w)>D+1:break
      u=v[:pos]+w+v[pos+1:]
      rr.append(i*m+IX[u]);cc.append(j*m+IX[w]);vv.append(int(c))
  J=coo_matrix((np.array(vv,dtype=np.int64),(rr,cc)),shape=(3*m,3*m)).tocsr()
  A=(kron(eye(3,dtype=np.int64),Sinv,format='csr')@J-eye(3*m,dtype=np.int64)).tocsr()
  A.data%=3;A.eliminate_zeros()
  rows,cols=A.nonzero();assert np.all(degree[rows]>degree[cols])
  N.append(A)
 return N,inds,ws

FUNCTIONAL = [(0, '000112', 1), (0, '001012', 2), (0, '001021', 1), (0, '001022', 2), (0, '001102', 1), (0, '001122', 1), (0, '001212', 1), (0, '001221', 1), (0, '002011', 1), (0, '002012', 1), (0, '002112', 1), (0, '002121', 2), (0, '010102', 2), (0, '010122', 2), (0, '010202', 1), (0, '010212', 2), (0, '010221', 2), (0, '012021', 1), (0, '0010212', 2), (0, '0010221', 1), (0, '0011022', 1), (0, '0012012', 1), (0, '0012201', 1), (0, '0020112', 2), (0, '0020121', 1), (0, '0021012', 1), (0, '0022101', 2), (0, '0101202', 1), (0, '0102012', 2), (0, '0102021', 1), (0, '0102102', 1), (0, '0110202', 2), (1, '001112', 1), (1, '001121', 1), (1, '001122', 1), (1, '001211', 2), (1, '001221', 2), (1, '010121', 1), (1, '010212', 1), (1, '010221', 1), (1, '011012', 2), (1, '011021', 1), (1, '011022', 2), (1, '011102', 2), (1, '011202', 1), (1, '011212', 1), (1, '011221', 2), (1, '012021', 2), (1, '012102', 2), (1, '012121', 1), (1, '0011212', 2), (1, '0011221', 1), (1, '0012121', 2), (1, '0101122', 2), (1, '0102112', 2), (1, '0110122', 1), (1, '0110221', 2), (1, '0112012', 1), (1, '0112021', 1), (1, '0112102', 1), (1, '0120121', 1), (1, '0121021', 2), (1, '0121102', 2), (2, '001122', 2), (2, '001212', 1), (2, '001221', 1), (2, '002112', 1), (2, '010212', 2), (2, '010221', 2), (2, '012202', 1), (2, '0101222', 2), (2, '0102212', 1), (2, '0112202', 2), (2, '0121202', 1)]

def main():
 t=time.time()
 # One-based Magnus generator indices, inverse fourth argument.
 def T(a,b,c,g):return comm(comm(comm((a,),(b,)),(c,)),(-g,))
 W=T(1,9,4,2)+T(1,9,4,5)+T(5,4,9,1)+inv(T(5,8,9,4))
 # Integral, not mod3, verification W lies in A5.
 SZ,EZ,wordsZ=scalar(5,0)
 assert not evaluate(W,SZ,EZ,0).any()
 print('PASS: integral Magnus action of W through degree5 is identity',flush=True)
 S,E,words=scalar(7,3)
 for g in range(1,10):assert not evaluate((g,-g),S,E,3).any()
 N,inds,ws=adjoints(S,words);m=len(ws);IX={w:j for j,w in enumerate(ws)}
 lam=np.zeros(3*m,dtype=np.int64)
 for out,w,c in FUNCTIONAL:lam[out*m+IX[tuple(map(int,w))]]=c
 # N raises degree; on degrees5..7 every product of three N is zero.
 lam=csr_matrix(lam.reshape(1,-1))
 first=[lam@A for A in N]
 forms=vstack(first+[f@A for f in first for A in N],format='csr')
 forms.data%=3;forms.eliminate_zeros()
 checked=0
 for a,b,c,g in product(range(1,10),repeat=4):
  V=evaluate(T(a,b,c,g),S,E,3)
  assert not V[:inds[0]].any()
  v=V[inds].T.reshape(-1)
  assert not ((forms@v)%3).any(),(a,b,c,g)
  checked+=1
 # Hence lambda vanishes on all gamma5 images by normal generation.
 V=evaluate(W,S,E,3);assert not V[:inds[0]].any()
 value=int((lam@V[inds].T.reshape(-1))[0]%3)
 assert value!=0
 print('PASS:',checked,'actual weight4 seeds annihilated by all90 dual forms',flush=True)
 print('PASS: lambda(W)=',value,'mod3; therefore W not in gamma5(IA3)',flush=True)
 print('seconds',time.time()-t,flush=True)
if __name__=='__main__':main()
