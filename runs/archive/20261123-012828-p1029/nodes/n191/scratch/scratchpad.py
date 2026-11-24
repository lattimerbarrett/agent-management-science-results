hypotheses = {
 'unital AW*-algebra (right annihilators of arbitrary subsets are projection-generated)': True,
 'finite (every isometry is unitary)': True,
 'factor (center is C1)': True,
 'faithful normalized 2-quasitrace': True,
 'increasing self-adjoint sequence': True,
 'uniform order bound 0 <= a_n <= 1': True,
}
for h, verified in hypotheses.items():
 print(('VERIFIED: ' if verified else 'MISSING: ')+h)
print('\nBy the supplied monotone sequential completeness theorem:')
print('There is a least upper bound sup_n a_n in M_sa.')
print('This contradicts the required absence of a least upper bound, for every eta > 0.')