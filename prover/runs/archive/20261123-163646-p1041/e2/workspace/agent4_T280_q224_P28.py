import itertools,json,numpy as np,sys,time
from pathlib import Path
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese,closure
s=Path('workspace/agent4_boundary256_orbits.py').read_text();exec(s[:s.index('m=9;mons=')])
mons=[sum(1<<j for j in I) for k in range(4) for I in itertools.combinations(range(9),k)];vs=[sum(1<<j for j,M in enumerate(mons) if x&M==M) for x in range(512)]
q=[sum((x>>(2*j)&1)*(x>>(2*j+1)&1) for j in range(3))&1 for x in range(512)]
P0=sorted({(r<<6)|x for r in range(2) for x in range(1,8)}|{(r<<6)|(y<<3) for r in range(2) for y in range(1,8)});assert len(P0)==28

def rank(vecs):
 B={}
 for v in vecs:
  while v:
   j=v.bit_length()-1
   if j in B:v^=B[j]
   else:B[j]=v;break
 return len(B)

def subspaces(r,j):
 for piv in itertools.combinations(range(r),j):
  free=[(i,k) for i,p in enumerate(piv) for k in range(p+1,r) if k not in piv]
  for bits in range(1<<len(free)):
   B=[1<<p for p in piv]
   for z,(i,k) in enumerate(free):
    if bits>>z&1:B[i]|=1<<k
   yield B

results=[];solved=[];st=time.time()
for t,j in [(3,1),(2,2),(2,3),(1,3)]:
 rad=[1<<i for i in range(t,3)]+[1<<(3+i) for i in range(t,3)]+[64];r=len(rad);cnt=0;hits=0
 for J in subspaces(r,j):
  cnt+=1;comp=[];BB=J[:]
  for i in range(r):
   if rank(BB+[1<<i])>len(BB):BB.append(1<<i);comp.append(1<<i)
  assert len(BB)==r
  cv=lambda a:__import__('functools').reduce(int.__xor__,[rad[k] for k in range(r) if a>>k&1],0)
  src=[x for i in range(t) for x in [1<<i,1<<(3+i)]]+[cv(a) for a in J]+[cv(a) for a in comp]
  tar=[x for i in range(t) for x in [1<<(2*i),1<<(2*i+1)]]+[1<<(6+i) for i in range(j)]+[1<<(2*t+2*i) for i in range(len(comp))]
  assert len(src)==len(tar)==7 and rank(src)==rank(tar)==7
  mp={0:0}
  for a,b in zip(src,tar):mp.update({x^a:y^b for x,y in list(mp.items())})
  assert len(mp)==128
  for x,y in mp.items():assert q[y]==(sum((x>>i&1)*(x>>(3+i)&1) for i in range(t))&1)
  P={mp[x] for x in P0};assert len(P)==28 and all(not q[x] for x in P)
  sol,rk=solve([(vs[x],int(x in P)) for x in range(512) if not q[x]],130)
  rr={'t':t,'j':j,'J':J,'solvable':sol is not None};results.append(rr)
  if sol is not None:
   hits+=1;h=[(v&sol).bit_count()&1 for v in vs];f=h+[h[x]^q[x] for x in range(512)];assert sum(f)==280 and degree(f)<=3
   S={x for x,b in enumerate(f) if b};unused=[v for v in range(1,1024) if all(x^v not in S for x in S)]
   cl,rk=closure(S,veronese(10,5));assert not cl
   rr.update({'support':sorted(S),'h_ANF':[M for k,M in enumerate(mons) if sol>>k&1],'unused_count':len(unused),'Kdim':280-rk})
   solved.append(rr)
 print('t,j',t,j,'cases',cnt,'solved',hits,'seconds',time.time()-st,flush=True)
print('TOTAL',len(results),'solved',len(solved),'Kdims',sorted({r['Kdim'] for r in solved}),flush=True)
Path('workspace/agent4_T280_q224_P28.json').write_text(json.dumps({'cases':results,'seconds':time.time()-st}))

# Type I: rank-six quadratic support on its affine six-dimensional span.
Pquad=[x for x in range(64) if q[x]]
assert len(Pquad)==28
mon2=[sum(1<<j for j in I) for k in range(3) for I in itertools.combinations(range(6),k)]
assert len(mon2)==22
assert rank([sum(1<<j for j,M in enumerate(mon2) if x&M==M) for x in Pquad])==21
# Thus its quadratic vanishing ideal is exactly <1+q>.
def nullspace(rows,n):
 B={}
 for v in rows:
  while v:
   j=v.bit_length()-1
   if j in B:v^=B[j]
   else:B[j]=v;break
 out=[]
 for f in range(n):
  if f in B:continue
  a=1<<f
  for j,v in sorted(B.items()):
   if (a&v).bit_count()&1:a^=1<<j
  assert all(not((a&v).bit_count()&1) for v in rows);out.append(a)
 return out
W=sorted(span([1,4,16,64,128,256]));WS=set(W)
assert len(W)==64 and all(not q[x] for x in W)
H=nullspace([vs[x] for x in range(512) if not q[x] and x not in WS],130)
images=[sum(((vs[x]&h).bit_count()&1)<<i for i,x in enumerate(W)) for h in H]
IB=[]
for v in images:
 if rank(IB+[v])>len(IB):IB.append(v)
assert len(H)==17 and len(IB)==7
hist={}
for bits in range(1<<len(IB)):
 v=0
 for j,b in enumerate(IB):
  if bits>>j&1:v^=b
 hist[v.bit_count()]=hist.get(v.bit_count(),0)+1
assert hist=={0:1,64:1,32:70,16:28,48:28}
assert 28 not in hist
assert len(results)==164 and not solved
print('TYPE I CERTIFIED: quadric vanishing ideal dim1; singular W image histogram',hist,'excludes28.')
