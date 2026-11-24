from sage.all import *
from sage.topology import simplicial_complex_examples as ex
import itertools,json,random,time,numpy as np
class RSet:
 def __init__(self,x=()):self.a=[];self.d={};[self.add(i)for i in x]
 def add(self,x):
  if x not in self.d:self.d[x]=len(self.a);self.a.append(x)
 def discard(self,x):
  if x in self.d:
   i=self.d.pop(x);y=self.a.pop()
   if i<len(self.a):self.a[i]=y;self.d[y]=i
 def pop(self):x=random.choice(self.a);self.discard(x);return x
 def __bool__(self):return bool(self.a)

def grow(core,trials):
 vertices=sorted(core.vertices(),key=str);n=len(vertices);mp={v:i for i,v in enumerate(vertices)}
 initial=[tuple(sorted(mp[v]for v in f))for f in core.facets()]
 qs=list(itertools.combinations(range(n),4));ts=list(itertools.combinations(range(n),3));es=list(itertools.combinations(range(n),2));ti={t:i for i,t in enumerate(ts)};ei={e:i for i,e in enumerate(es)}
 qt=np.array([[ti[t]for t in itertools.combinations(q,3)]for q in qs]);qe=np.array([[ei[e]for e in itertools.combinations(q,2)]for q in qs]);tq=[[]for t in ts];eq=[[]for e in es]
 for j,q in enumerate(qs):
  for a in qt[j]:tq[a].append(j)
  for a in qe[j]:eq[a].append(j)
 tq=list(map(np.array,tq));eq=list(map(np.array,eq))
 for trial in range(trials):
  tris=np.zeros(len(ts),bool);edges=np.zeros(len(es),bool)
  for f in initial:
   for t in itertools.combinations(f,3):tris[ti[t]]=True
   for e in itertools.combinations(f,2):edges[ei[e]]=True
  tc=tris[qt].sum(1);ec=edges[qe].sum(1);a3=RSet(np.flatnonzero(tc==3));a2=RSet(np.flatnonzero((tc==2)&(ec==5)));steps=0
  while a3 or a2:
   f=a3.pop()if a3 else a2.pop();affected=[];steps+=1
   for t in qt[f]:
    if not tris[t]:tris[t]=True;tc[tq[t]]+=1;affected.extend(tq[t])
   for e in qe[f]:
    if not edges[e]:edges[e]=True;ec[eq[e]]+=1;affected.extend(eq[e])
   for g in set(affected):
    if tc[g]==3:a3.add(g)
    else:a3.discard(g)
    if tc[g]==2 and ec[g]==5:a2.add(g)
    else:a2.discard(g)
  print('coregrowth',n,trial,'tris',int(tris.sum()),'of',len(ts),'steps',steps,flush=True)
  if not tris.all():
   fs=[qs[j]for j in np.flatnonzero(tc==4)];covered={t for f in fs for t in itertools.combinations(f,3)}
   pure=all(t in covered for i,t in enumerate(ts)if tris[i])
   print('PROPERTRAP',n,len(fs),'pure',pure,flush=True)
   open(f'workspace/agent4_barydunce_trap{n}_{trial}.json','w').write(json.dumps({'facets':fs,'triangles':[t for i,t in enumerate(ts)if tris[i]],'pure':pure}));return True
 return False
D=ex.DunceHat();D=D.barycentric_subdivision()
print('core',D.f_vector(),flush=True)
grow(D,10)
open('workspace/agent4_core_growth.py','w').write(open(__file__).read())
