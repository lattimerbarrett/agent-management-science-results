from pathlib import Path
code=r'''import sympy as s
th,ph=s.symbols('theta phi',real=True)
g=2+s.cos(ph)
h=s.sin(ph)+s.I*s.sin(2*ph)
z=s.exp(2*s.I*th)*g*g
w=s.exp(s.I*th)*g*h
D=s.simplify(s.diff(z,th)*s.diff(w,ph)-s.diff(z,ph)*s.diff(w,th))
assert s.simplify(D-2*s.I*s.exp(3*s.I*th)*g**3*s.diff(h,ph))==0
assert s.simplify(z.subs({th:th+s.pi,ph:-ph})-z)==0
assert s.simplify(w.subs({th:th+s.pi,ph:-ph})-w)==0
# h'=cos(phi)+2i cos(2phi) never zero: cos(phi)=0 => cos(2phi)=-1.
c,d=s.symbols('c d',real=True)
assert (2*c*c-1).subs(c,0)==-1
assert s.expand(c*c+4*(2*c*c-1)**2-(16*(c*c-s.Rational(15,32))**2+s.Rational(31,64)))==0
# h² as a function of c=cos(phi), independent of sign(sin(phi)).
R=1-5*c*c+4*c**4
I=4*c-4*c**3
assert s.expand((R-R.subs(c,d))-(c-d)*(c+d)*(4*c*c+4*d*d-5))==0
assert s.expand((I-I.subs(c,d))+4*(c-d)*(c*c+c*d+d*d-1))==0
# Distinct c,d with equal h² either d=-c and c²=1,
# or c²+d²=5/4, cd=-1/4. The latter forces max(|c|,|d|)>1.
large=(s.sqrt(7)+s.sqrt(3))/4
assert s.simplify(large**2-1)==(-3+s.sqrt(21))/8
assert s.sqrt(21)>3
# At c=1 and c=-1, h=0 but |z|=9 and |z|=1, respectively.
assert (2+c)**2 .subs(c,1) if False else True
assert ((2+c)**2).subs(c,1)==9
assert ((2+c)**2).subs(c,-1)==1
# Endpoint theta loops traverse z circles TWICE, so polynomial winding numbers
# at the two ends of the parameter cylinder are 2*N9 and 2*N1.
# Homotopy invariance forces N9=N1 whenever the polynomial is nonzero on K.
print('Verified Rudin Klein bottle immersion determinant, symmetry, and embedding algebra.')
print('Rational-hull annulus follows by argument principle as detailed in companion proof.')
print('NO claim about its neighborhood complement being non-Oka is established here.')
'''
# remove a deliberately inactive syntax distraction before storing
code=code.replace('assert (2+c)**2 .subs(c,1) if False else True\n','')
Path('workspace/agent2_rudin_klein_bottle_checks.py').write_text(code)
exec(code)
Path('workspace/agent2_rudin_klein_bottle.md').write_text(r'''# Explicit totally real Klein bottle and rational-hull annulus

This file proves geometry and a curve obstruction only, NOT non-Oka of a complement.

Put g(phi)=2+cos(phi), h(phi)=sin(phi)+i sin(2phi), and
j(theta,phi)=(exp(2i theta)g(phi)^2, exp(i theta)g(phi)h(phi)).
The free involution (theta,phi)->(theta+pi,-phi) leaves j invariant and reverses orientation. Its quotient is a Klein bottle. The complex determinant of the two real tangent vectors is
2i exp(3i theta) g(phi)^3 h'(phi),
which is nonzero: h'=cos(phi)+2i cos(2phi), and cos(phi)=0 forces cos(2phi)=-1. Thus j is a totally real immersion.

To prove the induced map on the quotient injective, note w²/z=h(phi)². With c=cos(phi), its real and imaginary parts are R(c)=1-5c²+4c⁴ and I(c)=4c-4c³. If c!=d and R(c)=R(d), I(c)=I(d), then either c+d=0 and c²=1, or c²+d²=5/4, cd=-1/4. The latter forces max(|c|,|d|)=(sqrt7+sqrt3)/4>1 and is impossible. In the endpoint case c=1,d=-1, |z| is respectively 9 and 1, so images differ. Otherwise cos(phi)=cos(psi), hence psi=phi or -phi. The z coordinate determines theta modulo pi, and the w coordinate selects exactly the stated involution (including h=0 at endpoints). Therefore the quotient map is an embedding. Compactness makes its image K0 a smooth compact totally real Klein bottle.

Let A={(z,0):1<=|z|<=9}. If P is any entire function nonzero on K0, then P(z,0) is not identically zero and is nonzero on both boundary circles of A. The loops theta->P(j(theta,phi)), 0<=theta<=2pi, are all nonzero and homotopic as phi runs from 0 to pi. At phi=0 and phi=pi their winding numbers are respectively twice the number of zeros of P(z,0) inside |z|<9 and inside |z|<1, counted with multiplicity. Equality of winding numbers proves there are no zeros in 1<|z|<9. Thus no entire function can vanish at any p in A and stay nonzero on K0. In particular A is contained in the rational hull of K0.

Every ambient closed analytic curve through p in A meets K0, since a closed analytic curve in C² is the zero set of a global entire function (Cartan divisor theorem on C²).

A small squared-distance tube K_delta={dist(.,K0)²<=delta} is smoothly bounded and strongly pseudoconvex: squared distance to a smooth totally real submanifold is strictly plurisubharmonic on a sufficiently small tubular neighborhood; its gradient is nonzero on positive small levels. It is bounded, connected, and excludes p=(4,0) for small delta. The closed-analytic-curve obstruction persists because K0 is contained in K_delta.

The missing analytic step is an exterior-specific non-Oka obstruction (possibly via rational hulls). Generic entire-image closed-curve selection was subsequently REFUTED by the Hénon-basin negative control. This file DOES NOT assert any such step or conclude non-Oka.
''')
pocket=r'''import sympy as s
c,d=s.symbols('c d',real=True)
# Exact maximum of h(phi)^2 magnitude.
assert s.expand((1-c*c)*(1+4*c*c)-(s.Rational(25,16)-4*(c*c-s.Rational(3,8))**2))==0
assert (s.Rational(9,4)*s.sqrt(2))**2<16
# Translation estimates: |Delta s|<=d and |Delta q|<4d.
# On M, |c|, |Re q|<=1, so errors satisfy these scalar majorants.
assert s.expand(2*d+d*d+8*d+16*d*d)==10*d+17*d*d
assert s.expand(4*d+2*(4*d+d+4*d*d))==14*d+8*d*d
delta=s.Rational(1,2**12)
epsilon=s.Rational(1,2**14)
assert delta<s.Rational(1,17)
assert delta<s.Rational(1,8)
assert 10*delta+17*delta**2<11*delta
assert 14*delta+8*delta**2<15*delta
assert (11**2+15**2)*delta**2==346*delta**2
assert 346*delta**2<epsilon
# Near p=(4,0), sqrt(z) stays within delta of2, q within delta of0.
assert 2*delta**2<s.Rational(1,2)
assert s.Rational(1,4)>epsilon
print('Verified explicit translated-KB inclusion and open rational-hull pocket radius 2^-12.')
print('These are geometric/hull checks only; no non-Oka implication is asserted.')
'''
Path('workspace/agent2_rudin_pocket_checks.py').write_text(pocket)
exec(pocket)
z3code=r'''import sympy as s
import z3 as z
# Modular exact audit of ACTUAL Levi matrix. A direct sextic nlsat attempt
# timed out; it has been replaced by this fast rational spectral certificate.
c,x,f,g,r=s.symbols('c x f g r',real=True)
J=s.Matrix([[c,x],[-x,-c-s.I/2]])
H0=2*s.conjugate(J.T)*J
H1=s.diag(1-1/r,s.Rational(1,2))
H2=s.Matrix([[-x/(2*r),-s.Rational(1,2)],[-s.Rational(1,2),0]])
H=H0+2*f*H1+2*g*H2
Ar=2*r*(c*c+x*x)+2*f*(r-1)-g*x
D=2*(c*c+x*x+s.Rational(1,4))+f
assert s.simplify(H[0,0]*r-Ar)==0
assert s.simplify(H[1,1]-D)==0
assert s.simplify(H[0,1]-(4*c*x-g+s.I*x))==0
# Exact Gram determinant completion, modulo c²+x²=1+f.
q=4*(c*c-(15+16*f)/32)**2+(31+32*f)/256
assert s.factor(s.det(s.conjugate(J.T)*J)-q)==(c*c+f+x*x+1)*(c*c-f+x*x-1)
assert s.trace(s.conjugate(J.T)*J)==2*c*c+2*x*x+s.Rational(1,4)
L=s.Rational(123,1024)
T=s.Rational(145,64)
alpha=2*L/T
assert alpha==s.Rational(123,1160)
assert (31+32*(-s.Rational(1,128)))/256==L
assert 2*(1+s.Rational(1,128))+s.Rational(1,4)==T
# Z3 checks the sharp input bounds and the abstract two-eigenvalue lemma.
def impossible(*constraints):
 solver=z.SolverFor('QF_NRA'); solver.set(timeout=10000)
 solver.add(*constraints)
 result=solver.check()
 assert result==z.unsat, (result,solver.reason_unknown())
F,G=z.Reals('F G')
impossible(F*F+G*G<=z.RealVal('1/16384'),z.Or(F>z.RealVal('1/128'),F<-z.RealVal('1/128'),G>z.RealVal('1/128'),G<-z.RealVal('1/128')))
a,b=z.Reals('a b')
impossible(a>=0,b>=0,a*b>=z.RealVal('123/256'),a+b<=z.RealVal('145/32'),a<z.RealVal('123/1160'))
# Since |c|,|x|<5/4, r=c+2>3/4. H1 has norm<=1.
# H2 has operator norm bounded by max row sum <= 5/6+1/2=4/3<2.
assert s.Rational(129,128)<s.Rational(25,16)
assert 2-s.Rational(5,4)==s.Rational(3,4)
assert 1-1/s.Rational(3,4)>-1
assert s.Rational(5,4)/(2*s.Rational(3,4))+s.Rational(1,2)==s.Rational(4,3)<2
# Thus perturbation norm <=2|f|+4|g|<=3/64.
assert 6*s.Rational(1,128)==s.Rational(3,64)
assert alpha-s.Rational(3,64)==s.Rational(549,9280)>0
print('Verified actual Levi decomposition and rational lower bound H >= (549/9280) I.')
print('Direct full-sextic nlsat was inconclusive; modular exact certificate above succeeded.')
print('This does not establish any Oka/non-Oka claim.')
'''
Path('workspace/agent2_rudin_actual_levi_z3_checks.py').write_text(z3code)
exec(z3code)
Path('workspace/agent2_rudin_explicit_pocket.md').write_text(r'''# Explicit open rational-hull pocket for the explicit KB tube
This uses the explicit defining function and Levi verification in agent1_rudin_explicit_candidate.md.

Let epsilon=2^-14, delta=2^-12, and K={R<=epsilon}. In square-root coordinates z=s²,w=sq put r=|s|, c=r-2, x=Re q,y=Im q, F1=c²+x²-1,F2=y-2cx,R=F1²+F2². On M, |s|>=1, |c|<=1, |x|<=1 and |q|<=5/4, because |q|²=(1-c²)(1+4c²)=25/16-4(c²-3/8)².

For an ambient translation a=(a_z,a_w) with ||a||<=delta, continue the square root along z+ta_z,0<=t<=1. Since |z+ta_z|>=1-delta>=1/2, the derivative bound gives |Delta s|<=delta/sqrt2<delta. Also |s'|>=1/sqrt2, so |Delta q|<=sqrt2(1+5/4)delta<4delta. Therefore |Delta c|<=delta, |Delta x|,|Delta y|<4delta. Since F1=F2=0 on M,
|F1'|<=10delta+17delta²<11delta,
|F2'|<=14delta+8delta²<15delta.
Hence R<=346delta²<epsilon on M+a. Thus every M+a with ||a||<=delta lies inside K.

Rational hull is monotone and translation equivariant. Since p=(4,0) belongs to the rational hull of M, p+a belongs to the rational hull of M+a and hence to the rational hull of K. Thus B(p,delta) is contained in the interior rational hull of K.

This entire ball is disjoint from K. For |z-4|,|w|<=delta, the square root near2 satisfies |s-2|<=delta, |s|>1; hence |q|<=delta, |c|<=delta and c²+x²<=2delta²<1/2. Thus R>=F1²>1/4>epsilon. Consequently B(p,2^-12) is an explicit open rational-hull pocket disjoint from K.

All scalar inequalities are checked exactly in agent2_rudin_pocket_checks.py. NO non-Oka consequence has yet been proved.
''')
