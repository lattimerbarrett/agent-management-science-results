from pathlib import Path
from itertools import combinations
import json

def hits(m,edges): return all(m&e for e in edges)
def private(m,edges,x): return any((e&m)==x for e in edges)
def gamma_complement(m,edges,n):
 return sum((1<<x) for x in range(n) if any((e&(1<<x)) and not((e^(1<<x))&m) for e in edges))
counts={'hypergraphs':0,'fixed_point_tests':0,'minimal_transversals':0,'bounded_rank_reductions':0}
for n in range(1,5):
 U=(1<<n)-1; all_edges=list(range(1,U+1))
 for mask in range(1<<len(all_edges)):
  edges=[e for j,e in enumerate(all_edges) if mask>>j&1]
  counts['hypergraphs']+=1
  for m in range(U+1):
   minimal=hits(m,edges) and all(private(m,edges,1<<x) for x in range(n) if m>>x&1)
   assert minimal==(gamma_complement(m,edges,n)==m)
   counts['fixed_point_tests']+=1
   if not minimal: continue
   counts['minimal_transversals']+=1
   for p in range(U+1):
    if not hits(p,edges): continue
    # The induction step in the bounded-edge-size lemma.
    reduced=[e&~p for e in edges if not(e&(p&m))]
    remaining=m&~p
    assert hits(remaining,reduced)
    assert all(private(remaining,reduced,1<<x) for x in range(n) if remaining>>x&1)
    if edges and reduced:
     assert max(e.bit_count() for e in reduced)<max(e.bit_count() for e in edges)
    counts['bounded_rank_reductions']+=1
print(json.dumps(counts,sort_keys=True))
Path('workspace/agent2_hypergraph_checks.json').write_text(json.dumps(counts,indent=2))
