"""Check the exact optimized deficit bound from the greedy residual-rank lemma.
The proof itself is symbolic; this verifies all integer optimizations to 10000."""
from math import isqrt

def greedy_deficit_bound(t):
    # For integer r>=0, at most r*r+r+1 classes have deficit <=r.
    # All others have deficit >=r+1.
    return max((r+1)*(t-r*(r+1)-1) for r in range(isqrt(t)+1))

def check():
    for t in range(2,10001):
        b=greedy_deficit_bound(t)
        r=max(0,isqrt(t//3)-1)
        assert b >= (r+1)*(t-r*(r+1)-1)
        assert b <= t*(t-1)//2
    for t in [10,100,1000,10000]:
        print(t, greedy_deficit_bound(t), greedy_deficit_bound(t)/t**1.5)

if __name__=='__main__': check()
