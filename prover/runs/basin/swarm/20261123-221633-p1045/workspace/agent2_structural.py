"""Exact symbolic certificates for twin-class structural inequalities."""
import sympy as S
p,t,r,h,k=S.symbols('p t r h k', real=True)
F=(1-3*p+3*p*p-t*t*p)/(1-p)
assert S.factor(F-(1-t)**2+(p-t)*(3*p+t-2)/(p-1))==0
# For 0<=p<=t<=1/2: F >= (1-t)^2 by factor signs.
# For two red-light rows x,y, h=(x+y)/2, k=(x-y)/2:
# ||h||²+||k||²<=t² and ||h||² >= r².
# Their blue dot >= 1-2r+2r²-t².
expr=1-2*r+2*r*r-t*t-(1-t)**2
assert S.expand(expr-2*(t-r)*(1-t-r))==0
# t<=1/2,r<=t makes RHS nonnegative.
# This proves R-types form a red clique above the homogeneous bound.
print('Exact all-red-light Goodman factorization:',S.factor(F-(1-t)**2))
print('Exact two-red-light blue-codegree gap:',S.factor(expr))
print('All symbolic assertions passed.')
