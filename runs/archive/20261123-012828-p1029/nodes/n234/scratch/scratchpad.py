from fractions import Fraction
# Consequences at eta=1/2, using monotonicity only.
h=Fraction(1,2)
for k in range(1,7):
    print(f'Nonempty sum of {k} increments: lower bound {h}, upper bound {1-h}')
print('Partition into three nonzero positive terms can have scalar quasitrace values:')
print((h,h,h),'sum of values =',3*h)
print('This is not an algebraic contradiction without additivity.')
print('Scaling any verified witness establishes all smaller positive increments,')
print('but neither attains 1/2 nor approaches it without an additional construction.')
