import sympy as S
x,mu,nu,c,L,A,B,C,th=S.symbols('x mu nu c L A B C th', nonzero=True)
Pm,Pn=-2*L/(mu-c),-2*L/(nu-c)
Pth=S.symbols('Pth', nonzero=True)
a,b=(mu-c)/(mu-nu),-(nu-c)/(mu-nu)
qm=Pm*C+L*B/2*(1-Pm/Pth)/(mu-th)
qn=Pn*C+L*B/2*(1-Pn/Pth)/(nu-th)
K=(th-c+2*L/Pth)/((mu-th)*(nu-th))
assert S.simplify(a+b-1)==0
# theta'=-B
assert S.factor(a*(-2*qm/L-4*A/L)+b*(-2*qn/L-4*A/L)-B*K+4*A/L)==0
# Exact rational barycentric sextic identity, nonzero values arbitrary.
nodes=list(map(S.Rational,[-3,-1,0,1,2]));mum,num=S.Rational(1,2),S.Rational(3,2)
allnodes=nodes+[mum,num];P7=S.prod(x-v for v in allnodes);weights=[2*S.Rational(3)/S.diff(P7,x).subs(x,v) for v in allnodes]
for j in range(7):
 assert S.simplify(sum(w*v**j for w,v in zip(weights,allnodes))-(6 if j==6 else 0))==0
print('PASS exact symbolic logmoment identity and sextic barycentric identities')
