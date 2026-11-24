import sympy as s
r,a=s.symbols('r a', positive=True)
# Candidate smooth compact nonpseudoconvex obstacle:
# K={ (|z1|^2-a)^2+|z'|^2 <= b }, b>a^2.
# At z1=0 the tangent Levi signs are (-,+,...,+).
for n in range(2,6):
    print(f'n={n}: tangent Levi signs =', ['-']+['+']*(n-2))
print('This verifies only the Levi signature; it does NOT establish the Oka property of the complement.')
print('A product with a ball does not preserve a non-Oka retract in the complement.')