p=open('workspace/agent4_cegar_search.py').read()
p=p.replace("for j,T in enumerate(required):embed_constraints(T,'req'+str(j),s,E)","req_vars=[embed_constraints(T,'req'+str(j),s,E) for j,T in enumerate(required)]")
p=p.replace("m=s.model();H=nx.Graph();H.add_nodes_from(range(n));H.add_edges_from(key for key,x in E.items() if z3.is_true(m.eval(x,model_completion=True)))",'''m=s.model();H=nx.Graph();H.add_nodes_from(range(n))
 vals=[]
 for xx in req_vars:
  ins,cp,ro=([m.eval(x,model_completion=True) for x in arr] for arr in xx)
  vals.append(([z3.is_true(x) for x in ins],[x.as_long() for x in cp],[x.as_long() for x in ro]))
 for u,v in E:
  if u and v and ((u<cut)==(v<cut)):continue
  yes=True
  for T,(ins,cp,ro) in zip(required,vals):
   yes &= (ins[u] or ins[v]) and (not(ins[u] and ins[v]) or (cp[u]==cp[v] and T.has_edge(ro[u],ro[v])))
  if yes:H.add_edge(u,v)''')
p=p.replace("open('workspace/agent4_cegar_checkpoint.smt2','w').write(s.to_smt2())","pass # checkpoint serialization too expensive")
p=p.replace("'workspace/agent4_cegar_search.py'","'workspace/agent4_cegar_maximal_search.py'")
exec(compile(p,'cegar_maximal','exec'))
