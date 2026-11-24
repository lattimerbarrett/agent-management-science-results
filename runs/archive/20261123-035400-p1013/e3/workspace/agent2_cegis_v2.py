import networkx as nx,z3,json,itertools,time,os
H=nx.node_link_graph(json.load(open('workspace/agent2_glue_b_vs_clique.json')))
NA=7;NB=8;N=NA+NB
PREFIX=f'workspace/agent2_cegis_{NA}_{NB}'

def inner(edges,timeout=30000):
 # labels0=Aregular infinite matching,1=Bregular independent,2..N+1 rarevertices0..N-1
 s=z3.Solver();s.set(timeout=timeout);w=(N+2).bit_length();width=1<<w
 q={v:z3.BitVec('q'+str(i),w) for i,v in enumerate(H)}
 for v in H:s.add(z3.ULT(q[v],N+2))
 for p in range(2,N+2):s.add(z3.PbLe([(q[v]==p,1) for v in H],1))
 rows=[0]*(N+2)
 def ae(i,j):
  if i==0 and j==0:return True
  if i==1 and j==1:return False
  if i<2 and j<2:return True
  if j<2:i,j=j,i
  if i==0:return j-2>=NA
  if i==1:return j-2<NA
  return tuple(sorted((i-2,j-2))) in edges
 for i in range(N+2):
  for j in range(N+2):
   if ae(i,j):rows[i]|=1<<j
 table=z3.K(z3.BitVecSort(w),z3.BitVecVal(0,width))
 for i,row in enumerate(rows):table=z3.Store(table,z3.BitVecVal(i,w),z3.BitVecVal(row,width))
 for u,v in H.edges():
  row=z3.Select(table,q[u]);ind=z3.ZeroExt(width-w,q[v]);s.add((z3.LShR(row,ind)&1)!=0)
 for v in H:
  ns=[q[u]==0 for u in H[v]]
  if ns:s.add(z3.Implies(q[v]==0,z3.PbLe([(x,1) for x in ns],1)))
 st=s.check()
 if st!=z3.sat:return str(st),None
 m=s.model();mp={v:m[q[v]].as_long() for v in H}
 req={tuple(sorted((mp[u]-2,mp[v]-2))) for u,v in H.edges() if mp[u]>=2 and mp[v]>=2}
 assert req and req<=edges
 return 'sat',sorted(req)

def outer(clauses):
 O=z3.SolverFor('QF_FD');O.set(timeout=30000);E={e:z3.Bool('e%d_%d'%e) for e in itertools.combinations(range(N),2)}
 deg=[]
 for i in range(N):deg.append(z3.Sum([z3.If(E[tuple(sorted((i,j)))],1,0) for j in range(N) if j!=i]))
 for part,cap in [(range(NA),5),(range(NA,N),3)]:
  for i in part:O.add(z3.PbLe([(E[tuple(sorted((i,j)))],1) for j in part if j!=i],cap))
  pp=list(part)
  for i,j in zip(pp,pp[1:]):O.add(z3.PbGe([(E[tuple(sorted((i,k)))],1) for k in range(N) if k!=i]+[(E[tuple(sorted((j,k)))],-1) for k in range(N) if k!=j],0))
 # Both single-part 2P3 decorators contain H with the other part's bulk.
 for verts in [range(NA),range(NA,N)]:
  triples=list(itertools.combinations(verts,3));P={t:z3.PbGe([(E[e],1) for e in itertools.combinations(t,2)],2) for t in triples}
  for i,t in enumerate(triples):
   for u in triples[i+1:]:
    if set(t).isdisjoint(u):O.add(z3.Not(z3.And(P[t],P[u])))
 for c in clauses:O.add(z3.Or([z3.Not(E[tuple(e)]) for e in c]))
 O.add(z3.PbGe([(v,1) for v in E.values()],NA*NB+NA//2+9))
 O.add(z3.PbGe([(v,10 if e[1]<NA else 20 if e[0]>=NA else 18) for e,v in E.items()],18*NA*NB+10*(NA//2)+145))
 st=O.check()
 if st!=z3.sat:return str(st),None,None
 m=O.model();edges={e for e,v in E.items() if z3.is_true(m.eval(v))}
 val=len(edges)-NA*NB-NA//2
 return 'sat',edges,val

clauses=json.load(open(PREFIX+'_clauses.json')) if os.path.exists(PREFIX+'_clauses.json') else []
t0=time.time()
for it in range(len(clauses),len(clauses)+1000):
 st,edges,val=outer(clauses)
 if st!='sat':print('OUTER',st,flush=True);break
 si,req=inner(edges)
 if it%10==0 or si!='sat':print('it',it,'edgebonus',val,'inner',si,'req',0 if req is None else len(req),'time',time.time()-t0,flush=True)
 if si=='unsat':
  json.dump({'NA':NA,'NB':NB,'bonus':val,'edges':sorted(edges)},open(PREFIX+'_solution.json','w'));break
 if si=='unknown':
  json.dump({'NA':NA,'NB':NB,'bonus':val,'edges':sorted(edges)},open(PREFIX+'_unknown.json','w'));break
 clauses.append(req);json.dump(clauses,open(PREFIX+'_clauses.json','w'))
 if time.time()-t0>100:break
# save reusable version

