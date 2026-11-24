"""Exact finite certificates for all even d>=10."""
from math import comb
from itertools import product
from functools import lru_cache

def dedekind6():
    n=6;N=1<<n
    lo=[sum(1<<j for j in range(N) if j&i==j) for i in range(N)]
    hi=[sum(1<<j for j in range(N) if j&i==i) for i in range(N)]
    @lru_cache(None)
    def rec(mask):
        if not mask:return 1
        bits=[i for i in range(N) if mask>>i&1]
        i=max(bits,key=lambda j:(mask&lo[j]).bit_count()*(mask&hi[j]).bit_count())
        return rec(mask&~lo[i])+rec(mask&~hi[i])
    return rec((1<<N)-1)

def even_good_pairs(d):
    assert d%2==0
    groups=[d//3+(i<d%3) for i in range(3)]
    count=sum(comb(groups[0],a)*comb(groups[1],b)*comb(groups[2],c)
              for a,b,c in product(*(range(1,s) for s in groups)) if a+b+c==d//2)
    assert count%2==0
    return count//2

def check_even_bounds():
    D6=dedekind6()
    assert D6==7828354
    h=lambda x:x*(x+1)//2
    D8_upper=h(h(D6))
    assert D8_upper<2**90
    assert even_good_pairs(10)==90
    assert even_good_pairs(12)==396 and 4*90<396
    for d in (14,16,18):
        L=even_good_pairs(d);W=comb(d-2,(d-2)//2)
        assert 2**L>3**W
    # For d=2m>=20, q=floor(2m/3)>=6. A random m-set
    # is monochromatic on any one specified group with probability <=2/2^q.
    # Thus L/W >= (2-1/m)*(1-6/2^q) >= (19/10)*(29/32)=551/320.
    assert 551*3>320*5
    assert 3**3<2**5 # log_2(3)<5/3
    return D8_upper,[(d,even_good_pairs(d)) for d in range(10,20,2)]

if __name__=='__main__':print(check_even_bounds())
