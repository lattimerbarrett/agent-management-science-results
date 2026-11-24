from fractions import Fraction
# Recalculate, rather than assume, the normalized energy error powers.
# eps=2^(-k^4), mu=tau*2^(-k^2), rho=2^(-k-3),
# delta=mu*eps^7, R=rho/eps; barrier scale delta^2.
for n in [17,18,19,20,25,40]:
 q=Fraction(2*n,n-2)
 print('\nn =',n,'q =',q)
 for k in [4,8,16]:
  le=-k**4; lm=-k**2; lr=-k-3
  ld=lm+7*le; lR=lr-le
  # Main proposed types of error, divided by delta^2:
  err={
   'tail_R^(16-n)':(16-n)*lR,
   'remote_energy_eps^(n-2)/delta^2':(n-2)*le-2*ld,
   'remote_cross_eps^a/delta':Fraction(n-2,2)*le-ld,
   'curvature_cubic':ld+max(23-n,0)*lR,
   'nonlinear_delta^(q-2)':(q-2)*ld,
  }
  print(' k',k, {x:float(v) for x,v in err.items()})
print('\nThese are conditional power-counting bounds, not proofs of uniform estimates.')
print('A fixed O(tau)*delta^2 error has a NONVANISHING normalized bound O(tau).')
print('A merely o(1) unnormalized error need not be o(delta^2).')
