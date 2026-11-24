import sys,itertools,json,time,z3,random
sys.path.insert(0,'workspace')
src=open('workspace/agent4_2closed_search.py').read().split('def main():')[0];exec(src)

def purify(base,n,seconds=30):
 ts=list(itertools.combinations(range(n),3));fs=list(itertools.combinations(range(n),4))
 S={t:z3.Bool('s'+str(t)) for t in ts};X={f:z3.Bool('x'+str(f)) for f in fs}
 s=z3.SolverFor('QF_FD');s.set(timeout=seconds*1000)
 for t in base:s.add(S[tuple(sorted(t))])
 s.add(z3.Or([z3.Not(S[t]) for t in ts]))
 for f in fs:
  tt=list(itertools.combinations(f,3));rr=[S[t] for t in tt]
  s.add(X[f]==z3.And(rr))
  for i in range(4):s.add(z3.Or(rr[i],*[z3.Not(rr[j]) for j in range(4) if j!=i]))
 for t in ts:s.add(z3.Implies(S[t],z3.Or([X[tuple(sorted((*t,v)))] for v in range(n) if v not in t])))
 a=s.check()
 if a==z3.sat:
  m=s.model();fac=[f for f in fs if z3.is_true(m.eval(X[f]))];tri=[t for t in ts if z3.is_true(m.eval(S[t]))]
  assert all(sum(t in tri for t in itertools.combinations(f,3))!=3 for f in fs)
  assert set(tri)=={t for f in fac for t in itertools.combinations(f,3)}
  return a,{'n':n,'facets':fac,'triangles':tri}
 return a,None

rng=random.Random(736845);tm=time.time();counts={}
for n in [10,12,15,20]:
 for i in range(30):
  T,_=run(n,rng);a,data=purify(T,n,10);counts[str(a)]=counts.get(str(a),0)+1
  if a==z3.sat:
   print('FOUND',n,i,len(T),len(data['triangles']),len(data['facets']),flush=True)
   json.dump(data,open('workspace/agent3_purified_candidate.json','w'));break
 else:print('n',n,counts,time.time()-tm,flush=True);continue
 break
