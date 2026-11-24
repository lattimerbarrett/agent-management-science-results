import sys,itertools,time,json,pathlib
import z3,networkx as nx
sys.path.insert(0,'workspace')
from agent2_homology_cuts import homology_cocycle_cuts

def search(n,seconds=60,maxmodels=30):
 V=range(n);tets=list(itertools.combinations(V,4));tris=list(itertools.combinations(V,3));edges=list(itertools.combinations(V,2))
 T={f:z3.Bool('t_'+''.join(map(lambda x:format(x,'x'),f))) for f in tets}
 Q={f:z3.Bool('q_'+''.join(map(lambda x:format(x,'x'),f))) for f in tris}
 s=z3.Solver();s.set(timeout=seconds*1000)
 for q in tris:
  incid=[T[f] for f in tets if set(q)<=set(f)]
  s.add(Q[q]==z3.Or(incid));s.add(z3.Or(z3.PbEq([(x,1) for x in incid],0),z3.PbEq([(x,1) for x in incid],2)))
 for e in edges:
  s.add(z3.PbGe([(T[f],1) for f in tets if set(e)<=set(f)],4))
 for v in V:
  s.add(z3.PbEq([(T[f],1) for f in tets if v in f],2*n-6))
 for f in tets:
  qs=[Q[q] for q in itertools.combinations(f,3)]
  s.add(z3.Implies(z3.Not(T[f]),z3.PbLe([(x,1) for x in qs],2)))
 s.add(T[0,1,2,3],T[0,1,2,4])
 print('built',n,flush=True)
 for modelno in range(maxmodels):
  ts=time.time();r=s.check();print(n,modelno,r,round(time.time()-ts,3),flush=True)
  if r!=z3.sat:return
  m=s.model();F=[f for f in tets if z3.is_true(m[T[f]])];tri=[q for q in tris if z3.is_true(m[Q[q]])]
  masks=[sum(1<<v for v in q) for q in tri];index={sum(1<<v for v in q):q for q in tris}
  added=0
  for p in [2,3,5,7]:
   cuts=homology_cocycle_cuts(n,masks,p)
   for cut in cuts:s.add(z3.Or([Q[index[q]] for q in cut]));added+=1
  print('cuts',added,flush=True)
  if added:continue
  # Each edge link must be connected cycle; each vertexlink connected follows with full graph if edge links all connected? Explicit check.
  bad=False
  for e in edges:
   g=nx.Graph()
   for f in F:
    if set(e)<=set(f):g.add_edge(*(set(f)-set(e)))
   if not nx.is_connected(g):bad=True;break
  if bad:
   print('bad edge link',e,flush=True)
   s.add(z3.Or([z3.Not(T[f]) if f in F else T[f] for f in tets]));continue
  out='workspace/agent2_homologysphere_'+str(n)+'.json';json.dump(F,open(out,'w'))
  print('POTENTIAL SPHERE SAVED',out,flush=True);return out

if __name__=='__main__':
 pathlib.Path('workspace/agent2_localflag_cegar.py').write_text(pathlib.Path(__file__).read_text())
 for n in [12,13,14,15]:
  if search(n,30,40):break
