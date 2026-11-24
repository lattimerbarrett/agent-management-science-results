"""Finite checks for maximal intersecting families and suitable permutations.
All assertions are exhaustive for k<=5, not proofs for arbitrary k.
"""
from itertools import combinations

def maximal_intersecting(k):
    U=(1<<k)-1
    # Complement pairs represented by member not containing element k.
    reps=list(range(1<<(k-1)))
    answer=[]
    for bits in range(1<<len(reps)):
        F=frozenset(A if (bits>>j)&1 else U^A for j,A in enumerate(reps))
        if 0 in F: continue
        # Self-duality plus upward closure is equivalent to maximal intersecting.
        if all((A|(1<<i)) in F for A in F for i in range(k)):
            assert all(A&B for A in F for B in F)
            assert all(any(not(A&B) for B in F) for A in range(U+1) if A not in F)
            answer.append(F)
    return answer

def suitable_orders(k, families):
    reps=list(range(1<<(k-1)))
    return [sorted(range(len(families)),key=lambda j:tuple(int((A in families[j])==bool(A&(1<<i))) for A in reps)) for i in range(k)]

def check_suitable(orders):
    n=len(orders[0]); positions=[{x:i for i,x in enumerate(o)} for o in orders]
    for x,y in combinations(range(n),2):
        assert any(p[x]>p[y] for p in positions)
        assert any(p[y]>p[x] for p in positions)
    for T in combinations(range(n),3):
        for x in T:
            assert any(all(p[x]>p[y] for y in T if x!=y) for p in positions), (T,x)

def check(k):
    families=maximal_intersecting(k)
    orders=suitable_orders(k,families)
    # One vertex is exceptional: no need to reverse an isolated pair.
    if len(families)>=2: check_suitable(orders)
    n=len(families)
    augmented=[[n]+o for o in orders]+[list(range(n+1))]
    check_suitable(augmented)
    return len(families)

if __name__=='__main__':
    expected=[1,2,4,12,81]
    for k,e in enumerate(expected,1):
        actual=check(k)
        assert actual==e
        print(f'k={k}: lambda={actual}; suitable construction and extra-vertex construction checked')
