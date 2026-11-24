"""Exact certificate for the mixed-row B-triangle existence lemma."""
import sympy as S
u,q,s,beta=S.symbols('u q s beta',real=True)
# Normalized masses: |R|=s, |B|=beta=1-s; a=u^2.
# Q_RB <= s(a-s), D_RB <= s sqrt(beta(a-s)).
# If B support trianglefree, Q_BB >= 2P_BB^2/beta^2.
P=S.symbols('P',real=True)
assert S.simplify((-2*P+2*P**2/beta**2+beta**2/2)-2*(P-beta**2/2)**2/beta**2)==0
# b>=1-beta/2 +s q^2-2s q =1/2+s(1/2+q^2-2q).
assert S.expand((1-beta/2+s*q*q-2*s*q).subs(beta,1-s)-(S.Rational(1,2)+s*(S.Rational(1,2)+q*q-2*q)))==0
u0=1-1/S.sqrt(2)
assert S.simplify(S.Rational(1,2)+u0*u0-2*u0)==0
# If u<=u0, bracket(q)>=0 for 0<=q<=u.
# If u>=u0, bracket(q)>=bracket(u), and s<=a=u^2.
lower=S.Rational(1,2)+u*u*(S.Rational(1,2)+u*u-2*u)
diff=S.factor(lower-(1-u)**2)
assert diff==(u-1)*(u+1)*(2*u*u-4*u+1)/2
# For u0<=u<1/2: both u^2-1 and 2u^2-4u+1 are nonpositive.
print('Mixed B-triangle algebra certificate passed.')
print('critical u0:',u0)
print('lower_bound - random_bound:',diff)
