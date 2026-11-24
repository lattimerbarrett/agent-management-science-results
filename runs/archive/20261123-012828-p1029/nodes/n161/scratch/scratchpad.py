import sympy as s
for n in range(1,6):
    N=2*n
    p=s.diag(*([1]*n+[0]*n))
    q=s.zeros(N)
    q[0,0]=q[n,n]=q[0,n]=q[n,0]=s.Rational(1,2)
    for j in range(n+1,N): q[j,j]=1
    c=p*q-q*p
    print('n=',n,'p,q projections:',p*p==p,q*q==q,
          'normalized squared commutator=',s.trace(c.T*c)/N,
          'nonzero commutator:',c!=s.zeros(N))
