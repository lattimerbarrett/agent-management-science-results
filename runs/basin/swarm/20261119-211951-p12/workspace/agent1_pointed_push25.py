from pathlib import Path
s=Path('workspace/agent3_fz25.py').read_text().split('cols=parts(N);')[0]
s=s.replace('N=12; g=25','N=13; g=25').replace('2*g-2 if n==0','2*g-1 if n==0').replace('range(1,11)','range(1,15)')
exec(s)
prime=1000000007
base=json.load(open('workspace/agent3_fz25.json'))
cols=parts(12);ix={c:i for i,c in enumerate(cols)}
pivs={}
def add(row):
 row=[int(x)%prime for x in row]
 for c,p in sorted(pivs.items()):
  if row[c]:
   z=row[c];row=[(x-z*y)%prime for x,y in zip(row,p)]
 if any(row):
  c=next(i for i,x in enumerate(row) if x);z=pow(row[c],-1,prime);row=[x*z%prime for x in row];pivs[c]=row
  return True
 return False
def mod(x):return x.numerator%prime*pow(x.denominator%prime,-1,prime)%prime
for row in base['rows']:add([mod(Q(x)) for x in row])
print('initial rank',len(pivs))
from collections import Counter
@lru_cache(None)
def subk(p):
 if not p:return (((),0,1),)
 v=p[0];out={}
 for rest,e,c in subk(p[1:]):
  out[(rest,e+v)]=out.get((rest,e+v),0)+c
  q=tuple(sorted((v,)+rest));out[(q,e)]=out.get((q,e),0)+c
 return tuple((q,e,c) for (q,e),c in out.items())
count=0
for r in range(1,14):
 for ai in [0,1]:
  for weight in range(max(0,3*r-g-ai)):
   if (r+weight+ai)%2:continue
   for sig in parts(weight):
    if any(x%3==2 for x in sig):continue
    for k in range(14-r):
     for extra in parts(k):
      pe=13-r-k;row=[0]*len(cols)
      for kp,v in H(sig).items():
       n=r-sum(kp)
       if n<0:continue
       coeff=v*(A if ai==0 else B)[n]
       if not coeff:continue
       for q,e,mult in subk(tuple(sorted(kp+extra))):
        psi=e+n+pe
        if not psi:continue
        if psi==1:q2=q;factor=48
        else:q2=tuple(sorted(q+(psi-1,)));factor=1
        row[ix[q2]]=(row[ix[q2]]+mod(coeff)*mult*factor)%prime
      count+=1
      if add(row):print('NEW RELATION!',r,ai,sig,extra,pe,'rank',len(pivs),flush=True)
print('pushed rows',count,'rank',len(pivs))
if Path(__file__).name == 'scratchpad.py':
 Path('workspace/agent1_pointed_push25.py').write_text(Path(__file__).read_text())
