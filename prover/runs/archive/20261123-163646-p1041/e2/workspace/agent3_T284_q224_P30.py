import itertools,json,pathlib,time

def solve(rows,n):
 B={}
 for a,b in rows:
  while a:
   p=a.bit_length()-1
   if p in B:a^=B[p][0];b^=B[p][1]
   else:B[p]=(a,b);break
  if not a and b:return None,len(B)
 x=0
 for p,(a,b) in sorted(B.items()):
  if ((a&x).bit_count()&1)^b:x^=1<<p
 assert all(((a&x).bit_count()&1)==b for a,b in rows)
 return x,len(B)
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
mons=[sum(1<<j for j in I) for k in range(4) for I in itertools.combinations(range(9),k)]
assert len(mons)==130
vs=[sum(1<<j for j,M in enumerate(mons) if x&M==M) for x in range(512)]
q=[sum((x>>(2*j)&1)*(x>>(2*j+1)&1) for j in range(3))&1 for x in range(512)]
P0=list(range(1,16))+[y<<4 for y in range(1,16)];assert len(P0)==30
results=[]
for t,j in [(3,2),(2,3)]:
 rad=[1<<i for i in range(t,4)]+[1<<(4+i) for i in range(t,4)];r=len(rad)
 for J in subspaces(r,j):
  comp=[];BB=J[:]
  for i in range(r):
   if rank(BB+[1<<i])>len(BB):BB.append(1<<i);comp.append(1<<i)
  assert len(BB)==r
  def cv(a):
   z=0
   for k in range(r):
    if a>>k&1:z^=rad[k]
   return z
  src=[x for i in range(t) for x in [1<<i,1<<(4+i)]]+[cv(a) for a in J]+[cv(a) for a in comp]
  tar=[x for i in range(t) for x in [1<<(2*i),1<<(2*i+1)]]+[1<<(6+i) for i in range(j)]+[1<<(2*t+2*i) for i in range(len(comp))]
  assert len(src)==len(tar)==8 and rank(src)==rank(tar)==8
  mp={0:0}
  for a,b in zip(src,tar):mp.update({x^a:y^b for x,y in list(mp.items())})
  assert len(mp)==256
  assert all(q[y]==(sum((x>>i&1)*(x>>(4+i)&1) for i in range(t))&1) for x,y in mp.items())
  P={mp[x] for x in P0};assert len(P)==30 and all(not q[x] for x in P)
  sol,rk=solve([(vs[x],int(x in P)) for x in range(512) if not q[x]],130)
  rr={'t':t,'j':j,'J':J,'solvable':sol is not None,'rank_at_finish':rk,'P':sorted(P)};results.append(rr)
print('cases',len(results),'solvable',sum(x['solvable'] for x in results))
assert len(results)==16
assert all(not x['solvable'] for x in results)
pathlib.Path('workspace/agent3_T284_q224_P30.json').write_text(json.dumps(results,indent=2))
pathlib.Path('workspace/agent3_T284_q224_P30.py').write_text(pathlib.Path(__file__).read_text())
