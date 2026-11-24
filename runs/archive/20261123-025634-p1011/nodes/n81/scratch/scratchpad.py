import sympy as s
r,R,d,n=s.symbols('r R d n',positive=True)
F=R**(2-d)
edge=s.simplify(R**(n-2)*s.diff(F,R))
L=(2-d)*r**(d-n+1)
print('Inverted homogeneous graph:',F)
print('Boundary mass edge term:',edge)
print('Compensation identity:',s.simplify(edge.subs(R,1/r)-L))
for nn in [3,4,7,17,18]:
 dd=nn//2+1
 lo=s.Rational(nn-2,2); hi=min(dd-1,nn-2)
 print('n=',nn,'first possible graph degree=',dd,'AF decay interval=',(lo,hi),'nonempty=',lo<hi)
