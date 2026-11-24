from pathlib import Path
import sympy as s
n=s.symbols('n',integer=True,positive=True)
coef=s.factor((n-2)**3/s.Integer(2)*(s.Rational(1,2)/((n-1)*(n-2))+s.Rational(3,2)/(n-1))-(n-2)**2/s.Integer(2))
assert s.simplify(coef-(n-3)*(n-2)**2/(4*(n-1)))==0
# Mass renormalization times the harmonic Pohozaev constant
omega=s.symbols('omega',positive=True)
shift=(3-n)/((n-1)*omega)
Pcoef=(n-2)**2*omega/4
assert s.simplify(-Pcoef*shift-coef)==0
print('General critical boundary-jet Pohozaev constant:',coef)
print('n5=',coef.subs(n,5),'n4=',coef.subs(n,4),'n3=',coef.subs(n,3))
assert s.Rational(3,8)==s.simplify((2*s.pi**2)/(2*(8*s.pi**2/3)))
print('n5 halfspace mass = B -(3/8)*average(f4)')

# Edge sign from linearized scalar and outward mean-curvature divergence
A,B=s.symbols('A B') # A=partial_a h_an, B=partial_n h_aa
Vn=A-B
H=A-B/2
assert s.simplify(-Vn+2*H-A)==0
print('Outward-normal convention gives PLUS boundary ADM edge term')

# All linear lower boundary jets: angular mean and adapted Pohozaev
k=s.symbols('k',integer=True,positive=True)
sigma=k+1-n
I=s.symbols('I')
gmean=s.factor((n-2)*((k-1)-k*(k+n-3)/(2*(n-1)))*I)
assert s.simplify(gmean+(n-2)*(k-2)*sigma*I/(2*(n-1)))==0
Q=(n-2)*(k-2)*I/(2*(n-1)*(k-1))
assert s.simplify(gmean+sigma*(sigma+n-2)*Q)==0
Pcross=-(n-2)*(k-1)*Q/2
counter=(n-2)**2*(k-2)*I/(4*(n-1))
assert s.simplify(Pcross+counter)==0
massbulk=2*(k-1)*Q/((n-2)*omega)
massboundary=(2-k)*I/((n-1)*omega)
assert s.simplify(massbulk+massboundary)==0
assert s.simplify(-Pcoef*massboundary-counter)==0
assert s.simplify(counter.subs({n:6,k:4})-s.Rational(8,5)*I)==0
print('All lower-jet angular means / ADM cancellations checked; n6 k4 counter=8I/(5r)')

# Explicit angular source constants in n5/n6 parametrices
f,Ds=s.symbols('f Ds')
for N,K,target in [(5,3,s.Rational(3,8)*(f-Ds)),(5,4,-s.Rational(3,8)*Ds),(6,4,s.Rational(4,5)*f-s.Rational(2,5)*Ds),(6,5,-s.Rational(2,5)*Ds)]:
    Dz=Ds+K*(K+N-3)*f
    source=(N-2)*(K-1)*f-s.Rational(N-2,2*(N-1))*Dz
    assert s.simplify(source-target)==0
print('All explicit n5/n6 Green angular Neumann sources checked')
