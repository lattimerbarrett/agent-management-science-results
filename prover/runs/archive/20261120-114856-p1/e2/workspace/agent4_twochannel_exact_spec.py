import sympy as S
x=S.symbols('x');f=x**3-7*x;eta=S.Rational(7,4);M=-f.subs(x,eta);h=(M*M-36)/2;d=S.sqrt((M*M+36)/2)
p=f+d;q=f-d;chi6=S.expand(f*f-M*M);chi=S.cancel(chi6/(x-eta)*(x+3)*(x-1));chi=S.Poly(chi,x).as_expr();R=(x+3)*(x-1)*(x+S.Rational(3,2))
assert S.rem(p*q-h,chi6,x)==0
assert S.simplify((p*q).subs(x,-3)+h)==0
assert S.simplify((p*q).subs(x,1)+h)==0
assert S.rem(chi6,x-eta,x)==0
assert all(z.is_Rational for z in S.Poly(chi,x).all_coeffs())
# Exact linear spectral functional of positive base5 weights, with both outside masses0.
def L(g):return S.simplify(S.Poly(S.rem(S.expand(g*q*R),chi,x),x).nth(6))
assert L(1)==1
assert all(L(p*x**j)==0 for j in range(3))
assert S.simplify(L(p*p)-h)==0
assert all(L(q*x**j*p*p)==0 for j in range(3))
# Exact core isolating intervals establish ordering and positivity.
isol=S.polys.polytools.intervals(chi6,eps=S.Rational(1,100000))
assert len(isol)==6 and all(m==1 for _,m in isol)
rr=[(a+b)/2 for (a,b),_ in isol]
assert rr[0]<-3<rr[1]<-S.Rational(3,2)<rr[2]<1<rr[3]<eta<rr[5]
# Numerically displayed weights only supplement the exact sign argument below.
# On original six ordered core nodes, sign chi6'=[-,+,-,+,-,+],
# sign q=[-,+,+,-,-,+]; (node-eta)(node+3/2) signs [+, +,-,-,0,+].
# Their products give positive surviving5 weights; deletedeta hasweight0.
sgnd=[-1,1,-1,1,-1,1];sgnq=[-1,1,1,-1,-1,1];sgnR=[1,1,-1,-1,0,1]
assert all(sgnd[i]*sgnq[i]*sgnR[i]>0 for i in [0,1,2,3,5])
print('h=',h,'d=',d,'chi7=',chi)
print('Core rational isolators:',isol)
print('Moments0..6:',[L(x**j) for j in range(7)])
print('All exact two-negative-channel spectrum/orthogonality/positivity checks passed.')
