import sympy as s
H=s.Matrix([[0,1],[1,0]])
A2=s.Matrix([[2,-1],[-1,2]])
for name,Q in [('S2 x S2 middle intersection form',H),('standard rank-two A2 singularity form',A2)]:
 print(name, 'matrix=',Q.tolist(), 'det=',Q.det(), 'eigenvalues=',Q.eigenvals())
print('Regular levels just below and above the two index-2 handles are S^3.')
print('The attaching link is the 0-framed Hopf link, with linking matrix H.')
