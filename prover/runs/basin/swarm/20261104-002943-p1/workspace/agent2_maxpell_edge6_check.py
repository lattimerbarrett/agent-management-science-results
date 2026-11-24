import pickle,sympy as S
D=pickle.load(open('workspace/agent2_maxpell_edge6_Q2_exact.pkl','rb'));b=S.sqrt(5);bs=S.symbols('b');Z=S.Matrix(S.symbols('z0:4'));Q=S.zeros(4,1)
for (i,j),vals in D['coeffs'].items():Q+=S.Matrix([S.sympify(v).subs(bs,b)*Z[i]*Z[j] for v in vals])
n=Z[0]+4*Z[2]-(7+3*b)*(Z[1]+Z[3]);pred=S.Matrix([S.Rational(3,4)*(78*b-175),0,S.Rational(15,4)*(9-4*b),0])*n*n
assert (Q-pred).applyfunc(S.simplify)==S.zeros(4,1)
assert S.simplify((Q[0]+4*Q[2])-S.Rational(3,4)*(5-2*b)*n*n)==0
x=S.symbols('x');P=x**4-5*x*x+4;h=-x**3-2*x*x+x+8;poly=P*P-1;a2=(5+b)/2
zt=Z[0]+Z[1]*x+Z[2]*x*x;phase=S.Poly(S.rem(-(x*x-a2)*P*h*zt,poly,x),x).nth(7)
assert S.simplify(phase-(3-b)*n.subs(Z[3],0)/2)==0
critical=x*x+x+3+3*b
assert S.discriminant(critical,x)==-11-12*b
assert bool(S.discriminant(critical,x)<0)
print('Exact six-support edge: Q2 rank-one square, phase-kernel coincidence, and irreducible positive critical quadratic checked.')
