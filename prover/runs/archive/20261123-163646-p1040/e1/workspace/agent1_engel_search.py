import json,time
from itertools import product
from sage.all import Matrix,ZZ
from agent1_degree3 import *
from agent1_degree3_closure import row_basis
from agent1_collision_reduce import reduce

def main():
 data=json.load(open('workspace/agent2_nielsen_actions_n3.json'))
 IG=[tuple(map(tuple,f)) for f in data['inverses']]
 ident=tuple((j+1,) for j in range(N))
 H=json.load(open('workspace/agent1_class3_HNF215.json'))
 cand=[]
 def ev(w):
  f=ident
  for s in w:f=compose(f,G[s-1] if s>0 else IG[-s-1])
  return f
 for ell in (1,2):
  for w in product(tuple(range(1,m+1))+tuple(range(-m,0)),repeat=ell):
   if red(w)!=w:continue
   a=[0]*m
   for s in w:a[abs(s)-1]+=1 if s>0 else -1
   if not any(a):continue
   cand.append((w,ev(w),ev(inv(w)),tuple(a)))
 cache={};eligible=0;hits=0;new=[];t=time.time()
 for ai,(wa,a,ia,u) in enumerate(cand):
  for wh,h,ih,v in cand:
   key=(u,v)
   if key not in cache:
    A={(i,):x for i,x in enumerate(u) if x};T={(i,):x for i,x in enumerate(v) if x}
    q=br(A,br(T,A))
    if not q:cache[key]=None;continue
    da=tuple({} for _ in range(N));dh=da
    da=tuple({} for _ in range(N));dh=tuple({} for _ in range(N))
    for i,x in enumerate(u):
     if x:da=tuple(add(p,q,x) for p,q in zip(da,Ds[i]))
    for i,x in enumerate(v):
     if x:dh=tuple(add(p,q,x) for p,q in zip(dh,Ds[i]))
    if any(dbr(da,dbr(dh,da))):cache[key]=None;continue
    z=[0]*36+[2*x for x in coords(q)]
    cache[key]=z if any(reduce(H,z)) else None
   z=cache[key]
   if z is None:continue
   eligible+=1;b=compose(h,compose(a,ih))
   if compose(a,b)!=compose(b,a):continue
   hits+=1;print('FOUND NEW ACTUAL ENGEL RELATION',wa,wh,flush=True)
   r=red(wa+wh+wa+inv(wh)+inv(wa)+wh+inv(wa)+inv(wh))
   assert ev(r)==ident
   from agent1_degree3_closure import initial_vector
   zactual=initial_vector(expand(r))
   assert zactual==z or zactual==[-x for x in z]
   new.append(zactual)
   H=[[int(x) for x in row] for row in row_basis(Matrix(ZZ,H+[zactual])).rows()]
   cache={}
  if ai%50==0:print('a',ai,'eligible pairs',eligible,'hits',hits,'seconds',round(time.time()-t,2),flush=True)
 json.dump(new,open('workspace/agent1_engel_vectors.json','w'))
 print('DONE eligible',eligible,'hits',hits,flush=True)
 return new
if __name__=='__main__':main()
