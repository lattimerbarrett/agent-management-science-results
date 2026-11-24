import z3,itertools,networkx as nx
roles=range(5) # a,b,p,q,r
B=5
N=B*5
s=z3.Solver()
w={(a,b):z3.Bool(f'w{a}{b}') for a in roles for b in roles if a<b}
c={(a,b):z3.Bool(f'c{a}{b}') for a in roles for b in roles}
def E(u,v):
 i,a=divmod(u,5);j,b=divmod(v,5)
 if u==v:return z3.BoolVal(False)
 if i==j:return w[min(a,b),max(a,b)]
 if i>j:i,j,a,b=j,i,b,a
 return c[a,b]
for a,b in [(0,2),(2,3),(3,4),(4,1)]:s.add(w[min(a,b),max(a,b)])
s.add(c[0,1],z3.Not(c[1,0]),z3.Not(w[0,1]))
# Force each side of ladder independent by C3 once enough blocks (also follows by odd girth).
s.add(z3.Not(c[0,0]),z3.Not(c[1,1]))
for v in itertools.combinations(range(N),3):s.add(z3.Not(z3.And(*(E(a,b) for a,b in itertools.combinations(v,2)))))
models=0;lemmas=0
while s.check()==z3.sat:
 m=s.model();g=nx.Graph();g.add_nodes_from(range(N))
 g.add_edges_from((a,b) for a,b in itertools.combinations(range(N),2) if z3.is_true(m.eval(E(a,b),model_completion=True)))
 found=False
 # Every 5-cycle contains edge ab and 4-edge simple path back.
 for a in range(N):
  for b in g[a]:
   for c1 in g[b]:
    if c1 in (a,b):continue
    for d in g[c1]:
     if d in (a,b,c1):continue
     for e in g[d]:
      if e not in (a,b,c1,d) and g.has_edge(e,a):
       cyc=[a,b,c1,d,e,a]
       s.add(z3.Not(z3.And(*(E(cyc[i],cyc[i+1]) for i in range(5)))))
       found=True;lemmas+=1;break
     if found:break
    if found:break
   if found:break
  if found:break
 if found:continue
 models+=1
 F=nx.Graph();F.add_nodes_from(g)
 for a in g:
  one=set(g[a]);three=set()
  for b in one:
   for cc in g[b]:three.update(g[cc])
  F.add_edges_from((a,b) for b in one|three if a!=b)
 clique=next((x for x in nx.find_cliques(F) if len(x)>=5),None)
 print('valid model',models,'edges',g.number_of_edges(),'clique',clique,flush=True)
 if clique is None:
  print('COUNTERMODEL',[(str(v),m.eval(v,model_completion=True)) for v in list(w.values())+list(c.values())],flush=True);break
 s.add(z3.Or(*(v!=m.eval(v,model_completion=True) for v in list(w.values())+list(c.values()))))
else:print('ALL MODELS EXHAUSTED',models,'cycle lemmas',lemmas)
