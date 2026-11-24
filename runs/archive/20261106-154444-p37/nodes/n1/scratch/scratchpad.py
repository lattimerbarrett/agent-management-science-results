import itertools,z3
for n in [6,7,8]:
 r=3;Q=[frozenset([i]) for i in range(n)]+[frozenset(e) for e in itertools.combinations(range(n),2)];P=list(range(8));X=list(itertools.product(P,Q));N=len(X);idx={x:i for i,x in enumerate(X)}
 s=z3.Solver();s.set(timeout=45000);t=5;a=[[z3.Int(f'a{k}_{i}') for i in range(N)] for k in range(t)]
 for k in range(t):
  for i,(p,q) in enumerate(X):
   for bit in range(r):
    if not p>>bit&1:s.add(a[k][i]<a[k][idx[(p|1<<bit,q)]])
   if len(q)==1:
    for e in Q[n:]:
     if q<e:s.add(a[k][i]<a[k][idx[(p,e)]])
 crit=[]
 for v in Q[:n]:
  for e in Q[n:]:
   if v<e:
    for bit in range(r):crit.append((idx[(1<<bit,v)],idx[(7^(1<<bit),e)]))
   else:crit.append((idx[(0,v)],idx[(7,e)]))
 for i,j in crit:s.add(z3.Or([a[k][i]>a[k][j] for k in range(t)]))
 print(n,s.check(),flush=True)
