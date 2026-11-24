from pathlib import Path
source=Path('workspace/agent3_fz25.py').read_text().split('cols=parts(N);')[0]
source=source.replace('N=12; g=25','N=14; g=25').replace('range(1,11)','range(1,17)').replace('(2*g-2 if n==0 else 1)','(k0 if n==0 else 1)').replace('def H(sig):','def H(sig,k0=50):').replace('H(tuple(sorted(rest)))','H(tuple(sorted(rest)),k0)')
exec(source)
from sage.all import matrix,GF,QQ
import itertools,time,json,pickle
start=time.time();prime=1000000007;F=GF(prime);cols=parts(12);ix={p:i for i,p in enumerate(cols)}
def mod(x):return int(x.numerator%prime)*pow(int(x.denominator%prime),-1,prime)%prime
def add(out,q,c):out[q]=out.get(q,0)+c
@lru_cache(None)
def push_state(p,e,f,D):
 if p:
  n=p[0];out={}
  for q,c in push_state(p[1:],e,f,D):add(out,tuple(sorted(q+(n,))),c)
  if D:
   for q,c in push_state(p[1:],e+n,0,1):add(out,q,c)
  else:
   for ee,ff,dd in [(e+n,f,0),(e,f+n,0),(e+f+n-1,0,1)]:
    for q,c in push_state(p[1:],ee,ff,dd):add(out,q,c)
  return tuple(out.items())
 if D:
  if e==0:return ()
  return (((),48),) if e==1 else (((e-1,),1),)
 if e==0 or f==0:return ()
 pp=tuple(sorted(x-1 for x in (e,f) if x>1));c=48**sum(x==1 for x in (e,f))
 return ((pp,c),)
@lru_cache(None)
def push_open(p,e,f):
 out=dict(push_state(p,e,f,0))
 if e+f:
  for q,c in push_state(p,e+f-1,0,1):add(out,q,c)
 return tuple(out.items())
def cols_at(d):return [(p,a,d-sum(p)-a) for k in range(d+1) for p in parts(k) for a in range(d-k+1)]
rows=[];labels=[]
for r in range(1,15):
 for a1,a2 in itertools.product(range(2),repeat=2):
  for weight in range(3*r-g-a1-a2):
   if (r+weight+a1+a2)%2:continue
   for sig in parts(weight):
    if any(x%3==2 for x in sig):continue
    rel={}
    for p,x in H(sig).items():
     d=sum(p)
     if d>r:continue
     for e in range(r-d+1):
      f=r-d-e;y=x*(A if a1==0 else B)[e]*(A if a2==0 else B)[f]
      if y:rel[p,e,f]=y
    tail={};s=sig.count(1)
    for m in range(s+1):
     factor=(-1)**(m+a1+a2)*factorial(s)//factorial(s-m);even=(m+a1+a2)%2==0
     for p,x in H(sig[m:],49).items():
      d=sum(p);l=r-d
      if l<1:continue
      add(tail,(p,l-1),x*factor*(-A[l] if even else B[l]))
    for q,b1,b2 in cols_at(14-r):
     row={}
     for (p,e,f),x in rel.items():
      for target,c in push_open(tuple(sorted(p+q)),e+b1,f+b2):add(row,target,x*c)
     if b1==b2==0:
      for (p,k),x in tail.items():
       for target,c in push_state(tuple(sorted(p+q)),k,0,1):add(row,target,x*c)
     rows.append([row.get(p,0) for p in cols]);labels.append((r,a1,a2,sig,q,b1,b2))
 print('r',r,'rows',len(rows),'elapsed',time.time()-start,flush=True)
old=json.load(open('workspace/agent3_fz25.json'));oldrows=[[Q(x) for x in row] for row in old['rows']]
print('pushrank',matrix(QQ,rows).rank(),'combinedrank',matrix(QQ,oldrows+rows).rank(),flush=True)
pickle.dump({'rows':rows,'labels':labels,'columns':cols,'prime':prime},open('workspace/agent3_rt_pushdown25_exact.pkl','wb'))
