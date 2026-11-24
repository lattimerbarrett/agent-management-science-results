from fractions import Fraction as F
# A normalized trace is already enough to disprove the proposed
# formula q(h^{-1/2} b h^{-1/2}) = q(b)/q(h).
h=(F(1,10),F(1))
b=(F(0),F(1,10))
q=lambda x:sum(x)/2
actual=q(tuple(bi/hi for bi,hi in zip(b,h)))
proposed=q(b)/q(h)
print('q(b) =',q(b),'q(h) =',q(h))
print('q(h^-1/2 b h^-1/2) =',actual)
print('q(b)/q(h) =',proposed)
assert actual != proposed
# The valid scalar-width/corner normalization is eta/(beta*q(p)).
eta=F(1,20); beta=F(1,2); dp=F(1,2)
print('Example scalar-width/corner normalization:',eta/(beta*dp))
