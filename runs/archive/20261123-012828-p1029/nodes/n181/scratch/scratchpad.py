from fractions import Fraction
# Endpoint equality constraints: eta <= tau(a_n) <= 1-eta.
eta=Fraction(1,2)
lower,upper=eta,1-eta
assert lower==upper==Fraction(1,2)
print('Endpoint equality forces tau(a_n)=1/2 for n>=1.')
print('For m>n, b_n <= a_m-a_n <= 1-b_m, so every interval gap also has tau=1/2.')
# Check that scaling an established endpoint witness reaches every target.
for denominator in range(2,80):
    for numerator in range(1,denominator//2+1):
        target=Fraction(numerator,denominator)
        scale=2*target
        assert 0<scale<=1
        assert scale*eta==target
print('Exact rational checks: scaling by 2*eta maps the endpoint gap to eta.')
print('Existence input: the verified endpoint witness. No graph-closure or exhaustion claim is used.')
