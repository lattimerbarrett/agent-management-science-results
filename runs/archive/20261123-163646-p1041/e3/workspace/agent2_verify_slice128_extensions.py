"""Exact finite checks supplementing the rank4/rank6 128-slice proofs."""
def verify():
    # Every hyperplane section of the second-weight12 word has <=8 points.
    S=[x for x in range(32) if ((x&1)*((x>>1)&1))^(((x>>2)&1)*((x>>3)&1))]
    assert len(S)==12
    assert max(sum(((a&x).bit_count()%2)==c for x in S) for a in range(1,32) for c in (0,1))==8
    for E in (66,70,74,78):
        for a in range(14):
            for b in range(14):
                if a+b==12 and 6*a+8*b==E:
                    assert (a,b) in {(11,1),(9,3)}
    # Rank6 quadratic plus radical linear term.
    def q6(x):
        return ((x&1)*((x>>1)&1))^(((x>>2)&1)*((x>>3)&1))^(((x>>4)&1)*((x>>5)&1))
    q7=[q6(x)^((x>>6)&1) for x in range(128)]
    assert [v for v in range(1,128) if all(q7[x]^q7[x^v] for x in range(128))]==[64]
    weights=set();outside=set()
    for a in range(128):
        for c in (0,1):
            h=[q6(x)^((a&x).bit_count()%2)^c for x in range(128)]
            weights.add(sum(h))
            outside.add(sum(h[x] for x in range(128) if x&63))
    assert weights=={56,64,72}
    assert min(outside)==54
    print('All exact finite checks for rank4/rank6 128-slice extensions passed.')
if __name__=='__main__':verify()
