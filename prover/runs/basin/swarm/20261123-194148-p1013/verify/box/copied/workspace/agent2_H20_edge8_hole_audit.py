import sys,networkx as nx,json,time
from pathlib import Path
sys.path.insert(0,'workspace');from agent2_hole_cegar import minholes
E=json.loads(Path('workspace/agent2_normal_audit_H20.json').read_text());H=nx.Graph();H.add_nodes_from(range(20));H.add_edges_from(E)
Cs=[]
for k in range(2,8):Cs.append((nx.path_graph(k),k//2,'P'+str(k)))
for k in range(3,8):Cs.append((nx.cycle_graph(k),k//2,'C'+str(k)))
types=[]
def rec(start,budget,gs,names):
 G=nx.disjoint_union_all(gs) if gs else nx.Graph();types.append((G,tuple(names)))
 for i in range(start,len(Cs)):
  C,c,name=Cs[i]
  if c<=budget:rec(i,budget-c,gs+[C],names+[name])
rec(0,3,[],[])
st=time.time();allowed=[]
for G,name in types:
 r=minholes(H,G,nx.Graph(),limit=1)
 if r['status']=='ok':allowed.append((G,name))
print('allowedtypes',len(allowed),'time',time.time()-st,flush=True)
out=[]
for i,(A,an) in enumerate(allowed):
 for j in range(i,len(allowed)):
  B,bn=allowed[j];I=A.number_of_edges()+B.number_of_edges()
  if I<8:continue
  r=minholes(H,A,B,cap=I-8);out.append((I,an,bn,r))
  if r['status']=='ok':print('POSITIVEHOLEEDGEIMPROVEMENT',I,an,bn,r,flush=True)
print('tested',len(out),'secs',time.time()-st,'statuses',{s:sum(r[3]['status']==s for r in out) for s in set(r[3]['status'] for r in out)},flush=True)
Path('workspace/agent2_H20_edge8_hole_audit.json').write_text(json.dumps(out,indent=2))
assert all(r[3]['status']=='unsat' for r in out)
normalA=nx.disjoint_union(nx.complete_graph(3),nx.complete_graph(3))
normalB=nx.path_graph(2)
assert minholes(H,normalA,normalB,cap=0)['status']=='ok'
assert nx.is_bipartite(H.subgraph(range(19)))
assert H.subgraph(range(8)).number_of_edges()==4
assert max(dict(H.subgraph(range(8)).degree()).values())==1
assert H.subgraph(range(8,20)).number_of_edges()==0
co=nx.bipartite.color(H.subgraph(range(19)))
assert sorted(sum(co[x]==c for x in H.neighbors(19)) for c in [0,1])==[3,3]
print('Exact finite normality certificate passed: all edge bonuses <=7, normal bonus7 attained.')
if __file__.endswith('scratchpad.py'):
 Path('workspace/agent2_H20_edge8_hole_audit.py').write_text(Path(__file__).read_text())
