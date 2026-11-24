import sympy as s
n,r,l=s.symbols('n r l',positive=True)
a=(n-2)/2;beta=(n-2)/(2*(n-1));A=(n-2)**2/2;C=(n-2)**2/(4*(n-1))
U2=(l/(l*l+r*r))**(n-2)
Ur2=(n-2)**2*r*r/(l*l+r*r)**2*U2
Uq=l*l/(l*l+r*r)**2*U2
E2=-beta/2*((n-2)*r**(n-2)*U2+r**(n-1)*s.diff(U2,r))
V=-Ur2/2+A*Uq
E1=(n-2)/r*E2+r**(n-1)*V
E0=-r**(n-2)*V
B=s.factor((E1-s.diff(E2,r))/U2)
assert s.simplify(E0-s.diff(E1-s.diff(E2,r),r))==0
print('E2/U2=',s.factor(E2/U2))
print('B/U2=',B)
assert s.simplify(E2/U2-C*r**(n-2)*(r*r-l*l)/(r*r+l*l))==0
print('Exact first-order graph stress is outer rim E2*Fbar_prime+B*Fbar; all coefficients checked.')
