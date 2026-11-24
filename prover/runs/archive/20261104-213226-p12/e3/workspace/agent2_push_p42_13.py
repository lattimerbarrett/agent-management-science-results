import json,math,sys
from collections import defaultdict
from pathlib import Path
P=1000000007
poly=json.load(open('workspace/agent2_jacobian_p42_13.json'))
relation=defaultdict(int)
for mon,c in poly:
 terms={((),0):c}
 for i,j in mon:
  if (i,j)==(0,-2): expansion=[((),1,1)]
  else:
   assert i==0 and j%2==0
   d=j//2
   expansion=[((),d,1)]
   for a in range(1,d+2):
    co=math.comb(d+1,a)*pow(2,-d-1,P)%P
    expansion.append(((a-1,) if a>1 else (),d+1-a,co*(48 if a==1 else 1)%P))
  out=defaultdict(int)
  for (k,e),v in terms.items():
   for kk,ee,w in expansion:
    dest=(tuple(sorted(k+kk)),e+ee)
    out[dest]=(out[dest]+v*w)%P
  terms=out
 for (k,e),v in terms.items():
  if e:
   dest=tuple(sorted(k+(e-1,))) if e>1 else k
   relation[dest]=(relation[dest]+v*(48 if e==1 else 1))%P
relation={k:v for k,v in relation.items() if v}
print('pushed relation terms',len(relation),'degrees',set(map(sum,relation)))
fz=json.load(open('workspace/agent2_fz25.json')); mons=list(map(tuple,fz['monomials']));rows=fz['rows'];basis={}
for row in rows:
 row=row[:]
 for j in range(len(row)):
  if not row[j]:continue
  c=row[j]
  if j in basis:row=[(a-c*b)%P for a,b in zip(row,basis[j])]
  else:
   basis[j]=[a*pow(c,-1,P)%P for a in row];break
row=[relation.get(m,0) for m in mons]
for j in range(len(row)):
 if row[j] and j in basis:
  c=row[j];row=[(a-c*b)%P for a,b in zip(row,basis[j])]
print('reduced nonzero',sum(bool(c) for c in row))
json.dump({'prime':P,'monomials':mons,'pushed':[relation.get(m,0) for m in mons],'reduced':row},open('workspace/agent2_p42_13_pushed.json','w'))

