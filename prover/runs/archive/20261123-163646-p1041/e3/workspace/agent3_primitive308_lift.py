import runpy,itertools,numpy as np,time
M=runpy.run_path('workspace/agent3_triple12_footprints.py');R=M['rankbasis'];N=4096;xx=np.arange(N,dtype=np.uint16)
A,S=next((A,S) for A,S in M['arrangements']() if A['atoms'][0]==0)
U=sorted(set.union(*S));G=S[0]^S[1]^S[2];ix={x:i for i,x in enumerate(U)};even=[x for x in U if x not in G]
def shortened(r):
 rows=[]
 for m in range(N):
  if m.bit_count()<=11-r:rows.append(sum(1<<i for i,x in enumerate(U) if x&m==m))
 P=R(rows);res=[]
 for j in range(len(U)):
  if j in P:continue
  v=1<<j
  for p in sorted(P):
   if (P[p]&v).bit_count()%2:v^=1<<p
  res.append(v)
 return res
H=shortened(6);C=shortened(7)
Pbig=sorted((S[0]&S[1])-S[2]);proj=R(sum(((v>>ix[x])&1)<<i for i,x in enumerate(Pbig)) for v in C)
print('Cdim',len(C),'bigpunctrank',len(proj))
vals=[0]
for v in proj.values():vals +=[x^v for x in vals]
print('bigpunctmin',min(x.bit_count() for x in vals if x))
assert min(x.bit_count() for x in vals if x)==7
Q={}
for h in H:
 q=sum(((h>>ix[x])&1)<<i for i,x in enumerate(even));v=h
 while q:
  j=q.bit_length()-1
  if j in Q:q^=Q[j][0];v^=Q[j][1]
  else:Q[j]=(q,v);break
pairs=[(0,0)]
for q,h in Q.values():pairs +=[(x^q,y^h) for x,y in pairs]
small={q:h for q,h in pairs if q.bit_count()<=13}
minor=0
for q in small:minor|=q
assert minor.bit_count()==6
cands={}
for q1,h1 in small.items():
 for q2,h2 in small.items():
  if (q1|q2)!=minor:continue
  a=(q1&~q2).bit_count();b=(q2&~q1).bit_count();c=(q1&q2).bit_count()
  if (a,b,c)!=(2,2,2):continue
  key=tuple(sorted([q1,q2,q1^q2]))
  if key not in cands:cands[key]=(small[key[0]],small[key[1]])
print('candidateGL2orbits',len(cands));assert len(cands)==15
# Majority logic exact bounded-distance decoder for RM(7,12).
mons=sorted((m for m in range(N) if m.bit_count()<=7),key=lambda m:-m.bit_count())
axes={m:tuple(11-i for i in range(12) if m>>i&1) for m in mons}
inds={m:(xx&m)==m for m in mons}
def decode(v):
 rem=v.copy(); coeff=[]
 for m in mons:
  arr=rem.reshape((2,)*12)
  par=np.bitwise_xor.reduce(arr,axis=axes[m]) if m else arr
  if int(par.sum())*2>par.size:
   rem[inds[m]]^=1;coeff.append(m)
 return v^rem,rem
ok=[];start=time.time()
for z,(key,(a,b)) in enumerate(cands.items()):
 h1=np.zeros(N,dtype=np.uint8);h2=np.zeros(N,dtype=np.uint8)
 for i,x in enumerate(U):h1[x]=(a>>i)&1;h2[x]=(b>>i)&1
 v=(h1*h2);v[[x for x in range(N) if x not in G]]=0
 c,err=decode(v); ew=int(err.sum())
 valid=ew<=11 and all(c[x]==0 for x in range(N) if x not in U) and all(c[x]==0 for x in Pbig) and sum(int(err[x]) for x in G)==5
 print('decode',z,'errors',ew,'oddErrors',sum(int(err[x]) for x in G),'outsideU',sum(int(c[x]) for x in range(N) if x not in U),'valid',valid,flush=True)
 assert sum(int(err[x]) for x in G)==0
 assert all(c[x]==0 for x in range(N) if x not in U)
 assert all(c[x]==0 for x in Pbig)
 if valid:ok.append((z,key))
print('VALID',ok,'time',time.time()-start)
assert not ok
from pathlib import Path
if Path(__file__).name=='scratchpad.py':
 Path('workspace/agent3_primitive308_lift.py').write_text(Path(__file__).read_text())
