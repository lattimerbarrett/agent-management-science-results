from z3 import Bool, Implies, Solver, Not
weakly_cototal = Bool('weakly_cototal')
skip_cototal = Bool('skip_cototal')
s = Solver()
# Check the logical consequence of the weak-cototality/skip implication.
# This does not establish that recursion-theoretic implication itself.
s.add(Implies(weakly_cototal, skip_cototal))
s.add(weakly_cototal, Not(skip_cototal))
print(s.check())
