from pathlib import Path
from itertools import combinations
import random,time,json
def neighbor(fac,n):
 while True:
  tris={};edges={frozenset(e) for f in fac for e in combinations(f,2)}
  for f in fac:
   for tri in combinations(f,3):tris.setdefault(frozenset(tri),[]).append(f)
  choices=[]
  for t,fl in tris.items():
   assert len(fl)==2
   uv=(fl[0]|fl[1])-t
   if uv not in edges:choices.append((t,fl,uv))
  if not choices:return fac,len(edges)
  t,fl,uv=rng.choice(choices);fac.difference_update(fl)
  fac.update(uv|frozenset(e) for e in combinations(t,2))
import sys
sys.path.insert(0,'workspace');from agent2_completion_light import complete_light
from collections import Counter
rng=random.Random(288157)
counts=Counter();traps=[];start=time.time()
for trial in range(1000):
 fac={frozenset(f) for f in combinations(range(5),4)}
 for n in range(5,19):
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
   if len(cs)<=1:continue
   counts['disconnectedD']+=1
   for C in cs:
    e=next(e for e in HH if e<=C)
    FF=D|{uv|e}
    good,E,Tfull,order=complete_light([list(f) for f in FF],n)
    counts['componenttests']+=1
    if not good:
     traps.append({'n':n,'D':[list(f) for f in D],'uv':list(uv),'first':list(uv|e),'added':order})
     Path('workspace/agent2_flip_trap_large.json').write_text(json.dumps(traps));print('TRAP',trial,n,uv,'component',C,'T',len(Tfull),flush=True)
  if traps:break
 if trial%100==0:print('trial',trial,'counts',counts,'seconds',time.time()-start,flush=True)
 if traps:break
print('END','trials',trial+1,'counts',counts,'traps',len(traps),'seconds',time.time()-start)
