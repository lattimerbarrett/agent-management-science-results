import itertools,time,z3

def test(n,k,timeout=60000):
 Q=[(i,) for i in range(n)]+list(itertools.combinations(range(n),2))
 X=list(itertools.product(range(8),range(len(Q))))
 def le(x,y): return x[0]&y[0]==x[0] and set(Q[x[1]])<=set(Q[y[1]])
 N=len(X); less=[[le(x,y) for y in X] for x in X]
 D=[{j for j in range(N) if j!=i and less[j][i]} for i in range(N)]
 U=[{j for j in range(N) if j!=i and less[i][j]} for i in range(N)]
 crit=[(i,j) for i in range(N) for j in range(N) if not less[i][j] and not less[j][i] and D[i]<=D[j] and U[j]<=U[i]]
 print('n,k,N,crit',n,k,N,len(crit),flush=True)
 s=z3.Solver();s.set(timeout=timeout)
 # critical reversal colors, ranks give acyclicity
 c=[z3.Int('c'+str(i)) for i in range(len(crit))]
 for x in c:s.add(x>=0,x<k)
 for i in range(min(k,len(crit))):s.add(c[i]<=i)
 arcs=[(i,j) for i,(x,y) in enumerate(crit) for j,(xx,yy) in enumerate(crit) if less[x][yy]]
 for i,j in arcs:
  if i<j and (j,i) in arcs:s.add(c[i]!=c[j])
 ranks=[[z3.Int(f'r{a}_{i}') for i in range(len(crit))] for a in range(k)]
 for a in range(k):
  for i,j in arcs:s.add(z3.Implies(z3.And(c[i]==a,c[j]==a),ranks[a][i]<ranks[a][j]))
 start=time.time();r=s.check();print(r,'time',time.time()-start,flush=True)
 if r==z3.sat:
  model=s.model(); cols=[model[x].as_long() for x in c];print('colors',cols,flush=True)
  # independently verify no monochromatic cycles
  import networkx as nx
  for a in range(k):
   G=nx.DiGraph();G.add_nodes_from(i for i in range(len(crit)) if cols[i]==a);G.add_edges_from((i,j) for i,j in arcs if cols[i]==a and cols[j]==a)
   assert nx.is_directed_acyclic_graph(G)
 return r
for n,k in [(3,5),(4,5),(5,6),(6,6)]:test(n,k)
