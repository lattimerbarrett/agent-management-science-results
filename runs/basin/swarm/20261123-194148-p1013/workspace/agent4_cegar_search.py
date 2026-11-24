import networkx as nx,z3,itertools,time,json
n=16
E={(u,v):z3.Bool(f'e{u}_{v}') for u in range(n) for v in range(u+1,n)}
def ez(u,v):return E[tuple(sorted((u,v)))]
def embed_constraints(T,prefix,solver,edges):
 k=len(T);inside=[z3.Bool(f'{prefix}i{v}') for v in range(n)];cp=[z3.Int(f'{prefix}c{v}') for v in range(n)];ro=[z3.Int(f'{prefix}r{v}') for v in range(n)]
 for v in range(n):solver.add(cp[v]>=0,cp[v]<=v,ro[v]>=0,ro[v]<k)
 tes=list(T.edges());tes+= [(b,a) for a,b in tes]
 for (u,v),e in edges.items():
  solver.add(z3.Implies(e,z3.Or(inside[u],inside[v])))
  solver.add(z3.Implies(z3.And(inside[u],inside[v],cp[u]==cp[v]),ro[u]!=ro[v]))
  solver.add(z3.Implies(z3.And(e,inside[u],inside[v]),z3.And(cp[u]==cp[v],z3.Or(*[z3.And(ro[u]==a,ro[v]==b) for a,b in tes]))))
 return inside,cp,ro

def find_embedding(H,T):
 s=z3.Solver();s.set(timeout=10000)
 ie={key:z3.BoolVal(H.has_edge(*key)) for key in E};xx=embed_constraints(T,'q',s,ie)
 status=s.check()
 if status==z3.unknown:raise RuntimeError('embedding solver timeout')
 if status==z3.unsat:return None
 m=s.model();ins,cp,ro=([m.eval(x,model_completion=True) for x in arr] for arr in xx)
 vals=([z3.is_true(x) for x in ins],[x.as_long() for x in cp],[x.as_long() for x in ro]);return vals
s=z3.Solver();s.set(timeout=120000)
cut=(n+1)//2
left=list(range(1,cut));right=list(range(cut,n))
for side in [left,right]:
 for u,v in itertools.combinations(side,2):s.add(z3.Not(ez(u,v)))
 for u,v in zip(side,side[1:]):
  s.add(z3.Implies(ez(0,v),ez(0,u)))
  if u!=side[0]:s.add(z3.Implies(ez(0,u)==ez(0,v),z3.Sum([z3.If(ez(u,w),1,0) for w in (right if side==left else left)])>=z3.Sum([z3.If(ez(v,w),1,0) for w in (right if side==left else left)])))
s.add(ez(0,1),ez(0,cut),ez(1,cut))
required=[nx.cycle_graph(3),nx.cycle_graph(4)]+list(nx.nonisomorphic_trees(5))
for j,T in enumerate(required):embed_constraints(T,'req'+str(j),s,E)
forbidden=[nx.path_graph(4),nx.star_graph(3)]
open('workspace/agent4_cegar_search.py','w').write(open(__file__).read())
start=time.time()
for it in range(10000):
 status=s.check()
 if status!=z3.sat:print('SYNTHESIS',status,'iteration',it);break
 m=s.model();H=nx.Graph();H.add_nodes_from(range(n));H.add_edges_from(key for key,x in E.items() if z3.is_true(m.eval(x,model_completion=True)))
 blocked=False
 for T in forbidden:
  wit=find_embedding(H,T)
  if wit is None:continue
  ins,cp,ro=wit;A=[v for v in range(n) if ins[v]];B=[v for v in range(n) if not ins[v]]
  bad=[ez(u,v) for u,v in itertools.combinations(B,2)]
  # Positive obstructions to the residual A graph lying in target packing.
  path_order=5 if max(dict(T.degree()).values())==2 else 4
  maxdeg=2 if path_order==5 else 3
  for u in A:
   if len(A)-1>=maxdeg+1:bad.append(z3.AtLeast(*[ez(u,v) for v in A if v!=u],maxdeg+1))
  for tri in itertools.combinations(A,3):bad.append(z3.And(*[ez(u,v) for u,v in itertools.combinations(tri,2)]))
  if path_order==5:
   for vs in itertools.combinations(A,4):
    a=vs[0]
    for rest in itertools.permutations(vs[1:]):
     if rest[0]<rest[-1]:
      cyc=(a,)+rest;bad.append(z3.And(*[ez(cyc[i],cyc[(i+1)%4]) for i in range(4)]))
  for vs in itertools.combinations(A,path_order):
   for pth in itertools.permutations(vs):
    if pth[0]<pth[-1]:bad.append(z3.And(*[ez(pth[i],pth[i+1]) for i in range(path_order-1)]))
  s.add(z3.Or(*bad));blocked=True
 if not blocked:
  print('FOUND',list(H.edges()));open('workspace/agent4_cegar_found.json','w').write(json.dumps(list(H.edges())));break
 if it%20==0:
  print('iteration',it,'e',len(H.edges()),'elapsed',round(time.time()-start,2),flush=True)
  open('workspace/agent4_cegar_checkpoint.smt2','w').write(s.to_smt2())
else:print('iteration limit')
print('elapsed',time.time()-start)
open('workspace/agent4_cegar_search.py','w').write(open(__file__).read())
