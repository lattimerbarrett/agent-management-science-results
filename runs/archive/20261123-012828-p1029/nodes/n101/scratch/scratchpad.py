import sympy as s
n=s.symbols('n', positive=True, integer=True)
A=s.diag(0,1/n)
B=s.Matrix([[0,1],[1,0]])
C=A*B-B*A
print('Noncommuting lifts, with commuting images in the norm ultraproduct:')
print('[A_n,B_n] =',C)
print('[A_n,B_n]^* [A_n,B_n] =',s.simplify(C.T*C))
print('Thus commutator norm = 1/n -> 0, though the lifts do not commute.')
print('This is a warning about the missing quotient-quasitrace proof, not a counterexample to additivity for traces.')
