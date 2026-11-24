import itertools,time,z3,networkx as nx

def audit(E,qa=6,qb=6,maxit=10000,verbose=False):
 h=max(max(e)for e in E)+1;q=qa+qb;parts=[0]*qa+[1]*qb
 pairs=list(itertools.combinations(range(q),2));idx={e:i for i,e in enumerate(pairs)}
 x=[z3.Bool('edge'+str(i))for i in range(len(pairs))];internal=[i for i,(u,v)in enumerate(pairs)if parts[u]==parts[v]];cross=[i for i,(u,v)in enumerate(pairs)if parts[u]!=parts[v]]
 I=z3.Sum([z3.If(x[i],1,0)for i in internal]);M=len(cross)-z3.Sum([z3.If(x[i],1,0)for i in cross]);D=I-M;W=13955*I-20000*M;clauses=[];seen=set();iters=0
 def embedding(model):
  Gadj={(u,v)for i,(u,v)in enumerate(pairs)if z3.is_true(model.eval(x[i]))};Gadj|={(v,u)for u,v in list(Gadj)}
  for u in range(q):
   for b in range(2):
    if parts[u]!=b:Gadj.add((u,q+b));Gadj.add((q+b,u))
  Gadj|={(q,q+1),(q+1,q)}
  rel=z3.K(z3.IntSort(),z3.BoolVal(False))
  for u,v in Gadj:rel=z3.Store(rel,u*(q+2)+v,True)
  mp=[z3.Int('map'+str(u))for u in range(h)];s=z3.Solver();s.add([z3.And(t>=0,t<q+2)for t in mp]);s.add([z3.Or(mp[u]>=q,mp[v]>=q,mp[u]!=mp[v])for u in range(h)for v in range(u)])
  s.add([z3.Select(rel,mp[u]*(q+2)+mp[v])for u,v in E])
  if s.check()!=z3.sat:return None
  mm=s.model();mapping=[mm.eval(t).as_long()for t in mp]
  cl=tuple(sorted({idx[tuple(sorted((mapping[u],mapping[v])))]for u,v in E if mapping[u]<q and mapping[v]<q}))
  assert cl
  return cl
 out=[]
 for objective in [(D,W),(W,D)]:
  s=z3.Optimize();s.add(clauses)
  for f in objective:s.maximize(f)
  while True:
   assert s.check()==z3.sat;m=s.model();cl=embedding(m);iters+=1
   if cl is None:
    out.append(dict(edge=m.eval(D).as_long(),weight=m.eval(W).as_long(),internal=m.eval(I).as_long(),holes=m.eval(M).as_long(),actualedges=[pairs[i]for i in range(len(pairs))if z3.is_true(m.eval(x[i]))],iterations=iters));break
   assert cl not in seen;seen.add(cl);constraint=z3.Not(z3.And(*[x[i]for i in cl]));clauses.append(constraint);s.add(constraint)
   if verbose and iters%100==0:print('it',iters,'clauses',len(clauses),flush=True)
   if iters>=maxit:return None
 return out
if __name__=='__main__':
 E=[(0,i)for i in range(1,7)]+[(1,2),(3,4),(5,6)]
 t=time.time();print(audit(E,6,6,verbose=True));print('seconds',time.time()-t)
