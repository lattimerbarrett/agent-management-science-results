import sympy as s
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
