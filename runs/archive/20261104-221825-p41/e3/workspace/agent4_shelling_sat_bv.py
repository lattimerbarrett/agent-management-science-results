import z3,itertools,json,time
for n in range(9,10):
 ts=list(itertools.combinations(range(n),4));ss=[q for size in range(1,4) for q in itertools.combinations(range(n),size)]
 N=len(ts); M=N*N+1; W=M.bit_length()+1
 V={t:z3.BitVec('v_'+str(t),W) for t in ts}
 R={t:z3.If(V[t]<N,N*V[t]+i+1,M) for i,t in enumerate(ts)}; T={q:z3.BitVec('t_'+str(q),W) for q in ss}
 s=z3.SolverFor("QF_BV");s.set(timeout=300000)
 for t in ts:s.add(V[t]>=0,V[t]<=N)
 s.add(V[ts[0]]==0,V[(0,1,2,4)]==1)
 for t in ts:
  if t!=ts[0]:s.add(R[t]>1)
  if t not in [ts[0],(0,1,2,4)]:s.add(R[t]>R[(0,1,2,4)])
 for q in ss:
  rs=[R[t] for t in ts if set(q)<=set(t)]
  s.add(z3.And([T[q]<=r for r in rs]),z3.Or([T[q]==r for r in rs]))
  if len(q)==1:s.add(T[q]<M)
 for v in range(4,n-1):s.add(T[(v,)]<T[(v+1,)])
 for t in ts:
  tris=list(itertools.combinations(t,3));small=[q for size in [1,2] for q in itertools.combinations(t,size)]
  # Selected nonfirst facets have pure codim-one intersection.
  conditions=[z3.Or([T[q]<R[t] for q in tris])]
  for q in small:
   conditions.append(z3.Implies(T[q]<R[t],z3.Or([T[z]<R[t] for z in tris if set(q)<=set(z)])))
  s.add(z3.Implies(z3.And(R[t]<M,R[t]!=1),z3.And(conditions)))
  s.add(z3.Implies(R[t]<M,z3.Or([T[q]==R[t] for q in tris])))
  ct=sum([z3.If(T[q]<M,z3.BitVecVal(1,W),z3.BitVecVal(0,W)) for q in tris]); s.add(ct!=3,z3.Implies(ct==2,z3.And([T[e]<M for e in itertools.combinations(t,2)])))
 s.add(z3.Or([T[q]==M for q in ss if len(q)==3]))
 start=time.time();ans=s.check();print('NONGRAPH SHELLING SAT',n,ans,time.time()-start,flush=True)
 if ans==z3.sat:
  model=s.model();facets=sorted([t for t in ts if model.eval(R[t]).as_long()<M],key=lambda t:model.eval(R[t]).as_long())
  print('TRAP',facets,flush=True);open('workspace/agent4_shellingtrap_'+str(n)+'.json','w').write(json.dumps(facets))
