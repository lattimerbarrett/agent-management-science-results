import sympy as s
u,v,w=s.symbols('u v w', real=True)
Z=s.Matrix([[u,v],[v,w]])
P=s.diag(1,0)
print('P Z^2 P - (P Z P)^2 =')
print(s.simplify(P*Z**2*P-(P*Z*P)**2))
print('Z^2 - Z P Z =')
print(s.simplify(Z**2-Z*P*Z))
print('These equal P Z (1-P) Z P and Z (1-P) Z, respectively, and are positive.')
