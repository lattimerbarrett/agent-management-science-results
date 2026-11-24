import z3,itertools
for m,n in [(3,3),(3,4),(4,4)]:
 def leS(a,b,s):return a==b or (a<s and b>=s and a!=b-s)
 X=list(itertools.product(range(2*m),range(2*n)));N=len(X)
 le=lambda a,b:leS(a[0],b[0],m) and leS(a[1],b[1],n)
 D=[{j for j in range(N) if j!=i and le(X[j],X[i])} for i in range(N)]
 U=[{j for j in range(N) if j!=i and le(X[i],X[j])} for i in range(N)]
 crit=[(i,j) for i in range(N) for j in range(N) if i!=j and not le(X[i],X[j]) and not le(X[j],X[i]) and D[i]<=D[j] and U[j]<=U[i]]
 t=m+n-3;s=z3.Solver();s.set(timeout=20000);a=[[z3.Int(f'a{k}_{i}') for i in range(N)] for k in range(t)]
 for k in range(t):
  for i in range(N):
   s.add(a[k][i]>=0,a[k][i]<N)
   for j in U[i]:s.add(a[k][i]<a[k][j])
 for i,j in crit:s.add(z3.Or([a[k][i]>a[k][j] for k in range(t)]))
 print(m,n,t,len(crit),s.check(),flush=True)
