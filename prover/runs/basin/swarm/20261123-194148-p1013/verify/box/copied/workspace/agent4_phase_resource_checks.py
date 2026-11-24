import z3,networkx as nx,json,time
Fs=nx.Graph([(0,6),(0,9),(0,11),(1,6),(1,11),(2,7),(2,8),(2,9),(2,10),(3,5),(3,6),(3,11),(4,5),(4,11),(6,11),(7,11),(8,11),(9,11),(10,11)])
Fp=nx.Graph(json.load(open('workspace/agent3_allcycle_p4_counter.json'))['edges'])
for name,H,T in [('star',Fs,nx.star_graph(3)),('path',Fp,nx.path_graph(4))]:
 a={u:z3.Bool('a'+str(u))for u in H};s=z3.Optimize();D=max(dict(T.degree()).values())
 s.add([z3.Implies(a[u],z3.PbLe([(a[w],1)for w in H[u]],D))for u in H if H.degree(u)>D])
 s.add([z3.Implies(z3.Not(a[u]),z3.PbLe([(z3.Not(a[w]),1)for w in H[u]],1))for u in H if H.degree(u)>1])
 obj=z3.Sum([z3.If(z3.And(z3.Not(a[u]),z3.Not(a[v])),1,0)for u,v in H.edges]);s.minimize(obj)
 it=0
 while s.check()==z3.sat:
  m=s.model();A={u for u in H if z3.is_true(m.eval(a[u]))};bad=[]
  for c in nx.connected_components(H.subgraph(A)):
   if len(c)>len(T)or not nx.algorithms.isomorphism.GraphMatcher(T,H.subgraph(c)).subgraph_is_monomorphic():bad.append(c)
  if not bad:
   print(name,'q',m.eval(obj),'A',sorted(A),'Bedge',list(H.subgraph(set(H)-A).edges()),'it',it);break
  for c in bad:s.add(z3.Or([z3.Not(a[u])for u in c]))
  it+=1
open('workspace/agent4_phase_resource_checks.py','w').write(open(__file__).read())
