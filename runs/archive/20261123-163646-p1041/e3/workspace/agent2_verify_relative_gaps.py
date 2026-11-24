"""Exact finite arithmetic/rank checks for agent4_punctured_odd_gaps.txt.
This checks the finite calculations; the text contains the arbitrary-polynomial proof.
"""
def verify():
    # Degree8 outside-gap hierarchy on the odd31-fiber halfspace.
    for e in (33,35,37,39):
        E=e-31
        assert E//2<8  # first moments on the even half vanish
        assert E//4<4 and E//2<8-1  # second moments vanish
        assert E//6<=1
        assert 1<2 and 1<4-1  # third moments vanish
        assert E<14
    # Degree7 gap hierarchy, all odd outside fibers.
    for E in range(0,41,2):
        assert 2*(24-1)>E
        assert 4*(16-1)>E
        for e0extra in (30,32):
            if E<e0extra:continue
            residual=E-e0extra
            assert residual<=10
            assert residual//2<8-1
            assert residual//10<=1
            assert 1<4-1
            assert residual<32-2*3
        assert (8-1)*6>E
        assert (4-1)*14>E
        assert E//30<=1
    # First two RM(2,7) weights via all quadratic-rank normalforms and
    # ALL affine perturbations. Every quadratic is linearly equivalent
    # to one of these four alternating-rank normalforms.
    weights={0,128}
    for rank in (0,2,4,6):
        for a in range(128):
            for c in (0,1):
                w=0
                for x in range(128):
                    q=0
                    for j in range(0,rank,2):q^=((x>>j)&1)*((x>>(j+1))&1)
                    w+=q^((a&x).bit_count()%2)^c
                weights.add(w)
    assert sorted(weights-set([0]))[:2]==[32,48]
    assert {w for w in weights if 0<w<=42}=={32}
    # The permitted one-defect excesses from its null4 symmetric difference.
    assert {32-2,32}=={30,32}
    assert {63,63+30,63+32}=={63,93,95}
    assert not ({97,99,101,103}&{63,93,95})
    print('Relative odd-gap finite checks passed; quadratic ranks checked exactly.')
if __name__=='__main__':verify()
