"""Exact finite certificate for d=8, with only Python standard library.
Bron--Kerbosch counts lambda(7). The decision-tree recurrence counts
pairwise incompatible intersecting families admitting 3 disjoint transversals.
"""
from itertools import combinations, product
from functools import lru_cache
import json

def lambda_by_maximal_cliques(k):
    n=(1<<k)-1  # vertices are all nonempty subsets
    adj=[sum(1<<(b-1) for b in range(1,n+1) if a!=b and a&b)
         for a in range(1,n+1)]
    def count(P,X):
        if not P:
            return int(not X)
        # Pivoted Bron--Kerbosch: branches enumerate every maximal clique once.
        choices=P|X
        best=-1
        while choices:
            z=choices&-choices
            u=z.bit_length()-1
            choices-=z
            score=(P&adj[u]).bit_count()
            if score>best:
                best=score
                pivot=u
        candidates=P&~adj[pivot]
        answer=0
        while candidates:
            z=candidates&-candidates
            v=z.bit_length()-1
            candidates-=z
            answer+=count(P&adj[v],X&adj[v])
            P-=z
            X|=z
        return answer
    return count((1<<n)-1,0)

def colorful_tree_count():
    # Restricted-growth strings enumerate unlabeled partitions into 3 classes.
    parts=[c for c in product(range(3),repeat=8)
           if c[0]==0 and set(c)=={0,1,2} and c.index(1)<c.index(2)]
    assert len(parts)==966
    U=255
    pairs=[(sum(1<<i for i in C),U^sum(1<<i for i in C))
           for C in combinations(range(8),4) if 0 in C]
    assert len(pairs)==35
    assert all(a.bit_count()==b.bit_count()==4 and not(a&b) and a|b==U
               for a,b in pairs)
    masks=[]
    for a,b in pairs:
        masks.append(tuple(sum(1<<j for j,c in enumerate(parts)
                               if len({c[i] for i in range(8) if s>>i&1})==3)
                           for s in (a,b)))
    @lru_cache(None)
    def leaves(state,k):
        assert state
        if k==len(pairs):
            return 1
        a,b=(state&m for m in masks[k])
        if not a or not b:
            # Important: skip this pair; impose no constraint at this node.
            return leaves(state,k+1)
        return leaves(a,k+1)+leaves(b,k+1)
    count=leaves((1<<len(parts))-1,0)
    return count,leaves.cache_info().currsize

if __name__=='__main__':
    values=[lambda_by_maximal_cliques(k) for k in range(1,8)]
    assert values==[1,2,4,12,81,2646,1422564]
    count,states=colorful_tree_count()
    assert count==1556341 and states==2050
    assert count>values[-1]
    print(json.dumps({'lambda_1_through_7':values,
                      'colorful_tree_leaves':count,
                      'memoized_states':states,
                      'strict_margin_over_lambda7':count-values[-1]},indent=2))
