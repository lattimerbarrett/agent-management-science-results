"""Finite certificates for F(d)=d-3 (d>=8). Standard library only."""
from itertools import product
from functools import lru_cache
from fractions import Fraction as F
from math import comb
import time

def independent_count(adj):
    @lru_cache(None)
    def rec(mask):
        if not mask: return 1
        bits=[]; m=mask
        while m:
            b=m & -m; m-=b; bits.append(b.bit_length()-1)
        v=max(bits, key=lambda j:(adj[j]&mask).bit_count())
        if not adj[v]&mask: return 1 << len(bits)
        return rec(mask & ~(1<<v)) + rec(mask & ~((1<<v)|adj[v]))
    ans=rec((1<<len(adj))-1)
    rec.cache_clear()
    return ans

def dedekind6():
    N=64
    adj=[sum(1<<b for b in range(N) if a!=b and (a&b==a or a&b==b)) for a in range(N)]
    return independent_count(adj)

def subset_pairs(d):
    full=(1<<d)-1
    ss=[s for s in range(1,full) if s<(full^s)]
    ss.sort(key=lambda s:(abs(2*s.bit_count()-d),s))
    return ss

def meet_masks(d):
    return [sum(1<<t for t in range(1<<d) if s&t) for s in range(1<<d)]

def lambda7():
    d=7; full=(1<<d)-1; pairs=subset_pairs(d); meet=meet_masks(d)
    def rec(k,allowed):
        while k<len(pairs):
            s=pairs[k]; t=full^s; k+=1
            a=(allowed>>s)&1; b=(allowed>>t)&1
            assert a or b
            if a and b:
                return rec(k,allowed&meet[s])+rec(k,allowed&meet[t])
            allowed &= meet[s if a else t]
        return 1
    return rec(0,(1<<(1<<d))-1)

def three_colour_tree8():
    d=8; full=(1<<d)-1; pairs=subset_pairs(d); meet=meet_masks(d)
    partitions=[]
    for a in range(1,full):
        for b in range(a+1,full):
            if a&b: continue
            c=full^a^b
            if c>b: partitions.append((a,b,c))
    assert len(partitions)==966
    colours=[sum(1<<j for j,pp in enumerate(partitions) if all(s&a for a in pp)) for s in range(1<<d)]
    def rec(k,allowed,cc):
        while k<len(pairs):
            s=pairs[k]; t=full^s; k+=1
            if not ((allowed>>s)&1 and (allowed>>t)&1): continue
            cs=cc&colours[s]; ct=cc&colours[t]
            if cs and ct:
                return rec(k,allowed&meet[s],cs)+rec(k,allowed&meet[t],ct)
        assert cc
        return 1
    return rec(0,(1<<(1<<d))-1,(1<<len(partitions))-1)

def groups(d):
    return sorted([d//3+(j<d%3) for j in range(3)])

def bit_count_construction(d):
    gg=groups(d); r=d//2; total=0
    for xs in product(*(range(1,g) for g in gg)):
        if sum(xs)!=r: continue
        if d%2:
            total += comb(gg[0]-1,xs[0]-1)*comb(gg[1],xs[1])*comb(gg[2],xs[2])
        else:
            total += comb(gg[0],xs[0])*comb(gg[1],xs[1])*comb(gg[2],xs[2])
    return total if d%2 else total//2

def entropy_certificate(m,e,i):
    # Proves H(1/m,1/m,1-2/m)>e/10000,
    # and H(1/m,1-1/m)>i/10000, with log base two.
    assert m**(m*10000)>2**(m*e)*(m-2)**((m-2)*10000)
    assert m**(m*10000)>2**(m*i)*(m-1)**((m-1)*10000)

def odd_log_lower(d,m,e,i):
    gg=groups(d); mask=(1<<d)-1; gm=[]; k=0
    for g in gg:
        gm.append(((1<<g)-1)<<k); k+=g
    sets=[s for s in range(1<<d) if s.bit_count()==d//2 and all(s&g and (mask^s)&g for g in gm)]
    left=[s for s in sets if s&1]; right=set(sets)-set(left)
    edges=[]; isolated=[]
    while right:
        s=right.pop(); t=(mask^1)^s
        if t in right:
            right.remove(t); edges.append((s,t))
        else: isolated.append(s)
    p=F(1,m); expected=F(0)
    for s in left:
        z=F(1)
        for a,b in edges:
            z *= 1-p*(int(not(s&a))+int(not(s&b)))
        for a in isolated:
            if not s&a: z *= 1-p
        expected += z
    bound=F(len(edges)*e+len(isolated)*i,10000)+expected
    return bound,(len(left),len(edges),len(isolated))

def main():
    start=time.time()
    D6=dedekind6(); assert D6==7828354
    print('D(6) =',D6,flush=True)
    lam=lambda7(); assert lam==1422564
    leaves=three_colour_tree8(); assert leaves==4586106
    assert leaves>lam+1
    print('lambda(7), tree(8) =',lam,leaves,flush=True)
    upper={6:D6}
    for n in range(7,12):
        x=upper[n-1]; upper[n]=x*(x+1)//2
    exponents={7:45,8:89,9:177,10:352,11:702}
    for n,a in exponents.items(): assert upper[n]+1<2**a
    entropy_certificate(5,13709,7219)
    entropy_certificate(10,9219,4689)
    for d,m,e,i,target in [(9,5,13709,7219,45),(11,10,9219,4689,177),(13,10,9219,4689,702)]:
        b,shape=odd_log_lower(d,m,e,i)
        assert b>target
        print('odd certificate',d,'(star,edges,isolated)',shape,'log lower >',b.numerator//b.denominator,flush=True)
    for d,target in [(10,89),(12,352)]:
        b=bit_count_construction(d); assert b>target
        print('even certificate',d,b,flush=True)
    assert 3**5<2**8
    for d in range(14,24):
        b=bit_count_construction(d); w=comb(d-2,(d-2)//2)
        assert 5*b>8*w
        print('middle-level certificate',d,b,w,flush=True)
    # Uniform analytic lower bounds for all remaining even/odd d.
    even=F(23,12)*(1-F(6,256))
    odd=F(24,13)*(1-2*F(13,24)**8-F(1,64))
    assert min(even,odd)>F(8,5)
    print('tail bounds > 8/5:',even,odd,flush=True)
    print('All finite certificates passed; seconds',round(time.time()-start,2))

if __name__=='__main__': main()
