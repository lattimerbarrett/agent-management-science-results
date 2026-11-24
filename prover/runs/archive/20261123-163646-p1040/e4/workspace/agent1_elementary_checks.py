"""Elementary exact finite checks for the Andreadakis problem.
No finite check here is asserted to establish an all-degree statement.
"""
from itertools import product
import numpy as np
from pathlib import Path

def rank_mod(rows, p=1000003):
    pivots={}
    for row in rows:
        row={i:int(a)%p for i,a in enumerate(row) if a%p}
        while row:
            j=min(row)
            if j not in pivots:
                a=pow(row[j],-1,p)
                pivots[j]={k:v*a%p for k,v in row.items()}
                break
            a=row[j]
            for k,v in pivots[j].items():
                q=(row.get(k,0)-a*v)%p
                if q: row[k]=q
                elif k in row: del row[k]
    return len(pivots)

def johnson_basis(n):
    # Magnus generators K_ij: x_i -> x_j x_i x_j^{-1};
    # K_ijk: x_i -> [x_j,x_k] x_i (j<k, j,k != i).
    basis=[(i,j,k) for i in range(n) for j in range(n) for k in range(j+1,n)]
    vectors=[]
    for i in range(n):
        for j in range(n):
            if i==j: continue
            v=[0]*len(basis)
            v[basis.index((i,min(i,j),max(i,j)))]=1 if j<i else -1
            vectors.append(v)
        for j in range(n):
            for k in range(j+1,n):
                if i in (j,k): continue
                v=[0]*len(basis); v[basis.index((i,j,k))]=1
                vectors.append(v)
    assert len(vectors)==len(basis)==n*n*(n-1)//2
    assert all(sum(abs(v[i]) for v in vectors)==1 for i in range(len(basis)))
    return len(basis)

def common_centralizer(n,d):
    # Over F_p, verify simultaneous commutators with X_0,X_1
    # have zero kernel on degree d free associative polynomials.
    words=list(product(range(n),repeat=d))
    out=list(product(range(n),repeat=d+1)); idx={w:i for i,w in enumerate(out)}
    rows=[]
    for w in words:
        row=[0]*(2*len(out))
        for g in range(2):
            row[g*len(out)+idx[w+(g,)]]+=1
            row[g*len(out)+idx[(g,)+w]]-=1
        rows.append(row)
    r=rank_mod(rows)
    assert r==len(words),(n,d,r,len(words))
    return r

if __name__=='__main__':
    import shutil
    shutil.copyfile(__file__, 'workspace/agent1_elementary_checks.py')
    for n in range(2,9):
        print('Johnson signed-permutation basis:',n,johnson_basis(n))
    for n,limit in [(2,8),(3,5),(4,3)]:
        for d in range(1,limit+1):
            print('Common associative centralizer zero:',n,d,common_centralizer(n,d))
