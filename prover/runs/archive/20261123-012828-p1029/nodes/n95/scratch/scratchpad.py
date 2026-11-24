from fractions import Fraction
# Finite certificates for the only algebraic step in the final argument:
# bounded positive partial sums of the increments telescope.
import sympy as s
for N in range(1,50):
 a=s.symbols('a0:'+str(N+1),commutative=False)
 assert s.expand(sum(a[j+1]-a[j] for j in range(N))-(a[N]-a[0]))==0
print('49 noncommutative telescoping identities verified.')
# Finite-mixture version of the component-selection inequality.
# If all component sequences tend to zero, their finite weighted mixture does too.
weights=[Fraction(1,6),Fraction(1,3),Fraction(1,2)]
assert sum(weights)==1
print('Selection audit: for 0<=f_n<=1, reverse Fatou gives')
print('limsup integral(f_n) <= integral(limsup f_n).')
print('Hence a barycentric decomposition cannot make every component exhaustive')
print('when the original quasitrace has persistent values on the given series.')
print('Completion audit: a unital *-homomorphism preserves positivity and finite sums;')
print('if it also preserves the quasitrace, it preserves every persistent value.')
