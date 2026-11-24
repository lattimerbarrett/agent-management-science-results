from functools import lru_cache
from math import factorial,comb
from itertools import product
import json,time
from sage.all import matrix,GF
P=1000000007;F=GF(P);start=time.time()
@lru_cache(None)
def parts(n,lo=1):
 if n==0:return ((),)
 return tuple((i,)+p for i in range(lo,n+1) for p in parts(n-i,i))
invdf=[1];v=1
for i in range(1,30):v=v*(2*i+1)%P;invdf.append(pow(v,-1,P))
fact=[factorial(i)%P for i in range(90)]
@lru_cache(None)
def poly(ps):
 if not ps:return (1,)
 first=ps[0];rest=ps[1:];vals=sorted(set(rest));counts=[rest.count(v) for v in vals];out=[0]*(len(ps)+1)
 for ns in product(*(range(c+1) for c in counts)):
  s=first+sum(v*n for v,n in zip(vals,ns));n=sum(ns);mult=(-1)**n;rem=[]
  for v,c,k in zip(vals,counts,ns):mult*=comb(c,k);rem.extend([v]*(c-k))
  z=mult*invdf[s]%P
  for k,x in enumerate(poly(tuple(rem))):out[k+1]=(out[k+1]+z*x)%P
 return tuple(out)
@lru_cache(None)
def val(h,ps,e):
 if sum(ps)+e!=h-1:return 0
 if h==1:return 1
 # scale(2h−3)!!/(2h−2)!
 scale=pow(invdf[h-2],-1,P)*pow(fact[2*h-2],-1,P)%P
 return scale*invdf[max(0,e-1)]*sum(x*fact[2*h-2+m] for m,x in enumerate(poly(ps)))%P
@lru_cache(None)
def splits(ps):
 vals=sorted(set(ps));counts=[ps.count(v) for v in vals];out=[]
 for ns in product(*(range(c+1) for c in counts)):
  a=[];b=[];mult=1
  for v,c,n in zip(vals,counts,ns):a.extend([v]*n);b.extend([v]*(c-n));mult*=comb(c,n)
  out.append((tuple(a),tuple(b),mult))
 return out
cols=parts(12);rows=[];labels=[]
for h in range(1,13):
 k=25-h
 for e in range(12):
  f=11-e
  if not (0<=h-1-e<=12 and 0<=k-1-f<=12):continue
  rows.append([sum(mult*val(h,a,e)*val(k,b,f) for a,b,mult in splits(ps))%P for ps in cols]);labels.append((h,e,f))
print('rows',len(rows),'rank',matrix(F,rows).rank(),'elapsed',time.time()-start,flush=True)
pivs=[]
def insert(row):
 row=row[:]
 for c,p in pivs:
  if row[c]:
   z=row[c];row=[(x-z*y)%P for x,y in zip(row,p)]
 if any(row):
  c=next(i for i,x in enumerate(row) if x);z=pow(row[c],-1,P);pivs.append((c,[x*z%P for x in row]));return True
 return False
for row in rows:insert(row)
bydeg={(ps,d):[(a,b,m) for a,b,m in splits(ps) if sum(a)==d] for ps in cols for d in range(13)}
def pointedcols(d):return [(ps,d-sum(ps)) for w in range(d+1) for ps in parts(w)]
for h in range(1,13):
 k=25-h
 for a in range(12):
  b=11-a;d=h-1-a
  if not 0<=d<=12:continue
  for qa,e in pointedcols(a):
   for qb,f in pointedcols(b):
    if not qa and not qb:continue
    row=[sum(mult*val(h,tuple(sorted(pa+qa)),e)*val(k,tuple(sorted(pb+qb)),f) for pa,pb,mult in bydeg[ps,d])%P for ps in cols]
    if insert(row):
     rows.append(row);labels.append((h,qa,e,qb,f));print('rank increased',len(pivs),'h',h,'elapsed',time.time()-start,flush=True)
    if len(pivs)==77:break
   if len(pivs)==77:break
  if len(pivs)==77:break
 print('finishedh',h,'rank',len(pivs),'elapsed',time.time()-start,flush=True)
 if len(pivs)==77:break
print('FINAL boundary necessaryconstraint rank',len(pivs),flush=True)
json.dump({'columns':cols,'rows':rows,'labels':labels,'prime':P},open('workspace/agent3_hodge_compact_boundary25.json','w'))
if __file__.endswith('scratchpad.py'):
 from pathlib import Path
 Path('workspace/agent3_hodge_compact_boundary25.py').write_text(Path(__file__).read_text())
