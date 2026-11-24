import networkx as nx,itertools,mpmath as mp,pickle
L0=list(range(4)); L1=list(range(4,8))
R0=list(range(8,12)); R1=list(range(12,16))
S0=list(range(16,19)); S1=list(range(19,22));v=22
H=nx.Graph();H.add_nodes_from(range(23))
for A,B in [(L0,L1),(R0,R1),(S0,S1)]:H.add_edges_from(itertools.product(A,B))
H.add_edges_from([(4,8),(5,9),(6,10),(7,16),(17,14)])
H.add_edges_from([(v,0),(v,1),(v,12),(v,13)])
print('H vertices, edges:',len(H),H.number_of_edges())
print('H-v bipartite:',nx.is_bipartite(H.subgraph(range(22))))
g={w:0 for w in L0+R0+S0};g.update({w:1 for w in L1+R1+S1})
profiles=[]
for flips in itertools.product([0,1],repeat=3):
 c={v:0}
 for (A,B),f in zip([(L0,L1),(R0,R1),(S0,S1)],flips):
  for w in A+B:c[w]=g[w]^f
 mono=[(a,b) for a,b in H.edges() if c[a]==c[b]]
 M=nx.Graph();M.add_edges_from(mono)
 if max(dict(M.degree()).values(),default=0)<=1:
  profile=tuple(sum(c[a]==j for a,b in mono) for j in [0,1]);profiles.append(profile)
  print('matching coloring:',flips,'profile:',profile,'edges:',mono)
assert set(profiles)=={(4,0),(3,1)}
c=dict(g);c[v]=0
print('star coloring internal edges:',[(a,b) for a,b in H.edges() if c[a]==c[b]])
mp.mp.dps=30
I=[mp.besseli(j,2) for j in range(3)]
print('I0,I1,I2:',*[str(z) for z in I])
print('larger/smaller cycle weights:',I[0]/I[1],I[2]/I[1])
print('cycle difference coefficient I0-2I2:',I[0]-2*I[2])
pickle.dump(H,open('H23_bounded_counterexample.pkl','wb'))
