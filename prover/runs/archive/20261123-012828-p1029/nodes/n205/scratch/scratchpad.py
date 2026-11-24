# Audit the hypotheses of the supplied monotone sequential completeness theorem.
hypotheses = {
    'unital C*-algebra': 'M is a nonzero unital complex C*-algebra',
    'AW* property': 'every subset S has right annihilator pM for a projection p',
    'factor': 'Z(M) = C1',
    'finite': 'v*v = 1 implies vv* = 1',
    'increasing self-adjoint sequence': '0 <= a_n <= a_(n+1)',
    'bounded sequence': '0 <= a_n <= 1, hence ||a_n|| <= 1',
}
for hypothesis, verification in hypotheses.items():
    print(hypothesis + ': ' + verification)
print('Supplied structural theorem applies: sup_n a_n exists in M_sa.')
print('This contradicts the required absence of a least upper bound.')
print('No quasitrace hypothesis is used.')
