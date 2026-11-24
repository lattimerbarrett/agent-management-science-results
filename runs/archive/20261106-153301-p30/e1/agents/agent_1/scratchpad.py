from math import comb, prod
from itertools import combinations, product
from pathlib import Path

# Expand (1+t)^n over F_2 by repeated squaring, using exact sets.
def mod2_binomial_support(n):
    support = {0}
    bit = 1
    while bit <= n:
        if n & bit:
            support ^= {i + bit for i in support}
        bit <<= 1
    return support

for s in range(3, 13):
    m = 1 << (s-1)
    j, d = 2*m-2, 3*m-2
    support = mod2_binomial_support(j)
    assert support == set(range(0, j+1, 2))
    survivors = {(j+i, 2*j-i) for i in support
                 if j+i <= d and 2*j-i <= d}
    assert survivors == {(d-2, d), (d, d-2)}
    assert comb(j, m-2) % 2 == 1
    assert 2*(d-1) == 3*j
    assert 2*(d-2) < 3*j
    print(f's={s}, j={j}, bounds=[{d-1},{d}], exact F2 survivors={sorted(survivors)}')

# Check every sign-history with <=2 root events; an event may flip
# either sign or both, so this includes simultaneous hyperplane roots.
checked = 0
for k in range(3):
    for initial in product((-1, 1), repeat=2):
        for flips in product(((1,0),(0,1),(1,1)), repeat=k):
            state = initial
            labels = {state}
            for f in flips:
                state = tuple(-v if flip else v for v, flip in zip(state, f))
                labels.add(state)
            assert len(labels) <= 3
            checked += 1
print('All short root sign histories checked:', checked)

# Actual reference-section zeros at s=3. All linear forms are evaluations
# of a polynomial at different positive integers. A projective zero is
# represented by the monic polynomial having its assigned roots.
s=3
m=1 << (s-1)
j,d=2*m-2,3*m-2
a,b=d-2,d
fixed=list(range(1,j+1))
mixed=list(range(j+1,2*j+1))
def evaluate_root_polynomial(roots,t):
    return prod(t-r for r in roots)
def vandermonde(points):
    return prod(y-x for i,x in enumerate(points) for y in points[i+1:])
count=0
for chosen in combinations(mixed,a-j):
    chosen=set(chosen)
    ur=fixed+sorted(chosen)
    vr=fixed+sorted(set(mixed)-chosen)
    assert len(ur)==a and len(vr)==b
    assert vandermonde(ur) != 0 and vandermonde(vr) != 0
    for t in mixed:
        U,V=evaluate_root_polynomial(ur,t),evaluate_root_polynomial(vr,t)
        assert U*V==0 and (U==0)!=(V==0)
    # Jacobian after grouping rows: evaluation Vandermondes, times
    # nonzero opposite-factor values in the product-equation rows.
    determinant=(vandermonde(ur)*vandermonde(vr)*
        prod(evaluate_root_polynomial(vr,t) for t in chosen)*
        prod(evaluate_root_polynomial(ur,t) for t in set(mixed)-chosen))
    assert determinant != 0
    count+=1
assert count==comb(j,a-j)==15
print('s=3 reference section: all',count,'zeros checked simple; parity odd')
Path('workspace/agent1_checks.py').write_text(Path('scratchpad.py').read_text())
