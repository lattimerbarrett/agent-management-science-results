"""Sage/FLINT implementation of the exact degree-two lattice certificate."""
import sys
from itertools import combinations,permutations,product
from sage.all import matrix,ZZ
from degree2_certificate import red,inv,compose,add,deriv
from degree1_certificate import generators,expansion

def certificate(n):
 ident=tuple((i+1,) for i in range(n));gs=[];ds=[]
 for _,i,w in generators(n):
  g=list(ident);g[i]=w;gs.append(tuple(g))
  d=[{} for _ in range(n)];d[i]=add(expansion(w+(-i-1,)),{():1},-1);ds.append(d)
 m=len(gs);pairs=list(combinations(range(m),2));N=len(pairs);bp={p:i for i,p in enumerate(pairs)}
 cols=[]
 for i,j in pairs:
  D=[add(deriv(ds[i],ds[j][k]),deriv(ds[j],ds[i][k]),-1) for k in range(n)]
  cols.append([D[k].get(w,0) for k in range(n) for w in product(range(n),repeat=3)])
 B=matrix(ZZ,cols).transpose();rankB=B.rank();target=N-rankB
 print('n',n,'bracket rank',rankB,'null',target,flush=True)
 cand=[]
 for i,g in enumerate(gs):cand.append((g,{i:1}))
 for i,j in combinations(range(m),2):
  cand.append((compose(gs[i],gs[j]),{i:1,j:1}))
  cand.append((compose(gs[j],gs[i]),{i:1,j:1}))
 R=[];seen=set()
 for i,a in enumerate(gs):
  for b,v in cand:
   if compose(a,b)!=compose(b,a):continue
   r=[0]*N
   for j,x in v.items():
    if i<j:r[bp[i,j]]+=x
    if i>j:r[bp[j,i]]-=x
   t=tuple(r)
   if any(r) and t not in seen:seen.add(t);R.append(r)
 H=matrix(ZZ,R).hermite_form(include_zero_rows=False)
 print('initial',len(R),'rank',H.nrows(),flush=True)
 assert B*H.transpose()==0
 keys=[];signs=[]
 for D in ds:
  k=next(k for k,p in enumerate(D) if p)
  w=next(w for w in D[k] if w[0]<w[1])
  keys.append((k,w));signs.append(D[k][w])
 actions=[]
 for ii,jj in permutations(range(n),2):
  t=list(ident);ti=list(ident);t[ii]=(ii+1,jj+1);ti[ii]=(ii+1,-jj-1)
  assert compose(t,ti)==ident and compose(ti,t)==ident
  C=[]
  for g in gs:
   h=compose(t,compose(g,ti));hd=[add(expansion(h[k]+(-k-1,)),{():1},-1) for k in range(n)]
   C.append([hd[k].get(w,0)*sgn for (k,w),sgn in zip(keys,signs)])
  A=matrix(ZZ,C).transpose();W={}
  for col,(p,q) in enumerate(pairs):
   u={i:A[i,p] for i in range(m) if A[i,p]};v={j:A[j,q] for j in range(m) if A[j,q]}
   for i,x in u.items():
    for j,y in v.items():
     if i<j:key=(bp[i,j],col);W[key]=W.get(key,0)+x*y
     elif i>j:key=(bp[j,i],col);W[key]=W.get(key,0)-x*y
  actions.append(matrix(ZZ,N,N,W,sparse=True).transpose())
 for roundno in range(1,5):
  old=H
  for t,W in enumerate(actions):
   HW=H*W
   H=H.stack(HW).hermite_form(include_zero_rows=False)
   assert B*H.transpose()==0
   print('round',roundno,'action',t,'rank',H.nrows(),flush=True)
  if H==old:break
  if H.nrows()==target:break
 diag=H.elementary_divisors();print('rank',H.nrows(),'elementary divisors',set(diag),flush=True)
 assert H.nrows()==target and all(x==1 for x in diag)
 print('PASS exact primitive true-relation lattice equals bracket kernel')
 return B,H

if __name__=='__main__':certificate(int(sys.argv[1]) if len(sys.argv)>1 else 3)
