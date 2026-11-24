import networkx as nx,itertools,json,os

def wide_coloring(G):
 V=list(G); N={v:set(G[v]) for v in V}
 # exact largest packing, only used on small verification instances
 reps=[]
 for r in range(1,len(V)+1):
  found=None
  for C in itertools.combinations(V,r):
   if all(not (N[a]&N[b]) for a,b in itertools.combinations(C,2)):
    found=list(C);break
  if found is None: break
  reps=found
 assert len(reps)<=4
 L={v:tuple(i for i,r in enumerate(reps) if N[v]&N[r]) for v in V}
 assert all(L[v] for v in V)
 S={i:{v for v in V if L[v]==(i,)} for i in range(len(reps))}
 core={v for v in V if len(L[v])>=2}
 B=G.subgraph(core)
 assert nx.is_bipartite(B)
 parity=nx.bipartite.color(B)
 col={}
 for v in V:
  if len(L[v])==1: col[v]=('singleton',L[v][0])
  else: col[v]=('core',parity[v],tuple(i for i in S if N[v]&S[i]))
 for a,b in G.edges():
  assert col[a]!=col[b]
  # Every three-walk x-a-b-y must have distinct endpoint colors.
  for x in N[a]:
   for y in N[b]: assert col[x]!=col[y],(G.edges(),reps,col,x,a,b,y)
 # The actual homomorphism into the universal finite triangle-free target.
 image={v:(col[v],frozenset(col[w] for w in N[v])) for v in V}
 for u,v in G.edges():
  i,A=image[u];j,B=image[v]
  assert i in B and j in A and not A&B
 return col

def no35(G):
 for v in G:
  if any(G.has_edge(a,b) for a,b in itertools.combinations(G[v],2)):return False
 for C in itertools.permutations(G.nodes(),5):
  if C[0]!=min(C):continue
  if all(G.has_edge(C[i],C[(i+1)%5]) for i in range(5)):return False
 return True

count=0
for G in nx.graph_atlas_g():
 n=len(G)
 if n and min(dict(G.degree()).values())>n/5 and no35(G):
  wide_coloring(G);count+=1
print('All admissible unlabeled graphs through 7 vertices checked:',count)
# Test trianglefree universal target explicitly for m<=5.
for m in range(1,6):
 verts=[(i,frozenset(S)) for i in range(m) for r in range(m) for S in itertools.combinations([j for j in range(m) if j!=i],r)]
 H=nx.Graph();H.add_nodes_from(verts)
 for (i,S),(j,T) in itertools.combinations(verts,2):
  if i in T and j in S and not S&T:H.add_edge((i,S),(j,T))
 assert sum(nx.triangles(H).values())==0
 print('Universal target checked:',m,len(H),H.number_of_edges())
# Check the universal target triangle constraints symbolically at full m=36.
import z3
m=36
i,j,k=z3.Ints('i j k'); A,B,C=z3.BitVecs('A B C',m)
s=z3.Solver()
def member(t,S): return z3.Or(*[z3.And(t==r,z3.Extract(r,r,S)==1) for r in range(m)])
def adjacent(i,A,j,B): return z3.And(member(i,B),member(j,A),(A&B)==0)
s.add(i>=0,i<m,j>=0,j<m,k>=0,k<m)
s.add(adjacent(i,A,j,B),adjacent(j,B,k,C),adjacent(k,C,i,A))
assert s.check()==z3.unsat
print('Full m=36 universal target triangle constraints: UNSAT')
