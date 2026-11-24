from fractions import Fraction
# Logical audit: scaling preserves a witness but cannot create an endpoint.
endpoint=Fraction(1,2)
for source in [Fraction(1,10), Fraction(1,4), Fraction(49,100)]:
    to_endpoint=endpoint/source
    print(f'witness at {source}: scaling to 1/2 requires factor {to_endpoint} > 1:',to_endpoint>1)
print('With downward closure, nonemptiness, upper bound 1/2, and exclusion of 1/2:')
print('G=(0,gamma) for 0<gamma<=1/2, or G=(0,gamma] for 0<gamma<1/2.')
print('These facts alone do not force gamma=1/2.')
