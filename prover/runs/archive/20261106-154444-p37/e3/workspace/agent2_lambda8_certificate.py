"""Exact lambda(8), Python standard library (~3 s).
Count intersecting antichains on [7]; proof gives lambda(8).
"""
from functools import lru_cache

def count_lambda(k):
    n=(1<<(k-1))-1  # nonempty subsets of [k-1]
    adj=[sum(1<<(b-1) for b in range(1,n+1)
             if a!=b and (not a&b or a&b==a or a&b==b)) for a in range(1,n+1)]
    @lru_cache(None)
    def count(P):
        if not P:return 1
        candidates=P
        best=-1
        isolated=0
        while candidates:
            bit=candidates&-candidates
            i=bit.bit_length()-1
            candidates-=bit
            degree=(adj[i]&P).bit_count()
            if not degree:isolated|=bit
            if degree>best:
                best=degree
                v=i
        if isolated:
            return (1<<isolated.bit_count())*count(P^isolated)
        component=frontier=1<<v
        while frontier:
            q=frontier
            frontier=0
            while q:
                bit=q&-q
                q-=bit
                frontier|=adj[bit.bit_length()-1]
            frontier&=P&~component
            component|=frontier
        if component!=P:
            return count(component)*count(P^component)
        Q=P&~(1<<v)
        return count(Q)+count(Q&~adj[v])
    # Empty antichain is allowed; the empty SET cannot be a member.
    answer=count((1<<n)-1)
    states=count.cache_info().currsize
    count.cache_clear()
    return answer,states

if __name__=='__main__':
    answer,states=count_lambda(8)
    assert answer==229809982112 and states==1200872
    print('lambda(8)=%d; memo states=%d'%(answer,states))
