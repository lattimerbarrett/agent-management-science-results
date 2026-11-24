from z3 import Bool, Implies, And, Solver
# Encode only the application of the supplied, verified theorem;
# this is not a computational proof of the structural theorem itself.
finite_aw_factor = Bool('finite_aw_factor')
bounded_increasing = Bool('bounded_increasing_sequence')
has_lub = Bool('has_lub_in_self_adjoint_part')
s = Solver()
s.add(Implies(And(finite_aw_factor, bounded_increasing), has_lub))
s.add(finite_aw_factor, bounded_increasing, ~has_lub)
print('Consistency of the proposed witness with the supplied theorem:', s.check())