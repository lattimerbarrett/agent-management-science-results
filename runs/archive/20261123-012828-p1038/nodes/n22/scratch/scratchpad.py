import sympy as s
z,w=s.symbols('z w')
# Exact interpolation rank obstruction: a self-reflective rational function
# R=p/p* of degree D has a Pick kernel of rank at most D.
for D in range(1,6):
 roots=[s.Rational(j+1,2*D+3) for j in range(D)]
 p=s.prod(z-a for a in roots)
 ps=s.prod(1-a*z for a in roots)
 numer=s.expand(ps*ps.subs(z,w)-p*p.subs(z,w))
 kernel=s.cancel(numer/(1-z*w))
 poly=s.Poly(kernel,z,w)
 assert poly.degree(z)<=D-1 and poly.degree(w)<=D-1
 nodes=[s.Rational(j+1,3*(D+4)) for j in range(D+3)]
 values=[s.cancel(p.subs(z,t)/ps.subs(z,t)) for t in nodes]
 K=s.Matrix([[(1-values[i]*values[j])/(1-nodes[i]*nodes[j]) for j in range(len(nodes))] for i in range(len(nodes))])
 print('degree',D,'nodes',len(nodes),'self-reflective kernel rank',K.rank())
# A strictly Schur target can have strictly positive definite Pick matrices
# of every size, excluding equality with the above low-rank kernels.
for n in range(2,9):
 nodes=[s.Rational(j+1,3*(n+1)) for j in range(n)]
 target=[(t+1)/4 for t in nodes]
 K=s.Matrix([[(1-target[i]*target[j])/(1-nodes[i]*nodes[j]) for j in range(n)] for i in range(n)])
 principal=[K[:j,:j].det()>0 for j in range(1,n+1)]
 print('strict-Schur target nodes',n,'all leading principal minors positive',all(principal))
print('Conclusion: if singularity supplies a self-reflective interpolant of degree <= D(m),')
print('and axial points supply > D(m) nodes for a strictly positive Pick kernel, it is impossible.')
print('Missing from this rank calculation alone: the construction and degree bound of that interpolant.')
