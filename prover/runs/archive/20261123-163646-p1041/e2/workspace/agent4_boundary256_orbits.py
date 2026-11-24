import itertools,json,numpy as np
from pathlib import Path

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

def span(ds):
 s={0}
 for d in ds:s|={x^d for x in s}
 return s

def degree(f):
 a=np.array(f,dtype=np.uint8)
 for b in range(a.size.bit_length()-1):a=a.reshape(-1,2,1<<b);a[:,1,:]^=a[:,0,:];a=a.reshape(-1)
 return max((int(i).bit_count() for i in np.nonzero(a)[0]),default=-1)

m=9;mons=[sum(1<<j for j in I) for k in range(4) for I in itertools.combinations(range(m),k)]
vs=[sum(1<<j for j,M in enumerate(mons) if x&M==M) for x in range(512)]
q=[((x>>0&1)&(x>>1&1))^((x>>2&1)&(x>>3&1))^((x>>4&1)&(x>>5&1)) for x in range(512)]
assert sum(q)==224
# Check independent q times all affine functions form the complete kernel.
kvec=[]
for a in [None]+list(range(9)):
 vals=[q[x]&(1 if a is None else (x>>a&1)) for x in range(512)]
 assert degree(vals)<=3
 cc=0
 mob=vals[:]
 for b in range(9):
  for x in range(512):
   if x>>b&1:mob[x]^=mob[x^(1<<b)]
 for i,M in enumerate(mons):
  if mob[M]:cc|=1<<i
 kvec.append(cc)
_,krank=solve([(v,0) for v in kvec],len(mons));assert krank==10
rows0=[(vs[x],0) for x in range(512) if not q[x]]
_,rank=solve(rows0,len(mons));assert len(mons)-rank==10
results=[]
for t in [1,2,3]:
 for typ in ['linear','affine_singular','affine_nonsingular']:
  if typ=='affine_singular' and t==3:continue
  ds=[1<<(2*j) for j in range(t)]
  if typ=='linear':offset=0
  elif typ=='affine_singular':offset=1<<(2*t)
  else:offset=1;ds[0]=3
  active={x^offset for x in span(ds)}
  P={x^r for x in active for r in span([1<<(6+j) for j in range(4-t)])}
  assert len(P)==16 and all(q[x]==0 for x in P)
  rows=[(vs[x],int(x in P)) for x in range(512) if not q[x]]
  sol,rank=solve(rows,len(mons))
  result={'t':t,'type':typ,'P':sorted(P),'solvable':sol is not None,'kernel_dim':len(mons)-rank}
  if sol is not None:
   h=[(v&sol).bit_count()&1 for v in vs];f=h+[h[x]^q[x] for x in range(512)]
   assert sum(f)==256 and degree(f)<=3
   S={x for x,b in enumerate(f) if b}
   unused=[v for v in range(1,1024) if all(x^v not in S for x in S)]
   result.update({'unused_count':len(unused),'unused_first':unused[:10],'support':sorted(S),'h_ANF':[M for j,M in enumerate(mons) if sol>>j&1]})
  print(t,typ,{k:v for k,v in result.items() if k not in ['support','P']},flush=True);results.append(result)
Path('workspace/agent4_boundary256_orbits.json').write_text(json.dumps(results))

# Independent terminal-kernel assertion for the exceptional cubic orbit.
def gf2rank(vecs):
 B={}
 for v in vecs:
  while v:
   j=v.bit_length()-1
   if j in B:v^=B[j]
   else:B[j]=v;break
 return len(B)
assert len(results)==8
assert [r['solvable'] for r in results]==[True,True,True,False,False,False,False,False]
mons5=[sum(1<<j for j in I) for k in range(6) for I in itertools.combinations(range(10),k)]
for r in results[:3]:
 assert r['unused_count']==0
 S=r['support']
 vv=[sum(1<<j for j,M in enumerate(mons5) if x&M==M) for x in S]
 assert gf2rank(vv)==245
 aff=[(1<<256)-1]+[sum(1<<i for i,x in enumerate(S) if x>>j&1) for j in range(10)]
 assert gf2rank(aff)==11
 assert all(sum(1 for x in S if x&M==M and (j<0 or x>>j&1))%2==0 for M in mons5 for j in range(-1,10))
print('CERTIFIED: unique solvable linear orbit; kernel10=q*affine; exceptional K_nu5=affine11; all 3 presentations terminal.')
