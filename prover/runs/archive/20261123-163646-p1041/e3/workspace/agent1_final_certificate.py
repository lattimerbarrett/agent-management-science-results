"""Self-contained exact certificate for the spectrum proof.
Run with Python3 (standard library only). It constructs and checks all low
and middle seed words using full truth tables and Boolean Mobius transforms.
It also exhaustively checks the finite fiber, Pluecker, and intersection
arithmetic used in the exclusion proof. KT strict normal forms and KTA
numerical low-weight theorems are external mathematical theorems, NOT
claims that this script enumerates the enormous Reed--Muller code.
"""
from itertools import combinations, product
from fractions import Fraction
from math import comb

LOW = {128: [127], 192: [127, 415], 224: [127, 911], 240: [127, 1927], 248: [127, 3971], 252: [127, 8065], 254: [127, 16256], 256: [127, 829, 4467], 272: [127, 3193, 4726], 288: [127, 5175, 7408], 296: [127, 4551, 10302], 304: [127, 12068, 11590], 308: [127, 2669, 13618], 312: [127, 9003, 8668], 314: [127, 7876, 16256], 316: [127, 4348, 12161], 320: [127, 3607, 13894], 324: [127, 15748, 13351], 328: [127, 2734, 9495], 332: [127, 9013, 13642]}
CENTRAL = """1366 2275 2366 1ee
3361 c9e 4f3 c1f
1c8d 2b64 11d9 ccd
136a 2d19 12e6 12d6
145d 12d3 70f 1517
2c3a 11e6 2e19 283b 262b
1593 22e5 26a5 165c
149b 2b64 1c8b 22da
1a74 2c47 319c 31cc
3b9 2936 3646 b39 9b9
10cf 236a 2365 31aa
f62 309b acd 349a f64
116d 3a32 3c70 1559
*
3c13 2b23 3ae b0f
acd 25b2 3532 2c1e
5b5 11cd 14b3 20eb
1719 32a6 8e7 2af 28e6
1c65 22d6 26cc 1cb1
1c8d acd 3532 360d
12f4 3256 3133 2695
6e3 1939 2627 19d8
119e db1 192d 6b3
1539 5e9 34c9 b36 2936
354c 252b 130f d65
3a7 1197 3c58 a67
26c6 c4f 292b 29b1
18ab 14ba 3a31 2b45
6ce 8b7 277 219b
14f8 b0f 2af0 2b07 ae9
2cb8 1672 292d 23b8
21d6 2c2b 151b 13d4
290f 29b2 c5d 1d70
53d 1d31 29d2 22ce
258b 13e1 2d07 af2
3929 3938 2347 6d6 29c3
7b4 be8 26ca 322e
357 322e 25f0 1a0f
769 3247 e5a 350d
26c9 1936 1758 350e
2e07 198d 381b 29e1
774 3c2a f34 3d5 2b68
3325 3293 2f6 15ca
2b0b 216d 3217 14f4
6f8 1aca 283b 9bc
2395 b2d 34d2 1a4e
de2 113d 2ae8 3147
25e4 11d3 30dc 1a1b 2764
3196 25e1 3a15 1e4c
28dc 26e4 3487 191b
254b 29d2 ab5 16e2
22c7 1d38 13a5 f38 2c4b
18b9 1e58 b1e 22e5
123e 1c33 3495 b6a 2437
3295 215e 2e0b f64
23d2 32a5 2a9a 3361 d5a
245e 7b4 3a07 12e9
ad3 32c6 381d 7e2
21ce 392c 271c 1cd2
6ba 38d1 1b46 e1e 72e
342e 3f1 330d 38cc
3076 eb4 1ae4 251b 16b8
2437 9cb 3dc 15e8
2956 4bd 3970 16a9 aab"""

def rank(vs):
    piv={}
    for v in vs:
        while v:
            j=v.bit_length()-1
            if j not in piv:piv[j]=v;break
            v^=piv[j]
    return len(piv)

def span(B):
    S=[0]
    for v in B:
        assert v not in S
        S += [x^v for x in S]
    return S

def coordinate_basis(mask):
    return [1<<i for i in range(14) if mask>>i&1]

def anf_degree(truth):
    a=[(truth>>i)&1 for i in range(16384)]
    for k in range(14):
        for i in range(16384):
            if i>>k&1:a[i]^=a[i^(1<<k)]
    return max((i.bit_count() for i,b in enumerate(a) if b),default=-1)

def word(bases):
    truth=0;occupied=set()
    for B in bases:
        assert len(B)==7 and rank(B)==7
        P=span(B)
        truth ^= sum(1<<x for x in P)
        occupied.update(x>>7 for x in P)
    assert anf_degree(truth)<=7
    return truth,occupied

def verify_inclusions():
    expected={128,192,224,240,248,252,254,256,272,288,296,304,
              308,312,314,316,318,320,324,328,332}
    for w,masks in LOW.items():
        T,_=word([coordinate_basis(a) for a in masks])
        assert T.bit_count()==w
    # U3=<e6,e7+e8,e10,...,e14>; all bases contain seven vectors.
    B318=[coordinate_basis(127),coordinate_basis(415),
          [32,192,512,1024,2048,4096,8192]]
    assert word(B318)[0].bit_count()==318
    assert set(LOW)|{318}==expected
    attained=set();maxocc=0
    for i,row in enumerate(CENTRAL.splitlines()):
        w=336+2*i
        if row=='*':
            bases=[[2,520,16,32,1024,2048,8192],
                   [2,4,32,64,128,256,4096],
                   [1,8,16,512,1024,2048,8192],
                   [1,2,8,16,32,2048,8192],
                   [1,2,8,32,512,1024,8192]]
        else:bases=[coordinate_basis(int(s,16)) for s in row.split()]
        truth,occupied=word(bases)
        assert truth.bit_count()==w and len(occupied)<=64
        maxocc=max(maxocc,len(occupied))
        empty=sorted(set(range(128))-occupied)
        for j in range(65):
            assert truth.bit_count()==w+128*j
            attained.add(truth.bit_count())
            if j<64:truth^=((1<<128)-1)<<(128*empty[j])
    assert attained==set(range(336,8656,2))
    attained|={16384-w for w in attained}
    assert set(range(336,16050,2))<=attained
    # The disjoint-sum induction's interval overlaps, valid for everyN>=16384.
    assert 672<=16384-334 and 16384+336<=2*16384-670
    print('PASS: 21 low and64 middle seed truth tables/ANFs; max blocks',maxocc)
    print('PASS: all m>=14 middle weights by explicit empty-block shifts,')
    print('complementation, and the proved disjoint-sum induction.')

def verify_exclusion_arithmetic():
    for m in (14,15):
        K=(1<<(m-10))-1;N=1<<m
        for w in (322,326,330,334):
            avg=Fraction(w)-2*comb(w,2)*Fraction(K,N-1)+4*comb(w,3)*Fraction(K*(K-1),(N-1)*(N-2))
            assert avg<256
            print('cubic projection',m,w,avg,float(avg))
    # Fiber Bonferroni for every occupancy in largest starting kernel.
    for t in range(33):assert t%2<=t-2*comb(t,2)+4*comb(t,3)
    for k in range(2,6):
        assert Fraction((1<<k)*167,(1<<(k+1))-1)<96
        # Every k-vector in dimension k+1 is decomposable: enumerate every
        # hyperplane via its covector and compute its Pluecker coordinates.
        n=k+1;seen=set()
        for ell in range(1,1<<n):
            rows=[v for v in range(1,1<<n) if (v&ell).bit_count()%2==0]
            B=[]
            for v in rows:
                if rank(B+[v])>len(B):B.append(v)
            assert len(B)==k
            pl=0
            for omitted in range(n):
                cols=[j for j in range(n) if j!=omitted]
                mat=[sum(((v>>j)&1)<<a for a,j in enumerate(cols)) for v in B]
                if rank(mat)==k:pl|=1<<omitted
            assert pl==ell
            seen.add(pl)
        assert len(seen)==(1<<n)-1
        # All k-fibers exactly obey the odd/even projection formula and
        # the nonzero-XOR half-characters identity (largest k5 has2^32
        # subsets, so use ALL subsets for k<=4 and all moment vectors k5).
        for v in range(1<<k):
            assert sum((v&ell).bit_count()%2 for ell in range(1,1<<k))==((1<<(k-1)) if v else 0)
        if k<=4:
            for mask in range(1<<(1<<k)):
                F=[x for x in range(1<<k) if mask>>x&1]
                v=0
                for x in F:v^=x
                for ell in range(1,1<<k):
                    c=sum((x&ell).bit_count()%2 for x in F)
                    wt=(c%2)+((len(F)-c)%2)
                    assert wt==(1 if len(F)%2 else 2*((v&ell).bit_count()%2))
        if k>=3:
            assert 128+Fraction(1<<(k-1),(1<<k)-1)*206<256
    # Classical numeric coefficient gaps suffice for the 2D anisotropic case.
    allowed=(64,96,112,120,124,126,128,136,144,148,152,154,156,158)
    triples=set()
    for ww in product(allowed,repeat=3):
        if sum(ww)<=334 and sum((w//2)%2 for w in ww)==1 and 64 not in ww:
            triples.add(tuple(sorted(ww)))
    assert triples=={(96,96,126),(96,112,126)}
    assert 3*126>334
    # Exterior ambient reduction: a common nonzero5-form essentialspace
    # forces the support sum dimension<=12, forbidding an external vector.
    assert 8+9-5==12<13
    assert 8-3<6
    # LemmaA convolution coset lowerbound and LemmaD punctured bounds.
    assert (1<<(14-7))-1==127
    assert 128+2*127>334
    assert 334-256<96 and 334-256-64<32
    assert 12<13<=14
    # ALL numerical three-flat intersection possibilities for weight256.
    sizes=(0,1,2,4,8,16,32)
    for p,q,r,t in product(sizes,repeat=4):
        if t>min(p,q,r) or p+q+r-2*t!=64:continue
        if t>=2:continue # actual common period
        if t==1:
            assert sorted((p,q,r))==[2,32,32]
            assert 5+5-7>0 # contradicts singleton commonintersection
        else:
            assert sorted((p,q,r)) in ([0,32,32],[16,16,32])
            logs=sorted((a.bit_length()-1 for a in (p,q,r) if a),reverse=True)
            assert logs[0]+logs[1]-7>=2
    for w in (96,112,120):assert w-64>=32
    assert 7+8-5+1==11
    # Final three first derivatives: average<272 and no allowed256..272interior.
    assert 128+Fraction(2,3)*206<272
    print('PASS: all bootstrap arithmetic, ALL hyperplanes/Pluecker vectors,')
    print('ALL fibers throughdim4, ambient exterior bound, triple256 cases, and final gaps.')

def mul(a,b,N):
 out=0
 for x in range(N):
  if a>>x&1:
   for y in range(N):
    if b>>y&1:out^=1<<(x^y)
 return out

def Q(a,N):
 S=[x for x in range(N) if a>>x&1]
 assert len(S)%2==0
 p=(len(S)//2)&1
 for x,y in combinations(S,2):p^=1<<(x^y)
 return p

def ymon(T,N):
 return sum(1<<x for x in range(N) if x&T==x)

def verify_group_algebra():
 for n in range(1,5):
  N=1<<n
  basis=[ymon(T,N) for T in range(1,N)]
  # Q polarizes to multiplication on augmentation ideal.
  for i,a in enumerate(basis):
   for b in basis[i+1:]:
    assert Q(a^b,N)^Q(a,N)^Q(b,N)==mul(a,b,N)
  # All monomials of degree >=2 have Q=0.
  for T in range(1,N):
   if T.bit_count()>=2:assert Q(ymon(T,N),N)==0
  # Exhaustively test Q(I^c) subset I^(2c) for c>=2.
  for c in range(2,n+1):
   Ts=[T for T in range(N) if T.bit_count()>=c]
   for mask in range(1<<len(Ts)):
    a=0;expected=0
    for i,T in enumerate(Ts):
     if mask>>i&1:
      a^=ymon(T,N)
      for j,U in enumerate(Ts[:i]):
       if mask>>j&1 and not T&U:expected^=ymon(T|U,N)
    assert Q(a,N)==expected
 print('Group-algebra identity verified exhaustively for n<=4')



def verify_relative_odd_gap_arithmetic():
    # Numeric inequalities in the full fiber-moment proof for degree7/F13
    # punctured outside a7-flat. No assertion of brute-force enumeration.
    for e in range(63,105,2):
        E=e-63
        assert E<=40
        assert 2*(24-1)>E # nonminimum second moment or distinct T's
        assert 4*(16-1)>E # rank>=4 alternating second-moment array
        assert 6*(8-1)>E and 14*(4-1)>E
        for e0 in (93,95):
            if e0<=e:
                R=e-e0
                assert R<=10 and R//2<8-1
                assert R//10<4-1
                assert 32-2*3>R
        assert E//30<=1
        assert E+2<48 # null5 word has weight32 or>=48
    assert {63,63+30,63+32}.isdisjoint({97,99,101,103})
    print('PASS: all numeric branches of the relative odd-gap moment proof')

if __name__=='__main__':
    verify_inclusions()
    verify_exclusion_arithmetic()
    verify_group_algebra()
    verify_relative_odd_gap_arithmetic()
    print('ALL EXACT CERTIFICATE CHECKS PASSED')
