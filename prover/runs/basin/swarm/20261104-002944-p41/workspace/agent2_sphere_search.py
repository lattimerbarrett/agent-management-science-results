from pathlib import Path
s=Path('workspace/agent2_sphere_search.py').read_text();exec(s[:s.index('start=time.time()')])
from collections import Counter
rng=random.Random(381735)
counts=Counter();targets=[];start=time.time()
for trial in range(500):
 fac={frozenset(f) for f in combinations(range(5),4)}
 for n in range(5,16):
  if n>5:
   f=rng.choice(tuple(fac));fac.remove(f);fac.update(frozenset([n-1])|frozenset(t) for t in combinations(f,3))
  fac,ec=neighbor(fac,n)
  if ec!=n*(n-1)//2:continue
  T={frozenset(t) for f in fac for t in combinations(f,3)};ef={}
  for f in fac:
   for e in combinations(f,2):ef.setdefault(frozenset(e),[]).append(f)
  for uv,ff in ef.items():
   if len(ff)!=3:continue
   abc=set().union(*ff)-uv
   if frozenset(abc) in T:continue
   D=(fac-set(ff))|{frozenset(abc|{u}) for u in uv}
   a,b=uv;TT={frozenset(t) for f in D for t in combinations(f,3)}
   HH=[frozenset(e) for e in combinations(set(range(n))-uv,2) if frozenset(e)|{a} in TT and frozenset(e)|{b} in TT]
   verts=set().union(*HH);cs=[]
   while verts:
    seen={verts.pop()};todo=list(seen)
    while todo:
     x=todo.pop()
     for e in HH:
      if x in e:
       for y in e-seen:seen.add(y);todo.append(y)
    verts-=seen;cs.append(seen)
   counts[(n,len(cs))]+=1
   if len(cs)>1:
    print('TARGET',n,uv,'components',list(map(len,cs)),flush=True)
    targets.append({'D':[sorted(f) for f in D],'uv':sorted(uv),'components':[sorted(c) for c in cs],'H':[sorted(e) for e in HH]})
    json.dump(targets,open('workspace/agent2_flip_multicomponents.json','w'))
 if targets:break
print('trials',trial+1,'time',time.time()-start,'counts',counts,'targets',len(targets))
