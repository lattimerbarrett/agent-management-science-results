"""Exhaustive finite checks for the elementary RM minimum-distance lemma."""
from itertools import combinations
from math import comb

def monomial_tables(m,r):
    return [sum(1<<x for x in range(1<<m) if all((x>>i)&1 for i in S))
            for k in range(r+1) for S in combinations(range(m),k)]

def check(m,r):
    basis=monomial_tables(m,r)
    word=0; prev=0; minwt=1<<m; count=0
    for j in range(1,1<<len(basis)):
        gray=j^(j>>1); flip=gray^prev
        word ^= basis[flip.bit_length()-1]; prev=gray
        w=word.bit_count()
        assert w >= 1<<(m-r)
        if r<m: assert w%2==0
        minwt=min(minwt,w);count+=1
    assert minwt == 1<<(m-r)
    return (m,r,len(basis),count,minwt)

if __name__=='__main__':
    for m in range(1,6):
        for r in range(m+1):
            if sum(comb(m,k) for k in range(r+1))<=17:
                print(check(m,r))
    print('All checks passed.')
