import networkx as nx,itertools as it,json,math
M=10
H=nx.Graph();groups={};meta={};n=0
for i in range(3):
 for p in range(2):
  groups[i,p]=list(range(n,n+M));n+=M;H.add_nodes_from(groups[i,p])
 for a in groups[i,0]:
  for b in groups[i,1]:H.add_edge(a,b)
profiles=[]
# actual vertex record=(variable,polarity)
for i in range(3):
 vertices=[];edges=[];spec={}
 def add(v,p):
  global n
  x=n;n+=1;H.add_node(x);spec[x]=(v,p);vertices.append(x)
  for y in groups[v,1-p]:H.add_edge(x,y)
  return x
 def star(d,pol=0):
  a=add(i,pol);ls=[add((i+1)%3,pol) for _ in range(d)]
  edges.extend((a,b) for b in ls);return a
 if i==0:
  for _ in range(2):
   a=add(i,0);b=add((i+1)%3,0);edges.append((a,b))
 elif i==1:center=star(5)
 else:star(4);a=add(i,1);b=add((i+1)%3,1);edges.append((a,b))
 H.add_edges_from(edges);profiles.append((vertices,edges,spec))
assert len(H)==77
assert not nx.is_bipartite(H)
assert nx.is_bipartite(H.subgraph(set(H)-{center}))
checks=[]
for bits in it.product(range(2),repeat=3):
 c={x:bits[i]^p for (i,p),xs in groups.items() for x in xs}
 for vs,es,sp in profiles:
  c.update({x:bits[v]^p for x,(v,p) in sp.items()})
 mono={(min(a,b),max(a,b)) for a,b in H.edges() if c[a]==c[b]}
 active=[i for i in range(3) if bits[i]==bits[(i+1)%3]]
 expected={(min(a,b),max(a,b)) for i in active for a,b in profiles[i][1]}
 assert mono==expected
 checks.append({'bits':bits,'active':active,'monoedges':len(mono)})
 if active==[1]:
  c3=c.copy();c3[center]=2
  assert all(c3[a]!=c3[b] for a,b in H.edges())
  # Actual explicit embedding into complete bipartite plus K1,5:
  # all same-colour edges in c are exactly the five star edges.
  assert len(mono)==5
# Exhaustively classify all isolate-free admissible gadgets <=7 vertices.
allowed=[]
for G in nx.graph_atlas_g():
 if not len(G) or any(d==0 for _,d in G.degree()):continue
 if max(dict(G.degree()).values())<=4 and len(nx.max_weight_matching(G,maxcardinality=True))<=1:
  assert nx.is_connected(G)
  assert nx.is_isomorphic(G,nx.star_graph(len(G)-1)) or nx.is_isomorphic(G,nx.complete_graph(3))
  allowed.append(G)
assert max(G.number_of_edges() for G in allowed)==4
maxsplit=0;maxpairs=[]
for A in allowed:
 for B in allowed:
  if (max(dict(A.degree()).values())>=4 and B.number_of_edges()) or (max(dict(B.degree()).values())>=4 and A.number_of_edges()):continue
  e=A.number_of_edges()+B.number_of_edges()
  if e>maxsplit:maxsplit=e;maxpairs=[]
  if e==maxsplit:maxpairs.append((list(A.edges()),list(B.edges())))
assert maxsplit==6
assert all(len(a)==len(b)==3 for a,b in maxpairs)
result={'vertices':len(H),'edges':H.number_of_edges(),'critical_vertex':center,'orientation_checks':checks,'allowed_gadgets':[(len(G),G.number_of_edges(),sorted(dict(G.degree()).values())) for G in allowed],'maxsplit':maxsplit,'number_max_pairs':len(maxpairs)}
print(result)
with open('workspace/agent3_r2_realizer.json','w') as f:json.dump({'edges':list(H.edges()),'result':result},f)
