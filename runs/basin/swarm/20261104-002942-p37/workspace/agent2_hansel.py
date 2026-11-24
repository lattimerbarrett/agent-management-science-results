from collections import defaultdict
from math import comb

def gk_pairs(n,x):
    stack=[]; pairs=[]
    for i in range(n):
        if (x>>i)&1: stack.append(i)
        elif stack: pairs.append((stack.pop(),i))
    return tuple(sorted(pairs))

def check_gk(n):
    chains=defaultdict(list)
    for x in range(1<<n): chains[gk_pairs(n,x)].append(x)
    assert len(chains)==comb(n,n//2)
    for pairs,chain in chains.items():
        chain.sort(key=int.bit_count)
        assert len(chain)==n-2*len(pairs)+1
        assert all((a&b)==a for a,b in zip(chain,chain[1:]))
        for a,b,c in zip(chain,chain[1:],chain[2:]):
            # The alternative midpoint in the Boolean interval [a,c].
            y=a|((c^a)^(b^a))
            yp=gk_pairs(n,y)
            assert len(yp)>len(pairs), (n,a,b,c,y,pairs,yp)
            assert set(pairs)<=set(yp)
    return len(chains)

if __name__=='__main__':
    for n in range(1,13):
        print(n,check_gk(n))
