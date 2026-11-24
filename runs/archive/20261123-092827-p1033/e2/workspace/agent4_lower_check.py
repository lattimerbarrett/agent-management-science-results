import math
def minimum_deficit(i):
    if i == 1: return 0
    d = max(1, math.isqrt(i+1)-1)
    while d*(d+2) < i: d += 1
    assert d*(d+2) >= i
    assert (d-1)*(d+1) < i
    return d
for t in [2,3,10,100,1000,10000,100000]:
    lower = sum(minimum_deficit(i) for i in range(1,t+1))
    assert lower >= (2/3)*(t**1.5-1)-(t-1)
    print(t, lower, lower/t**1.5)
