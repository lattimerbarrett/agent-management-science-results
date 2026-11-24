import itertools,json,time
from pathlib import Path
h=2;n=2*h*h;t=h**3
G=[(b*2*h+a,b*2*h+h+c) for b in range(h) for a in range(h) for c in range(h)]
E=list(itertools.combinations(range(n),2));idx={e:i for i,e in enumerate(E)}
start=time.time();res=[]
for vv in [(0,2),(0,1),(0,4)]:
 vi=idx[vv];avail=[j for j in range(len(E)) if j!=vi];bad=set()
 for q in range(t):
  for C in itertools.combinations(avail,q):
   mask=sum(1<<x for x in C);deg=[0]*n
   for x in C:
    a,b=E[x];deg[a]+=1;deg[b]+=1
   J=0
   for i,(a,b) in enumerate(G):
    own=int(bool(mask>>idx[(a,b)]&1))
    ta=h-int(a in vv and (a,b)!=vv);tb=h-int(b in vv and (a,b)!=vv)
    if deg[a]-own>=ta and deg[b]-own>=tb:J|=1<<i
   assert J.bit_count()<=q+1
   if J.bit_count()==q+1:bad.add(J)
 minimal=[I for I in bad if not any(J!=I and J&I==J for J in bad)]
 lam=None;hitter=None
 for s in range(t+1):
  for T in itertools.combinations(range(t),s):
   tm=sum(1<<i for i in T)
   if all(tm&I for I in minimal):lam=s;hitter=T;break
  if lam is not None:break
 result={'point':vv,'minimal_bad_coalitions':[[i for i in range(t) if I>>i&1] for I in minimal],'lambda':lam,'hitter':hitter,'all_bad_activated_masks':len(bad)}
 res.append(result);print(result,flush=True)
Path('workspace/agent2_star_badcoalitions_h2.json').write_text(json.dumps(res,indent=2));Path('workspace/agent2_star_badcoalitions_h2.py').write_text(Path('scratchpad.py').read_text())
print('seconds',time.time()-start)
