import sys,json,time
from pathlib import Path
from itertools import product
from collections import defaultdict
import numpy as np
from scipy.sparse import coo_matrix,eye,kron,save_npz
sys.path.insert(0,'workspace')
from agent3_magnus import K,C,magnus
D=9; LO=4
WORDS=[w for l in range(LO,D+1) for w in product(range(3),repeat=l)]
IX={w:i for i,w in enumerate(WORDS)}; M=len(WORDS); N=3*M
LENS=np.array([len(w) for w in WORDS])
def clean(P):return {w:int(c)%3 for w,c in P.items() if c%3}
def mul(P,Q):
 out=defaultdict(int)
 for u,c in P.items():
  for v,e in Q.items():
   if len(u)+len(v)<=D:out[u+v]+=c*e
 return clean(out)
def poly(w):
 P=magnus(w,D);P.pop((),None)
 return {tuple(i-1 for i in u):c%3 for u,c in P.items() if c%3}
def spclean(A):
 A=A.tocsr();A.sum_duplicates();A.data%=3;A.eliminate_zeros();return A

def operator(G,H):
 # P is scalar polynomial substitution by H; build cache for every prefix.
 cache={():{():1}}
 rows=[];cols=[];vals=[]
 for l in range(1,D+1):
  for w in product(range(3),repeat=l):
   Q=mul(cache[w[:-1]],H[w[-1]])
   cache[w]=Q
   if l>=LO:
    col=IX[w]
    for u,c in Q.items():rows.append(IX[u]);cols.append(col);vals.append(c)
 P=coo_matrix((np.array(vals,dtype=np.int32),(rows,cols)),shape=(M,M)).tocsr()
 rows=[];cols=[];vals=[]
 for i,Gi in enumerate(G):
  for v,c in Gi.items():
   maxlen=D-len(v)+1
   for pos,j in enumerate(v):
    for l in range(LO,maxlen+1):
     for w in product(range(3),repeat=l):
      u=v[:pos]+w+v[pos+1:]
      rows.append(i*M+IX[u]);cols.append(j*M+IX[w]);vals.append(c)
 J=coo_matrix((np.array(vals,dtype=np.int32),(rows,cols)),shape=(N,N)).tocsr()
 out=spclean(kron(eye(3,dtype=np.int32),P,format='csr')@J-eye(N,dtype=np.int32))
 rr,cc=out.nonzero();assert np.all(LENS[rr%M]>LENS[cc%M])
 return out

def substitute_poly(P,H):
 cache={():{():1}}
 def ev(w):
  if w not in cache:cache[w]=mul(ev(w[:-1]),H[w[-1]])
  return cache[w]
 out=defaultdict(int)
 for w,c in P.items():
  for u,e in ev(w).items():out[u]+=c*e
 return clean(out)
def compose_poly(F,G):return tuple(substitute_poly(P,F) for P in G)
gens=[]; labels=[]
for i in range(1,4):
 for j in range(1,4):
  if i!=j:gens.append(K(3,i,j));labels.append(['K',i,j])
 other=[j for j in range(1,4) if j!=i]
 gens.append(C(3,i,*other));labels.append(['C',i,*other])
meta={'degree':D,'min_degree':LO,'word_order':'length then lex, letters 0,1,2','vector_order':'output-major, output*M+word_index','M':M,'labels':labels,'orientation':'N_g f = displacement(g^-1 F g)-f to linear order in f','polynomials':[]}
for k,(g,gi) in enumerate(gens):
 for invflag in (False,True):
  gg,hh=(gi,g) if invflag else (g,gi)
  G=tuple(poly(w) for w in gg);H=tuple(poly(w) for w in hh)
  start=time.time();A=operator(G,H)
  filename=f'workspace/agent4_tensor_d9_N_{k}'+('_inv' if invflag else '')+'.npz'
  save_npz(filename,A)
  # Direct exact substitution check on arbitrary order-4 displacement (wordlength 5).
  for i in range(3):
   w=tuple((i+j)%3 for j in range(5))
   F=[{(j,):1} for j in range(3)];F[i][w]=1
   actual=compose_poly(H,compose_poly(tuple(F),G))
   vec=np.zeros(N,dtype=np.int32);vec[i*M+IX[w]]=1
   predicted=(A@vec+vec)%3
   out=np.zeros(N,dtype=np.int32)
   for j,P0 in enumerate(actual):
    P0=dict(P0);P0[(j,)]=(P0.get((j,),0)-1)%3
    for u,c in P0.items():
     if c:assert len(u)>=LO;out[j*M+IX[u]]=c
   assert np.array_equal(out,predicted)
  print(k,invflag,'nnz',A.nnz,'seconds',round(time.time()-start,2),flush=True)
  meta['polynomials'].append({'generator':k,'inverse':invflag,'G':[[[list(w),c] for w,c in P.items()] for P in G],'H':[[[list(w),c] for w,c in P.items()] for P in H],'file':filename})
print('PASS all 18 conjugation linearizations, each checked by 3 direct substitutions')
