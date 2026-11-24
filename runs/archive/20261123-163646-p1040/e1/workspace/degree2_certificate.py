"""An exact integral proof certificate for degree-2 injectivity for IA_3.
Dependencies: Magnus generation and the degree-one Johnson homomorphism.
Relations used are genuine commuting pairs and their Nielsen conjugates.
"""
import sys
from itertools import combinations,product,permutations
from sympy import Matrix,ZZ
from sympy.matrices.normalforms import smith_normal_form, hermite_normal_form
from degree1_certificate import generators,expansion

def red(w):
 s=[]
 for x in w:
  if s and s[-1]==-x:s.pop()
  else:s.append(x)
 return tuple(s)
def inv(w):return tuple(-x for x in reversed(w))
def compose(f,g):
 return tuple(red(y for x in w for y in (f[x-1] if x>0 else inv(f[-x-1]))) for w in g)
def add(a,b,scale=1):
 a=a.copy()
 for w,v in b.items():a[w]=a.get(w,0)+scale*v
 return {w:v for w,v in a.items() if v}
def deriv(d,p):
 o={}
 for w,v in p.items():
  for t,i in enumerate(w):
   for u,x in d[i].items():
    key=w[:t]+u+w[t+1:];o[key]=o.get(key,0)+v*x
 return {w:v for w,v in o.items() if v}
def certificate(n=3):
 ident=tuple((i+1,) for i in range(n));gs=[];ds=[]
 for _,i,w in generators(n):
  g=list(ident);g[i]=w;gs.append(tuple(g))
  p=add(expansion(w+(-i-1,)),{():1},-1)
  d=[{} for _ in range(n)];d[i]=p;ds.append(d)
 m=len(gs);pairs=list(combinations(range(m),2));bp={p:i for i,p in enumerate(pairs)}
 cols=[]
 for i,j in pairs:
  D=[add(deriv(ds[i],ds[j][k]),deriv(ds[j],ds[i][k]),-1) for k in range(n)]
  cols.append([D[k].get(w,0) for k in range(n) for w in product(range(n),repeat=3)])
 B=Matrix(cols).T
 rankB=B.rank()
 print('n',n,'m',m,'bracket rank',rankB,'null',len(pairs)-rankB,flush=True)
 cand=[]
 for i,g in enumerate(gs):cand.append((g,{i:1},('g',i)))
 for i,j in combinations(range(m),2):
  cand.append((compose(gs[i],gs[j]),{i:1,j:1},('p',i,j)))
  cand.append((compose(gs[j],gs[i]),{i:1,j:1},('p',j,i)))
 R=[];seen=set();cert=[]
 for (a,u,namea),(b,v,nameb) in combinations(cand,2):
  if compose(a,b)!=compose(b,a):continue
  r=[0]*len(pairs)
  for i,y in u.items():
   for j,x in v.items():
    if i<j:r[bp[i,j]]+=x*y
    if i>j:r[bp[j,i]]-=x*y
  t=tuple(r)
  if any(r) and t not in seen:
   seen.add(t);R.append(r);cert.append((namea,nameb))
 M=Matrix(R).T
 print('relations',len(R),'rank',M.rank(),flush=True)
 assert B*M==Matrix.zeros(B.rows,M.cols)
 keys=[];signs=[]
 for D in ds:
  k=next(k for k,p in enumerate(D) if p)
  w=next(w for w in D[k] if w[0]<w[1])
  keys.append((k,w));signs.append(D[k][w])
 actions=[]
 for ii,jj in permutations(range(n),2):
  t=list(ident);ti=list(ident)
  t[ii]=(ii+1,jj+1);ti[ii]=(ii+1,-jj-1)
  assert compose(t,ti)==ident and compose(ti,t)==ident
  C=[]
  for g in gs:
   h=compose(t,compose(g,ti))
   hd=[add(expansion(h[k]+(-k-1,)),{():1},-1) for k in range(n)]
   C.append([hd[k].get(w,0)*sgn for (k,w),sgn in zip(keys,signs)])
  A=Matrix(C).T
  W=Matrix([[A[i,p]*A[j,q]-A[i,q]*A[j,p] for p,q in pairs] for i,j in pairs])
  actions.append(W)
 M=Matrix.hstack(M,*[W*M for W in actions])
 rankM=M.rank()
 print('GL-closure relations',M.cols,'rank',rankM,flush=True)
 for roundno in range(2,5):
  if rankM==len(pairs)-rankB:break
  H=hermite_normal_form(M)
  assert H.cols==rankM
  M=Matrix.hstack(H,*[W*H for W in actions])
  newrank=M.rank()
  print('GL-closure round',roundno,'relations',M.cols,'rank',newrank,flush=True)
  if newrank==rankM:break
  rankM=newrank
 assert B*M==Matrix.zeros(B.rows,M.cols)
 S=smith_normal_form(M,domain=ZZ)
 diag=[abs(S[i,i]) for i in range(min(S.shape)) if S[i,i]]
 print('SNF',diag,flush=True)
 assert rankM==len(pairs)-rankB
 assert all(x==1 for x in diag)
 print('PASS: actual group relations equal the full integral bracket kernel')
 return B,M,cert

if __name__=='__main__':certificate(int(sys.argv[1]) if len(sys.argv)>1 else 3)
