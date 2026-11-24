"""Executable checks for the lower bound and the random-block upper construction."""
from itertools import combinations, product
from math import isqrt, ceil, log, exp, e, comb
import json

# Exact sorted-deficiency lower-bound sum, and its closed form.
def lower_bound(t):
    m = isqrt(t)
    return (6*m*t - 2*m**3 - 3*m*m + 5*m - 6)//6
for t in range(2, 10001):
    assert lower_bound(t) == sum(isqrt(j) for j in range(2, t+1))

# These rational inequalities also certify the elementary estimates 5/2<e<11/4.
from fractions import Fraction
partial = sum((Fraction(1, __import__('math').factorial(j)) for j in range(4)), Fraction())
assert partial > Fraction(5, 2)
assert partial + Fraction(1, 18) < Fraction(11, 4)  # tail from j=4 bounded geometrically
assert Fraction(25) > 2*Fraction(11,4)**2

# Check the displayed probability bounds numerically, over many parameter values.
# The proof establishes them for every n>=100; this is an independent arithmetic audit.
parameter_results = []
for n in list(range(100, 10001)) + [10**j for j in range(5,101,5)]:
    r = isqrt(n) + (isqrt(n)**2 < n)
    L = ceil(log(n))
    m = 100*n*L
    assert 2*r*(r-1) >= n-1
    assert r*r <= 2*n
    assert log(m) + log(n) <= 4*L + 1e-12
    assert log(5*L/(2*e)) > 1
    logs = [2*log(n)-20*L, log(n)-25*r*L, -L*r]
    top = max(logs)
    log_failure = top + log(sum(exp(x-top) for x in logs))
    assert log_failure < 0
    if n in [100, 1000, 10000, 10**20, 10**100]:
        d = r*(200*L+1)
        parameter_results.append({'n':str(n),'log_failure_bound':log_failure,
                                  'log_upper_over_log_n':log(n*d)/log(n),
                                  'log_lower_over_log_n':log(lower_bound(n))/log(n)})

# Exhaustive finite audit of the ACTUAL construction (including private padding).
# Small pair-block systems need not have the asymptotic parameters.  We calculate
# their exact contact bound and use the same construction and cover-avoidance rule.
def toy_check(n):
    r = 2
    blocks = [frozenset(B) for B in combinations(range(n),2)]
    incident = [{a for a,B in enumerate(blocks) if i in B} for i in range(n)]
    codeg = [[len(incident[i]&incident[j]) for j in range(n)] for i in range(n)]
    def contacts(i,E):
        return {j for j in range(n) if j != i and
                2*len(E & incident[j]) >= codeg[i][j]}
    modes = []
    for i in range(n):
        for s in range(r+1):
            for EE in combinations(sorted(incident[i]),s):
                E = set(EE)
                modes.append((i,E,contacts(i,E)))
    D = max(map(len,incident))
    K = max(len(J) for i,E,J in modes)
    d = D+K
    nxt = 0
    X=[]
    for i in range(n):
        X.append(set(range(nxt,nxt+n))); nxt += n
    z=list(range(nxt,nxt+len(blocks))); nxt += len(blocks)
    P=[]
    for i in range(n):
        P.append(set(range(nxt,nxt+d+n))); nxt += d+n
    V=set(range(nxt)); k=n+d
    # Enumerate every possible core-contact choice.  Extra padding can only add
    # intersections, so checking these unpadded edges checks every full edge pair.
    bases=[]
    for i,E,J in modes:
        fixed=X[i] | {z[a] for a in incident[i]-E}
        for reps in product(*(sorted(X[j]) for j in sorted(J))):
            B=fixed | set(reps)
            assert len(B)-n <= d
            assert all(not (X[j] <= B) for j in range(n) if j != i)
            bases.append((i,B))
    for i,B in bases:
        for j,C in bases:
            assert B&C
    # Every (n-1)-set C is defeated by explicitly constructing a valid k-edge.
    checked=0
    for CC in combinations(sorted(V),n-1):
        C=set(CC)
        U=[i for i in range(n) if not C&X[i]]
        Z={a for a,zz in enumerate(z) if zz in C}
        assert len(U)>len(Z)
        i=min(U,key=lambda j:len(Z & incident[j]))
        E=Z & incident[i]
        assert len(E)<r
        J=contacts(i,E)
        F=X[i] | {z[a] for a in incident[i]-E}
        for j in J:
            F.add(min(X[j]-C))
        padding=k-len(F)
        F |= set(sorted(P[i]-C)[:padding])
        assert len(F)==k and not F&C
        assert X[i] <= F and all(not(X[j]<=F) for j in range(n) if j!=i)
        checked+=1
    return {'n':n,'vertices':len(V),'k':k,'modes':len(modes),
            'unpadded_edges':len(bases),'all_small_covers_defeated':checked}

# An actual indexed random block witness for the lemma at n=100.
# Here its universal expansion property is checked exactly by r^2 < 5Lr.
from random import Random
rng=Random(20260417)
n=100; r=10; L=5; m=100*n*L
degree=[0]*n; co=[[0]*n for _ in range(n)]
for _ in range(m):
    B=rng.sample(range(n),r)
    for i in B: degree[i]+=1
    for i,j in combinations(B,2):
        co[i][j]+=1; co[j][i]+=1
minimum=min(co[i][j] for i in range(n) for j in range(i))
assert minimum>=10*L and max(degree)<=200*r*L
assert r*r<5*L*r
witness={'n':n,'blocks':m,'minimum_codegree':minimum,'maximum_degree':max(degree)}
results={'parameters':parameter_results,'toy_checks':[toy_check(3),toy_check(4)],'actual_block_witness':witness}
print(json.dumps(results,indent=2))
with open('workspace/agent1_complete_checks.json','w') as f: json.dump(results,f,indent=2)
with open('workspace/agent1_complete_checks.py','w') as f: f.write(open('scratchpad.py').read())
