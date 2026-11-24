from itertools import combinations
import z3,time,json

def search(n,seconds=120,graphs=None):
 fs=list(combinations(range(n),4));ts=list(combinations(range(n),3));F={f:z3.Bool('f'+str(f)) for f in fs};T={t:z3.Bool('t'+str(t)) for t in ts}
 s=z3.Solver();s.set(timeout=seconds*1000)
 for t in ts:
  cnt=z3.Sum([z3.If(F[f],1,0) for f in fs if set(t)<=set(f)])
  s.add(z3.Or(cnt==0,cnt==2),T[t]==(cnt==2))
 for f in fs:
  s.add(z3.Or(F[f],z3.Sum([z3.If(T[t],1,0) for t in combinations(f,3)])<=2))
  if 0 in f and 1 in f:s.add(z3.Not(F[f]))
 for v in range(n):s.add(z3.Sum([z3.If(F[f],1,0) for f in fs if v in f])==(2*n-8 if v<2 else 2*n-6))
 for a,b in combinations(range(n),2):
  if (a,b)==(0,1):continue
  s.add(z3.Or([F[f] for f in fs if a in f and b in f]))
 for a,b in combinations(range(2,n),2):s.add(z3.Not(z3.And(T[(0,a,b)],T[(1,a,b)])))
 I,J=graphs
 m=n-2
 assert set(I)==set(J)==set(range(m))
 assert all(not J.has_edge(a,b) for a,b in I.edges())
 for a,b,c in combinations(range(m),3):
  ti=all(I.has_edge(x,y) for x,y in combinations((a,b,c),2));tj=all(J.has_edge(x,y) for x,y in combinations((a,b,c),2))
  s.add(F[(0,a+2,b+2,c+2)]==ti,F[(1,a+2,b+2,c+2)]==tj)

 tm=time.time();ans=s.check();print('onemissing',n,ans,time.time()-tm,flush=True)
 if ans==z3.sat:
  m=s.model();fac=[f for f in fs if z3.is_true(m.eval(F[f]))]
  json.dump(fac,open('workspace/agent1_icosapair'+str(n)+'.json','w'));print('facets',len(fac),flush=True)
  from sage.all import SimplicialComplex
  K=SimplicialComplex(fac);print('HOMOLOGY',K.homology(),flush=True)
 return ans
if __name__=='__main__':
 import networkx as nx,random,math
 rng=random.Random(1781923)
 def flag_sphere(m):
  G=nx.icosahedral_graph()
  for v in range(12,m):
   a,b=rng.choice(list(G.edges()));ns={a,b}|(set(G[a])&set(G[b]));assert len(ns)==4
   G.remove_edge(a,b);G.add_edges_from((v,x) for x in ns)
  return G
 def pack(I,J,steps=30000):
  m=len(I);pi=list(range(m));rng.shuffle(pi)
  def energy():return sum(I.has_edge(pi[a],pi[b]) for a,b in J.edges())
  val=energy();best=val
  for it in range(steps):
   if val==0:return nx.relabel_nodes(J,{i:pi[i] for i in range(m)})
   a,b=rng.sample(range(m),2);pi[a],pi[b]=pi[b],pi[a];nv=energy()
   temp=max(.10,2*(1-(it%5000)/5000))
   if nv<=val or rng.random()<math.exp((val-nv)/temp):val=nv
   else:pi[a],pi[b]=pi[b],pi[a]
   best=min(best,val)
  return None
 for m in [13,14,15,16]:
  for trial in range(3):
   I,J=flag_sphere(m),flag_sphere(m);J=pack(I,J)
   print('m',m,'trial',trial,'packed',J is not None,flush=True)
   if J is None:continue
   ans=search(m+2,20,(I,J))
   if ans==z3.sat:raise SystemExit
