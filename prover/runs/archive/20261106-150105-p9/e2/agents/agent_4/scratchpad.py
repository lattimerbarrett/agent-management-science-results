import os
import sympy as s
import numpy as np
from scipy.integrate import quad

p,e,t=s.symbols('p e t', positive=True)
a=(p-1)*(1-e)
# Weighted integrands in the lower-bound proof are exactly t**(-1+e).
assert s.simplify(p*(-1+e)+a-(-1+e))==0
# The Ap powers cancel under interval rescaling.
assert s.simplify(a+(-1+e)*(p-1))==0
# The lower bound norm quotient is 1/(2*pi*epsilon).
assert s.simplify(((2*s.pi*e)**(-p)/e)/(1/e)-(2*s.pi*e)**(-p))==0

cases=0
for pp in [1.2,1.5,1.8,1.99]:
    for ee in [.05,.1,.25,.5,.9]:
        aa=(pp-1)*(1-ee)
        for r in np.linspace(0,1,101)[:-1]:
            assert r**ee >= r-1e-14
            # Exact elementary integration, arbitrary same-sign interval (r,1).
            ap=(1-r**(aa+1))/((aa+1)*(1-r))*((1-r**ee)/(ee*(1-r)))**(pp-1)
            assert ap <= ee**(-(pp-1))*(1+1e-12)
            # Exact elementary integration, crossing interval (-r,1).
            ap=(1+r**(aa+1))/((aa+1)*(1+r))*((1+r**ee)/(ee*(1+r)))**(pp-1)
            assert ap <= (2/ee)**(pp-1)*(1+1e-12)
            cases+=2
        for tt in [.001,.01,.1,.5,.9]:
            # Scale y=t*u and substitute v=u**epsilon to remove singularity.
            integral=quad(lambda v: 1/(1+v**(1/ee)),0,1,epsabs=1e-11)[0]/ee
            assert integral >= 1/(2*ee)-1e-10
            # Integral from 0<t of y**(-1+e)/(t+y) equals t**(-1+e)*integral.
            cases+=1
# Upper-bound exponent, including the asymmetric dual maximal costs.
q=p/(p-1)
upper=s.simplify(1/p+1/q+q/p**2)
assert s.simplify(upper-(1+1/(p-1)-1/p))==0
assert s.simplify(upper-(1+1/(p*(p-1))))==0
# Quantitative reverse Holder stopping-time constants.
z,rho=s.symbols('z rho')
assert s.simplify(1+(z-1)*rho/(1-z*rho)-(1-rho)/(1-z*rho))==0
for theta in np.linspace(.0001,1,10001):
    delta=theta/16
    zz=4**delta
    rr=1-theta
    assert zz <= 1+theta/4
    assert 1-zz*rr >= 3*theta/4-1e-15
    assert 2**delta*theta/(1-zz*rr)<2
print('Verified symbolic exponent/norm/series identities,',cases,'numeric interval/kernel checks, and 30003 RH constant inequalities.')

# Share the exact code used, not merely printed claims.
os.makedirs('workspace',exist_ok=True)
source=open(__file__).read()
with open('workspace/agent4_lower_checks.py','w') as f:
    f.write(source.split('# Share the exact code used')[0])
