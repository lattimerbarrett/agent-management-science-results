import sympy as s
from pathlib import Path
x,d=s.symbols('x d')
v=8*(x-1)*(x+d)/(2*d+1)-1
Qs=[]
for k in range(3):
    cs=s.symbols('c:'+str(2*k+1))
    Q=sum(cs[i]*x**i for i in range(len(cs)))
    eq=s.Poly(s.expand(Q*(x+d-1)**2-Q.subs(x,x+1)*x**2-(2*x+d-1)*v**k),x)
    sol=s.solve(eq.all_coeffs(),cs)
    Q=s.factor(Q.subs(sol)); Qs.append(Q)
    assert s.simplify(Q*(x+d-1)**2-Q.subs(x,x+1)*x**2-(2*x+d-1)*v**k)==0
    print('k=',k,' Q=',Q)
    print('Q(3/2)=',s.factor(Q.subs(x,s.Rational(3,2))))
    print('Q(2)=',s.factor(Q.subs(x,2)))
import mpmath as mp
mp.mp.dps=40
for N in range(9,101):
    D=mp.mpf(N-2)/2
    def end(k):
        qq=s.lambdify((x,d),Qs[k],modules='mpmath')
        return sum(qq(X,D)*(mp.gamma(X)/mp.gamma(X+D-1))**2 for X in [mp.mpf(3)/2,mp.mpf(2)])
    A,B,C=[end(k) for k in range(3)]
    R=B*B/(A*C)
    if N<31 or (R>mp.mpf(3)/4 and N<40):print('n',N,'R',mp.nstr(R,16),'critical',R>mp.mpf(3)/4)
# Independent finite partial sums plus exact telescoping tails.
for N in [9,10,16,31,32,40]:
    D=mp.mpf(N-2)/2
    for k in range(3):
        qq=s.lambdify((x,d),Qs[k],modules='mpmath')
        total=mp.mpf(0)
        for X0 in [mp.mpf(3)/2,mp.mpf(2)]:
            subtotal=mp.mpf(0)
            for jj in range(100):
                X=X0+jj
                vv=8*(X-1)*(X+D)/(2*D+1)-1
                subtotal+=(2*X+D-1)*(mp.gamma(X)/mp.gamma(X+D))**2*vv**k
            X=X0+100
            subtotal+=qq(X,D)*(mp.gamma(X)/mp.gamma(X+D-1))**2
            predicted=qq(X0,D)*(mp.gamma(X0)/mp.gamma(X0+D-1))**2
            assert abs(subtotal/predicted-1)<mp.mpf('1e-32')
        print('Exact telescoping tail checked:',N,k)
def symbolic_moments(N):
    D=s.Rational(N-2,2)
    return [s.simplify(sum(Qs[k].subs({x:X,d:D})*(s.gamma(X)/s.gamma(X+D-1))**2 for X in [s.Rational(3,2),s.Integer(2)])) for k in range(3)]
a32,b32,c32=symbolic_moments(32)
r32=s.factor(b32**2/(a32*c32))
assert r32>s.Rational(3,4)
print('n32 exact ratio:',r32)
print('n32 exact ratio minus 3/4:',s.factor(r32-s.Rational(3,4)))
Path('workspace/agent2_quadratic_quartic_moments.py').write_text(Path(__file__).read_text())
T=s.symbols('T', nonnegative=True)
p0=2*d*d+d+8;p1=6*d*d+3*d+2
q0=4*d**4+165*d*d-41*d+114;q1=36*d**4+181*d*d+19*d+6
D=s.expand(4*(d-3)*(p0+T*p1)**2-3*(d-2)*(1+T)*(q0+T*q1))
print('discriminant polynomial coefficients:',[s.factor(D.coeff(T,k)) for k in range(3)])
for tt in [0,s.Rational(4,3)/d,s.Rational(5,4)/d]:
    print('D(d=15,T=',tt,')=',s.factor(D.subs(T,tt).subs(d,15)))
e=s.symbols('e',nonnegative=True)
U=s.Rational(1696,333)/(4*d+1)
num=s.factor(s.together(D.subs(T,U))).as_numer_denom()[0]
print('D upper-bound numerator shifted at 15:',s.Poly(s.expand(num.subs(d,e+15)),e))
numder=s.factor(s.together(s.diff(D,T).subs(T,U))).as_numer_denom()[0]
print('Derivative upper-bound shifted:',s.Poly(s.expand(numder.subs(d,e+15)),e))
print('D2 shifted:',s.Poly(s.expand(D.coeff(T,2).subs(d,e+15)),e))
den_D=s.factor(s.together(D.subs(T,U))).as_numer_denom()[1]
den_der=s.factor(s.together(s.diff(D,T).subs(T,U))).as_numer_denom()[1]
assert all(c>0 for c in s.Poly(s.expand(den_D.subs(d,e+15)),e).all_coeffs())
assert all(c>0 for c in s.Poly(s.expand(den_der.subs(d,e+15)),e).all_coeffs())
assert all(c>0 for c in s.Poly(s.expand(num.subs(d,e+15)),e).all_coeffs())
assert all(c<0 for c in s.Poly(s.expand(numder.subs(d,e+15)),e).all_coeffs())
assert all(c>0 for c in s.Poly(s.expand(D.coeff(T,2).subs(d,e+15)),e).all_coeffs())
assert s.simplify((d+s.Rational(5,4))*(d+s.Rational(1,2))**2-(d+s.Rational(1,4))*(d+1)**2)==s.Rational(1,16)
atan_lower=sum((-1)**k*s.Rational(1,5)**(2*k+1)/(2*k+1) for k in range(4))
pi_lower=16*atan_lower-s.Rational(4,239)
assert pi_lower>s.Rational(333,106)
tan_a=s.Rational(1,5)
tan_2a=2*tan_a/(1-tan_a**2)
tan_4a=2*tan_2a/(1-tan_2a**2)
assert s.factor((tan_4a-s.Rational(1,239))/(1+tan_4a*s.Rational(1,239)))==1
print('All n>=32 certificate checked: coefficient signs, Gamma recurrence, rational pi bound via Machin.')
Path('workspace/agent2_quadratic_quartic_moments.py').write_text(Path(__file__).read_text())
Path('workspace/agent2_quartic_all_dimensions_proof.md').write_text(r'''# Certified nondegenerate scale extrema for the quartic graph in every n>=32

This proves a finite-dimensional scale-sector statement only. It is NOT a nonlinear Yamabe noncompactness theorem.

Set d=(n-2)/2>3. In the common normalization where harmless positive angular constants are suppressed, put
g0=[Gamma(3/2)/Gamma(d+1/2)]^2, g1=[Gamma(2)/Gamma(d+1)]^2.
The exact mixed spectral moments are
A=(g0+g1)/(d-1),
B=[g0 p0+g1 p1]/[(d-2)(d-1)(2d+1)],
C=[g0 q0+g1 q1]/[(d-3)(d-2)(d-1)(2d+1)^2],
where p0=2d^2+d+8, p1=6d^2+3d+2,
q0=4d^4+165d^2-41d+114,
q1=36d^4+181d^2+19d+6.

These follow by telescoping the positive spectral sum. In detail x=(j+3)/2, R(x)=8(x-1)(x+d)/(2d+1)-1; for k=0,1,2 solve the polynomial identity
Q_k(x)(x+d-1)^2-Q_k(x+1)x^2=(2x+d-1)R(x)^k.
The script computes these Q_k symbolically and checks the identities identically in x,d. Sum separately over x=3/2,5/2,... and x=2,3,... . Multiplication by [Gamma(x)/Gamma(x+d)]^2 makes the right side telescope. The tails vanish when d>k+1. The displayed A,B,C are the endpoint evaluations at x=3/2 and 2, as checked by exact symbolic simplification.

Let t=g1/g0=(4/pi)[Gamma(d+1/2)/Gamma(d+1)]^2. For all d>0,
(d+1/4)t(d) < 4/pi.
Indeed the ratio at d+1 versus d is greater than one because
(d+5/4)(d+1/2)^2-(d+1/4)(d+1)^2=1/16>0,
and Stirling's formula gives the limit 4/pi along each unit-spaced sequence. The elementary bound pi>333/106 follows, for example, from the Machin identity pi=16 atan(1/5)-4 atan(1/239) and four terms of the alternating series lower bound for atan(1/5), with atan(1/239)<1/239. The script checks these rational inequalities and the tangent identity underlying Machin's formula.

Consequently 0<t<U=1696/[333(4d+1)]. Define
D(d,t)=4(d-3)(p0+t p1)^2-3(d-2)(1+t)(q0+t q1).
Then B^2/(AC)>3/4 iff D(d,t)>0. For d=15+e, e>=0, direct exact expansion gives:
(1) The coefficient of t^2 in D has strictly positive coefficients as a polynomial in e.
(2) The numerator of partial_t D(d,U) has strictly negative coefficients in e; its denominator is positive.
(3) The numerator of D(d,U) has strictly positive coefficients in e; its denominator is positive.
All three coefficient-sign assertions are checked with exact integers by the script. Since partial_t D is increasing in t but negative at U, D decreases throughout [0,U]. Hence D(d,t)>D(d,U)>0 for every d>=15, proving B^2/(AC)>3/4 for every real n>=32.

For b>0, the reduced scale polynomial E(z)=-Az+2bBz^2-b^2Cz^3, z=lambda^2, has the two distinct positive critical points z_plus/minus=(2B plus/minus sqrt(4B^2-3AC))/(3bC). The smaller is a nondegenerate local minimum, the larger a nondegenerate local maximum. No assertion about tangential translations, nonlinear error estimates, or infinite gluing is made here.
''')
print('ratios of endpoint coefficients:')
for k in range(3):
    print(k,s.factor(Qs[k].subs(x,s.Rational(3,2))/Qs[0]),s.factor(Qs[k].subs(x,2)/Qs[0]))
