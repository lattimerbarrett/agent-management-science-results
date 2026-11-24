from fractions import Fraction
for N in [2,5,10,20]:
 qbound=Fraction(1,2**(N-1))
 dangerous_lower=Fraction(2**N,2**(N-1))
 assert dangerous_lower>1
 print(f'N={N}: sup_|t|<=1 |u_N(t)| <= {qbound}; if |t+3|<=1, then |u_N(t)| >= {dangerous_lower}.')
print('Hence F_N(t)=(t+3,0,2^(1-N)t^N) avoids closed B^2 x closed D for every complex t.')
print('Its projection hits the interior of B^2 at t=-3, while F_N converges to (t+3,0,0) on the unit disc.')
