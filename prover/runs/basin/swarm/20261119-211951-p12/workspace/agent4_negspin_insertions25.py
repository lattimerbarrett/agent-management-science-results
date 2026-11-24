from pathlib import Path
src=Path('workspace/agent1_negative_spin25.py').read_text().split('@lru_cache(None)\ndef parts')[0]
src=src.replace('p=1000000007;','p=1000000007;')
exec(src)
import numpy as np,time,itertools
start=time.time()
@lru_cache(None)
def partitions(n,lo=1):
 if n==0:return ((),)
 return tuple((i,)+x for i in range(lo,n+1) for x in partitions(n-i,i))
allparts=tuple(part for d in range(13) for part in partitions(d));ixall={a:i for i,a in enumerate(allparts)};weights=np.array([sum(a) for a in allparts])
W0=np.zeros((NN+1,len(allparts)),dtype=np.int64)
for n,row in enumerate(S):
 for a,v in row.items():
  for b,w in C.items():
   if sum(a)+sum(b)<=12:W0[n,ixall[tuple(sorted(a+b))]]=(W0[n,ixall[tuple(sorted(a+b))]]+v*w)%p
maps={}
for d in range(13):
 si=np.flatnonzero(weights<=12-d);di=np.array([ixall[tuple(sorted(allparts[i]+((d,) if d else ())))] for i in si]);maps[d]=(si,di)
@lru_cache(None)
def gseries(t,l):
 G=np.zeros((24,13),dtype=np.int64)
 for n in range(1,24):
  for d in range(max(0,t-1),13):
   j=d-t
   if j>=-1:G[n,d]=Ls[n][j+n]*((-1)**(n-1))*pow(n,l,p)*(48 if d==0 else 1)%p
 return G
@lru_cache(None)
def gmul(lam,t,l):
 W=Wpoly(lam);G=gseries(t,l);out=np.zeros_like(W)
 for d,(si,di) in maps.items():
  for n in range(1,24):
   v=int(G[n,d])
   if v:out[n:,di]=(out[n:,di]+v*W[:24-n,si])%p
 return out
@lru_cache(None)
def Wpoly(lam):
 if not lam:return W0
 first=lam[0];rest=lam[1:];vals=sorted(set(rest));counts=[rest.count(v) for v in vals];out=np.zeros_like(W0)
 for ns in itertools.product(*(range(c+1) for c in counts)):
  rem=[];mult=1;t=first;l=1
  for v,c,k in zip(vals,counts,ns):
   rem +=[v]*(c-k);mult*=__import__('math').comb(c,k);t+=v*k;l+=k
  out=(out+mult*gmul(tuple(rem),t,l))%p
 return out
cols=partitions(12);colix={a:i for i,a in enumerate(cols)};pivs={}
def add(row):
 row=row[:]
 for c,v in sorted(pivs.items()):
  if row[c]:
   a=row[c];row=[(x-a*y)%p for x,y in zip(row,v)]
 if any(row):
  c=next(i for i,x in enumerate(row) if x);a=pow(row[c],-1,p);pivs[c]=[x*a%p for x in row];return True
 return False
base=json.load(open('workspace/agent3_fz25.json'))
for row in base['rows']:
 add([Q(x).numerator%p*pow(Q(x).denominator,-1,p)%p for x in row])
print('initialrank',len(pivs),flush=True);new=[];nrows=0
for I in range(10):
 for lam in partitions(I):
  W=Wpoly(lam)
  for n in range(1,24):
   for d in range(13):
    if d+n-I<=48-n:continue
    for extra in partitions(12-d):
     row=[0]*len(cols)
     for k in np.flatnonzero(weights==d):
      if W[n,k]:row[colix[tuple(sorted(allparts[k]+extra))]]=int(W[n,k])
     if any(row):
      nrows+=1
      if add(row):new.append((n,lam,d,extra,row));print('NEW',n,lam,d,extra,'rank',len(pivs),flush=True)
 print('insertdegree',I,'rows',nrows,'rank',len(pivs),'sec',time.time()-start,flush=True)
json.dump({'prime':p,'rank':len(pivs),'rows_checked':nrows,'new_rows':new},open('workspace/agent4_negspin_insertions25.json','w'))
if Path(__file__).name=='scratchpad.py':Path('workspace/agent4_negspin_insertions25.py').write_text(Path(__file__).read_text())
