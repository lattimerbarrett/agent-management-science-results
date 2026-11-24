import networkx as nx,itertools,os

def template(m):
 G=nx.Graph();roles='apqrb'
 for i in range(m):
  for x,y in zip(roles,roles[1:]):G.add_edge((i,x),(i,y))
 for i in range(m):
  for j in range(i+1,m):G.add_edge((i,'a'),(j,'b'))
 return G

def odd3(G):
 F=nx.Graph();F.add_nodes_from(G)
 for u in G:
  for a in G[u]:
   F.add_edge(u,a)
   for b in G[a]:
    for v in G[b]:F.add_edge(u,v)
 return F

for m in range(3,13):
 G=template(m);F=odd3(G)
 support=[(i,r) for i in range(1,m-1) for r in 'apqrb']+[(0,'a'),(m-1,'b')]
 # Exhaustively enumerate maximal independent sets = maximal cliques of complement.
 alpha=max(map(len,nx.find_cliques(nx.complement(F.subgraph(support)))))
 assert alpha==m-1,(m,alpha)
 for i in range(1,m-1):
  pairs=[set(p) for p in itertools.combinations('apqrb',2) if not F.has_edge((i,p[0]),(i,p[1]))]
  assert pairs==[set('aq'),set('pr'),set('qb')],pairs
  for j in range(i+1,m-1):
   for pair1 in pairs:
    for pair2 in pairs:
     assert any(F.has_edge((i,x),(j,y)) for x in pair1 for y in pair2)
 for end in [(0,'a'),(m-1,'b')]:
  for i in range(1,m-1):
   permitted=[r for r in 'apqrb' if not F.has_edge(end,(i,r))]
   assert len(permitted)==2 and F.has_edge((i,permitted[0]),(i,permitted[1]))
 print(m,len(support),alpha,f'fractional lower {len(support)}/{alpha}')
print('All finite template claims checked, m=3..12.')
