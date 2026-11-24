from itertools import product

def upper_checks():
    U = set(range(2))
    subsets = [frozenset(x for x in U if m >> x & 1) for m in range(4)]
    normal = diagonal = joins = 0
    for bits in product((0,1), repeat=8):
        R = dict(zip(product(U,repeat=3),bits))
        H = {(x,u) for x,u in product(U,repeat=2)
             if all(R[x,u,v] for v in U)}
        A = {x for x in U if any(all(R[x,u,v] for v in U) for u in U)}
        assert A == {x for x,u in H}
        normal += 1
    axioms = list(product(U,subsets))
    rows = [[a for k,a in enumerate(axioms) if m >> k & 1] for m in range(256)]
    def image(row,A): return {x for x,F in row if F <= A}
    for r0,r1 in product(rows,repeat=2):
        rs = [r0,r1]
        flat = [(i,F) for i in U for x,F in rs[i] if x == i]
        for A in subsets:
            assert image(flat,A) == {i for i in U if i in image(rs[i],A)}
            diagonal += 1
    for A,row in product(subsets,rows):
        if image(row,A) == U-A:
            T = {(0,x) for x in A} | {(1,x) for x in U-A}
            assert {(1-b,x) for b,x in set(product(U,U))-T} == T
            joins += 1
    return normal, diagonal, joins

def tree_checks(depth=4):
    INF = -1
    outcomes = (INF,0,1)
    nodes = [s for d in range(depth+1) for s in product(outcomes,repeat=d)]
    U = set(nodes)
    def pref(a,b): return b[:len(a)] == a
    def region(s): return {t for t in U if pref(s,t)}
    def body(s):
        return {s} | set().union(*(region(s+(j,)) for j in (0,1)))
    def Z(s):
        return set().union(*(body(s[:i]) for i,x in enumerate(s) if x == INF))
    def exclusion(s,j): return Z(s) | {s} | region(s+(j,))
    def merge(c,k,v):
        if k in c and c[k] != v: return False
        c[k] = v
        return True
    bg = failures = 0
    for s in nodes:
        if len(s) >= depth: continue
        assert body(s).isdisjoint(region(s+(INF,)))
        assert body(s) | region(s+(INF,)) == region(s)
        for failure in (False,True):
            for j in ((0,1) if failure else (None,)):
                current = {s[:i]:(None if x == INF else x) for i,x in enumerate(s)}
                current[s] = j
                deleted = ({s} | region(s+(j,))) if failure else body(s)
                for t in nodes:
                    if t == s or (failure and pref(s+(j,),t)): continue
                    for k in (0,1):
                        c = dict(current)
                        possible = merge(c,t,k)
                        for i,x in enumerate(t):
                            if x != INF: possible = merge(c,t[:i],x) and possible
                        if possible:
                            # Overestimates R_{s,j} by the whole bank {s}.
                            assert deleted <= exclusion(t,k)
                            if failure: failures += 1
                            else: bg += 1
    for t in nodes:
        for i,x in enumerate(t):
            if x == INF: assert body(t[:i]) <= Z(t)
    return len(nodes), bg, failures

if __name__ == '__main__':
    print('upper:', upper_checks())
    print('tree:', tree_checks())
