"""Exact finite checks of universal identities in agent3_uniform_homology.md."""
import itertools as it,json
from collections import defaultdict

def add(*ps):
 o=defaultdict(int)
 for p in ps:
  for k,v in p.items():o[k]+=v
 return {k:v for k,v in o.items() if v}
def scale(p,t):return {k:t*v for k,v in p.items() if t*v}
def mul(p,q):
 o=defaultdict(int)
 for (xs,ys),v in p.items():
  for (xt,yt),w in q.items():
   cs=xs+tuple(j for r,j in ys);ct=xt+tuple(j for r,j in yt)
   if set(cs)&set(ct):continue
   sign=(-1)**sum(a>b for a in xs for b in xt)
   key=(tuple(sorted(xs+xt)),tuple(sorted(ys+yt)))
   o[key]+=v*w*sign
 return {k:v for k,v in o.items() if v}
def d(p):
 o=defaultdict(int)
 for (xs,ys),v in p.items():
  for a,(r,j) in enumerate(ys):
   sg=(-1)**(len(xs)+sum(t>j for t in xs))
   o[tuple(sorted(xs+(j,))),ys[:a]+ys[a+1:]]+=sg*v
 return {k:v for k,v in o.items() if v}
def y(r,j):return {((),((r,j),)):1}
def xsum(n):return {((j,),()):1 for j in range(n)}
def h(r,n):return add(*(y(r,j) for j in range(n)))
def E(r,n):return add(*(mul(y(r,i),y(r,j)) for i,j in it.combinations(range(n),2)))
def diffy(r,s,j):return add(y(r,j),scale(y(s,j),-1))
def phi_coords(p):
 o=defaultdict(int)
 for (xs,ys),v in p.items():
  assert len(xs)==1 and len(ys)==3
  rr=[r for r,j in ys];counts=[rr.count(r) for r in range(3)]
  if 2 not in counts:continue
  r=counts.index(2);s=counts.index(1)
  sig=1 if (r,s) in [(0,1),(1,2),(2,0)] else -1
  S=tuple(sorted(xs+tuple(j for r,j in ys)))
  o[S]+=v*sig
 return {S:v for S,v in o.items() if v}
def checkcap(p,b=(1,2,2)):
 for xs,ys in p:
  assert all(sum(r==s for r,j in ys)<=b[s] for s in range(3))

def main():
 out={}
 for n in range(6,11):
  X=xsum(n)
  for r in range(3):
   assert d(h(r,n))==X
   assert d(E(r,n))==mul(X,h(r,n))
  za=mul(diffy(0,1,0),E(2,n));checkcap(za)
  assert d(za)==mul(X,mul(diffy(0,1,0),h(2,n)))
  pa=phi_coords(mul(X,za))
  assert pa=={S:6 for S in it.combinations(range(n),4) if 0 in S}
  for a,b in [(0,1),(1,0),(0,n-1),(n-2,n-1)]:
   u=mul(diffy(0,1,a),diffy(1,2,b));z=mul(u,h(2,n));checkcap(z)
   assert d(z)==mul(X,u)
   pp=phi_coords(mul(X,z))
   assert pp=={S:-6 for S in it.combinations(range(n),4) if a in S and b in S}
  out[n]='all exact singleton/pair cycle and projection identities passed'
 # Formal coefficient proof of pair decomposition, on every allowed coloring.
 for rows in it.product(range(3),repeat=3):
  if rows.count(0)>1 or max(rows.count(i) for i in range(3))>2:continue
  c=[rows.count(r) for r in range(3)]
  f=int(c==[0,2,1])-int(c==[1,2,0])+int(c==[1,0,2])-int(c==[0,1,2])
  rhs=0
  for pair in it.combinations(range(3),2):
   rr=sorted(rows[i] for i in pair)
   rhs+=int(rr==[1,1])-int(rr==[2,2])+int(rr==[0,2])-int(rr==[0,1])
  assert f==rhs,(rows,f,rhs)
 # Local cochain annihilates all allowed four-y boundaries.
 n=4
 for rows in it.product(range(3),repeat=4):
  if max(rows.count(r) for r in range(3))>2:continue
  p={((),tuple(sorted(zip(rows,range(4))))):1}
  assert not phi_coords(d(p))
  assert not d(d(p))
 print(json.dumps(out,indent=2))
 return out
if __name__=='__main__':
 out=main()
 with open('workspace/agent3_polynomial_checks.json','w') as f:json.dump(out,f,indent=2)
