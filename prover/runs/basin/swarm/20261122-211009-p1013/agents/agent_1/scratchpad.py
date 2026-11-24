import z3,itertools,time,networkx as nx,json

def witness(s,es,n,name,J):
 B=[z3.Bool(name+'b'+str(i)) for i in range(n)]
 comp=[z3.Int(name+'c'+str(i)) for i in range(n)]
 pos=[z3.Int(name+'p'+str(i)) for i in range(n)]
 for i in range(n):s.add(comp[i]>=0,comp[i]<=i,pos[i]>=0,pos[i]<len(J))
 for u,v in itertools.combinations(range(n),2):
  adj=z3.Or(*[z3.And(pos[u]==a,pos[v]==b) for a,b in list(J.edges())+[(b,a) for a,b in J.edges()]])
  s.add(z3.Implies(es[u,v],z3.And(z3.Not(z3.And(B[u],B[v])),z3.Or(B[u],B[v],z3.And(comp[u]==comp[v],adj)))))
  s.add(z3.Implies(z3.And(z3.Not(B[u]),z3.Not(B[v]),comp[u]==comp[v]),pos[u]!=pos[v]))
 return B

def search(q,seconds=90):
 p=4;n=q+p+1; X=range(1,p+1);Y=range(p+1,n);pairs=list(itertools.combinations(range(n),2));es={}
 for u,v in pairs:
  if u==0 and v in X:es[u,v]=z3.BoolVal(True)
  elif u==0 or (u in X and v in Y):es[u,v]=z3.Bool(f'e{u}_{v}')
  else:es[u,v]=z3.BoolVal(False)
 s=z3.Solver();s.set(timeout=20000)
 s.add(z3.PbGe([(es[0,y],1) for y in Y],p))
 # Order Y by their adjacency bit codes (symmetry breaking).
 for y in range(p+1,n-1):
  s.add(z3.Sum([z3.If(es[x,y],1<<x,0) for x in range(p+1)])<=z3.Sum([z3.If(es[x,y+1],1<<x,0) for x in range(p+1)]))
 fork=nx.Graph([(0,1),(0,2),(0,3),(3,4)])
 for name,J in [('tri',nx.complete_graph(3)),('C4',nx.cycle_graph(4)),('P5',nx.path_graph(5)),('fork',fork)]:witness(s,es,n,name,J)
 start=time.time();it=0
 while time.time()-start<seconds:
  result=s.check()
  if result!=z3.sat:return str(result),it
  mod=s.model();G=nx.Graph();G.add_nodes_from(range(n));G.add_edges_from((u,v) for u,v in pairs if z3.is_true(mod.eval(es[u,v],model_completion=True)))
  found_decomp=False
  for name,J in [('P4',nx.path_graph(4)),('S3',nx.star_graph(3))]:
   ps=z3.Solver();constes={(u,v):z3.BoolVal(G.has_edge(u,v)) for u,v in pairs};bs=witness(ps,constes,n,'test',J)
   if ps.check()!=z3.sat:continue
   found_decomp=True;pm=ps.model();B=[i for i in range(n) if z3.is_true(pm.eval(bs[i],model_completion=True))];A=[i for i in range(n) if i not in B]
   terms=[es[u,v] for u,v in itertools.combinations(B,2)]
   # Exclude this cut being any union of subgraphs of J, via connected forbidden subgraphs on <=5 vertices.
   for k in range(3,6):
    for vs in itertools.combinations(A,k):
     possible=[e for e in itertools.combinations(vs,2) if not z3.is_false(es[e])]
     # All connected graph patterns; include minimal failures only by <=6 edges.
     for ecount in range(k-1,min(len(possible),k)+1):
      for ee in itertools.combinations(possible,ecount):
       F=nx.Graph();F.add_nodes_from(vs);F.add_edges_from(ee)
       if nx.is_connected(F) and (k>len(J) or not nx.isomorphism.GraphMatcher(J,F).subgraph_is_monomorphic()):terms.append(z3.And(*[es[e] for e in ee]))
   s.add(z3.Or(*terms));break
  if not found_decomp:return 'FOUND',it,sorted(G.edges())
  it+=1
 return 'TIME',it
for q in range(7,10):
 res=search(q,600);print(q,res,flush=True)
 if res[0]=='FOUND':json.dump(res,open('apex_k4_found.json','w'));break
