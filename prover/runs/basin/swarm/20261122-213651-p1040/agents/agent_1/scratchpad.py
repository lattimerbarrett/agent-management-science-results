from collections import defaultdict

def mul(a, b, degree=2):
    out = defaultdict(int)
    for u, x in a.items():
        for v, y in b.items():
            if len(u + v) <= degree:
                out[u + v] += x*y
    return {w: a for w, a in out.items() if a}

def expand(word):
    p = {(): 1}
    for a in word:
        i = abs(a)-1
        factor = {(): 1, (i,): 1} if a > 0 else {(): 1, (i,): -1, (i,i): 1}
        p = mul(p, factor)
    return p

def johnson_column(n, target, word):
    # Degree-two Magnus coefficient of phi(x_target)*x_target^{-1}.
    p = expand(word + [-(target+1)])
    assert p.get((), 0) == 1
    assert not any(len(w)==1 and a for w,a in p.items())
    result = {}
    for j in range(n):
        assert p.get((j,j), 0) == 0
        for k in range(j+1,n):
            a = p.get((j,k),0)
            assert p.get((k,j),0) == -a
            if a:
                result[(target,j,k)] = a
    return result

def check(n):
    basis = {(i,j,k) for i in range(n) for j in range(n) for k in range(j+1,n)}
    pivots = set()
    for i in range(n):
        for j in range(n):
            if i==j:
                continue
            # x_i -> x_j*x_i*x_j^{-1}
            col = johnson_column(n,i,[j+1,i+1,-(j+1)])
            assert len(col)==1 and abs(next(iter(col.values())))==1
            pivot = next(iter(col))
            assert pivot not in pivots
            pivots.add(pivot)
        for j in range(n):
            for k in range(j+1,n):
                if i in (j,k):
                    continue
                # x_i -> x_i*[x_j,x_k]
                col = johnson_column(n,i,[i+1,j+1,k+1,-(j+1),-(k+1)])
                assert col == {(i,j,k):1}
                assert (i,j,k) not in pivots
                pivots.add((i,j,k))
    assert pivots == basis
    print(f'n={n}: verified signed-permutation Johnson matrix of size {len(basis)}')

for n in range(2,11):
    check(n)
