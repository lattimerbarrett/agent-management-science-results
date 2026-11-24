import networkx as nx,itertools,json
from pathlib import Path
E=[(0,6),(0,9),(0,11),(1,6),(1,11),(2,7),(2,8),(2,9),(2,10),(3,5),(3,6),(3,11),(4,5),(4,11),(6,11),(7,11),(8,11),(9,11),(10,11)]
H=nx.Graph(E)
def graph(q):
 G=H.copy();groups={1:[1],7:[7]}
 for u in [1,7]:
  for j in range(q-1):
   z=len(G);groups[u].append(z);G.add_edges_from((z,v)for v in H[u])
 return G,groups
def starforest(G):
 for C in nx.connected_components(G):
  ds=sorted((G.degree(u)for u in C),reverse=True)
  if len(C)>1 and ds != [len(C)-1]+[1]*(len(C)-1):return False
 return True
Gs={q:graph(q)for q in [3,4]};others=[u for u in H if u not in [1,7]];proof=[]
for mask in range(1<<len(others)):
 base={u for i,u in enumerate(others)if mask>>i&1}
 for x,y in itertools.product([0,'all'],[0,1,'all']):
  aa={}
  for q,(G,groups) in Gs.items():
   A=base|set(groups[1] if x=='all' else [])|set(groups[7] if y=='all' else groups[7][:y])
   if G.subgraph(set(G)-A).number_of_edges() or not starforest(G.subgraph(A)):break
   aa[q]=A
  if len(aa)<2:continue
  lines=[]
  for u in base:
   d3=Gs[3][0].subgraph(aa[3]).degree(u);d4=Gs[4][0].subgraph(aa[4]).degree(u);lines.append((d4-d3,4*d3-3*d4))
  assert any(s>=1 and 3*(s-1)+c>=3 for s,c in lines),(base,x,y,lines)
  proof.append({'base':sorted(base),'x':x,'y':y,'lines':lines})
print('all symbolic q>=3 cases pass:',len(proof))
Path('workspace/agent3_star_family_symbolic.json').write_text(json.dumps(proof))
Path('workspace/agent3_star_family_checks.py').write_text(Path(__file__).read_text())
