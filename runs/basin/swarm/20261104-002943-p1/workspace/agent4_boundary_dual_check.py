import sympy as S
from pathlib import Path
z=S.symbols('z');active=[-3,-1,1,3];weights=[S.Rational(3,16),S.Rational(5,16),S.Rational(5,16),S.Rational(3,16)]
P=z*z-4;Q=z*z-6;C=S.Integer(15);inactive=[-5,-2,0,2,5,6];allnodes=sorted(active+inactive)
D=S.prod(z-a for a in allnodes);DS=S.prod(z-a for a in active);DI=S.prod(z-a for a in inactive)
w=dict(zip(active,weights));ww={a:S.factor(w[a]*P.subs(z,a)**2/C) for a in active}
S1=sum(w[a]*P.subs(z,a)/(z-a) for a in active);S2=sum(ww[a]*Q.subs(z,a)/(z-a) for a in active)
f1=S.cancel(D*S1/C);f2=S.cancel(D*S2/C)
assert S.expand(f1-f2)==0
assert S.expand(f1-DI*z)==0
assert S.degree(f1,z)==len(allnodes)-2-1
print('Boundarycontinuousdual factorization / 2cycle invariance PASS:',S.factor(f1))
