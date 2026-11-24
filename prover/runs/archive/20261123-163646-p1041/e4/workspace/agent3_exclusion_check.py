"""Arithmetic audit of the application of the classical KTA theorem.
This does NOT re-prove the KTA theorem; the theorem is the mathematical input.
For corank 7 its necessary positive weights below 5*128/2 are KTA_LOW.
"""
KTA_LOW = frozenset((128,192,224,240,248,252,254,256,272,288,296,304,308,310,312,314,316,318))
LOW_INTERVALS = ((0,0),(128,128),(192,192),(224,224),(240,240),(248,248),(252,256),(272,272),(288,288),(296,296),(304,304))

def check(m):
    assert m >= 14
    n = 1 << m
    assert all(w % 2 == 0 and 0 < w < 320 for w in KTA_LOW)
    low = {w for lo,hi in LOW_INTERVALS for w in range(lo,hi+1,2)}
    assert low == {0} | {w for w in KTA_LOW if w < 308}
    intervals = list(LOW_INTERVALS) + [(308,n-308)] + [(n-hi,n-lo) for lo,hi in reversed(LOW_INTERVALS)]
    assert len(intervals) == 23
    assert all(lo <= hi and lo%2 == hi%2 == 0 for lo,hi in intervals)
    assert all(intervals[i][1]+2 < intervals[i+1][0] for i in range(len(intervals)-1))
    # Every omitted even number has distance <308 from an end.
    for (_,hi),(lo,_) in zip(intervals,intervals[1:]):
        assert hi+2 <= lo-2
        if hi < 308:
            assert lo <= 308
            assert not any(w in KTA_LOW for w in range(hi+2,lo,2))
        else:
            assert n-lo < 308
            assert not any(n-w in KTA_LOW for w in range(hi+2,lo,2))
    return intervals

if __name__ == '__main__':
    for m in range(14,101): check(m)
    print('PASS: theorem-specialization arithmetic, intervals, maximality, reflected exclusions for m=14,...,100')
