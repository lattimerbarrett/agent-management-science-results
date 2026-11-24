import sys,json,time
from pathlib import Path
from itertools import product
from collections import defaultdict
import numpy as np
from scipy.sparse import coo_matrix,eye,kron,save_npz
sys.path.insert(0,'workspace')
from agent3_magnus import K,C,magnus
D=8; LO=4
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
  filename=f'workspace/agent4_tensor_N_{k}'+('_inv' if invflag else '')+'.npz'
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
# Check quadratic correction against actual degree-3 IA seeds, not arbitrary linearization.
from scipy.sparse import load_npz
seedfile=Path('workspace/agent3_gamma3_tensor_seeds.npz')
if seedfile.exists():
 seeds=np.load(seedfile)['seeds'].reshape(-1,N)
 nonzero=np.where(np.any(seeds,axis=1))[0][:12]
 count=0
 for entry in meta['polynomials'][::2]:
  G=tuple({tuple(w):c for w,c in P} for P in entry['G']);H=tuple({tuple(w):c for w,c in P} for P in entry['H'])
  A=load_npz(entry['file'])
  for si in nonzero:
   f=seeds[si].astype(np.int32);F=[{(j,):1} for j in range(3)]
   for j in range(3):
    for wi in np.flatnonzero(f[j*M:(j+1)*M]):F[j][WORDS[wi]]=int(f[j*M+wi])
   actual=compose_poly(H,compose_poly(tuple(F),G))
   out=np.zeros(N,dtype=np.int32)
   for j,P0 in enumerate(actual):
    P0=dict(P0);P0[(j,)]=(P0.get((j,),0)-1)%3
    for u,c in P0.items():
     if c:assert len(u)>=LO;out[j*M+IX[u]]=c
   pred=(f+A@f)%3
   for j,Gi in enumerate(G):
    for w,c in Gi.items():
     if len(w)==2:
      pred[j*M+M-3**8:(j+1)*M]+=c*np.kron(f[w[0]*M:w[0]*M+81],f[w[1]*M:w[1]*M+81])
   assert np.array_equal(out,pred%3),(entry['generator'],int(si))
   count+=1
 print('PASS quadratic conjugation correction on',count,'actual IA gamma3 seeds')
Path('workspace/agent4_crossed_cover_lemma.md').write_text(r'''# Central crossed covers and lower-central detectors

Let A=<S|R> be a finitely presented group, N a finitely generated normal subgroup generated by images of Y={y_1,...,y_m}. Suppose explicit words W_y(S) give those images, and endomorphisms sigma_s,sigma_sinv of F(Y) give the actual conjugation actions of s,s^{-1} on N.

Define H=F(Y)/M, where M is the smallest normal subgroup invariant under every sigma_s and sigma_sinv and containing:
(1) inverse-action relations sigma_s sigma_sinv(y)y^{-1} and sigma_sinv sigma_s(y)y^{-1};
(2) action consistency sigma_r(y)y^{-1} for r in R;
(3) Peiffer relations sigma_Wy(z) (y z y^{-1})^{-1} for y,z in Y.
All of these are true relations in N. In H, the substitutions are automorphisms, satisfy R, and hence define an A-action. The map f:H->N is equivariant and surjective. Peiffer identities on generators imply f(h) dot a = h a h^{-1} for every h,a in H, where dot denotes the left A-action. Thus if f(h)=1, Inn(h)=identity: ker f is central in H.

## Graded central-kernel lemma

For any surjection f:H->N with central kernel K, the kernel of gr_gamma(H)->gr_gamma(N) is contained in the center of gr_gamma(H). Indeed if x in gamma_c(H) maps into gamma_{c+1}(N), surjectivity gives x=z k for z in gamma_{c+1}(H),k in K. Then [x,H] is contained in gamma_{c+2}(H), proving its graded class brackets trivially with every degree-one class, hence with the entire generated graded Lie ring.

## Conditional all-degree torsion detector

Suppose a torsion class t in gr_d(H) admits iterated brackets t_k=[...[t,x_1],...,x_k] nonzero for arbitrarily large k, with each x_j in gr_1(H). Every t_k is torsion. If some t_k maps to zero in gr(N), then its centrality forces t_{k+1}=0 and all later brackets zero, a contradiction. Thus every t_k survives in gr(N). When N=IA_n, every torsion class maps to zero under the integral Johnson homomorphism, whose target is free abelian. This proves strictness in every corresponding degree.

The lemma does NOT by itself produce such a torsion tower or establish rank stabilization. Those are still required. It avoids the stronger and unnecessary demand that the finite invariant cover H be exactly IA_n or that all identities among GL_n quotient relators be known. Its construction is an invariant L-presentation with explicit finite seed relators and substitutions.
''')
