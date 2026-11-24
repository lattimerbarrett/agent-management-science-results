import sympy as S
import numpy as np
from scipy.special import jv, hyp0f1
from scipy.optimize import brentq

# Exact algebra for the auxiliary energy and its translation kernel.
r=S.symbols('r', positive=True)
n,lam=S.symbols('n lam', positive=True)
z=S.Function('z')(r)
Z=z*z
ode=-(n-1)*S.diff(z,r)/r-lam*z
Wp=(S.diff(Z,r,2)+(n-1)*S.diff(Z,r)/r).subs(S.diff(z,r,2),ode).simplify()
assert S.simplify(Wp-(-2*lam*z*z+2*S.diff(z,r)**2))==0
Wpp=(S.diff(Wp,r)/(2*z*S.diff(z,r))).subs(S.diff(z,r,2),ode).simplify()
assert S.simplify(Wpp+4*lam+2*(n-1)*S.diff(z,r)/(r*z))==0
p=S.diff(Z,r)
Lp=-S.diff(p,r,2)-(n-1)*S.diff(p,r)/r+(n-1)*p/r**2+Wpp*p
Lp=Lp.subs(S.diff(z,r,3),S.diff(ode,r)).subs(S.diff(z,r,2),ode).simplify()
assert Lp==0

# Exact algebra for the spherical-harmonic Hessian's large-degree limit.
h,A,B=S.symbols('h A B', positive=True)
k=1/h
wm=k/(2*k+n-2); wp=(k+n-2)/(2*k+n-2)
d=lambda j,X:j-X/(2*j)
c=d(k,A)-wm*d(k-1,B)-wp*d(k+1,B)
assert S.simplify(S.limit(c/h,h,0)-(B-A-(n-2))/2)==0
# Exponents in the sharp sequence, t=e/k^2.
e,kk=S.symbols('e k', positive=True)
t=e/kk**2
assert S.simplify(t*t/kk+t**4*kk**3-(e**2+e**4)/kk**5)==0
# Rearrangement Wronskian identity, with M'=r^(n-1)v.
v=S.Function('v')(r)
M=S.Function('M')(r)
err=lam*M+r**(n-1)*S.diff(v,r)
wr=r**(n-1)*(S.diff(v,r)*z-v*S.diff(z,r))
check=S.diff(wr,r)-z*S.diff(err,r)
check=check.subs(S.diff(M,r),r**(n-1)*v).subs(S.diff(z,r,2),ode)
assert S.simplify(check)==0
print('Exact symbolic identities: passed')

def first_zero(nu):
    lo=.05
    for hi in np.arange(.1,100,.05):
        if jv(nu,lo)*jv(nu,hi)<0:
            return brentq(lambda x:jv(nu,x),lo,hi,xtol=1e-14)
        lo=hi
    raise RuntimeError('root not bracketed')

def D(n,k,x):
    # Continued fraction avoids the underflow of J_{k+nu} for large k.
    f=0.
    for ell in range(k+150,k-1,-1):
        f=x*x/(2*ell+n-f)
    return k-f

def coeff(n,k,a,b):
    return D(n,k,a)-k/(2*k+n-2)*D(n,k-1,b)-(k+n-2)/(2*k+n-2)*D(n,k+1,b)

for n in range(2,9):
    a,b=first_zero(n/2-1),first_zero(n/2)
    assert b*b-a*a>n-1
    for k in range(3,61):
        nu=n/2-1
        direct=k-a*jv(k+nu+1,a)/jv(k+nu,a)
        assert abs(D(n,k,a)-direct)<1e-10
        assert coeff(n,k,a,b)>0
    limit=(b*b-a*a-(n-2))/2
    observed=2000*coeff(n,2000,a,b)
    assert abs(observed/limit-1)<.01
    print('n=%d: k*c_k at k=2000 %.8f; limit %.8f'%(n,observed,limit))

# Independent planar Fourier--Bessel collocation checks.
# This is a numerical diagnostic, NOT used to establish the theorem.
def matrix(q,k,e,l,J=4,N=128):
    js=np.arange(-J,J+1)
    theta=2*np.pi*np.arange(N)/(N*k)
    r=1+e*np.cos(k*theta)
    modes=l+js*k
    M=np.empty((N,len(js)),complex)
    for a,m in enumerate(modes):
        h=abs(int(m))
        M[:,a]=np.exp(1j*m*theta)*r**h*hyp0f1(h+1,-q*q*r*r/4)
    return np.exp(-1j*np.outer(modes,theta))@M/N

def shape_root(k,e,l,J):
    def residual(q):
        M=matrix(q,k,e,l,J=J)
        ix=[j for j in range(2*J+1) if j!=J]
        return float(np.real(M[J,J]-M[J,ix]@np.linalg.solve(M[np.ix_(ix,ix)],M[ix,J])))
    q0=first_zero(l)
    return brentq(residual,.99*q0,1.01*q0,xtol=1e-14)

a,b=first_zero(0),first_zero(1)
for k in [4,6,8,12,16,24]:
    e=.1/k**2
    th=np.linspace(0,2*np.pi,20001)
    rr=1+e*np.cos(k*th)
    rp=-e*k*np.sin(k*th)
    rpp=-e*k*k*np.cos(k*th)
    assert np.min(rr*rr+2*rp*rp-rr*rpp)>0
    roots=[]
    for J in [3,4]:
        roots.append([shape_root(k,e,l,J) for l in [0,1]])
    assert np.max(np.abs(np.array(roots[0])-roots[1]))<1e-10
    q0,q1=roots[1]
    deficit=(b/a)**2-(q1/q0)**2
    area=np.pi*(1+e*e/2)
    Ac=np.trapezoid(abs(rr*rr-area/np.pi),th)/(2*area)
    assert deficit>0
    print('k=%2d: deficit %.10g; centered difference %.10g; quotient %.7f'%(k,deficit,Ac,deficit/Ac**2.5))
print('All executable checks passed.')
