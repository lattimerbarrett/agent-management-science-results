from z3 import Real, Solver, sat
# Only necessary scalar consequences, NOT an AW*-algebra model.
for eta in ['1/3', '2/5', '1/2', '3/5']:
    e=Real('e')
    alphas=[Real('a'+str(i)) for i in range(8)]
    S=Solver(); S.add(e==eval(eta,{'__builtins__':{}}, {}) if False else True)
    p,q=map(int,eta.split('/'))
    S.add(q*e==p)
    for a in alphas: S.add(e<=a, a<=1-e)
    for a,b in zip(alphas,alphas[1:]): S.add(a<=b)
    print(eta, S.check())
print('These results concern only the scalar relaxation; sat does not construct a witness.')
