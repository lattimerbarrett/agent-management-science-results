from itertools import product
from pathlib import Path
import json

def build(times, last_stage):
 n=len(times); tokens={}; expanded=set(); edges=[]; creation={}; nxt=0
 for s in range(last_stage+1):
  nxt=max(nxt,s)
  approx=tuple(int(t is not None and t<=s) for t in times)
  for depth in range(min(s,n-1)+1):
   node=approx[:depth]
   assert not node or node in tokens
   if node in expanded: continue
   expanded.add(node)
   children=[]
   for bit in (0,1):
    child=node+(bit,); tokens[child]=nxt; creation[child]=s
    children.append(nxt); nxt+=1
   edge=set(children)
   for j,bit in enumerate(node): edge.add(tokens[node[:j]+(1-bit,)])
   edges.append((node,edge))
 final=tuple(int(t is not None) for t in times)
 branch={tokens[final[:j]] for j in range(1,n+1)}
 assert len(branch)==n
 for node,edge in edges:
  assert edge&branch
  if node==final[:len(node)]: assert len(edge&branch)==1
 for j in range(1,n+1):
  x=tokens[final[:j]]
  assert any(edge&branch=={x} for node,edge in edges)
  settling=max([t for t in times[:j-1] if t is not None]+[0])
  assert creation[final[:j]]>=settling
  assert x>=creation[final[:j]]
 gamma={x for node,e in edges for x in e if (e-{x}).isdisjoint(branch)}
 assert gamma==branch
 return len(edges),len(tokens)
counts={'finite_enumeration_histories':0,'hyperedges_checked':0,'tokens_checked':0}
for n in range(1,6):
 for times in product((None,0,1,2,3),repeat=n):
  e,t=build(times,max(4,n)+1)
  counts['finite_enumeration_histories']+=1
  counts['hyperedges_checked']+=e; counts['tokens_checked']+=t
print(counts)
Path('workspace/agent2_hi_cototal_check.json').write_text(json.dumps(counts,indent=2))
