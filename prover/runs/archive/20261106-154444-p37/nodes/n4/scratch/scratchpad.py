import itertools,z3
for n,t in [(3,4),(4,4),(5,5),(6,5),(7,5),(8,5)]:
 r=3;s=z3.Solver();s.set(timeout=30000)
 a=[[z3.Int(f'a{j}_{v}') for v in range(n)] for j in range(t)]
 c=[[z3.Int(f'c{j}_{v}') for v in range(n)] for j in range(t)]
 for j in range(t):
  for v in range(n):s.add(a[j][v]>=0,a[j][v]<n,c[j][v]>=0,c[j][v]<r)
  for v,w in itertools.combinations(range(n),2):s.add(z3.Implies(a[j][v]==a[j][w],c[j][v]==c[j][w]))
 for v in range(n):
  for w in range(n):
   for i in range(r):s.add(z3.Or([z3.And(a[j][v]>=a[j][w],c[j][v]==i) for j in range(t)]))
 for T in itertools.combinations(range(n),3):
  for v in T:s.add(z3.Or([z3.And([a[j][v]>a[j][w] for w in T if w!=v]) for j in range(t)]))
 ans=s.check();print(n,t,ans,flush=True)
 if ans==z3.sat and n==3:
  mod=s.model();print([[[(mod.eval(a[j][v]).as_long(),mod.eval(c[j][v]).as_long()) for v in range(n)] for j in range(t)]])
