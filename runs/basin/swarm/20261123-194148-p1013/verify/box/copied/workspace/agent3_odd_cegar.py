import networkx as nx,z3,itertools,time,json
from pathlib import Path

def bothtri(H):
 n=len(H);p=[z3.Bool('p'+str(u))for u in H];x=[z3.Bool('x'+str(u))for u in H];s=z3.Solver();s.add(p[0])
 for u,v in H.edges():s.add(z3.Implies(p[u]==p[v],z3.And(x[u],x[v])))
 for b in [False,True]:s.add(z3.PbLe([(z3.And(x[u],p[u]==b),1)for u in H],3))
 if s.check()==z3.unsat:return None
 m=s.model();return [z3.is_true(m.eval(p[u],model_completion=True))for u in H],[z3.is_true(m.eval(x[u],model_completion=True))for u in H]
Bsize=12;n=6+Bsize;cols={1:0,2:1,3:0,4:1,5:1};
for j,u in enumerate(range(6,n)):cols[u]=j%2
fixed=[(0,1),(0,2),(1,2),(3,4),(3,5)]+[(0,u)for u in [6,8,7,9,11,13]]
pool=[(u,v)for u in range(1,6)for v in range(6,n)if cols[u]!=cols[v]]
e={p:z3.Bool('e'+str(i))for i,p in enumerate(pool)};R=[z3.Bool('r'+str(u))for u in range(n)];edges=[(u,v,z3.BoolVal(True))for u,v in fixed]+[(u,v,e[u,v])for u,v in pool];s=z3.Solver()
for u,v,b in edges:s.add(z3.Implies(b,z3.Or(R[u],R[v])))
for u,v in pool:s.add(z3.Implies(z3.Xor(R[u],R[v]),e[u,v]))
mono=[z3.And(b,R[u],R[v])for u,v,b in edges];s.add(z3.PbEq([(b,1)for b in mono],3))
for u in range(n):s.add(z3.PbLe([(z3.And(b,R[x],R[y]),1)for x,y,b in edges if u in(x,y)],1))
start=time.time()
for it in range(10000):
 if s.check()==z3.unsat:print('UNSAT',n,it,time.time()-start);break
 m=s.model();E=fixed+[p for p in pool if z3.is_true(m.eval(e[p]))];H=nx.Graph();H.add_nodes_from(range(n));H.add_edges_from(E)
 mp=bothtri(H)
 if mp is None:
  data={'n':n,'edges':E,'matchingA':[u for u in range(n)if z3.is_true(m.eval(R[u]))]};print('COUNTER',it,data,flush=True);Path('workspace/agent3_odd_counter.json').write_text(json.dumps(data));break
 p,x=mp;missing=[e[u,v]for u,v in pool if p[u]==p[v]and not(x[u]and x[v])]
 assert all(not z3.is_true(m.eval(b))for b in missing)
 s.add(z3.Or(missing))
 if it%100==0:print(it,time.time()-start,flush=True)
Path('workspace/agent3_odd_cegar.py').write_text(Path(__file__).read_text())
