import sympy as S
import numpy as np
# Exact identities behind the s=1 proof.
a,b,t=S.symbols('a b t', real=True)
mu=a*t+b*(1-t)
H2=S.factor(t*(a-mu)**2+(1-t)*(b-mu)**2)
assert S.simplify(H2-(mu-a)*(b-mu))==0
# The normalized squared weights are interchanged by one step.
tprime=S.factor(t*(a-mu)**2/H2)
assert S.simplify(tprime-(1-t))==0
# General monic-polynomial map: rational exact checks on distinct supports.
def qnorm(lam,w,s):
    M=S.Matrix([[sum(wi*li**(i+j) for li,wi in zip(lam,w)) for j in range(s)] for i in range(s)])
    rhs=-S.Matrix([sum(wi*li**(i+s) for li,wi in zip(lam,w)) for i in range(s)])
    coeff=list(M.inv()*rhs)+[S.Integer(1)]
    q=[sum(coeff[j]*li**j for j in range(s+1)) for li in lam]
    H=sum(wi*qi**2 for wi,qi in zip(w,q))
    return q,S.factor(H)
for s in range(1,5):
    lam=list(map(S.Integer,range(1,s+4)))
    w=[S.Rational(i+1,sum(range(1,len(lam)+1))) for i in range(len(lam))]
    q,h=qnorm(lam,w,s)
    w1=[S.factor(wi*qi**2/h) for wi,qi in zip(w,q)]
    q1,h1=qnorm(lam,w1,s)
    # Inner product y,F²y = sum w_i q_i q'_i /sqrt(h*h1)
    dotnum=S.factor(sum(wi*qi*qpi for wi,qi,qpi in zip(w,q,q1)))
    assert dotnum==h
    assert h1>=h
    # Cauchy-Schwarz equality defect and monotonicity are exact.
    print('s=',s,'H²=',h,'next H²=',h1,'monotone=',bool(h1>=h))
print('All exact symbolic and rational checks passed.')
