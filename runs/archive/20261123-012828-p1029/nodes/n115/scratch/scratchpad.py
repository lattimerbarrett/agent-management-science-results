import sympy as s
epsilon=s.symbols('epsilon', positive=True)
t=epsilon/2
d=s.simplify((epsilon-t)/(1-t))
print('Spectral dimension lower bound:',d)
print('Bessel bound for cut projections:',s.simplify(1/t))
print('Check scalar cut inequality at the extremal dimension:',s.simplify(t+(1-t)*d-epsilon))
# The positive-series increments telescope as elements, not quasitrace values.
N=6
a=s.symbols('a0:'+str(N+1), commutative=False)
print('Algebraic telescope:',s.expand(sum(a[i+1]-a[i] for i in range(N))))
