import networkx as nx,itertools,math,json
from fractions import Fraction as F
from pathlib import Path

def stats(G,upto=3):
 es=list(G.edges());out=[0]*(upto+1)
 for j in range(upto+1):
  for E in itertools.combinations(es,j):
   P=nx.Graph();P.add_edges_from(E)
   if any(d>2 for v,d in P.degree()) or not nx.is_forest(P):continue
   out[j]+=2**nx.number_connected_components(P)
 return out
S=nx.star_graph(15);R=nx.disjoint_union(nx.star_graph(7),nx.cycle_graph(8))
w=lambda G:sum(math.comb(d,2) for v,d in G.degree())
assert len(S)==len(R)==16 and S.number_of_edges()==R.number_of_edges()==15
assert w(S)==105 and w(R)==29 and w(S)-w(R)==76
# Empty graph is_forest raises; compute constant separately below.
def low(G):
 e=G.number_of_edges();wg=w(G)
 out=[1,2*e,0,0]
 es=list(G.edges())
 for j in [2,3]:
  for E in itertools.combinations(es,j):
   P=nx.Graph();P.add_edges_from(E)
   if any(d>2 for v,d in P.degree()) or not nx.is_forest(P):continue
   out[j]+=2**nx.number_connected_components(P)
 assert out[2]==4*math.comb(e,2)-2*wg
 log2=out[2]-F(out[1]**2,2)
 assert log2==-2*(e+wg)
 return {'e':e,'w':wg,'poly_first4':out,'log_z2':str(log2)}
a,b=low(S),low(R)
assert F(a['log_z2'])-F(b['log_z2'])==-152
q=F(3,4);shift=F(152)/q**2
print(a,b,'endpoint advantage shift',shift,float(shift))
# high-wedge U formula, and positivity of exact leading quadratic
for U in range(3,15):
 X=nx.complete_graph(3);X.add_edges_from((0,j) for j in range(3,U))
 d=low(X);assert d['w']==math.comb(U-1,2)+2
 for p in range(1,U+1):
  for t in [1,2,5]:
   m=U+8*t
   assert m-math.ceil((m-U+p)/8)<m-t
Path('workspace/agent2_endpoint_wedge_checks.json').write_text(json.dumps({'star16':a,'star8_cycle8':b,'advantage_shift_r4':str(shift)},indent=2))
Path('workspace/agent2_endpoint_wedge_checks.py').write_text(Path(__file__).read_text())
