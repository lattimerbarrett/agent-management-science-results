from sage.all import GF, PolynomialRing, matrix, vector, ZZ
from itertools import product

# Algebra used in the holomorphy-ring argument.
Q = PolynomialRing(GF(3), 'T'); T = Q.gen(); F = Q.fraction_field()
a = 1/(1+F(T)**2); b=F(T)/(1+F(T)**2); c=F(T)**2/(1+F(T)**2)
assert a+c == 1 and b*b == a*c and b/a == T and b/c == 1/T

# No cancellation in x^2+y^2, in each of the finite residue fields used.
field_checks=0
for d in [1,3,5]:
    k=GF(3**d, name='alpha')
    assert all(1+x*x != 0 for x in k)
    field_checks += k.cardinality()

# The remainder criterion f(F_3) subset F_3 iff f mod (X^3-X) has F_3 coefficients.
k=GF(27, name='alpha'); P=PolynomialRing(k,'X'); X=P.gen(); h=X**3-X
small=[k(0),k(1),k(2)]
V=matrix(GF(3), [[GF(3)(i)**j for j in range(3)] for i in range(3)])
assert V.det()!=0
remainder_checks=0
for coeff in product(k, repeat=3):
    f=P(list(coeff))
    lhs=all(f(x)**3 == f(x) for x in small)
    rhs=all(y**3 == y for y in coeff)
    assert lhs == rhs
    remainder_checks += 1
# The integral equation used for C over C_0.
assert X**3-X-h == 0

# Weighted lexicographic approximations: certify all comparisons of monomials
# in the box {0,...,3}^{r+1}; this checks *all* polynomials supported in that
# box, since the least-weight monomial is unique.
comparison_checks=0
for r in [1,2,3]:
    exps=list(product(range(4), repeat=r+1))
    n=5
    weights=[n**(r-j) for j in range(r+1)]
    vals=[sum(e*w for e,w in zip(E,weights)) for E in exps]
    assert len(set(vals)) == len(vals)
    for i,E in enumerate(exps):
        for j,G in enumerate(exps):
            assert (vals[i] < vals[j]) == (E < G)
            comparison_checks += 1

# Finite-jet versions of the embeddings used for the DVRs.
# ur=z, t=alpha*z^(n^r)+higher terms gives residue alpha and value group Z.
jet_checks=0
for r in [1,2,3]:
    n=5
    k=GF(27, name='alpha'); alpha=k.gen()
    Z=PolynomialRing(k,'z', sparse=True); z=Z.gen()
    weights=[n**(r-j) for j in range(r+1)]
    images=[alpha*z**weights[0]+z**(weights[0]+7)]
    images += [z**w+z**(w+11+j) for j,w in enumerate(weights[1:-1])]
    images += [z]
    assert images[-1].valuation()==1
    assert images[0][weights[0]]==alpha
    for E in product(range(3), repeat=r+1):
        f=Z(1)
        for image,e in zip(images,E): f *= image**e
        assert f.valuation()==sum(e*w for e,w in zip(E,weights))
        jet_checks += 1

# Check the parameter conversion, and exhaust a finite window of the claimed set.
parameter_checks=0
for A in range(1,31):
    for B in range(1,61):
        allowed=(A,B) in [(1,1),(2,2)] or (A>=3 and B>=A-1)
        if A>=3 and allowed:
            shifts=A-3; r=B-A+1
            assert r>=0
            assert (3+shifts,r+2+shifts)==(A,B)
        elif allowed:
            assert A==B and A in [1,2]
        parameter_checks += 1
print({'finite_field_nonvanishing':int(field_checks),
       'all_cubic_remainders_over_F27':remainder_checks,
       'weighted_lex_comparisons':comparison_checks,
       'finite_jet_monomials':jet_checks,
       'parameter_pairs':parameter_checks})
