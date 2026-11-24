import sympy as S
a=S.Rational(1,4)
for n in range(2,9):
 z=S.symbols('z0:'+str(n))
 y=S.symbols('y0:'+str(n))
 H=S.Matrix([z[0]**2+a*z[-1]]+[z[j]**2+a*z[j-1] for j in range(1,n-1)]+[a*z[n-2]])
 inv=[None]*n
 inv[n-2]=y[n-1]/a
 for j in range(n-2,0,-1): inv[j-1]=(y[j]-inv[j]**2)/a
 inv[n-1]=(y[0]-inv[0]**2)/a
 assert H.subs(dict(zip(z,inv)),simultaneous=True)==S.Matrix(y)
 # Do not expand the inverse expressions: degrees grow exponentially.
 J=H.jacobian(z)
 assert S.factor(J.det())==(-1)**(n-1)*a**n
 A=J.subs(dict.fromkeys(z,0))
 assert A.T*A==a*a*S.eye(n)
 print('Dimension',n,': polynomial inverse, Jacobian determinant, cyclic contraction checked')
# Strong domination estimate for D={||Z||^2-|w|^2<1}:
# A+delta*r controls positive-coordinate norm. Its excess square over r^2
# is at most A^2/(1-delta^2) by an exact completed square.
r,A,d=S.symbols('r A d',real=True)
expr=S.factor(A*A/(1-d*d)-((A+d*r)**2-r*r))
assert S.factor(expr-((1-d*d)*r-A*d)**2/(1-d*d))==0
print('Indefinite-ball containment completion:',expr)
open('workspace/agent4_indefinite_ball_refutation.py','w').write(open('scratchpad.py').read())