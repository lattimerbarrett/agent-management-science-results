from sage.all import *
from sage.topology import simplicial_complex_examples as ex
import itertools,json,random,time,numpy as np

def grow(fs0,trials,name):
 vertices=sorted(set().union(*map(set,fs0)));n=len(vertices);mp={v:i for i,v in enumerate(vertices)}
 qs=list(itertools.combinations(range(n),4));ts=list(itertools.combinations(range(n),3));es=list(itertools.combinations(range(n),2));qi={q:i for i,q in enumerate(qs)};ti={t:i for i,t in enumerate(ts)};ei={e:i for i,e in enumerate(es)}
 qt=np.array([[ti[t]for t in itertools.combinations(q,3)]for q in qs]);qe=np.array([[ei[e]for e in itertools.combinations(q,2)]for q in qs]);tq=[[]for t in ts];eq=[[]for e in es]
 for j,q in enumerate(qs):
  for a in qt[j]:tq[a].append(j)
  for a in qe[j]:eq[a].append(j)
 tq=list(map(np.array,tq));eq=list(map(np.array,eq));initial=[qi[tuple(sorted(mp[v]for v in f))]for f in fs0]
 for trial in range(trials):
  selected=np.zeros(len(qs),bool);selected[initial]=True;tris=np.zeros(len(ts),bool);edges=np.zeros(len(es),bool)
  tris[qt[initial].ravel()]=True;edges[qe[initial].ravel()]=True
  tc=tris[qt].sum(1);ec=edges[qe].sum(1)
  elig=set(np.flatnonzero((~selected)&((tc>=3)|((tc==2)&(ec==5)))))
  seq=list(initial)
  while elig:
   f=random.choice(tuple(elig));elig.remove(f);selected[f]=True;seq.append(f);affected=[]
   for t in qt[f]:
    if not tris[t]:tris[t]=True;tc[tq[t]]+=1;affected.extend(tq[t])
   for e in qe[f]:
    if not edges[e]:edges[e]=True;ec[eq[e]]+=1;affected.extend(eq[e])
   for g in affected:
    if not selected[g] and (tc[g]>=3 or(tc[g]==2 and ec[g]==5)):elig.add(g)
    else:elig.discard(g)
  if len(seq)<len(qs):
   print('TRAP',name,n,trial,len(seq),'of',len(qs),flush=True)
   with open(f'workspace/agent4_{name}_growtrap{n}_{trial}.json','w')as out:json.dump({'facets':[qs[j]for j in seq],'initial_count':len(initial),'oldvertices':list(map(int,vertices))},out)
   return [qs[j]for j in seq]
  if trial%20==0:print('completed',name,n,trial,flush=True)
 return None
for name in ['ZieglerBall','RudinBall']:
 base=getattr(ex,name)();fs=[tuple(f)for f in base.facets()]
 print(name,len(base.vertices()),len(fs),flush=True)
 result=grow(fs,100,name)
 if result:
  import sys
  sys.path.insert(0,'workspace');from agent4_fastcert import fastcert
  masks=tuple(sorted(sum(1<<v for v in f)for f in result))
  for k in [0,1,2]:
   t=time.time();c=fastcert(masks,k);print('certificate',name,k,bool(c),time.time()-t,flush=True)
   if c:open(f'workspace/agent4_{name}_cert.json','w').write(json.dumps(c));break
open('workspace/agent4_ballgrowth.py','w').write(open(__file__).read())
