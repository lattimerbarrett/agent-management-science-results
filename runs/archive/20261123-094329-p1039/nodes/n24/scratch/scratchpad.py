import sympy as s
# Local slice lifting: transverse coordinates H(x,t) approximate t.
a,b,c,d=s.symbols('a b c d')
B=s.Matrix([[a,b],[c,d]])
print('Transverse derivative determinant:',s.factor((s.eye(2)+B).det()))
print('Thus a sufficiently small transverse derivative error gives an invertible block, and H=0 is locally a graph.')
# Distinguish this local graph from a global entire parameterization.
print('The global zero locus is a closed Stein analytic set; the implicit-function theorem supplies a graph only near the approximation compact.')
# Exact elementary projection counterexample, n>=3.
# rho=||zprime||^2+(|w|^2-1)^2-4; take slice z_2=0.
print('At (z1,z2,w)=(0,2,0), rho=',4+1-4)
print('Its projection onto z2=0 has rho=',1-4)
