import networkx as nx,z3,sys,itertools,time,json
from pathlib import Path
sys.path.insert(0,'workspace');from agent2_hole_cegar import minholes

def embeds(H,FA,FB,holes):
 n=len(H);s=n+max(len(FA),len(FB));xs=[z3.Int('x'+str(i)) for i in range(n)];sol=z3.Solver();sol.set(timeout=3000);sol.add(z3.Distinct(xs));sol.add(*[z3.And(x>=0,x<2*s) for x in xs])
 for u,v in H.edges:
  x,y=xs[u],xs[v];cross=z3.And(x/s!=y/s,z3.Not(z3.Or(*[z3.Or(z3.And(x==i,y==s+j),z3.And(y==i,x==s+j)) for i,j in holes])))
  ine=[]
  for F,shift in [(FA,0),(FB,s)]:
   for a,b in F.edges:ine.extend([z3.And(x==shift+a,y==shift+b),z3.And(y==shift+a,x==shift+b)])
  sol.add(z3.Or(cross,*ine))
 return str(sol.check())
H=nx.Graph();H.add_nodes_from(range(7));H.add_edges_from((0,i) for i in range(1,7));H.add_edges_from([(1,2),(3,4),(5,6)])
F=nx.disjoint_union(nx.complete_graph(3),nx.complete_graph(3));r=minholes(H,F,F);holes=set(map(tuple,r['hole_edges']));assert embeds(H,F,F,holes)=='unsat'
st=time.time();counter=[];wits=[]
for e in holes:
 newholes=holes-{e};ok=False
 for side in [0,1]:
  for f in list(F.edges):
   A=F.copy();B=F.copy();(A if side==0 else B).remove_edge(*f)
   if embeds(H,A,B,newholes)=='unsat':ok=True;wits.append((e,side,f));break
  if ok:break
 if not ok:counter.append(e)
print('cross-exchange fan3',len(holes),'holes','counter',counter,'seconds',time.time()-st)
Path('workspace/agent2_cross_exchange_fan3.json').write_text(json.dumps({'holes':list(holes),'counter':counter,'witnesses':wits}))
if __file__.endswith('scratchpad.py'):Path('workspace/agent2_cross_exchange_check.py').write_text(Path(__file__).read_text())
