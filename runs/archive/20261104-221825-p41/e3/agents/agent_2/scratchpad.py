import sys,json,collections
sys.path.insert(0,'workspace')
from agent3_check import *
F=tuple(json.load(open('workspace/agent2_corridor_trap_K1_certified.json'))['facets']);S=all_faces(F)
for v in range(20):
 D=maximal(g for g in S if not g>>v&1);low=[g for g in D if g.bit_count()!=4]
 print(v,'del lowfaces',len(low),'facets',len(D),flush=True)
