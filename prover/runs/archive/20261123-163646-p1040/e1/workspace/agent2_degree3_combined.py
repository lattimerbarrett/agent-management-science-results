"""Integral class-three relation closure; exploratory until PASS.
Coordinates are degree2 and twice degree3 of log in exponential variables.
"""
import json
from itertools import combinations
from sage.all import Matrix, ZZ
from agent1_degree3 import *

pairs=list(combinations(range(m),2))
L2=[br({(i,):1},{(j,):1}) for i,j in pairs]
def coords2(p):
 v=[p.get((i,j),0) for i,j in pairs]
 z={}
 for x,q in zip(v,L2):z=add(z,q,x)
 assert z==p
 return v

def initial_vector(ex):
 r2={t:x for t,x in ex.items() if len(t)==2}
 p3={t:2*x for t,x in ex.items() if len(t)==3}
 for (i,j),x in r2.items():
  p3=add(p3,{(i,i,j):x,(i,j,j):x})
 return coords2(r2)+coords(p3)

def linear_sub(p,L):
 out={}
 for w,x in p.items():
  q={():x}
  for i in w:q=mul(q,L[i],3)
  out=add(out,q)
 return out

def action_matrix(words):
 L=[];Q=[]
 for w in words:
  ex=expand(w);li={t:x for t,x in ex.items() if len(t)==1}
  f2={t:x for t,x in ex.items() if len(t)==2}
  qi=add({t:2*x for t,x in f2.items()},mul(li,li,3),-1)
  for (i,),x in li.items():qi=add(qi,{(i,i):x})
  coords2(qi)
  L.append(li);Q.append(qi)
 cols=[]
 for i,j in pairs:
  a=coords2(br(L[i],L[j]))
  b=coords(add(br(Q[i],L[j]),br(L[i],Q[j])))
  cols.append(a+b)
 for p in LP:cols.append([0]*len(pairs)+coords(linear_sub(p,L)))
 return Matrix(ZZ,cols).transpose()

def row_basis(M):
 return M.hermite_form(include_zero_rows=False)

def main(collision_file=None, vector_file=None):
 data=json.load(open('workspace/agent2_nielsen_actions_n3.json'))
 # Audit supplied action words against their exact automorphisms.
 acts=[]
 for name,d in data['actions'].items():
  words=[tuple(w) for w in d['words']]
  # The source file independently checks these; audit again here.
  ident=tuple((i+1,) for i in range(N))
  ig=[tuple(map(tuple,f)) for f in data['inverses']]
  def ev(w):
   f=ident
   for s in w:f=compose(f,G[s-1] if s>0 else ig[-s-1])
   return f
  t=tuple(map(tuple,d['auto']));ti=tuple(map(tuple,d['inverse']))
  assert compose(t,ti)==ident and compose(ti,t)==ident
  for g,w in zip(G,words):assert ev(w)==compose(t,compose(g,ti))
  A=action_matrix(words);acts.append(A)
  print('built and audited action',name,flush=True)
 rel=commuting_relators()
 init=[initial_vector(ex) for w,ex in rel]
 for fn in ['workspace/agent2_peiffer_degree3_vectors.json','workspace/agent2_aut_consistency_degree3_vectors.json']:
  init += json.load(open(fn))
 if collision_file:
  for w in json.load(open(collision_file)):
   f=ident
   for t in w:f=compose(f,G[t-1] if t>0 else ig[-t-1])
   assert f==ident
   init.append(initial_vector(expand(w)))
  print('audited collision relators',len(init)-len(rel),flush=True)
 if vector_file:
  init.extend(json.load(open(vector_file)))
 H=row_basis(Matrix(ZZ,init))
 print('initial relation lattice rank',H.nrows(),flush=True)
 for r in range(1,9):
  parts=[H]+[H*A.transpose() for A in acts]
  extra=[]
  for z in H.rows():
   r2={}
   for x,q in zip(z[:len(pairs)],L2):r2=add(r2,q,x)
   if not r2:continue
   for i in range(m):extra.append([0]*len(pairs)+[2*x for x in coords(br({(i,):1},r2))])
  if extra:parts.append(Matrix(ZZ,extra))
  newH=row_basis(Matrix(ZZ,[list(z) for P in parts for z in P.rows()]))
  print('closure',r,'rank',newH.nrows(),flush=True)
  if H==newH:break
  H=newH
 R2=H[:,:len(pairs)]
 K=R2.transpose().right_kernel().basis_matrix()
 C=K*H[:,len(pairs):]
 assert all(x%2==0 for x in C.list())
 C=C.apply_map(lambda x:x//2)
 C=row_basis(C)
 print('quadratic rank',R2.rank(),'cubic relation rank',C.nrows(),flush=True)
 # Compute exact target matrix in Lyndon coordinates.
 keys=[(i,w) for i in range(N) for w in product(range(N),repeat=4)]
 B=Matrix(ZZ,[[ld(w)[i].get(t,0) for w in L3] for i,t in keys])
 assert B*C.transpose()==0
 S=C.smith_form(transformation=False)
 diag=[abs(S[i,i]) for i in range(min(S.dimensions())) if S[i,i]]
 print('Johnson rank',B.rank(),'kernel',len(L3)-B.rank(),'SNF counts',{int(x):diag.count(x) for x in set(diag)},flush=True)
 if C.nrows()==len(L3)-B.rank() and all(x==1 for x in diag):print('PASS: degree3 IA3 integral Johnson injectivity')
 else:print('INCOMPLETE: no injectivity claim')
 return H,C,B
if __name__=='__main__':main()
