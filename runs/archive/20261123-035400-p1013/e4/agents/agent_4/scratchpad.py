import networkx as nx,itertools
G=nx.Graph([(0,5),(0,6),(0,7),(1,4),(1,7),(2,7),(3,4),(3,7),(0,8),(1,8),(2,8),(4,8),(5,8),(6,8)])
patterns={}
for mask in range(1<<9):
 A=[i for i in range(9) if mask>>i&1];B=[i for i in range(9) if not(mask>>i&1)]
 FA=G.subgraph(A);FB=G.subgraph(B)
 if FB.number_of_edges()!=1:continue
 if max(dict(FA.degree()).values(),default=0)>2:continue
 comps=[FA.subgraph(c) for c in nx.connected_components(FA) if len(c)>1]
 if any(len(c)>3 for c in comps) or sum(len(c)==3 for c in comps)>1:continue
 if not any(len(c)==3 for c in comps):continue
 key=tuple(sorted((len(c),c.number_of_edges()) for c in comps))
 patterns.setdefault(key,[]).append((A,B))
requirements=set()
for key,vals in patterns.items():
 for A,B in vals:
  FA=G.subgraph(A);FB=G.subgraph(B)
  C=next(c for c in nx.connected_components(FA) if len(c)==3);C=sorted(C)
  e=next(iter(FB.edges()))
  for pp in itertools.permutations(range(3)):
   for qq in itertools.permutations(range(2)):
    req=0
    for i,u in enumerate(C):
     for j,v in enumerate(e):
      if G.has_edge(u,v):req|=1<<(2*pp[i]+qq[j])
    requirements.add(req)
valid=[m for m in range(64) if all(m&q for q in requirements)]
print('requirements',len(requirements),'minimum',[q for q in requirements if not any(p!=q and p&q==p for p in requirements)])
print('min missing',min(m.bit_count() for m in valid),'patterns',[m for m in valid if m.bit_count()==min(x.bit_count() for x in valid)])
