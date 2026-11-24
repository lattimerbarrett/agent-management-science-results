from agent2_decomp import witness, prefix_order, link

def check_relative_blocker():
    K=frozenset([11,13,21,35])
    L=frozenset([11,13,21,22,26,35,38,44,50,56])
    assert K < L
    assert witness(K,1) is not None and witness(L,1) is not None
    for f in L-K:
        assert witness(K|{f},2) is None # not even shellable
    # Therefore nonedge-capping cannot in general be interpolated using only
    # facets from the prescribed final cap, despite both endpoints being kD.
    a,b=64,128
    D=frozenset(a|f for f in L)|frozenset(b|f for f in K)
    assert witness(D,1) is not None
    for f in L-K:
        assert link(D|{b|f},b)==K|{f}
        assert witness(D|{b|f},3) is None
    return sorted(K), sorted(L), prefix_order(L,1)

if __name__=='__main__': print(check_relative_blocker())
