from itertools import combinations, product
import sympy as sp

def johnson_basis_check(n):
    # Coordinates (i,j,k) of e_i^* tensor (e_j wedge e_k), j<k.
    coords = [(i,j,k) for i in range(n) for j,k in combinations(range(n),2)]
    pos = {v:a for a,v in enumerate(coords)}
    columns = []
    # K_ij: x_i -> x_j x_i x_j^{-1}.
    for i in range(n):
        for j in range(n):
            if i != j:
                a,b = sorted((j,i))
                columns.append((pos[i,a,b], 1 if j<i else -1))
    # K_ijk: x_i -> [x_j,x_k] x_i, j<k, i not in {j,k}.
    for i in range(n):
        for j,k in combinations([j for j in range(n) if j != i], 2):
            columns.append((pos[i,j,k],1))
    assert len(columns) == len(coords) == n*n*(n-1)//2
    assert sorted(a for a,s in columns) == list(range(len(coords)))
    assert all(s in (-1,1) for a,s in columns)
    return len(coords)

def centralizer_check(d):
    # P -> ([P,X],[P,Y]) on the entire degree-d tensor space over Q.
    words = list(product(range(2), repeat=d))
    out = list(product(range(2), repeat=d+1))
    pos = {w:i for i,w in enumerate(out)}
    M = sp.zeros(2*len(out),len(words))
    for col,w in enumerate(words):
        for x in range(2):
            M[x*len(out)+pos[w+(x,)],col] += 1
            M[x*len(out)+pos[(x,)+w],col] -= 1
    assert M.rank() == len(words)
    return len(words)

for n in range(2,9):
    print('Johnson signed-basis check:',n,johnson_basis_check(n))
for d in range(1,7):
    print('Two-variable tensor centralizer check:',d,centralizer_check(d))
