"""Exact finite-hole audit by fixed internal graph types and hitting-set CEGAR.
Nonactive H vertices can always be embedded in the infinite pure bulk.
"""
import networkx as nx,z3,itertools,time

def internal_types():
 out=[nx.Graph()]
 for G in nx.graph_atlas_g():
  if not len(G) or any(G.degree(v)==0 for v in G):continue
  if max(dict(G.degree()).values())>2:continue
  if len(nx.max_weight_matching(G,maxcardinality=True))>2:continue
  out.append(nx.convert_node_labels_to_integers(G))
 return out

def minholes(H,A,B,limit=500,cap=None):
 qa,qb=len(A),len(B);q=qa+qb;n=len(H)
 holes={(i,j):z3.Bool('hole_%d_%d'%(i,j)) for i in range(qa) for j in range(qb)}
 col=[z3.Bool('c%d'%v) for v in range(n)]
 active=[z3.Or(*[col[v]==col[u] for u in H.neighbors(v)]) for v in range(n)]
 mp=[z3.Int('m%d'%v) for v in range(n)]
 inner=z3.Solver();inner.set(timeout=10000)
 for v in range(n):
  inner.add(z3.If(active[v],z3.If(col[v],z3.And(mp[v]>=qa,mp[v]<q),z3.And(mp[v]>=0,mp[v]<qa)),mp[v]==-1))
 for u,v in itertools.combinations(range(n),2):inner.add(z3.Implies(z3.And(active[u],active[v]),mp[u]!=mp[v]))
 terms=[]
 for u,v in A.edges:terms.extend([(u,v,None),(v,u,None)])
 for u,v in B.edges:terms.extend([(qa+u,qa+v,None),(qa+v,qa+u,None)])
 for (i,j),h in holes.items():terms.extend([(i,qa+j,h),(qa+j,i,h)])
 for u,v in H.edges:
  allows=[z3.And(mp[u]==i,mp[v]==j) if h is None else z3.And(mp[u]==i,mp[v]==j,z3.Not(h)) for i,j,h in terms]
  inner.add(z3.Implies(z3.And(active[u],active[v]),z3.Or(*allows)))
 outer=z3.Optimize();outer.set(timeout=10000)
 M=z3.Sum([z3.If(h,1,0) for h in holes.values()]) if holes else z3.IntVal(0);outer.minimize(M)
 if cap is not None:outer.add(M<=cap)
 for iteration in range(limit):
  ck=outer.check()
  if ck!=z3.sat:return {'status':str(ck),'iterations':iteration}
  om=outer.model();hs={ij for ij,h in holes.items() if z3.is_true(om.eval(h,model_completion=True))}
  status=inner.check(*[h if ij in hs else z3.Not(h) for ij,h in holes.items()])
  if status==z3.unsat:return {'status':'ok','holes':len(hs),'hole_edges':sorted(hs),'iterations':iteration}
  if status!=z3.sat:return {'status':str(status),'iterations':iteration}
  im=inner.model();maps=[im.eval(m).as_long() for m in mp];used=set()
  for u,v in H.edges:
   a,b=maps[u],maps[v]
   if a<0 or b<0:continue
   if a>=qa:a,b=b,a
   if a<qa<=b:used.add((a,b-qa))
  if not used:return {'status':'impossible','iterations':iteration}
  outer.add(z3.Or(*[holes[ij] for ij in used]))
 return {'status':'limit','iterations':limit}

if __name__=='__main__':
 ts=internal_types();print('internal types:',len(ts),[(len(G),G.number_of_edges()) for G in ts])
 H=nx.Graph();H.add_nodes_from(range(7));H.add_edges_from((0,i) for i in range(1,7));H.add_edges_from([(1,2),(3,4),(5,6)])
 # Three-fan: known extremal internal graph two triangles (6 edges), cross-complete.
 tri=nx.disjoint_union(nx.complete_graph(3),nx.complete_graph(3));empty=nx.Graph()
 assert minholes(H,tri,empty)['status']=='ok'
 print('sanity:',minholes(H,tri,empty),minholes(H,tri,tri))
