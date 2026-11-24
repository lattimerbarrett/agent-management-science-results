"""Exact truth-table/ANF verification for all exceptional low weights.
Run from repository root: python workspace/agent3_verify_low.py
No packages required. Bit i in a mask denotes coordinate x_(i+1).
"""
from itertools import combinations
WITNESSES = {
128: [0x7f],
192: [0x7f,0x19f],
224: [0x7f,0x38f],
240: [0x7f,0x787],
248: [0x7f,0xf83],
252: [0x7f,0x1f81],
254: [0x7f,0x3f80],
256: [0x7f,0x33d,0x1173],
272: [0x7f,0xc79,0x1276],
288: [0x7f,0x1437,0x1cf0],
296: [0x7f,0x11c7,0x283e],
304: [0x7f,0x2f24,0x2d46],
308: [0x7f,0xa6d,0x3532],
312: [0x7f,0x232b,0x21dc],
314: [0x7f,0x1ec4,0x3f80],
316: [0x7f,0x10fc,0x2f81],
320: [0x7f,0xe17,0x3646],
324: [0x7f,0x3d84,0x3427],
328: [0x7f,0xaae,0x2517],
332: [0x7f,0x2335,0x354a],
}
FULL=(1<<14)-1

def anf_degree(v):
    a=list(v)
    for i in range(14):
        for mask in range(1<<14):
            if mask & (1<<i): a[mask] ^= a[mask^(1<<i)]
    return max((i.bit_count() for i,c in enumerate(a) if c),default=-1)

def verify():
    for w, masks in WITNESSES.items():
        assert all(a.bit_count()==7 and a&FULL==a for a in masks)
        v=[sum((x & (FULL^a))==0 for a in masks)%2 for x in range(1<<14)]
        assert sum(v)==w, (w,sum(v))
        assert anf_degree(v)<=7
        # Independent intersection inclusion-exclusion check.
        w2=0
        for k in range(1,len(masks)+1):
            for group in combinations(masks,k):
                intersection=FULL
                for a in group: intersection &= a
                w2+=(-2)**(k-1)*(1<<intersection.bit_count())
        assert w2==w
    # For 318 use the indicator polynomials of three 7-dimensional spaces:
    # U1=<e1,...,e7>; U2=<e1,...,e5,e8,e9>;
    # U3=<e6,e7+e8,e10,...,e14>.
    # U3 equations: x1=...=x5=x9=x7+x8=0.
    v=[]
    for x in range(1<<14):
        b1=(x & (FULL ^ 0x7f))==0
        b2=(x & (FULL ^ 0x19f))==0
        b3=(x&0x11f)==0 and ((x>>6)&1)==((x>>7)&1)
        v.append(int(b1)^int(b2)^int(b3))
    assert sum(v)==318
    assert anf_degree(v)<=7
    target={128,192,224,240,248,252,254,256,272,288,296,304,308,312,314,316,318,320,324,328,332}
    assert set(WITNESSES)|{318}==target
    print('Verified all 21 positive exceptional weights by full 16384-point truth tables and ANF transforms.')
    print('All witnesses have degree <=7; embedding by product(1+x_i), i=15,...,m, proves all m>=14.')
if __name__=='__main__':verify()
