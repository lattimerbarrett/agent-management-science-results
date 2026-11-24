import sys,json,itertools,collections,pathlib,time
sys.path.insert(0,'workspace')
from agent3_check import *
from agent4_fastcert import fastcert
from agent1_filling import check_certificate
from agent2_dim3_upper import prefix_order,boundary_extend

def convert(c):
 if c[0]=='s':return ('simplex',c[1])
 return ('shed',c[1],convert(c[2]),convert(c[3]))
a=json.load(open('workspace/agent2_saturation_corridor3_11_trace.json'));B=tuple(sorted(sum(1<<v for v in t) for t in a['base']));orig=[sum(1<<v for v in t) for t in a['order']]
ix=list(range(123))+[125,126,127,130,123,124,128,129];assert sorted(ix)==list(range(131))
trace=[orig[i] for i in ix];c=convert(fastcert(B,0));assert check_certificate(B,0,c)
baseorder=[f for f,cc in prefix_order(B,0,c)];F=B;counts=collections.Counter();s=None
for i,f in enumerate(trace):
 S=all_faces(F);I=maximal(g for g in submasks(f) if g in S)
 assert f not in S and all(g.bit_count()==3 for g in I),(i,f,I)
 R=sum(1<<v for v in range(20) if f>>v&1 and f^(1<<v) in S);counts[R.bit_count()]+=1
 if R.bit_count()==2:
  s=R;c=('shed',s,c,('simplex',f^s))
 elif R.bit_count()==3:
  assert R&s==s and c[0]=='shed' and c[1]==s,(i,f,R,s)
  L=tuple(sorted({g^s for g in F+(f,) if g&s==s}));lc=convert(fastcert(L,0))
  c=('shed',s,c[2],lc)
 elif R.bit_count()==4:c=boundary_extend(F,f,1,c)
 else:raise AssertionError((i,f,R))
 F=tuple(sorted(F+(f,)));assert check_certificate(F,1,c),(i,f)
assert set(F)==set(a['facets'])
order=baseorder+trace
S=set()
for f in order:
 if S:
  I=maximal(g for g in submasks(f) if g in S);assert all(g.bit_count()==3 for g in I)
 S.update(submasks(f))
print('FULL K1CERT + SHELLING VERIFIED',len(order),'restrictioncounts',dict(counts),flush=True)
json.dump({'facets':F,'shelling':order,'k1certificate':c,'base':B,'basek0certificate':convert(fastcert(B,0)),'trace_permutation':ix},open('workspace/agent2_corridor_trap_K1_certified.json','w'))
pathlib.Path('workspace/agent2_corridor_trap_K1_certified.py').write_text(pathlib.Path(__file__).read_text())
