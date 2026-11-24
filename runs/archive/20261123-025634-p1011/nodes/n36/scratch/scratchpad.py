# Audit the fixed-domain scale separation, independent of profile certificates.
from fractions import Fraction
for n in [19,20,24,25,40]:
 print('n =',n)
 for k in [3,5,8]:
  # eps=2^(-k^4), mu=tau*2^(-k^2), delta=mu*eps^7.
  # Remote energy / delta^2 has scale eps^(n-16)/mu^2 (omit tau).
  remote_log2=-(n-16)*k**4+2*k**2
  # For derivatives up to order m the uniform estimate is mu*r^(8-m),
  # r=2^(-k-3). Divide by |p_k|^N to test flatness.
  m,N=30,20
  flat_log2=-k*k-(8-m)*(k+3)+k*N
  print(' k',k,'log2(remote ratio)',remote_log2,'log2(flatness bound, m=30,N=20)',flat_log2)
print('All fixed m,N flatness exponents are -k^2+O(k); all remote ratios tend to zero for n>16.')
