from functools import lru_cache
from itertools import combinations
from agent4_checker import dec

D=tuple(sorted([39,15,99,53,141,139,113,85,43,165,225,114,209,201,153]))
H=114
order=(114,99,39,15,43,113,53,85,139,141,165,225,201,209,153)

def subs(f):
    s=f
    while True:
        yield s
        if not s:break
        s=(s-1)&f

def verify_edge_decomposition_by_prefix(order):
    old=set(subs(order[0]))
    for F in order[1:]:
        new=[s for s in subs(F) if s not in old]
        minimal=[s for s in new if not any(t!=s and t&s==t for t in new)]
        assert len(minimal)==1
        R=minimal[0]
        assert 1<=R.bit_count()<=2
        assert all((s not in old)==(s&R==R) for s in subs(F))
        # Thus deleting R from the new pure facet complex gives the old one,
        # and its link is a simplex. This is an exact recursive witness.
        old.update(subs(F))
    return True

shared=[i for i in range(8) if H>>i&1]
other=[i for i in range(8) if not H>>i&1]
mp={i:i if i in shared else 8+other.index(i) for i in range(8)}
def mapped(f):
    return sum(1<<mp[i] for i in range(8) if f>>i&1)
Gorder=order+tuple(mapped(f) for f in order[1:])
G=tuple(sorted(Gorder))
if __name__=='__main__':
    assert set(order)==set(D)
    assert verify_edge_decomposition_by_prefix(Gorder)
    skeleton={f^(1<<i) for f in G for i in range(12) if f>>i&1}
    assert dec(tuple(sorted(skeleton)),0)
    for i in (0,8):
        assert not dec(tuple(sorted(f for f in skeleton if not f>>i&1)),0)
    assert not any((f&257)==257 for f in G)
    print('Exact counterexample to bad-deletion-clique/existence lemma checked.')
    print('Edge-decomposition prefix witness:',Gorder)
    print('Nonadjacent bad deletion vertices:',0,8)
