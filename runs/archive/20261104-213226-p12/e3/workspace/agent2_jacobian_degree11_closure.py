from collections import Counter,defaultdict
import math,time,json
P=1000000007;G=25;PSI=(0,-2)
def prod(mon,vs):
 coeff=1;out=list(mon)
 for i,j in vs:
  if (i,j)==PSI:out.append((i,j));continue
  if i<0 or j<0 or i>j+2 or (i+j)%2:return None,0
  if i==j==0:coeff=coeff*G%P
  else:out.append((i,j))
 return tuple(sorted(out)),coeff

def deriv(poly):
 out=defaultdict(int)
 for mon,coef in poly.items():
  c=Counter(mon); keys=[v for v in c if v[0]>0]
  for a,(i,j) in enumerate(keys):
   n=c[i,j];rest=list(mon);rest.remove((i,j))
   dest,w=prod(rest,[(i-2,j)])
   if w:out[dest]=(out[dest]+coef*n*w)%P
   for k,l in keys[a:]:
    m=c[k,l]-(i==k and j==l)
    if m<=0:continue
    factor=n*m*(pow(2,-1,P) if (i,j)==(k,l) else 1)%P
    rest2=rest[:];rest2.remove((k,l))
    dest,w=prod(rest2,[PSI,(i-1,j-1),(k-1,l-1)])
    if w:out[dest]=(out[dest]+coef*factor*w)%P
    dest,w=prod(rest2,[(i+k-2,j+l)])
    if w:out[dest]=(out[dest]-coef*factor*math.comb(i+k-2,i-1)*w)%P
 return {k:v for k,v in out.items() if v}

from functools import lru_cache
fz=json.load(open('workspace/agent2_fz25.json')); mons=list(map(tuple,fz['monomials']));basis={}
for row in fz['rows']:
 row=row[:]
 for j in range(len(row)):
  if not row[j]:continue
  c=row[j]
  if j in basis:row=[(a-c*b)%P for a,b in zip(row,basis[j])]
  else:
   basis[j]=[a*pow(c,-1,P)%P for a in row];break
@lru_cache(None)
def push(mon):
 terms={((),0):1}
 for i,j in mon:
  if (i,j)==PSI: expansion=[((),1,1)]
  else:
   assert i==0 and j%2==0
   d=j//2;expansion=[((),d,1)]
   for a in range(1,d+2):
    co=math.comb(d+1,a)*pow(2,-d-1,P)%P
    expansion.append(((a-1,) if a>1 else (),d+1-a,co*(48 if a==1 else 1)%P))
  out=defaultdict(int)
  for (k,e),v in terms.items():
   for kk,ee,w in expansion:
    dest=(tuple(sorted(k+kk)),e+ee)
    out[dest]=(out[dest]+v*w)%P
  terms=out
 relation=defaultdict(int)
 for (k,e),v in terms.items():
  if e:
   dest=tuple(sorted(k+(e-1,))) if e>1 else k
   relation[dest]=(relation[dest]+v*(48 if e==1 else 1))%P
 return [relation.get(m,0) for m in mons]
def reduce(poly):
 row=[0]*len(mons)
 for mon,c in poly.items():row=[(a+c*b)%P for a,b in zip(row,push(mon))]
 for j in range(len(row)):
  if row[j] and j in basis:
   c=row[j];row=[(a-c*b)%P for a,b in zip(row,basis[j])]
 return row
vs=[(i,j) for j in range(1,5) for i in range(1 if j%2 else 2,j+3,2)]
def enum(rem,lo=0):
 if not rem:yield ()
 for k in range(lo,len(vs)):
  if vs[k][1]<=rem:
   for r in enum(rem-vs[k][1],k):yield (vs[k],)+r
poly={tuple([(3,1)]*22):1}
t=time.time()
for r in range(32):poly=deriv(poly)
print('intermediate',len(poly),'time',time.time()-t,flush=True)
candidates=list(enum(4))
results=[]
for c,mon in enumerate(candidates):
 q={tuple(sorted(k+mon)):v for k,v in poly.items()}
 for r in range((sum(i for i,j in mon)+2)//2):q=deriv(q)
 row=reduce(q)
 results.append([mon,any(row)])
 if any(row):
  print('EXTRA RELATION',mon,row,flush=True);break
 if c%10==0:print(c+1,'/',len(candidates),'time',round(time.time()-t,2),flush=True)
json.dump(results,open('workspace/agent2_jacobian_degree11_closure_results.json','w'))
print('completed',len(results),'extra',sum(b for a,b in results),'time',time.time()-t)
