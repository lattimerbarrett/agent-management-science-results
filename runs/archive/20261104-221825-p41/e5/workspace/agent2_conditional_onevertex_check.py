import json,sys,time,itertools
sys.path.insert(0,'workspace')
from exact_decomp_a4 import *
from a3_fastkd import kd as fast
from agent2_nearcone import nearcone_order
from agent2_VD_completion import completion
J=json.load(open('workspace/a3_bad_edge_add.json'))
C=complex_from_facets([frozenset(i for i in range(8) if f>>i&1) for f in J['facets']]);a=8
X=C;cone=[r|{a} for r in nearcone_order(C,1)]
for F in cone:
 X=X|subfaces(F)
 assert fast(tuple(sorted(sum(1<<v for v in f) for f in facets(X))),1)
assert fast(tuple(sorted(sum(1<<v for v in f) for f in facets(X))),0)
order=completion(X)
for F in order:
 assert F not in X;X=X|subfaces(F)
 assert fast(tuple(sorted(sum(1<<v for v in f) for f in facets(X))),0)
assert len(facets(X))==126
print('nearcone',len(cone),'VDcompletion',len(order))
json.dump({'nearcone':len(cone),'VDcompletion':len(order),'total':len(cone)+len(order)},open('workspace/agent2_conditional_onevertex_checks.json','w'))
