import networkx as nx,itertools,z3,time,json

def audit_odd(E,qa=4,qb=4):
 h=max(max(e) for e in E)+1;q=qa+qb
 pairs=list(itertools.combinations(range(q),2));idx={e:i for i,e in enumerate(pairs)}
 Av=[idx[e] for e in pairs if e[1]<qa];Bv=[idx[e] for e in pairs if e[0]>=qa];Xv=[i for i in range(len(pairs)) if i not in Av+Bv]
 clauses=set()
 for cc in itertools.product(range(2),repeat=h):
  c=cc;mono=[(u,v) for u,v in E if c[u]==c[v]];ma=nx.Graph();ma.add_edges_from([(u,v) for u,v in mono if c[u]==0])
  A=sum([list(C) for C in nx.connected_components(ma)],[])
  B=list(set(sum(([u,v] for u,v in mono if c[u]==1),[])))
  active=set(A+B)
  if len(A)>qa or len(B)>qb:continue
  for aa in itertools.permutations(range(qa),len(A)):
   for bb in itertools.permutations(range(qa,q),len(B)):
    m=dict(zip(A+B,aa+bb));cl=tuple(sorted(idx[tuple(sorted((m[u],m[v])))] for u,v in E if u in active and v in active))
    clauses.add(cl)
 x=[z3.Bool('x'+str(i)) for i in range(len(pairs))]
 constraints=[z3.Not(z3.And(*[x[i] for i in cl])) for cl in clauses]
 I=z3.Sum([z3.If(x[i],1,0) for i in Av]);J=z3.Sum([z3.If(x[i],1,0) for i in Bv]);X=z3.Sum([z3.If(x[i],1,0) for i in Xv]);D=2*(I+J+X-qa*qb);W=8663*I+28663*J+20000*(X-qa*qb)
 out=[]
 for objectives in [(D,W),(W,D)]:
  s=z3.Optimize();s.add(*constraints)
  for f in objectives:s.maximize(f)
  assert s.check()==z3.sat;m=s.model()
  out.append({'2d':m.eval(D).as_long(),'2w':m.eval(W).as_long(),'IA':m.eval(I).as_long(),'IB':m.eval(J).as_long(),'holes':qa*qb-m.eval(X).as_long(),'edges':[pairs[i] for i in range(len(x)) if z3.is_true(m.eval(x[i]))]})
 return out
