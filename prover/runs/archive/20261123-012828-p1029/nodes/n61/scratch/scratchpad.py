from z3 import Bool, Solver, Implies, Not
# Separate the two requirements. The verified supremum result applies
# to the algebra/quasitrace/order/fixed-positive-increment hypotheses.
fixed_increment_hypotheses = Bool('fixed_increment_hypotheses')
has_lub = Bool('has_lub')
s = Solver()
s.add(Implies(fixed_increment_hypotheses, has_lub))
s.push()
s.add(fixed_increment_hypotheses)
print('Fixed-increment hypotheses alone:', s.check())
s.add(Not(has_lub))
print('Fixed-increment hypotheses plus no least upper bound:', s.check())
s.pop()
print('Conclusion: the verified supremum result excludes membership in G,')
print('not the possibility of fixed-increment sequences themselves.')
