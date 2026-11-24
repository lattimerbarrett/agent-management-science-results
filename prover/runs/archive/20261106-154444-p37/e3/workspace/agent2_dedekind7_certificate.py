"""Exact Dedekind number D(7), only Python standard library (~10 s).
Independent sets of the comparability graph are antichains.
"""
from functools import lru_cache

def count_dedekind(k):
    n=(1<<k)-1  # nonempty subsets
    adj=[sum(1<<(b-1) for b in range(1,n+1)
             if a!=b and (a&b==a or a&b==b)) for a in range(1,n+1)]
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
    # The omitted empty-set vertex is universal. Its only antichain is {empty}.
    answer=count((1<<n)-1)+1
    states=count.cache_info().currsize
    count.cache_clear()
    return answer,states

if __name__=='__main__':
    answer,states=count_dedekind(7)
    assert answer==2414682040998 and states==3525359
    print('D(7)=%d; memo states=%d'%(answer,states))
