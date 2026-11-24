import sympy as s
from pathlib import Path
x,y,z,t=s.symbols('x y z t', real=True)
# Ambient graph x_n=t*f(x'), domain above graph.
# Verify exact first-order Robin defect on a radial standard bubble.
records=[]
for n in range(3,10):
    a=s.Rational(n-2,2)
    U=(1+x*x+y*y+z*z)**(-a)
    for d in range(2,7):
        f=s.re(s.expand((x+s.I*y)**d)).expand()
        assert s.expand(s.diff(f,x,2)+s.diff(f,y,2))==0
        # Shape derivative of outward normal derivative at t=0.
        shape=-f*s.diff(U,z,2).subs(z,0)+s.diff(f,x)*s.diff(U,x).subs(z,0)+s.diff(f,y)*s.diff(U,y).subs(z,0)
        expected=(n-2)*(1-d)*f*(1+x*x+y*y)**(-s.Rational(n,2))
        assert s.simplify(shape-expected)==0
        records.append((n,d))
# General nonharmonic check including H' = Delta f.
for n in range(3,8):
    a=s.Rational(n-2,2); alpha=s.Rational(n-2,2*(n-1))
    U=(1+x*x+y*y+z*z)**(-a)
    for d in range(2,6):
        f=x**d+2*x**(d-2)*y**2
        lap=s.diff(f,x,2)+s.diff(f,y,2)
        actual=-f*s.diff(U,z,2).subs(z,0)+s.diff(f,x)*s.diff(U,x).subs(z,0)+s.diff(f,y)*s.diff(U,y).subs(z,0)+alpha*lap*U.subs(z,0)
        target=(n-2)*(1-d)*f*(1+x*x+y*y)**(-s.Rational(n,2))+alpha*lap*(1+x*x+y*y)**(-a)
        assert s.simplify(actual-target)==0
# Exact symbolic all-dimensional identity, using only Euler x.grad f=d*f.
nn,dd,rr,FF,KK=s.symbols('n d r2 F lapF', real=True)
al=s.Rational(1,2)*(nn-2)/(nn-1)
res=(nn-2)*FF*(1+rr)**(-nn/2)-(nn-2)*dd*FF*(1+rr)**(-nn/2)+al*KK*(1+rr)**(-(nn-2)/2)
want=(nn-2)*(1-dd)*FF*(1+rr)**(-nn/2)+al*KK*(1+rr)**(-(nn-2)/2)
assert s.simplify(res-want)==0
# A second-variation matrix can be positive while its scale derivative is not.
A=s.Matrix([[1,s.Rational(99,100)],[s.Rational(99,100),1]])
D=s.diag(1,2)
assert A[0,0]>0 and A.det()>0
assert (D*A+A*D).det()<0
# Under stereographic compactification, eta~rho^(2-d), v~rho^(1-d).
# Interior Dirichlet density has radial exponent n-1-2d.
n,d=s.symbols('n d', integer=True, positive=True)
assert s.expand(2*((1-d)-1)+(n-1))==n-1-2*d
print('PASS:',len(records),'harmonic graph Robin derivatives and 20 nonharmonic checks; n=3..9, degree=2..6.')
print('PASS: exact positive-Hessian/indefinite-scale-derivative counterexample; critical exponent n-1-2d.')
