import sympy as S
u,Q=S.symbols('u Q',positive=True)
r=S.sqrt(3);u0=1/(2*r);u1=4/r-2;d=2*r-3
kap=3-d/u;T=2*r*u
C=1/(9*u*u)+kap/(3*T)
assert S.simplify(C-((r/S.Integer(6)-S.Rational(2,9))/u**2+1/(2*r*u)))==0
assert r/S.Integer(6)-S.Rational(2,9)>0
C0=S.simplify(C.subs(u,u0));assert S.simplify(C0-(2*r-S.Rational(5,3)))==0
assert S.Rational(11,6)>C0
kapamax=S.simplify((kap*u*u).subs(u,u1))
assert S.Rational(18,125)>kapamax
# lambda_i ranges: T>=1, T+kap*h<=Tmax+kapamax<2
assert S.simplify(T.subs(u,u1)+kapamax)<2
Cmin=S.Rational(7,4)-r/2;cmin=2*r-3
pen=S.Rational(18,125)*(S.Rational(11,6)*Q*Q-1)
q0=S.sqrt(S.Rational(6,11));q1=2/r
lo1=Cmin-2/r+cmin*Q-pen
assert S.simplify(lo1.subs(Q,q0))>0
assert S.simplify(lo1.subs(Q,q1))>0
assert S.diff(lo1,Q,2)<0
lo2=S.expand(Cmin+(cmin-2)*Q+r*Q*Q/2-pen)
poly=S.Poly(lo2,Q);disc=S.discriminant(poly.as_expr(),Q)
assert poly.LC()>0 and disc<0
print('Cmax=',C0,'<11/6')
print('kap*a max=',kapamax,'<18/125')
print('first interval endpoint lowerbounds:',S.N(lo1.subs(Q,q0),15),S.N(lo1.subs(Q,q1),15))
print('second interval discriminant=',disc, S.N(disc,15))
# exact baseline F0 identity
G,R2=S.symbols('G R2',real=True)
lam=2/(r*u)-2;c0=3-(r-1)/u
F0=(G-3*u)**2/(3*u)+c0*(R2-G*G/3)+3*u*(u1-u)
base=2*r*u-kap*u*u-2*G+(1+kap/3)*R2+lam*(G*G-R2)/2
assert S.simplify(F0-base)==0
# Sum H_i P_i <=Q^2/3 via PSD + following SOS:
a,b,c=S.symbols('a b c',real=True)
sos=( (a*a-b*b)**2+(b*b-c*c)**2+(c*c-a*a)**2)/2+S.Rational(3,2)*((a*b-b*c)**2+(b*c-c*a)**2+(c*a-a*b)**2)
assert S.expand(sos-((a*a+b*b+c*c)**2-3*a*b*c*(a+b+c)))==0
print('All exact finite-lemma algebra checks passed.')

# Frozen-certificate random extension a in [u1^2,1/9].
T1=2*r*u1;kap1=S.Rational(3,2);aa=u1*u1
C1=S.simplify(1/(9*aa)+kap1/(3*T1))
assert C1<S.Rational(5,3)
assert kap1/S.Integer(9)==S.Rational(1,6)
A1=S.simplify(2*r*u1-kap1*aa);cc1=S.Rational(3,2)-r/2
assert S.simplify(A1-(4*r-6))==0
pen1=S.Rational(1,6)*(S.Rational(5,3)*Q*Q-1)
r0=S.sqrt(S.Rational(3,5))
b1=A1-2/r+cc1*Q-pen1
assert S.simplify(b1.subs(Q,r0))>0
assert S.simplify(b1.subs(Q,2/r))>0
assert S.diff(b1,Q,2)<0
b2=S.expand(A1+(cc1-2)*Q+r*Q*Q/2-pen1)
assert S.Poly(b2,Q).LC()>0 and S.discriminant(b2,Q)<0
# Resulting lower bound compared with random curve.
X=S.symbols('X',real=True)
K1=4*r-5
bound=K1/3-r*X*X-X*X*(X*X-aa)/2-(1-X)**2
cubic=X**3+u1*X*X+(2+2*r)*X-4*r/3
assert S.simplify(bound+(X-u1)*cubic/2)==0
assert S.simplify(cubic.subs(X,S.Rational(1,3)))<0
# Cubic is increasing on X>=0 as all nonconstant coefficients are positive.
print('Frozen random-extension audit passed; C1=',C1)
print('Random comparison factor:',S.factor(bound,extension=r))
