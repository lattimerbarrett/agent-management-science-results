exec(open('interval_product.py').read().split('S=list(')[0])
import networkx as nx
n=13
Q=list(itertools.combinations(range(n),2));ql=lambda x,y:x==y or x[1]<y[0]
ans,rr=solve(Q,ql,3,2000)
S=list(itertools.product(range(2),range(3)))
sl=lambda x,y:x==y or (x[0]==0 and y[0]==1 and x[1]!=y[1])
E=list(itertools.product(S,Q));le=lambda a,b:sl(a[0],b[0]) and ql(a[1],b[1])
cp,covers,lo,up=data(E,le);N=len(E);t=4
print('lazy',N,len(cp),len(covers),flush=True)
solver=z3.Solver();solver.set(timeout=10000)
colors=[z3.Int('c%d'%i) for i in range(len(cp))]
solver.add([z3.And(c>=0,c<t) for c in colors]);
# symmetry: any dimension forces all 4 colors if Q dim4. fix first cp color0
solver.add(colors[0]==0)
base=nx.DiGraph();base.add_nodes_from(range(N));base.add_edges_from(covers)
edge_index={(j,i):k for k,(i,j) in enumerate(cp)}
st=time.time();num=0
for iteration in range(3000):
 ans=solver.check()
 if ans!=z3.sat:print('finished',ans,flush=True);break
 m=solver.model();cs=[m.eval(c).as_long() for c in colors]
 new=0
 graphs=[]
 for c in range(t):
  graph=base.copy();graph.add_edges_from([(j,i) for k,(i,j) in enumerate(cp) if cs[k]==c]);graphs.append(graph.copy())
  for repeat in range(200):
   try:cycle=nx.find_cycle(graph)
   except nx.NetworkXNoCycle:break
   indices=[edge_index[u,v] for u,v in cycle if (u,v) in edge_index]
   assert indices
   solver.add(z3.Or([colors[k]!=c for k in indices]));new+=1
   for k in indices:
    a,b=cp[k];graph.remove_edge(b,a)
 if not new:
  print('SAT REALIZER',flush=True)
  ranks=[]
  for graph in graphs:
   order=list(nx.topological_sort(graph));ranks.append([order.index(i) for i in range(N)])
  assert all(le(E[i],E[j])==all(r[i]<=r[j] for r in ranks) for i in range(N) for j in range(N))
  json.dump({'n':n,'ranks':ranks},open('lazy_counterexample.json','w'));break
 num+=new
 if iteration%10==0:print(iteration,new,num,time.time()-st,flush=True)
 if time.time()-st>160:break
