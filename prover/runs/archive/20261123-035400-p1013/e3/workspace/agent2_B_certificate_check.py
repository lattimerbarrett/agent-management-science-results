import networkx as nx,itertools,json
H=nx.node_link_graph(json.load(open('workspace/agent2_glue_b_vs_clique.json')));h=len(H)
C=json.load(open('workspace/agent2_B_upper_explicit_certificates.json'))
def good(G):
 if max(dict(G.degree()).values(),default=0)>3:return False
 p=[set(t) for t in itertools.combinations(G,3) if G.subgraph(t).number_of_edges()>=2]
 return not any(a.isdisjoint(b) for a,b in itertools.combinations(p,2))
levels={1:[nx.empty_graph(1)]}
for n in range(2,8):
 out=[]
 for F in levels[n-1]:
  E=[v for v in F if F.degree(v)<3]
  for k in range(1,min(3,len(E))+1):
   for nei in itertools.combinations(E,k):
    G=F.copy();G.add_node(n-1);G.add_edges_from((n-1,v) for v in nei)
    if good(G) and not any(nx.is_isomorphic(G,T) for T in out):out.append(G)
 levels[n]=out
patterns=[]
for c in C:
 F=nx.from_graph6_bytes(c['F_graph6'].encode());B=F.copy()
 for _ in range(c['f']):B=nx.disjoint_union(B,nx.path_graph(2))
 assert len(B)==c['B_nodes'] and set(B.edges())=={tuple(e) for e in c['B_edges']}
 assert B.number_of_edges()>=8
 if len(F):assert c['f']==max(0,8-F.number_of_edges());patterns.append(F)
 else:assert c['f']==8
 mp={tuple(v):x for v,x in c['map']};assert set(mp)==set(H) and len(set(mp.values()))==h
 assert all(0<=x<2*h+len(B)+h for x in mp.values())
 def adj(x,y):
  if x<2*h and y<2*h:return x!=y and x//2==y//2
  if (x<2*h)!=(y<2*h):return True
  x-=2*h;y-=2*h
  return x<len(B) and y<len(B) and B.has_edge(x,y)
 assert all(adj(mp[u],mp[v]) for u,v in H.edges())
assert len(C)==22 and len(patterns)==21
assert all(any(nx.is_isomorphic(F,G) for F in patterns) for n in range(3,8) for G in levels[n])
print('PASS: exhaustive type generation and22 explicit injectiveH embedding certificates; NO SAT SOLVER')
