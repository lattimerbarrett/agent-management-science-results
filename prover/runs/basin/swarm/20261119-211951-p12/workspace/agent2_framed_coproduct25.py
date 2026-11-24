from pathlib import Path
s=Path('workspace/agent2_framed_actual_fz25.py').read_text().split('records=[];failed=[]')[0]
exec(s)
from sage.all import GF,matrix,vector
from math import comb
from collections import Counter
from itertools import product
F=GF(prime)
def rel(h,d):
 cols=parts(d);ix={p:i for i,p in enumerate(cols)};rows=[]
 for r in range(1,d+1):
  for a in range(2):
   for wt in range(3*r-h-a):
    if (r+wt+a-h+1)%2:continue
    for sig in parts(wt):
     if any(x%3==2 for x in sig):continue
     vals={p:mod(x) for p,x in H(sig,2*h-1).items() if sum(p)==r}
     for extra in parts(d-r):
      row=[0]*len(cols)
      for p,x in vals.items():row[ix[tuple(sorted(p+extra))]]=x
      rows.append(row)
 return cols,matrix(F,rows if rows else [],ncols=len(cols)).right_kernel().basis_matrix()
a=json.load(open('workspace/agent2_anomaly25.json'));outputs=[]
for h1,d1,h2,d2 in [(20,10,5,2),(22,11,3,1),(24,12,1,0)]:
 A,KA=rel(h1,d1);B,KB=rel(h2,d2);ixA={p:i for i,p in enumerate(A)};ixB={p:i for i,p in enumerate(B)};CP=matrix(F,len(A),len(B))
 for ks,c in zip(a['monomials'],a['coefficients']):
  if not int(c):continue
  vals=sorted(set(ks));cs=[ks.count(x) for x in vals]
  for ns in product(*(range(n+1) for n in cs)):
   aa=tuple(x for x,n in zip(vals,ns) for _ in range(n))
   if sum(aa)!=d1:continue
   bb=tuple(x for x,c,n in zip(vals,cs,ns) for _ in range(c-n));cf=int(c)%prime
   for cc,n in zip(cs,ns):cf=cf*comb(cc,n)%prime
   CP[ixA[aa],ixB[bb]]+=F(cf)
 V=KA*CP*KB.transpose();print('FRAMED COPRODUCT',h1,d1,h2,d2,'quotdim',KA.nrows(),KB.nrows(),'value',V.list(),'rank',V.rank(),flush=True)
 outputs.append({'channel':[h1,d1,h2,d2],'value':[[int(x) for x in r] for r in V]})
json.dump(outputs,open('workspace/agent2_framed_coproduct25.json','w'))
if Path(__file__).name=='scratchpad.py':Path('workspace/agent2_framed_coproduct25.py').write_text(Path(__file__).read_text())
