import math

def hansel_chains(n):
    chains=[[0]]
    for bit in range(n):
        b=1<<bit
        new=[]
        for C in chains:
            if len(C)>1:new.append([x|b for x in C[:-1]])
            new.append(C+[C[-1]|b])
        chains=new
    return chains

def check(n):
    chains=hansel_chains(n)
    assert len(chains)==math.comb(n,n//2)
    assert sorted(x for C in chains for x in C)==list(range(1<<n))
    earlier=set()
    for C in chains:
        for x,y,z in zip(C,C[1:],C[2:]):
            diff=z^x
            bits=[1<<i for i in range(n) if diff>>i&1]
            assert len(bits)==2
            other=x|(diff^(y^x))
            assert other in earlier
        earlier.update(C)
    return len(chains)
