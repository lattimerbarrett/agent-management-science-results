"""Finite checks for agent4's minimum-second-derivative192 relativegap."""
def verify():
    Q={x for x in range(16) if ((x&1)*((x>>1)&1))^(((x>>2)&1)*((x>>3)&1))}
    # Enumerate ALL subsets of F2^4, retaining affine flats dim>=2.
    odd_sections=set();flats=0
    for mask in range(1<<16):
        n=mask.bit_count()
        if n not in (4,8,16):continue
        pts={i for i in range(16) if mask>>i&1}
        a=min(pts);linear={x^a for x in pts}
        if any(x^y not in linear for x in linear for y in linear):continue
        flats+=1
        w=len(pts&Q)
        if w%2:odd_sections.add(w)
    assert flats==171
    assert odd_sections=={1,3}
    for p in (65,67,69,71):
        assert p+6<96
        for a in (1,3):
            e0=64-a;E=p-e0
            assert E<=10
            assert (6-a)+E//2 < 16
            assert (6-a)+E//4 < 8
            assert a+E//2 < 16
            assert 6+E//6 < 8
            assert E<14 and E<16
    assert {64-a for a in (1,3)}=={61,63}
    print('192-relativegap: all171affinequadricsections and finitebounds passed.')
if __name__=='__main__':verify()
