import sympy as sp
B,G = sp.symbols('B G')
t,c,u,v,a,b,x,y,z = sp.symbols('t c u v a b x y z')
s1,s2,s3=sp.symbols('s1 s2 s3')
half=sp.Rational(1,2)
def check(expr):
    assert sp.cancel(expr)==0, sp.factor(expr)
P=c-t; Q=c*c+c+t
# Coordinate maps, inverse maps, and all factors defining the localizations.
forward={t:u*(1+u)*v,c:(1+u)*v}
inverse={u:t/c,v:c*c/(c+t)}
for w in (u,v): check(w.subs(inverse).subs(forward, simultaneous=True)-w)
for w in (t,c): check(w.subs(forward).subs(inverse, simultaneous=True)-w)
check(P.subs(forward, simultaneous=True)-(1-u)*(1+u)*v)
check(Q.subs(forward, simultaneous=True)-(1+u)**2*v*(v+1))
check((c+t).subs(forward, simultaneous=True)-(1+u)**2*v)
check((u-1).subs(inverse)+P/c)
check((u+1).subs(inverse)-(c+t)/c)
check((v+1).subs(inverse)-Q/(c+t))
jac=sp.det(sp.Matrix([[sp.diff(forward[w],j) for j in (u,v)] for w in (t,c)]))
check(jac-(1+u)**2*v)
# Pullback of f and every monomial that could contribute.
f=y*(z*y-x*x)*(z*z+x*x*y+z*y*y+x**3)
sub={x:a*b**3,y:a*b**2,z:a*a*b**4*c}
Q2=c-1/a; Q3=c*c+c+1/a
fsub=sp.expand(f.subs(sub, simultaneous=True))
check(fsub-a**8*b**16*Q2*Q3*(1+b/(a*Q3)))
monomials=[(i,j,k) for i in range(7) for j in range(10) for k in range(5) if 3*i+2*j+4*k<=2]
assert monomials==[(0,0,0),(0,1,0)]
# All other monomials have weighted degree >2 and cannot contribute.
formal=sum(sp.prod(G-1-j for j in range(n))/sp.factorial(n)*(b/(a*Q3))**n for n in range(3))
def Jcoefficient(psi):
    return sp.factor(-a**3*sp.expand(fsub*psi.subs(sub, simultaneous=True)*formal).coeff(b,18))
j0=Jcoefficient(sp.Integer(1)); jy=Jcoefficient(y)
check(j0+G*(G-1)/2*a**9*Q2/Q3)
check(jy+a**12*Q2*Q3)
# t=1/a changes the volume by -t^-2; the first gauge is g.
g=P*Q*t**-14
check(jy.subs(a,1/t)*(-t**-2)/g-1)
check(j0.subs(a,1/t)*(-t**-2)/g-G*(G-1)/2*t**3/Q**2)
# Connection after first gauge.
old=[sp.Rational(27,2)/t+(B-1)*sp.diff(P,t)/P+(G-1)*sp.diff(Q,t)/Q,
     (B-1)*sp.diff(P,c)/P+(G-1)*sp.diff(Q,c)/Q]
new=[-half/t+B*sp.diff(P,t)/P+G*sp.diff(Q,t)/Q,
     B*sp.diff(P,c)/P+G*sp.diff(Q,c)/Q]
for i,w in enumerate((t,c)): check(old[i]+sp.diff(g,w)/g-new[i])
C=B+2*G+sp.Rational(3,2)
D=B+G+half
S=2*B+2*G+1
omega_u=-half/u+B/(u-1)+C/(u+1)
omega_v=D/v+G/(v+1)
# Pullback and second gauge, by the Jacobian.
for w,target in [(u,omega_u),(v,omega_v)]:
    pulled=sum(new[i].subs(forward, simultaneous=True)*sp.diff(forward[r],w) for i,r in enumerate((t,c)))
    check(pulled+sp.diff(jac,w)/jac-target)
check((t**3/Q**2).subs(forward, simultaneous=True)-u**3/(u+1)*v/(v+1)**2)
# Explicit one-variable exactness certificates.
Lu=lambda h: sp.diff(h,u)+omega_u*h
Lv=lambda h: sp.diff(h,v)+omega_v*h
Pu=u*(u-1)*(u+1)
check(Lu(Pu)-((S+3)*u*u+(B-C)*u-half))
check(Lu(u*(u-1))-((S+2)*u-half-2*C+2*C/(u+1)))
K=-(D+1)*(D+G+1)/(G*(G-1))
hv=(v/(v+1)+(D+1)/G*v)/(G-1)
check(v/(v+1)**2-K-Lv(hv))
A0=1/(2*(S+3))-1/(4*C)
A1=(C-B)/(S+3)-G/C
hu=Pu/(S+3)-u*(u-1)/(2*C)
check(u**3/(u+1)-A0-A1*u-Lu(hu))
N=6*B+8*G*G+8*G+9
check(A1-N/(4*C*(S+3)))
# Matrix of the two generators in the tensor-product basis (1,u) tensor 1.
M=sp.Matrix([[1,G*(G-1)/2*K*A0],[0,G*(G-1)/2*K*A1]])
check(M.det()+(D+1)*N/(8*(S+3)))
# Nonintegrality conditions imply all nonzero denominators used above.
check(D+1-(B+G+sp.Rational(3,2)))
check(C-(B+2*G+sp.Rational(3,2)))
check(S+1-2*(B+G+1))
check(D+G-(C-1))
# Check the infinite-family leading-coefficient formulas used in the lemma.
lam,k,r=sp.symbols('lam k r')
w=sp.symbols('w', nonzero=True)
check((-k+lam)-(lam-k))
# d(w^-k)+lam/w*w^-k has leading coefficient lam-k.
check((sp.diff(w**(-k),w)+lam/w*w**(-k))*w**(k+1)-(lam-k))
# d(P*z^n)+omega*P*z^n: leading coefficient n+m+sum(lambda).
n=sp.symbols('n')
for roots,ls in [([0,1,-1],[-half,B,C]),([0,-1],[D,G])]:
    Z=sp.symbols('Z'); poly=sp.prod(Z-r for r in roots)
    numerator=sp.diff(poly,Z)+sum(l*sp.cancel(poly/(Z-r)) for r,l in zip(roots,ls))+n*sp.cancel(poly/Z)
    check(sp.Poly(sp.expand(numerator),Z).LC()-(n+len(roots)+sum(ls)))
# Translate, compute the reduced lexicographic Groebner basis, and check ideals.
H=2*s1+6*s2+8*s3+27
Ns=sp.expand(N.subs({B:s2+1,G:s3+1}))
gb=sp.groebner([H,Ns],s1,s2,s3,order='lex',domain=sp.QQ)
expected=[s1-4*s3**2-8*s3-2,s2+sp.Rational(4,3)*s3**2+4*s3+sp.Rational(31,6)]
assert list(gb)==expected
for p in [H,Ns]: assert gb.reduce(p)[1]==0
# On the exceptional parabola every excluded condition is nonconstant.
Bcurve=-(8*G**2+8*G+9)/6
conditions=[B,G,B+G+sp.Rational(3,2),B+2*G+sp.Rational(3,2),2*(B+G+1)]
for p in conditions:
    assert sp.Poly(sp.expand(p.subs(B,Bcurve)),G).degree()>0
# Polynomial parametrization verifies that the curve has prime ideal.
par={s3:G-1,s2:Bcurve-1,s1:(4*s3**2+8*s3+2).subs(s3,G-1)}
for p in expected: check(p.subs(par, simultaneous=True))
print('All symbolic checks passed.')
print('Exceptional polynomial in beta,gamma:',N)
print('Generator determinant:',sp.factor(M.det()))
print('Reduced lexicographic Groebner basis:',list(gb))
