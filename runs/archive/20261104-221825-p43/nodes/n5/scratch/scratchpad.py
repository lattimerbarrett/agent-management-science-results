import sympy as s
x,y,u,v=s.symbols('x y u v', real=True)
f=x**3-3*x*y**2+u**2-v**2
variables=(x,y,u,v)
print('Degenerate local model gradient:', [s.diff(f,z) for z in variables])
perturbed=f-3*x
print('Critical points after perturbation:', s.solve([s.diff(perturbed,z) for z in variables],variables))
for p in [(-1,0,0,0),(1,0,0,0)]:
    A=s.hessian(perturbed,variables).subs(dict(zip(variables,p)))
    print(p, 'Hessian eigenvalues:', A.eigenvals())
print('Betti numbers of S^2 x S^2:', [1,0,2,0,1], '; sum =',4)
print('Cup length = 2; unconditional cup-length fixed-point bound =',3)
