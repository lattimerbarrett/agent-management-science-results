import json,itertools,time
from collections import Counter
from pathlib import Path
C=lambda seq,r:itertools.combinations(sorted(seq),r)
order=[frozenset(f) for f in json.loads(Path('workspace/agent3_2core_order.json').read_text())]
def closure(fs):return {frozenset(s) for f in fs for j in range(len(f)+1) for s in C(f,j)}
def seedcheck():
 old=set();ears=[]
 for i,f in enumerate(order):
  new=closure([f])-old
  mins=[a for a in new if not any(b<a for b in new)]
  assert len(mins)==1
  R=mins[0]
  if i:assert len(R) in [1,2]
  assert new=={a for a in closure([f]) if R<=a}
  ears.append(R);old|=new
 assert len({v for f in order for v in f})==9
 assert all(frozenset(e) in old for e in C(range(9),2))
 tetra_counts=Counter(sum(frozenset(t) in old for t in C(q,3)) for q in C(range(9),4))
 assert 3 not in tetra_counts and 4 not in tetra_counts
 print('seed',len(order),tetra_counts,flush=True)
 return ears

def certify(rank,m,ears):
 start=time.time()
 blocks={v:frozenset(range(m*v,m*(v+1))) for v in range(9)}
 clusters=[set().union(*(blocks[v] for v in f)) for f in order]
 expansions=[{frozenset(t) for t in C(U,rank)} for U in clusters]
 current=set().union(*expansions)
 original=len(current)
 ridges=Counter(q-{v} for q in current for v in q)
 steps=0
 for i in range(len(order)-1,0,-1):
  R=sorted(ears[i]);parts=[sorted(blocks[v]) for v in R]
  for tup in itertools.product(*parts):
   sigma=frozenset(tup)
   removed={f for f in current if sigma<=f}
   assert removed
   links={f-sigma for f in removed};U=set().union(*links)
   assert links=={frozenset(t) for t in C(U,rank-len(sigma))}
   for f in removed:
    for v in f:ridges[f-{v}]-=1
   for f in removed:
    for v in sigma:assert ridges[f-{v}]>0
   current-=removed;steps+=1
  expected=set().union(*expansions[:i])
  assert current==expected
 assert current==expansions[0]
 result=(rank,m,original,steps,len(current),time.time()-start)
 print('CERT',result,flush=True)
 return result
if __name__=='__main__':
 ears=seedcheck()
 results=[certify(r,r,ears) for r in [4,5]]
 Path('workspace/agent4_inflation_results.json').write_text(json.dumps(results))
 Path('workspace/agent4_inflation_check.py').write_text(Path('scratchpad.py').read_text())
