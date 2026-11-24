"""Exhaustive checks of the upper-bound finite combinatorial lemmas."""
from itertools import combinations,product

def universal(k):
    V=[(a,A) for a in range(k) for A in range(1<<k) if not (A>>a&1)]
    def edge(x,y):
        a,A=x; b,B=y
        return bool((A>>b&1) and (B>>a&1) and not(A&B))
    E={frozenset((i,j)) for i,j in combinations(range(len(V)),2) if edge(V[i],V[j])}
    assert all(not all(frozenset(e) in E for e in combinations(t,2)) for t in combinations(range(len(V)),3))
    return len(V),len(E)

def supports(k):
    pairs=list(combinations(range(k),2)); count=0
    for bits in range(1<<len(pairs)):
        adj=[0]*k
        for j,(a,b) in enumerate(pairs):
            if bits>>j&1: adj[a]|=1<<b;adj[b]|=1<<a
        def nbr(S):
            z=0
            for i in range(k):
                if S>>i&1:z|=adj[i]
            return z
        nonempty=range(1,1<<k)
        for S,T,U in product(nonempty,repeat=3):
            if (S&T) or (T&U) or (U&S):continue
            Ns,Nt,Nu=map(nbr,(S,T,U))
            if Ns&Nt or Nt&Nu or Nu&Ns:continue
            union=S|T|U
            if union&nbr(union):continue
            six=(S,T,U,Ns,Nt,Nu)
            assert all(not(a&b) for a,b in combinations(six,2))
            assert sum(a.bit_count() for a in six)<=k
            count+=1
    return count

if __name__=='__main__':
    print('Universal triangle-free targets:', [universal(k) for k in range(1,5)])
    print('Support configurations exhaustively verified:', [supports(k) for k in range(1,6)])
