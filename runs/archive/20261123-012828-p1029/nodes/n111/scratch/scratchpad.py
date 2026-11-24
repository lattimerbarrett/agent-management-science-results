import sympy as s
# Formal block identities; P,Q stand for positive square roots.
P,Q=s.symbols('P Q',commutative=False)
X=s.Matrix([[P,Q],[0,0]])
Xs=s.Matrix([[P,0],[Q,0]])
U=s.diag(1,-1)
G=Xs*X
print('XX* =',X*Xs)
print('X*X =',G)
print('pinching =',s.simplify((G+U*G*U)/2))
print('off-diagonal difference =',G-(G+U*G*U)/2)
h=s.Rational(1,2)
print('Endpoint quasitrace bookkeeping:')
print('q2(XX*) = q2(X*X) =',h)
print('q2(pinching(X*X)) = q(P^2)+q(Q^2) =',h+h)
print('q2(G)+q2(UGU*) =',h+h)
print('q2(G+UGU*) =',2*(h+h))
