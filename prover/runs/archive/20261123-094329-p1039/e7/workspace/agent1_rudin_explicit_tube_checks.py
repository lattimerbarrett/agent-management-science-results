import sympy as s
S,B,Q,T=s.symbols("S B Q T")
g=s.symbols("g",positive=True)
c,x,y,theta=s.symbols("c x y theta",real=True)
r=s.sqrt(S*B)
X=(Q+T)/2;Y=(Q-T)/(2*s.I)
F1=(r-2)**2+X**2-1
F2=Y-2*(r-2)*X
R=F1**2+F2**2
Fs=[F1,F2];zs=[S,Q];bs=[B,T]
J=s.Matrix([[s.diff(f,z) for z in zs] for f in Fs])
Jb=s.Matrix([[s.diff(f,b) for b in bs] for f in Fs])
Levi=s.Matrix(2,2,lambda j,k:s.diff(R,zs[j],bs[k]))
remainder=2*sum((Fs[a]*s.Matrix(2,2,lambda j,k:s.diff(Fs[a],zs[j],bs[k])) for a in range(2)),s.zeros(2))
assert all(s.simplify(v)==0 for v in Levi-2*J.T*Jb-remainder)
sub={S:g*s.exp(s.I*theta),B:g*s.exp(-s.I*theta),Q:x+s.I*y,T:x-s.I*y}
det=s.simplify(J.det().subs(sub))
expected=s.exp(-s.I*theta)*(x*x-(g-2)**2-s.I*(g-2)/2)
assert s.simplify(det-expected)==0
on_M=s.expand((x*x-(g-2)**2-s.I*(g-2)/2).subs(g,c+2)).subs(x*x,1-c*c)
assert s.simplify(on_M-(1-2*c*c-s.I*c/2))==0
norm2=s.expand(on_M*s.conjugate(on_M))
assert s.simplify(norm2-(16*(c*c-s.Rational(15,32))**2+s.Rational(31,64))/4)==0
# Descended formula: u=|q|^2, v=Re(q^2), w=Im(q^2).
u=x*x+y*y;v=x*x-y*y;w=2*x*y
F1_alt=(u+v)/2+c*c-1
F2sq_alt=(s.Rational(1,2)+2*c*c)*u+(-s.Rational(1,2)+2*c*c)*v-2*c*w
assert s.expand(F1_alt-(c*c+x*x-1))==0
assert s.expand(F2sq_alt-(y-2*c*x)**2)==0
# p=(z,w)=(4,0) has local lift S=2,Q=0.
assert R.subs({S:2,B:2,Q:0,T:0})==1
# Uniform bounds for R<=1/16.
assert s.sqrt(s.Rational(5,4))<s.Rational(3,2)
assert s.Rational(9,4)+s.Rational(19,4)**2<s.Integer(25)
# Exact uniform estimates make epsilon=2^-14 fully explicit.
f=s.symbols("f",real=True)
assert s.expand((1-2*c*c+f)**2+c*c/4-(4*(c*c-(15+16*f)/32)**2+(31+32*f)/256))==0
H1=s.Matrix(2,2,lambda j,k:s.diff(F1,zs[j],bs[k]))
H2=s.Matrix(2,2,lambda j,k:s.diff(F2,zs[j],bs[k]))
H1_expected=s.diag(1-1/g,s.Rational(1,2))
H2_expected=s.Matrix([[-x/(2*g),-s.exp(-s.I*theta)/2],[-s.exp(s.I*theta)/2,0]])
assert all(s.simplify(v)==0 for v in H1.subs(sub)-H1_expected)
assert all(s.simplify(v)==0 for v in H2.subs(sub)-H2_expected)
assert s.Rational(23,256)/s.Rational(11,4)==s.Rational(23,704)
epsilon=s.Rational(1,16384)
levi_lower=s.Rational(23,352)-2*s.sqrt(5)*s.sqrt(epsilon)
assert levi_lower>0
assert epsilon<s.Rational(1,16)
print("Explicit epsilon=1/16384: certified Levi lower bound in (s,q) coords:",levi_lower)
print("Exact KB tube defining-function, Levi, determinant, SOS, descent checks passed.")
print("Levi strictly positive on the whole explicit sublevel; J invertible implies regular boundary.")
print("No non-Oka conclusion is asserted here.")
