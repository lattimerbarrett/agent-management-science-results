from pathlib import Path
s=Path('workspace/agent2_S320_direct_grassmann.py').read_text();s=s[:s.index('while time.time()-start<120:')]
s+='''seen=set();profiles=collections.Counter();examples=[]
def canon(R):
 B={}
 for r in [ONE]+R:insert(B,r)
 for j in sorted(B):
  for k in sorted(B):
   if k>j and B[k]>>j&1:B[k]^=B[j]
 return tuple(B[k] for k in sorted(B))
while time.time()-start<120:
 mut+=1;RR=R[:]
 for _ in range(40):
  i,j=rng.sample(range(12),2);RR[i]^=RR[j]
 rng.shuffle(RR);drop=rng.choice([2,3,4]);base=RR[:-drop];candidate=base[:];valid=True
 for stage in range(drop):
  last=stage==drop-1;eq=[(p,0) for p in prodrows(candidate,5)]
  if last:
   gg=groups(candidate)
   if any(len(g)>2 for g in gg):valid=False;break
   eq += [((1<<g[0])|(1<<g[1]),1) for g in gg if len(g)==2]
  sol=solve(eq)
  if sol is None:valid=False;break
  row=None;BB={}
  for x in [ONE]+candidate:insert(BB,x)
  for tries in range(12):
   a=sol[0]^ran(sol[1])
   if not insert(dict(BB),a):continue
   if not last and any(len(g)>(1<<(drop-stage-1)) for g in groups(candidate+[a])):continue
   row=a;break
  if row is None:valid=False;break
  candidate.append(row)
 if not valid:continue
 key=canon(candidate)
 if key in seen:continue
 seen.add(key)
 PK=solve((p,0) for p in prodrows(candidate,5))[1];khist[len(PK)]+=1
 if len(PK)<15:continue
 R=candidate;acc+=1;S=pts(R);assert len(set(S))==320
 odd=sum((a&b).bit_count()%2 for i,a in enumerate(PK) for b in PK[i+1:])
 if odd:
  assert all(p.bit_count()%2==0 for p in prodrows(R,6));hits.append({'support':S,'K5':PK,'odd':odd});print('HIT',len(PK),odd,flush=True);break
 if acc%10==0:
  k6=len(solve((p,0) for p in prodrows(R,6))[1]);per=periods(S);prof=(len(PK),k6,len(per));profiles[prof]+=1
  if profiles[prof]==1:examples.append({'support':S,'K5':len(PK),'K6':k6,'periods':per});print('NEWPROFILE',prof,'mut',mut,'accepted',acc,flush=True)
print('DONE',mut,acc,'uniquerowspaces',len(seen),'fullK5',khist,'profiles',profiles,'hits',len(hits),'sec',time.time()-start)
json.dump({'mutations':mut,'accepted':acc,'unique':len(seen),'fullK5dims':dict(khist),'profiles':{str(k):v for k,v in profiles.items()},'examples':examples,'hits':hits},open('workspace/agent2_S320_direct_grassmann_drop234.json','w'))
'''
Path('workspace/agent2_S320_direct_grassmann_drop234.py').write_text(s);exec(compile(s,__file__,'exec'))
