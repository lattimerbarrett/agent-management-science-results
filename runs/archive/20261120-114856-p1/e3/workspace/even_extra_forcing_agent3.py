"""Exact symbolic s=2 cubic-map jets and negative-extra forcing for an even quartic.
All formulas are checked algebraically. This does not establish a counterexample.
"""
import sympy as s,pickle
z,d,q,h,t,w=s.symbols('z d q h t w');x=s.symbols('x');P=x**4+q*x*x-h
M=[1,-z,d-q,-d*z+q*z]
M1,M2,M3=[M[j]+w*(t**j-M[j])for j in [1,2,3]]
AA=(M1*M2-M3)/(M2-M1*M1);BB=-M2-AA*M1
Ac=s.factor(s.diff(AA,w).subs(w,0));Bc=s.factor(s.diff(BB,w).subs(w,0));p=x*x+q-d
f=(x-z)*(x*x+d)
poly0=s.rem(f*p*p,P,x);poly1=s.rem(f*2*p*(Ac*x+Bc),P,x)
H0=-d*d+q*d+h
assert s.expand(poly0-H0*(x-z)*(x*x+q-d))==0
f1=s.Poly(s.cancel(poly1/H0-poly0*s.Poly(poly1,x).coeff_monomial(x**3)/H0**2),x)
dz=s.factor(-f1.as_expr().subs(x,z)/(z*z+q-d));dc=s.factor(f1.coeff_monomial(x*x)+dz);dd=s.factor(f1.coeff_monomial(x)+z*dc)
e=s.Matrix([dz,dc,dd])
c=s.symbols('c');m=c-z;mm2=d-c*z-q;mm3=-d*z-q*m;A=s.factor((m*mm2-mm3)/(mm2-m*m));B=s.factor(-mm2-A*m);H=s.factor(h+B*d-z*(A*d+B*c));Z=s.factor((B*d*z-(m+A)*h)/H)
J=s.Matrix([Z,A,B]).jacobian([z,c,d]).subs(c,0).applyfunc(s.factor)
ep=e.subs(d,q-d, simultaneous=True);Jp=J.subs(d,q-d, simultaneous=True)
e2=(Jp*e+ep*(t*t+q-d)**2/H0).applyfunc(s.factor)
NN=s.Poly((t*t+d)*(t*t+q-d)+H0,t)
expected=s.Matrix([-2*(q-2*d)*(t+z)*(t*t+q-d)*(z**4+q*z*z-h)/((d+z*z)*(q-d+z*z)*H0),-4*(t+z)*(t*t+q-d)/(d+z*z),-4*(t*z-d)*(t*t+q-d)/(d+z*z)])
for a,b in zip(e2,expected):
 num=s.fraction(s.cancel(a-b))[0]
 assert s.rem(num,NN.as_expr(),t)==0
print('Verified even-quartic one-step identity and all three negative-extra forcing formulas.')
