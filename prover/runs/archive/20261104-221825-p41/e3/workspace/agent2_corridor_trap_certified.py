import sys,json,itertools,time,pathlib,collections
sys.path.insert(0,'workspace')
from agent3_check import *
from agent4_fastcert import fastcert
from agent1_filling import check_certificate
from agent2_dim3_upper import prefix_order,boundary_extend

def convert(c):
 if c[0]=='s':return ('simplex',c[1])
 return ('shed',c[1],convert(c[2]),convert(c[3]))
a=json.load(open('workspace/agent2_saturation_corridor3_11_trace.json'));B=tuple(sorted(sum(1<<v for v in t) for t in a['base']));trace=[sum(1<<v for v in t) for t in a['order']]
c=convert(fastcert(B,0));assert check_certificate(B,0,c)
baseorder=[f for f,cc in prefix_order(B,0,c)];F=B;counts=collections.Counter()
for f in trace:
 S=all_faces(F);I=maximal(s for s in submasks(f) if s in S)
 assert f not in S and all(g.bit_count()==3 for g in I),(f,I)
 R=sum(1<<v for v in range(20) if f>>v&1 and f^(1<<v) in S)
 counts[R.bit_count()]+=1
 if R.bit_count()<=3:c=('shed',R,c,('simplex',f^R))
 else:c=boundary_extend(F,f,2,c)
 F=tuple(sorted(F+(f,)));assert check_certificate(F,2,c)
assert set(F)==set(a['facets'])
order=baseorder+trace
S=set()
for f in order:
 if S:
  I=maximal(g for g in submasks(f) if g in S);assert all(g.bit_count()==3 for g in I)
 S.update(submasks(f))
print('FULLSHELLING VERIFIED',len(order),'base',len(baseorder),'added',len(trace),'restrictioncounts',dict(counts),flush=True)
json.dump({'facets':F,'shelling':order,'k2certificate':c,'base':B,'basek0certificate':convert(fastcert(B,0))},open('workspace/agent2_corridor_trap_certified.json','w'))
pathlib.Path('workspace/agent2_corridor_trap_certified.py').write_text(pathlib.Path(__file__).read_text())
