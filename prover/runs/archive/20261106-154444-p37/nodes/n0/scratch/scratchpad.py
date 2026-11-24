import itertools,z3
for r in [4,5,6,8]:
 n=3;Q=[frozenset([i]) for i in range(n)]+[frozenset(e) for e in itertools.combinations(range(n),2)];P=list(range(2*r+2));top=2*r+1
 def lep(i,j):return i==j or i==0 or j==top or (1<=i<=r and r+1<=j<=2*r and i-1!=j-r-1)
 X=list(itertools.product(P,Q));N=len(X);le=lambda a,b:lep(a[0],b[0]) and a[1]<=b[1]
 U=[{j for j in range(N) if j!=i and le(X[i],X[j])} for i in range(N)];idx={x:i for i,x in enumerate(X)}
 crit=[]
 for v in Q[:n]:
  for e in Q[n:]:
   if v<e:
    for bit in range(r):crit.append((idx[(bit+1,v)],idx[(r+bit+1,e)]))
   else:crit.append((idx[(0,v)],idx[(top,e)]))
 t=r+1;s=z3.Solver();s.set(timeout=30000);a=[[z3.Int(f'a{k}_{i}') for i in range(N)] for k in range(t)]
 for k in range(t):
  for i in range(N):
   s.add(a[k][i]>=0,a[k][i]<N)
   for j in U[i]:s.add(a[k][i]<a[k][j])
 for i,j in crit:s.add(z3.Or([a[k][i]>a[k][j] for k in range(t)]))
 print(r,s.check(),flush=True)
