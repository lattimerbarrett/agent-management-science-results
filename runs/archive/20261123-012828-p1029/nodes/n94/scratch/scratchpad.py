import sympy as s
# Exact interpolation identity and the residual coefficient after r steps.
g,eta=s.symbols('g eta', positive=True)
print('increment factor:',s.simplify((eta/g)*g))
t=s.symbols('t0:5')
w=s.Integer(1)
weights=[]
for ti in t:
 weights=[s.expand((1-ti)*v) for v in weights]
 weights.append(ti)
 w=s.expand((1-ti)*w)
print('total convex weight:',s.simplify(w+sum(weights)))
print('residual:',s.factor(w))
# Projection onto the graph of a scalar contraction z.
z=s.symbols('z',real=True)
P=s.Matrix([[1,z],[z,z*z]])/(1+z*z)
print('graph projection identity:',s.simplify(P*P-P))
print('vertical compression:',P[1,1])
print('recovered graph operator:',s.simplify(P[1,0]/P[0,0]))
