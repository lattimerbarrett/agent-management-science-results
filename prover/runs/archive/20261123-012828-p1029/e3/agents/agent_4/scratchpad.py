import sympy as s
A=s.Matrix([[1,0],[0,0]])
B=s.Matrix([[2,1],[1,1]])
D=B-A
assert D.eigenvals()=={s.Integer(2):1,s.Integer(0):1}
r=s.sqrt(5)
P=(B-(3-r)/2*s.eye(2))/r
assert s.simplify(P*P-P)==s.zeros(2)
assert s.simplify((s.eye(2)-P)*A)!=s.zeros(2)
assert s.simplify(s.trace(P))==1
print('Exact verified counterexample to spectral-projection monotonicity: A<=B but 1_(1/2,infty)(A) not<=1_(1/2,infty)(B).')
print('A=',A, 'B=',B, 'spectral P_B=',P)
