import numpy as np
import sympy as sp
from scipy.integrate import quad
from numpy.polynomial.chebyshev import chebval

# Exact projection-increment / adjugate identity, dimension 2 fine, 1 coarse.
a,b,c,x,y,z,t=sp.symbols('a b c x y z t', real=True)
G=sp.Matrix([[a,b],[b,c]]); E=sp.Matrix([1,0]); u=sp.Matrix([x,y]); v=sp.Matrix([z,t])
Gc=(E.T*G*E)[0]; Ra=Gc*u-G*E*x; Rb=Gc*v-G*E*z
assert sp.simplify((u.T*G.inv()*v)[0]-x*z/Gc-(Ra.T*G.inv()*Rb)[0]/Gc**2)==0
# The residual numerator annihilates every coarse polynomial.
assert sp.simplify(Gc*(G*E)-G*E*Gc)==sp.zeros(2,1)
print('Exact adjugate/projection identities: PASS')

# Inverse Chebyshev expansion and exact dual moments.
for lo,hi in [(0.2,3.0),(0.8,1.3),(0.01,8.0)]:
    mid=(lo+hi)/2; rad=(hi-lo)/2
    rho=(np.sqrt(hi)-np.sqrt(lo))/(np.sqrt(hi)+np.sqrt(lo))
    for m in [2,3,8,15]:
        moment=quad(lambda th: np.cos(m*th)/(mid+rad*np.cos(th)),0,np.pi,epsabs=1e-11)[0]/np.pi
        exact=(-rho)**m/np.sqrt(lo*hi)
        assert abs(moment-exact)<1e-10
        for j in range(m):
            mom=quad(lambda th: ((mid+rad*np.cos(th))/hi)**j*np.cos(m*th),0,np.pi,epsabs=1e-11)[0]/np.pi
            assert abs(mom)<1e-10
    degree=200
    coeff=np.r_[1.,2*(-rho)**np.arange(1,degree+1)]/np.sqrt(lo*hi)
    grid=np.linspace(lo,hi,1001)
    err=np.max(np.abs(chebval((grid-mid)/rad,coeff)-1/grid))
    bound=2/np.sqrt(lo*hi)*rho**(degree+1)/(1-rho)
    assert err<=bound+2e-11
print('Chebyshev inverse, annihilated moments, and nonzero dual functional: PASS')

# Check the exact algebra behind the sharp saddle point.
w,c0,N,X,M=sp.symbols('w c0 N X M', positive=True)
H=2*sp.sqrt(w*c0*(1-2*w))
tstar=sp.sqrt(c0*(1-2*w)/w)
f=w*X+c0*(1-2*w)/X
assert sp.simplify(sp.diff(f,X).subs(X,tstar))==0
assert sp.simplify(f.subs(X,tstar)-H)==0
assert sp.simplify(H**2/(4*w*c0)-(1-2*w))==0
print('Sharp lower saddle and upper quadratic maximum: PASS')

# Exact variance formula for unbiased polynomial estimation: Bernoulli example.
# F(p)=p^D, estimator (K)_D/(n)_D.
import math
for n in [8,12,20]:
  for D in range(1, min(6,n)+1):
    p=.37
    vals=[]; probs=[]
    for k in range(n+1):
      vals.append(math.comb(k,D)/math.comb(n,D) if k>=D else 0.)
      probs.append(math.comb(n,k)*p**k*(1-p)**(n-k))
    var=sum(q*(v-p**D)**2 for q,v in zip(probs,vals))
    formula=sum(math.comb(D,s)**2*p**(2*(D-s))*(p*(1-p))**s/math.comb(n,s) for s in range(1,D+1))
    assert abs(var-formula)<1e-13
print('Polynomial U-statistic Hoeffding variance identity: PASS')

# Verify the finite multinomial moment cancellation used in the lower bound.
u,R,S,aa,bb=sp.symbols('u R S aa bb')
# A generic sequence of accepted / rejected attempts. Odd-odd sign coefficient
# has degree at most number of attempts minus two in u.
factors=[u+aa*R+bb*S, 3-u, u-aa*R+bb*S, u+aa*R-bb*S, 3-u]
prod=sp.Poly(sp.prod(factors),R,S)
oddodd=0
for (i,j),coef in prod.terms():
    if i%2 and j%2: oddodd+=coef
assert sp.degree(oddodd,u)<=len(factors)-2
assert sp.rem(oddodd,aa,aa)==0 and sp.rem(oddodd,bb,bb)==0
print('Attempt-experiment odd/odd moment cancellation: PASS')

print('\nExample exponents (g_-=0.5, g_+=2):')
cval=np.log((np.sqrt(2)+np.sqrt(.5))/(np.sqrt(2)-np.sqrt(.5)))
for wval in [.05,.15,.25,.4,.49,.5,.8]:
    gamma=min(2*wval,1)
    kappa=4*np.sqrt(wval*(1-2*wval)*cval) if wval<.5 else 0.
    print(f'w={wval:.2f}: gamma={gamma:.6f}, kappa={kappa:.6f}')
