from itertools import product
from functools import lru_cache
from collections import defaultdict
from sympy import SparseMatrix


def add(a, b, scale=1):
    c = defaultdict(int, a)
    for w, k in b.items():
        c[w] += scale*k
    return {w:k for w,k in c.items() if k}


def mul(a, b, cutoff):
    c = defaultdict(int)
    for u, x in a.items():
        for v, y in b.items():
            if len(u)+len(v) <= cutoff:
                c[u+v] += x*y
    return {w:k for w,k in c.items() if k}


def expansion(word, n, cutoff):
    ans = {():1}
    for signed in word:
        i = abs(signed)-1
        factor = {():1}
        if signed > 0:
            factor[(i,)] = 1
        else:
            for d in range(1, cutoff+1):
                factor[(i,)*d] = (-1)**d
        ans = mul(ans, factor, cutoff)
    return ans


def check_first_johnson(n):
    coords = [(i,a,b) for i in range(n) for a in range(n) for b in range(a+1,n)]
    row = {v:k for k,v in enumerate(coords)}
    cols = []
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            # phi(x_i)*x_i^-1 for x_i -> x_j*x_i*x_j^-1
            cols.append((i, [j+1,i+1,-j-1,-i-1]))
        for j in range(n):
            for k in range(j+1,n):
                if i in (j,k):
                    continue
                # x_i -> [x_j,x_k]*x_i
                cols.append((i, [j+1,k+1,-j-1,-k-1]))
    entries = {}
    for col, (i,word) in enumerate(cols):
        p = expansion(word,n,2)
        assert p.get((),0) == 1
        assert not any(len(w)==1 for w in p)
        for a in range(n):
            assert p.get((a,a),0) == 0
            for b in range(a+1,n):
                val = p.get((a,b),0)
                assert val == -p.get((b,a),0)
                if val:
                    entries[row[(i,a,b)], col] = val
    M = SparseMatrix(len(coords),len(cols),entries)
    # An integer inverse is certified by M^T M=I and squareness.
    assert M.rows == M.cols
    assert M.T*M == SparseMatrix.eye(M.cols)
    return M.rows


def lyndon(w):
    return all(w < w[i:] for i in range(1,len(w)))


@lru_cache(None)
def lie_bracket_word(w):
    if len(w)==1:
        return {w:1}
    for i in range(1,len(w)):
        if lyndon(w[i:]):
            a,b=lie_bracket_word(w[:i]),lie_bracket_word(w[i:])
            return add(mul(a,b,len(w)),mul(b,a,len(w)),-1)
    raise AssertionError(w)


def check_no_lie_center(n,d):
    basis=[w for w in product(range(n),repeat=d) if lyndon(w)]
    rows={}
    entries={}
    for col,w in enumerate(basis):
        p=lie_bracket_word(w)
        for i in range(n):
            x={(i,):1}
            q=add(mul(p,x,d+1),mul(x,p,d+1),-1)
            for v,k in q.items():
                key=(i,v)
                if key not in rows:
                    rows[key]=len(rows)
                entries[rows[key],col]=k
    M=SparseMatrix(len(rows),len(basis),entries)
    rank=M.rank()
    assert rank==len(basis)
    return len(basis),rank


if __name__=='__main__':
    for n in range(2,8):
        print('tau_1 Magnus-generator matrix:',n,check_first_johnson(n),'integrally invertible')
    for n,max_d in [(2,6),(3,4)]:
        for d in range(1,max_d+1):
            dimension,rank=check_no_lie_center(n,d)
            print('free-Lie common centralizer test:',n,d,'dimension',dimension,'rank',rank)
