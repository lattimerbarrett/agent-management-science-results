from fractions import Fraction

def verify():
    N=32768
    K={64,96,112,120,124,126,128,136,144,148,152,154,156,158}
    triples=[]
    for w in (322,326,330,334):
        assert Fraction(N*w-w*w,N-1)>(w-316)**2
        for a in sorted(K):
            if 128<=a<=156:
                for b in (64,96):
                    c=w-a-b
                    if c>=b and c in K:triples.append((w,a,b,c))
    assert triples==[(326,136,64,126),(330,154,64,112),(334,144,64,126)]
    powers=[0,1,2,4,8,16];exc=set()
    for p in powers:
        for q in powers:
            for r in powers:
                for t in powers:
                    if t>min(p,q,r) or p+q+r-2*t<18:continue
                    logs=[x.bit_length()-1 if x else None for x in (p,q,r)]
                    big=any(logs[i] is not None and logs[j] is not None and logs[i]+logs[j]>=5 for i in range(3) for j in range(i))
                    if not big:exc.add((tuple(sorted((p,q,r))),t))
    assert exc=={((1,1,16),0)}
    print('ConstantQ15 conditional proof: Parseval,sumset,triple-span arithmetic verified.')
    print('WARNING: coarse KTA input remains a separate unproved assumption in our work.')
if __name__=='__main__':verify()
