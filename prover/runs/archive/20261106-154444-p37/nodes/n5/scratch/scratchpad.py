import z3,itertools
cases=[(4,5,[2,2]),(5,13,[2,3]),(6,5,[2,2,2]),(6,9,[2,2,2]),(6,13,[2,2,2]),(6,20,[2,2,2])]
for d,n,groups in cases:
 s=z3.Solver();s.set(timeout=20000)
 a=[[z3.Int(f'x{k}_{i}') for i in range(n)] for k in range(d)]
 for row in a:
  for x in row:s.add(x>=0,x<n)
 for T in itertools.combinations(range(n),3):
  for v in T:s.add(z3.Or([z3.And([a[k][v]>a[k][w] for w in T if w!=v]) for k in range(d)]))
 start=0
 for g in groups:
  for v in range(n):
   for w in range(n):
    if v!=w:s.add(z3.Or([a[k][v]>=a[k][w] for k in range(start,start+g)]))
  start+=g
 print(d,n,groups,s.check(),flush=True)
