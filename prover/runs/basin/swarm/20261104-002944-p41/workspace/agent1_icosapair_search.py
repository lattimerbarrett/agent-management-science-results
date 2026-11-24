from itertools import combinations
import z3,time,json

def search(n,seconds=120):
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
 import networkx as nx
 I=nx.icosahedral_graph();J=nx.Graph();J.add_nodes_from(I)
 for a,b in combinations(range(12),2):
  if nx.shortest_path_length(I,a,b)==2:J.add_edge(a,b)
 assert len(I.edges())==len(J.edges())==30 and not(set(I.edges())&set(J.edges()))
 for a,b,c in combinations(range(12),3):
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
 search(14,600)
