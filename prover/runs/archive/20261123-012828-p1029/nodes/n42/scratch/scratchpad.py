from z3 import Bool, Solver, Implies, And, Not
# Logical application only: the structural theorem is supplied as verified,
# not proved by this computation.
finite_aw_factor = Bool('finite_aw_factor')
bounded_increasing = Bool('bounded_increasing')
has_lub = Bool('has_lub')
s = Solver()
s.add(Implies(And(finite_aw_factor, bounded_increasing), has_lub))
s.add(finite_aw_factor, bounded_increasing, Not(has_lub))
print('Verified structural theorem together with the proposed witness:', s.check())
