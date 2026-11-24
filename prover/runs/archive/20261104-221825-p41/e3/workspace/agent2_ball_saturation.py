import sys,itertools,json,random,time,pathlib
import numpy as np
from sage.all import simplicial_complexes
sys.path.insert(0,'workspace')
from agent4_fastcert import fastcert

def run(name,trials):
 K=getattr(simplicial_complexes,name)();vs=sorted(K.vertices());ren={v:i for i,v in enumerate(vs)};n=len(vs)
 base=[tuple(sorted(ren[v] for v in f)) for f in K.facets()]
 ts=list(itertools.combinations(range(n),4));qs=list(itertools.combinations(range(n),3));es=list(itertools.combinations(range(n),2))
 ti={t:i for i,t in enumerate(ts)};qi={q:i for i,q in enumerate(qs)};ei={e:i for i,e in enumerate(es)}
 TQ=np.array([[qi[q] for q in itertools.combinations(t,3)] for t in ts]);TE=np.array([[ei[e] for e in itertools.combinations(t,2)] for t in ts])
 QT=[np.array([i for i,t in enumerate(ts) if set(q)<=set(t)]) for q in qs];ET=[np.array([i for i,t in enumerate(ts) if set(e)<=set(t)]) for e in es]
 for trial in range(trials):
  F=np.zeros(len(ts),bool);F[[ti[t] for t in base]]=True;Q=np.zeros(len(qs),bool);Q[TQ[F].flatten()]=True;E=np.zeros(len(es),bool);E[TE[F].flatten()]=True
  ct=Q[TQ].sum(axis=1);ce=E[TE].sum(axis=1);steps=0
  while True:
   pos=np.flatnonzero(~F & ((ct>=3)|((ct==2)&(ce==5))))
   if not len(pos):break
   if trial%3==1:
    two=pos[ct[pos]==2]
    if len(two):
     missing=TE[two][~E[TE[two]]]
     counts=np.bincount(missing,minlength=len(es));best=np.flatnonzero(counts==counts.max());e=random.choice(best)
     candidates=two[np.any(TE[two]==e,axis=1)];f=random.choice(candidates)
    else:f=random.choice(pos)
   elif trial%3==2:
    # Prefer additions with 3 old triangles: delay introduction of new graph edges.
    three=pos[ct[pos]>=3];f=random.choice(three if len(three) else pos)
   else:f=random.choice(pos)
   assert not F[f]
   for q in TQ[f]:
    if not Q[q]:Q[q]=True;ct[QT[q]]+=1
   for e in TE[f]:
    if not E[e]:E[e]=True;ce[ET[e]]+=1
   F[f]=True;steps+=1
  if not F.all():
   facets=[sum(1<<v for v in ts[i]) for i in np.flatnonzero(F)]
   path='workspace/agent2_saturation_'+name+'_'+str(trial)+'.json';json.dump(facets,open(path,'w'))
   print('PROPER TRAP',name,trial,'facets',F.sum(),'triangles',Q.sum(),'edges',E.sum(),path,flush=True)
   # do not risk an unbounded decomposability search in this loop
   return path
  if trial%10==0:print(name,trial,'full',flush=True)

if __name__=='__main__':
 random.seed(88320);pathlib.Path('workspace/agent2_ball_saturation.py').write_text(pathlib.Path(__file__).read_text())
 for name in ['ZieglerBall','RudinBall']:
  if run(name,100):break
