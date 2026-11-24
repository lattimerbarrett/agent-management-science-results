import sys
sys.path.insert(0,'workspace')
import networkx as nx,itertools as it,json,z3
from pathlib import Path
G=nx.node_link_graph(json.load(open('workspace/agent2_glue_b_vs_clique.json')))
def embeds(a,bcliques,missing=(),timeout=30000,A_edges=None,B_edges=None):
 nlab=2+a+sum(bcliques);Apart={0}|set(range(2,2+a));Bpart=set(range(nlab))-Apart
 blocks={u:0 for u in range(2,2+a)};off=2+a
 for i,s in enumerate(bcliques,1):
  for u in range(off,off+s):blocks[u]=i
  off+=s
 miss={frozenset(x) for x in missing};adj=[]
 AE=None if A_edges is None else {frozenset(e) for e in A_edges};BE=None if B_edges is None else {frozenset(e) for e in B_edges}
 for x in range(nlab):
  for y in range(nlab):
   if x in Apart and y in Bpart or x in Bpart and y in Apart:yes=frozenset((x,y)) not in miss
   elif x==y==0:yes=True
   elif x!=y and x in blocks and y in blocks and blocks[x]==blocks[y]:
    if blocks[x]==0:yes=AE is None or frozenset((x-2,y-2)) in AE
    else:yes=BE is None or frozenset((x-2-a,y-2-a)) in BE
   else:yes=False
   if yes:adj.append((x,y))
 S=z3.Solver();S.set(timeout=timeout);vs=list(G);lab={v:z3.Int('l'+str(i)) for i,v in enumerate(vs)}
 for v in G:S.add(lab[v]>=0,lab[v]<nlab)
 for u,v in G.edges():S.add(z3.Or(*[z3.And(lab[u]==x,lab[v]==y) for x,y in adj]))
 for v in G:
  nei=[lab[w]==0 for w in G[v]]
  if nei:S.add(z3.Implies(lab[v]==0,z3.PbLe([(q,1) for q in nei],1)))
 for i in range(2,nlab):S.add(z3.PbLe([(lab[v]==i,1) for v in G],1))
 return str(S.check())
Bs=[nx.node_link_graph(x) for x in json.load(open('workspace/agent2_Bmaximal_small.json'))]
Bs.append(nx.disjoint_union(nx.complete_graph(4),nx.path_graph(2)))

def twoP3(F):
 ts=[set(t) for t in it.combinations(F,3) if F.subgraph(t).number_of_edges()>=2]
 return any(a.isdisjoint(b) for a,b in it.combinations(ts,2))
As=[]
for F in nx.graph_atlas_g():
 if len(F)<3 or not nx.is_connected(F) or twoP3(F) or max(dict(F.degree()).values())>=6:continue
 X=F.number_of_edges()-len(F)//2
 if X<2:continue
 As.append(F)
print('A candidates',len(As),flush=True)
count=0;free=[]
for bi,B in enumerate(Bs):
 for A in As:
  X=A.number_of_edges()-len(A)//2;Y=B.number_of_edges()
  if X+Y<9:continue
  res=embeds(len(A),[len(B)],A_edges=A.edges(),B_edges=B.edges())
  count+=1
  if res!='sat':
   row={'A':list(A.edges()),'B':list(B.edges()),'X':X,'Y':Y,'result':res}
   free.append(row);print('POSSIBLE RESCUE',row,flush=True)
 print('B type',bi,'done',flush=True)
print('checks',count,'free',len(free))
Path('workspace/agent3_conditional_matrix_results.json').write_text(json.dumps(free))
