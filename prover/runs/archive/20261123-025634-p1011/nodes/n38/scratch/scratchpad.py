# Check the candidate countable graph, derivative by derivative.
# h_k(x)=mu_k eps_k^8 sum_{j=0}^3 c_j eps_k^(-2-2j)
#        P_2(x-p_k)|x-p_k|^(2*j) chi((x-p_k)/r_k).
# Each monomial has degree d=2,4,6,8. A Leibniz term of total order m
# is bounded by C_m mu_k eps_k^(8-d) r_k^(d-m).
# Since eps_k<=r_k, this is <=C_m mu_k r_k^(8-m).
from fractions import Fraction
for m in [0,1,2,4,8,9,20,100]:
 print('derivative order',m)
 for k in [10,50,200]:
  # base-2 exponent of mu_k r_k^(8-m), mu=tau*2^(-k^2)
  exp=-k*k-(k+3)*(8-m)
  print(' k=',k,'log2(bound/C_m/tau)=',exp)
print('For every fixed m,N, bound/|p_k|^N has log2 exponent')
print(' -k^2 + (m+N-8)k + 3(m-8), which tends to -infinity.')
print('Thus this stated choice of countable graph is C-infinity and flat at 0.')
print('Outside a fixed compact set the graph is zero, so spherical compactification')
print('adds a standard smooth equatorial boundary point.')
