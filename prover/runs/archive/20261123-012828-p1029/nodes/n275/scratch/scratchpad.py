from z3 import Bool, Solver, Implies, And
# Logical audit only: the monotone-completeness theorem is an input,
# not something this finite computation purports to prove.
finite_AW = Bool('M_is_finite_AW_factor')
bounded_increasing_sa = Bool('sequence_is_bounded_increasing_selfadjoint')
has_lub = Bool('sequence_has_lub_in_M_sa')
s = Solver()
s.add(Implies(And(finite_AW, bounded_increasing_sa), has_lub))
s.add(finite_AW, bounded_increasing_sa, ~has_lub)
print('The theorem together with all stipulated witness conditions is:', s.check())
print('Boundedness: 0 <= a_n <= 1 implies ||a_n|| <= 1.')
print('The quasitrace and the positive increment value are not needed.')
