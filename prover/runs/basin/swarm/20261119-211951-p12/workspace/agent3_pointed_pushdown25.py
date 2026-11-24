from pathlib import Path
source=Path('workspace/agent3_fz25.py').read_text().split('cols=parts(N);')[0]
source=source.replace('N=12; g=25','N=13; g=25').replace('range(1,11)','range(1,15)').replace('(2*g-2 if n==0 else 1)','(2*g-1 if n==0 else 1)')
exec(source)
from sage.all import matrix,GF,QQ
import itertools,time,json,pickle
start=time.time();prime=1000000007;F=GF(prime)
cols=parts(12);ix={p:i for i,p in enumerate(cols)}
def mod(x):return int(x.numerator%prime)*pow(int(x.denominator%prime),-1,prime)%prime
@lru_cache(None)
def push(p,e):
 # substituteκlog_i=κbase_i+ψ^i and pushdownψ^m.
 if p:
  out={};n=p[0]
  for q,c in push(p[1:],e):out[tuple(sorted(q+(n,)))]=out.get(tuple(sorted(q+(n,))),0)+c
  for q,c in push(p[1:],e+n):out[q]=out.get(q,0)+c
  return tuple(out.items())
 if e==0:return ()
 if e==1:return (((),48),)
 return (((e-1,),1),)
rows=[];labels=[]
for r in range(1,14):
 for a in range(2):
  for weight in range(3*r-g-a):
   if (r+weight+a)%2:continue
   for sig in parts(weight):
    if any(x%3==2 for x in sig):continue
    rel={}
    for p,x in H(sig).items():
     d=sum(p)
     if d>r:continue
     e=r-d;y=x*(A if a==0 else B)[e]
     if y:rel[p,e]=y
    for k in range(14-r):
     for q in parts(k):
      extra=13-r-k;row=[0]*len(cols)
      for (p,e),x in rel.items():
       for target,c in push(tuple(sorted(p+q)),e+extra):row[ix[target]]+=x*c
      rows.append([mod(x) if x else 0 for x in row]);labels.append((r,a,sig,q,extra))
print('pushrows',len(rows),'elapsed',time.time()-start,flush=True)
old=json.load(open('workspace/agent3_fz25.json'));oldrows=[[mod(Q(x)) for x in row] for row in old['rows']]
print('pushrank',matrix(F,rows).rank(),'combinedrank',matrix(F,oldrows+rows).rank(),flush=True)
pickle.dump({'rows':rows,'labels':labels,'columns':cols,'prime':prime},open('workspace/agent3_pointed_pushdown25.pkl','wb'))
if Path(__file__).name=='scratchpad.py':Path('workspace/agent3_pointed_pushdown25.py').write_text(Path(__file__).read_text())
