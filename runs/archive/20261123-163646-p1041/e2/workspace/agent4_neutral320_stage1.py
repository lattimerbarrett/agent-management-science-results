import json,time,itertools,numpy as np
from pathlib import Path
st=time.time();D=json.loads(Path('workspace/agent4_T288_twoextra_quadratic320.json').read_text());S=set(D['seeds320'][0]['support']);p0=min(S);periods=[p^p0 for p in S if all(x^p^p0 in S for x in S)];p=len(periods).bit_length()-1
print('perioddimension',p,flush=True)
def insert(B,v):
 while v:
  k=v.bit_length()-1
  if k in B:v^=B[k]
  else:B[k]=v;return v
 return 0
def coordmap(basis,n):
 B={};out=[]
 for v in basis:
  if insert(B,v):out.append(v)
 for j in range(n):
  if insert(B,1<<j):out.append(1<<j)
 vals=[0]
 for v in out:vals +=[x^v for x in vals]
 inv=np.zeros(1<<n,dtype=np.int32);inv[np.array(vals)]=np.arange(1<<n,dtype=np.int32)
 return out,np.array(vals,dtype=np.int32),inv
basis,vals,inv=coordmap(periods,13);T=set(int(inv[x])>>p for x in S);n=13-p;d=8-p
print('core',n,len(T),sorted(T),flush=True)
def flats_through(T,origin,target):
 TT={x^origin for x in T};levels=[((),(0,))]
 for dd in range(target):
  nxt=[]
  for bas,U in levels:
   for v in sorted(TT):
    if v<=max(U):continue
    VV=tuple(v^x for x in U)
    if min(VV)!=v or not all(x in TT for x in VV):continue
    nxt.append((bas+(v,),tuple(sorted(U+VV))))
  levels=nxt
 return [(bas,tuple(x^origin for x in U)) for bas,U in levels]
flatdict={}
for origin in sorted(T):
 for bas,U in flats_through(T,origin,d-2):flatdict[tuple(sorted(U))]=bas
print('containedflats',len(flatdict),flush=True)
trip=np.array([(a,b,a^b) for a in range(1,128) for b in range(a+1,128) if b<a^b],dtype=np.int32);assert len(trip)==2667
candidates={};flatdata=[]
for i,(U,bas) in enumerate(flatdict.items()):
 org=U[0];full,vs,iv=coordmap(bas,n);q=d-2;ct=np.bincount([int(iv[x^org])>>q for x in T],minlength=128)
 assert ct[0]==1<<q
 hits=np.flatnonzero(ct[trip].sum(axis=1)==1<<q)
 flatdata.append({'points':U,'basis':bas})
 for ii in hits:
  a,b,ab=map(int,trip[ii]);A=tuple(sorted(int(vs[(z<<q)|r])^org for z in [0,a,b,ab] for r in range(1<<q)))
  assert len(set(A)&T)==1<<(d-1)
  candidates[A]=i
print('neutralcandidates',len(candidates),time.time()-st,flush=True)
new=[];perhist={}
for A in candidates:
 Tp=set(T)^set(A);TT=Tp|{x|(1<<n) for x in T};assert len(TT)==2*len(T)
 pp=min(TT);PV=[x^pp for x in TT if all(y^x^pp in TT for y in TT)];pd=len(PV).bit_length()-1;perhist[pd]=perhist.get(pd,0)+1
 if pd==0:new.append({'T':sorted(TT),'A':A})
print('newcoreperiodhist',perhist,'APERIODIC',len(new),time.time()-st,flush=True)
R={'source320':sorted(S),'source_basis':basis,'p':p,'n':n,'T':sorted(T),'flats':flatdata,'neutral_count':len(candidates),'newcore_periodhist':perhist,'aperiodic':new,'seconds':time.time()-st}
Path('workspace/agent4_neutral320_stage1.json').write_text(json.dumps(R));Path('workspace/agent4_neutral320_stage1.py').write_text(Path('scratchpad.py').read_text().split('