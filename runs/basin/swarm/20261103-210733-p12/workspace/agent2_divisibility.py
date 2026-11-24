import sys,json,pickle,time,os
sys.path.insert(0,'workspace')
import agent2_pointed_fz as T
from functools import lru_cache
from collections import Counter
from itertools import product
from math import comb
from sage.all import matrix,GF,vector
P=T.P;K=GF(P);start=time.time()
@lru_cache(None)
def factor(h,d):
 n=len(T.basis(d))
 if d>h-1:E={i:[int(i==j) for j in range(n)] for i in range(n)}
 else:E=T.echelon(T.relation_rows(h,d,cap=max(12,3*d-h-1)),n)
 free=[j for j in range(n) if j not in E];positions={j:i for i,j in enumerate(free)}
 red=[]
 for j in range(n):
  row=[0]*n;row[j]=1
  for i in sorted(E):
   c=row[i]
   if c:row=[(x-c*y)%P for x,y in zip(row,E[i])]
  red.append([row[i] for i in free])
 return {'basis':T.basis(d),'free':free,'red':red,'dim':len(free)}
@lru_cache(None)
def psi(h,d):
 a=factor(h,d);b=factor(h,d+1);idx={v:i for i,v in enumerate(b['basis'])}
 return [b['red'][idx[(a['basis'][j][0],a['basis'][j][1]+1)]] for j in a['free']]
@lru_cache(None)
def splits(a):
 c=Counter(a);ks=tuple(c);cs=tuple(c[k] for k in ks);out=[]
 for vv in product(*(range(v+1) for v in cs)):
  x=tuple(k for k,v in zip(ks,vv) for _ in range(v));y=tuple(k for k,c0,v in zip(ks,cs,vv) for _ in range(c0-v));z=1
  for c0,v in zip(cs,vv):z*=comb(c0,v)
  out.append((x,y,z))
 return out

def layout(a,b,d):
 keys=[]
 for i in range(d+1):
  for x in range(factor(a,i)['dim']):
   for y in range(factor(b,d-i)['dim']):keys.append((i,x,y))
 return keys,{k:i for i,k in enumerate(keys)}
def run(a):
 b=25-a;dom,di=layout(a,b,11);cod,ci=layout(a,b,12)
 M=matrix(K,len(cod),len(dom),sparse=False)
 for j,(d,x,y) in enumerate(dom):
  for i,c in enumerate(psi(a,d)[x]):
   if c:M[ci[(d+1,i,y)],j]+=c
  for i,c in enumerate(psi(b,11-d)[y]):
   if c:M[ci[(d,x,i)],j]+=c
 V=vector(K,len(cod));p=json.load(open('workspace/agent2_P24.json'))
 for part,coeff in p['terms']:
  q=T.Q(coeff);c0=q.numerator*pow(q.denominator,-1,P)%P
  for x,y,mult in splits(tuple(part)):
   d=sum(x)
   if d>a-1 or 12-d>b-1:continue
   fa=factor(a,d);fb=factor(b,12-d)
   ra=fa['red'][fa['basis'].index((x,0))];rb=fb['red'][fb['basis'].index((y,0))]
   for i,c in enumerate(ra):
    if c:
     for j,e in enumerate(rb):
      if e:V[ci[(d,i,j)]]+=c0*mult*c*e
 r=M.rank();aug=M.augment(matrix(K,len(cod),1,list(V))).rank()
 D=matrix(K,len(cod),77)
 for col,part in enumerate(T.F.partitions(12)):
  for x,y,mult in splits(part):
   d=sum(x)
   if d>a-1 or 12-d>b-1:continue
   fa=factor(a,d);fb=factor(b,12-d)
   ra=fa['red'][fa['basis'].index((x,0))];rb=fb['red'][fb['basis'].index((y,0))]
   for i,c in enumerate(ra):
    if c:
     for j,e in enumerate(rb):
      if e:D[ci[(d,i,j)],col]+=mult*c*e
 C=M.left_kernel().basis_matrix()*D
 json.dump([[int(x) for x in row] for row in C.rows()],open('workspace/agent2_obstruction_%02d.json'%a,'w'))
 out={'split':a,'shape':M.dimensions(),'rank':r,'augmented_rank':aug,'obstruction_rank':C.rank()}
 print(out,'time',time.time()-start,flush=True)
 return out
out=[]
for a in range(1,6):
 out.append(run(a));json.dump(out,open('workspace/agent2_divisibility_tests.json','w'))
