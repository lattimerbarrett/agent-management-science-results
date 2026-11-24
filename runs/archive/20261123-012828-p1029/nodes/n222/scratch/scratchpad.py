import sympy as s
# Test whether the proposed equivalent-corner repetition amplifies a fixed
# additivity defect. Matrix quasitraces are unnormalized sums on diagonals.
a,b,c=s.symbols('tau_a tau_b tau_a_plus_b', real=True)
D=c-a-b
for k in [2,3,8,32]:
    one=s.expand(D/k)
    repeated=s.expand(k*one)
    print(f'{k} equivalent corners: defect of one supported copy = {one}; defect after filling all corners = {repeated}')
    assert repeated==D
# Boundedness of an infinite direct sum of positive defects cannot be
# inferred from cornerwise repetition: mutually orthogonal corners have
# total dimension at most one.
r=s.symbols('r', positive=True)
print('N equivalent orthogonal corners of dimension r require N*r <= 1.')
print('Thus they cannot support infinitely many fixed-positive-quasitrace copies.')
print('\nFrom the supplied verified nonemptiness and downward closure:')
print('G is (0,gamma) or (0,gamma], with 0<gamma<=1/2; gamma remains to be determined.')
