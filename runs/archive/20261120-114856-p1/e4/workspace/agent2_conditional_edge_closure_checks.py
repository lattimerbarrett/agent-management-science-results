from fractions import Fraction as F
import random
random.seed(92)
for N in range(2,20):
 z=[F(random.randrange(-9,10),11) for _ in range(N+1)];p=[F(random.randrange(-9,10),7) for _ in range(N+1)]
 lhs=sum(z[i]*(p[i+1]-p[i]) for i in range(N))
 rhs=z[-1]*p[-1]-z[0]*p[0]-sum(p[i+1]*(z[i+1]-z[i]) for i in range(N))
 assert lhs==rhs
print('Exact finite summation-by-parts checks PASS (18 random rational sequences).')
