from itertools import combinations
from collections import Counter
import pickle,sys,time,os
sys.path.insert(0,'workspace')
from kdecomp_agent4 import kdecomp,facets_normalize

def subs(W,q):
 return {frozenset(s) for j in range(q+1) for s in combinations(W,j)}
def pure(faces,q):
 for s in faces:
  if len(s)<q and not any(s|{v} in faces for v in set().union(*faces)-s):return False
 return True

def main(d=3):
 n,tt=pickle.load(open('workspace/no3hypertree_agent3.pkl','rb'))
 tris=set(map(frozenset,tt));orig=set(tris)
 edges={e for t in tris for e in map(frozenset,combinations(t,2))};origedges=set(edges)
 assert len(edges)==n*(n-1)//2
 assert all(sum(t<=Q for t in tris)<=2 for Q in map(frozenset,combinations(range(n),4)))
 collapses=[]
 while tris:
  free=next(((e,t) for e in sorted(edges,key=lambda e:tuple(sorted(e))) for t in tris if e<t and sum(e<s for s in tris)==1),None)
  assert free is not None
  e,t=free;edges.remove(e);tris.remove(t);collapses.append((e,t))
 assert len(edges)==n-1
 seen={0}
 while True:
  new=seen|set().union(*(e for e in edges if e&seen))
  if new==seen:break
  seen=new
 assert len(seen)==n
 blocks={v:set(range(d*v,d*(v+1))) for v in range(n)}
 tree=set(edges)
 faces={frozenset()}
 for e in edges:faces|=subs(set().union(*(blocks[v] for v in e)),d+1)
 assert pure(faces,d+1)
 # Independently verify VD leaf-clone deletion scaffold for initial tree expansion.
 basefaces=set(faces);active=set(range(n));vedges=set(edges);vsteps=0
 while len(active)>2:
  degrees=Counter(v for e in vedges for v in e)
  leaf=next(v for v in active if degrees[v]==1)
  edge=next(e for e in vedges if leaf in e);u=next(iter(edge-{leaf}))
  remain=set(blocks[leaf])
  for v in sorted(blocks[leaf]):
   remfaces={s for s in basefaces if v not in s}
   lk={s-{v} for s in basefaces if v in s}
   remain.remove(v)
   assert lk==subs(blocks[u]|remain,d)
   assert pure(remfaces,d+1)
   basefaces=remfaces;vsteps+=1
  active.remove(leaf);vedges.remove(edge)
 assert basefaces==subs(set().union(*(blocks[v] for v in active)),d+1)
 start=time.time();count=0
 for edge,tri in reversed(collapses):
  a,b=sorted(edge);c=next(iter(tri-edge));A,B,C=blocks[a],blocks[b],blocks[c]
  allowed=set()
  for av in sorted(A):
   for bv in sorted(B):
    e=frozenset([av,bv]);allowed.add(e)
    local=subs(A|B|C,d+1)
    new={s for s in local if e<=s and all(frozenset([x,y]) in allowed for x in s&A for y in s&B)}
    assert not any(e<=s for s in faces)
    assert not (new&faces)
    current=faces|new
    assert {s for s in current if not e<=s}==faces
    link={s-e for s in current if e<=s}
    assert kdecomp(facets_normalize(link),1)
    # All new lower faces extend through universal C block.
    for s in new:
     if len(s)<d+1:assert any(s|{v} in current for v in C-s)
    faces=current;count+=1
 # Exact final identity and shelling blockage (r=0).
 Dfaces={frozenset()}|{frozenset([v]) for v in range(n)}|origedges|orig
 expected={f for f in subs(range(n*d),d+1) if frozenset(v//d for v in f) in Dfaces}
 assert faces==expected
 facets=[f for f in faces if len(f)==d+1]
 eligible=0
 for F in map(frozenset,combinations(range(n*d),d+1)):
  if F in faces:continue
  R=frozenset(v for v in F if F-{v} in faces)
  if R not in faces:eligible+=1
 assert eligible==0
 print('VERIFIED d',d,'vertices',n*d,'facets',len(facets),'base leaf clone steps',vsteps,'edge shedding steps',count,'eligible missing facets',eligible,'seconds',time.time()-start,flush=True)
 pickle.dump((d,n,tt,collapses,facets),open('workspace/lower_certificate_agent4_d'+str(d)+'.pkl','wb'))

if __name__=='__main__':
 source=open(__file__).read()
 if os.path.basename(__file__)!='verify_lower_agent4.py':open('workspace/verify_lower_agent4.py','w').write(source)
 main(3)
 main(4)
