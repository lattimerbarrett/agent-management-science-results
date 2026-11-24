import sympy as s
M=s.symbols('M', positive=True)
A=s.Matrix([[1,0,(M-1)/s.sqrt(M)],[0,1,0],[(M-1)/s.sqrt(M),0,M+1/M-1]])
P=s.diag(1,1,0)
print('Compression onto span(e1,e2):', A[:2,:2])
print('det(A):', s.factor(A.det()))
print('Eigenvalues:', A.eigenvals())
print('Commutator with projection:', s.simplify(A*P-P*A))
A0=A.subs(M,4)
S=s.Matrix([[0,1,0],[1,0,0],[0,0,1]])
B0=S*A0*S.T
xs=s.symbols('x0:9')
X=s.Matrix(3,3,xs)
eqs=list(X*A0-A0*X)+list(X*B0-B0*X)
print('Common commutant of A0 and B0:', s.linsolve(eqs,xs))
for p in [1.5,3,6]:
    print('p =',p)
    for m in [1e2,1e6,1e12]:
        effective=((m**(2/p)+m**(1-2/p))/(m+1))**(p/2)
        # Put A on source for p>2, on target for p<2.
        gain=effective**(-1/p if p>2 else 1/p)
        print('M =',m,'full restricted effective scalar weight =',effective,'source/target gain factor =',gain)
