from fractions import Fraction as F
from pathlib import Path
beta_lo,beta_hi=F(829,1000),F(831,1000)
delta_lo,delta_hi=F(162,1000),F(163,1000)
sq_lo=F(643,1000)
# beta=(sqrt265-3)/16 and delta=sqrt10-3
assert (16*beta_lo+3)**2<265<(16*beta_hi+3)**2
assert (delta_lo+3)**2<10<(delta_hi+3)**2
assert sq_lo**2<beta_lo/2
assert delta_hi<beta_lo**2/2
lhs=2*(F(1,2)+1/beta_hi)*(1+delta_lo/beta_hi)*(1+sq_lo)**2
rhs=F(5,2)*(1+2*delta_hi)*(beta_hi+1/beta_lo)*(1+F(1,2)/beta_lo)
assert lhs>rhs
print('exact rate lower:',lhs,float(lhs))
print('exact rate upper:',rhs,float(rhs))
print('gap positive:',lhs-rhs)
