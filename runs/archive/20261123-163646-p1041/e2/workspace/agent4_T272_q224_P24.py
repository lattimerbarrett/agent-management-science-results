import itertools,json,numpy as np,sys
from pathlib import Path
s=Path('workspace/agent4_boundary256_orbits.py').read_text();exec(s[:s.index('m=9;mons=')])
mons=[sum(1<<j for j in I) for k in range(4) for I in itertools.combinations(range(9),k)];vs=[sum(1<<j for j,M in enumerate(mons) if x&M==M) for x in range(512)]
q=[sum((x>>(2*j)&1)*(x>>(2*j+1)&1) for j in range(3))&1 for x in range(512)]

def kernel(rows,n):
 B={}
 for v in rows:
  while v:
   j=v.bit_length()-1
   if j in B:v^=B[j]
   else:B[j]=v;break
 out=[]
 for f in range(n):
  if f in B:continue
  x=1<<f
  for p,v in sorted(B.items()):
   if (x&v).bit_count()&1:x^=1<<p
  assert all(not((x&v).bit_count()&1) for v in rows);out.append(x)
 return out

def basis(vecs):
 B={}
 for v in vecs:
  while v:
   j=v.bit_length()-1
   if j in B:v^=B[j]
   else:B[j]=v;break
 return list(B.values())

# A: maximum singular W=span(x0,x2,x4,r0,r1,r2)
W=sorted(span([1,4,16,64,128,256]));assert len(W)==64 and all(not q[x] for x in W)
ker=kernel([vs[x] for x in range(512) if not q[x] and x not in W],130)
images=basis([sum(((vs[x]&h).bit_count()&1)<<i for i,x in enumerate(W)) for h in ker])
print('A Hdim',len(ker),'imageD',len(images));hist={}
for bits in range(1<<len(images)):
 v=0
 for j,h in enumerate(images):
  if bits>>j&1:v^=h
 hist[v.bit_count()]=hist.get(v.bit_count(),0)+1
print('A image histogram',hist);assert 24 not in hist
# B: W affine: first4active free,r0/r1free,lastactivepair11,r2=0
W={x^48 for x in span([1,2,4,8,64,128])};P={x for x in W if not q[x]};assert len(W)==64 and len(P)==24
sol,r=solve([(vs[x],int(x in P)) for x in range(512) if not q[x]],130)
R={'A_Hdim':len(ker),'A_imageD':len(images),'A_histogram':hist,'B_solvable':sol is not None}
if sol is not None:
 h=[(v&sol).bit_count()&1 for v in vs];f=h+[h[x]^q[x] for x in range(512)];assert sum(f)==272 and degree(f)<=3
 S={x for x,b in enumerate(f) if b};unused=[v for v in range(1,1024) if all(x^v not in S for x in S)]
 R.update({'support':sorted(S),'unused':unused,'h_ANF':[M for j,M in enumerate(mons) if sol>>j&1]})
 print('B solvable,unused',len(unused),'h_ANF',R['h_ANF'])
else:print('B impossible')
Path('workspace/agent4_T272_q224_P24.json').write_text(json.dumps(R))
