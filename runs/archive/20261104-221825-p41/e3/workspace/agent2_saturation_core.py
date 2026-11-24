import sys,itertools,json,random,time,pathlib
import numpy as np
import networkx as nx
sys.path.insert(0,'workspace')
from agent3_check import *
from agent4_fastcert import fastcert

def saturate(base,n,trials=100,forced=(),name='custom'):
 ts=list(itertools.combinations(range(n),4));qs=list(itertools.combinations(range(n),3));es=list(itertools.combinations(range(n),2))
 ti={t:i for i,t in enumerate(ts)};qi={q:i for i,q in enumerate(qs)};ei={e:i for i,e in enumerate(es)}
 TQ=np.array([[qi[q] for q in itertools.combinations(t,3)] for t in ts]);TE=np.array([[ei[e] for e in itertools.combinations(t,2)] for t in ts])
 QT=[np.array([i for i,t in enumerate(ts) if set(q)<=set(t)]) for q in qs];ET=[np.array([i for i,t in enumerate(ts) if set(e)<=set(t)]) for e in es]
 for trial in range(trials):
  F=np.zeros(len(ts),bool);F[[ti[t] for t in base]]=True
  for t in forced:
   masks=tuple(sum(1<<v for v in ss) for ss in ts if F[ti[ss]])
   assert appendable(masks,sum(1<<v for v in t));F[ti[t]]=True
  Q=np.zeros(len(qs),bool);Q[TQ[F].flatten()]=True;E=np.zeros(len(es),bool);E[TE[F].flatten()]=True
  ct=Q[TQ].sum(axis=1);ce=E[TE].sum(axis=1);steps=0
  while True:
   pos=np.flatnonzero(~F & ((ct>=3)|((ct==2)&(ce==5))))
   if not len(pos):break
   if trial%4==3:
    three=pos[ct[pos]>=3]
    if len(three):f=random.choice(three)
    else:
     groups={}
     for g in pos:
      e=int(TE[g][~E[TE[g]]][0]);groups.setdefault(e,[]).append(int(g))
     choices=[]
     for e,gs in groups.items():
      graph=nx.Graph();graph.add_edges_from(tuple(set(ts[g])-set(es[e])) for g in gs)
      comps=list(nx.connected_components(graph));small=random.choice([c for c in comps if len(c)==min(map(len,comps))])
      choices.append((len(comps),-len(small),e,small,gs))
     best=max((x[0],x[1]) for x in choices)
     _,_,e,small,gs=random.choice([x for x in choices if x[:2]==best])
     f=random.choice([g for g in gs if set(ts[g])-set(es[e])<=small])
   elif trial%4==1:
    two=pos[ct[pos]==2]
    if len(two):
     missing=TE[two][~E[TE[two]]];counts=np.bincount(missing,minlength=len(es));e=random.choice(np.flatnonzero(counts==counts.max()));f=random.choice(two[np.any(TE[two]==e,axis=1)])
    else:f=random.choice(pos)
   elif trial%4==2:
    three=pos[ct[pos]>=3];f=random.choice(three if len(three) else pos)
   else:f=random.choice(pos)
   for q in TQ[f]:
    if not Q[q]:Q[q]=True;ct[QT[q]]+=1
   for e in TE[f]:
    if not E[e]:E[e]=True;ce[ET[e]]+=1
   F[f]=True;steps+=1
  if not F.all():
   facets=[sum(1<<v for v in ts[i]) for i in np.flatnonzero(F)];path='workspace/agent2_saturation_'+name+'_'+str(trial)+'.json';json.dump(facets,open(path,'w'))
   print('PROPER TRAP',name,trial,'facets',F.sum(),'triangles',Q.sum(),'edges',E.sum(),path,flush=True);return path
  if trial%100==0:print(name,trial,'full',flush=True)
 return None

if __name__=='__main__':
 random.seed(9820)
 pathlib.Path('workspace/agent2_saturation_core.py').write_text(pathlib.Path(__file__).read_text())
 for m in [2,3,4]:
  P=list(range(4,4+m));R=list(range(4+m,4+2*m));z=4+2*m
  disk=[]
  for x,path in [(0,[2]+P+[3]),(1,[2]+R+[3])]:
   disk.extend(tuple(sorted((x,a,b))) for a,b in zip(path,path[1:]))
  disk.extend([tuple(sorted((2,P[0],R[0]))),tuple(sorted((3,P[-1],R[-1])))])
  for i in range(m-1):disk.extend([tuple(sorted((P[i],P[i+1],R[i+1]))),tuple(sorted((P[i],R[i],R[i+1])))])
  base=[]
  for a,b,c in disk:base.extend([(a,b,c,c+z),(a,b,b+z,c+z),(a,a+z,b+z,c+z)])
  print('Corridor',m,'vertices',2*z,'facets',len(base),flush=True)
  if saturate(base,2*z,100,[(0,1,2,2+z)],'corridor'+str(m)):break
