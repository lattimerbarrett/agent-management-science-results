from itertools import combinations, product
from math import comb
from functools import lru_cache
from fractions import Fraction
"""Exact lambda(k+1) as intersecting upsets on B_k (Shannon restriction).
An intersecting upset U of subsets of [k] determines a self-dual upset on
[k+1]: F restricted to sets not containing k+1 is U, and its other choices
are forced by complement. This is monotone iff U is intersecting.
The recurrence selects an undecided nonempty set A. Include A: force all
supersets, forbid all disjoint sets. Exclude A: forbid all subsets.
Previously forced/forbidden sets cannot conflict since every remaining
available set has no forbidden superset or included disjoint set.
Empty upset is counted, but empty set itself is never available.
"""
from functools import lru_cache

def lambda_next(k):
    vals=list(range(1,1<<k)); n=len(vals)
    up=[]; down=[]; dis=[]
    for a in vals:
        up.append(sum(1<<i for i,b in enumerate(vals) if a&b==a))
        down.append(sum(1<<i for i,b in enumerate(vals) if a&b==b))
        dis.append(sum(1<<i for i,b in enumerate(vals) if not a&b))
    @lru_cache(None)
    def count(state):
        if not state:
            return 1
        ids=[i for i in range(n) if state>>i&1]
        i=max(ids,key=lambda i:min((up[i]&state).bit_count()+(dis[i]&state).bit_count(),(down[i]&state).bit_count()))
        return count(state&~(up[i]|dis[i]))+count(state&~down[i])
    return count((1<<n)-1)


"""Executed exact upper certificate lambda(8)<=237758434088.

For a maximal intersecting family F on [8] with no singleton, let H be its
3-subsets. H is an intersecting triple family. Let f(H) count 4-sets containing
a member of H, and e(H) count pairs whose every triple superset is in H.
For fixed H there are 2**e(H) choices of pairs and 2**(35-f(H)) middle-level
choices. All other set memberships are forced by complementation/upwardness.
Thus lambda(8)=8+sum_H 2**(35-f(H)+e(H)).

The eligible pairs form an intersecting graph, hence a star or a triangle.
For e eligible star edges, H contains at least 21-C(7-e,2) triples; a triangle
requires 16 triples. Consequently for e=0,...,7 the necessary minimum h values
are 0,6,11,15,18,20,21,21. Replacing e(H) by the resulting emax(|H|) gives
a rigorous upper bound. No EKR theorem is needed.
"""
from itertools import combinations

def lambda8_upper():
    T=[sum(1<<x for x in a) for a in combinations(range(8),3)]
    Q=[sum(1<<x for x in a) for a in combinations(range(8),4)]
    intersect=[sum(1<<j for j,b in enumerate(T) if a&b) for a in T]
    shadow=[sum(1<<j for j,b in enumerate(Q) if a&b==a) for a in T]
    minima=[0,6,11,15,18,20,21,21]
    emax=[max(e for e,v in enumerate(minima) if v<=h) for h in range(57)]
    nodes=0
    def visit(candidates,forced,h):
        nonlocal nodes
        nodes+=1
        total=1<<(35-forced.bit_count()+emax[h])
        while candidates:
            bit=candidates&-candidates
            v=bit.bit_length()-1
            candidates-=bit
            total+=visit(candidates&intersect[v],forced|shadow[v],h+1)
        return total
    answer=8+visit((1<<56)-1,0,0)
    assert answer==237758434088 and nodes==32095507
    assert answer+1<618474403306
    return answer,nodes


"""Compute Dedekind numbers D6,D7 exactly in about ten seconds."""
import os,pickle

def certify_d6_d7(cache=None):
    if cache and os.path.exists(cache):
        ideals,up,down=pickle.load(open(cache,'rb'))
    else:
        ideals=[0,1] # ideals of B0
        for n in range(1,6):
            shift=1<<(n-1)
            ideals=[a|(b<<shift) for a in ideals for b in ideals if b&a==b]
        assert len(ideals)==7581
        up=[sum(1<<j for j,b in enumerate(ideals) if a&b==a) for a in ideals]
        down=[sum(1<<j for j,b in enumerate(ideals) if a&b==b) for a in ideals]
        if cache:pickle.dump((ideals,up,down),open(cache,'wb'))
    D6=sum(x.bit_count() for x in up)
    D7=0
    for i,mask in enumerate(up):
        while mask:
            low=mask&-mask;j=low.bit_length()-1;mask-=low
            D7+=(up[i]&down[j]).bit_count()**2
    assert (D6,D7)==(7828354,2414682040998)
    return D6,D7


def suitable(ranks):
    n=len(ranks[0])
    return all(any(R[a]>max(R[b],R[c]) for R in ranks)
               for a in range(n) for b,c in combinations([v for v in range(n) if v!=a],2))

def truncated_cube_product_ideals(a,b):
    """Counts all ideals of (B_a minus endpoints) x (B_b minus endpoints)."""
    from functools import lru_cache
    X=list(product(range(1,(1<<a)-1),range(1,(1<<b)-1)))
    N=len(X);lo=[];hi=[]
    for x,y in X:
        lo.append(sum(1<<i for i,(z,w) in enumerate(X) if z&x==z and w&y==w))
        hi.append(sum(1<<i for i,(z,w) in enumerate(X) if z&x==x and w&y==y))
    @lru_cache(None)
    def rec(mask):
        if not mask:return 1
        bits=[i for i in range(N) if mask>>i&1]
        i=max(bits,key=lambda j:(mask&lo[j]).bit_count()*(mask&hi[j]).bit_count())
        return rec(mask&~lo[i])+rec(mask&~hi[i])
    answer=rec((1<<N)-1)
    return answer,rec.cache_info().currsize

def check_gluing_masks():
    # P=(012,345,67), U=(0,3,6,7); Q chosen with pair in U-complement.
    P=(0b00000111,0b00111000,0b11000000)
    U=0b11001001;Uc=255^U
    # Uc={1,2,4,5}; take Qpair={1,2}, remaining groups each hit Uc.
    Q=(0b00000110,0b00011001,0b11100000)
    assert sum(P)==255 and sum(Q)==255
    assert P[2]&U==P[2] and Q[0]&Uc==Q[0]
    assert all(U&x for x in P) and all(Uc&x for x in Q)
    count,states=truncated_cube_product_ideals(3,3)
    assert count==783558
    assert 2*count>1422564+1
    return count,states

def check_variable_embedding(ranks,colors,t=3,m=2):
    """colors[i][a] is a P coordinate assigned at vertex a in Q coordinate i."""
    n=len(ranks[0]);s=len(ranks)
    assert suitable(ranks)
    assert all(any(ranks[i][a]>ranks[i][b] and colors[i][a]==j for i in range(s))
               for a in range(n) for b in range(n) if a!=b for j in range(t))
    Q=[(a,) for a in range(n)]+list(combinations(range(n),2))
    X=list(product(product(range(m),repeat=t),Q))
    def image(p,A):
        return tuple(max(m*ranks[i][a]+p[colors[i][a]] for a in A) for i in range(s))
    Y=[image(*x) for x in X]
    for u,(p,A) in enumerate(X):
        for v,(q,B) in enumerate(X):
            assert (all(a<=b for a,b in zip(p,q)) and set(A)<=set(B))==all(a<=b for a,b in zip(Y[u],Y[v]))
    return len(X),s

def ordered_scd(n):
    chains=[[0]]
    for j in range(n):
        bit=1<<j
        out=[]
        for C in chains:
            if len(C)>1:
                out.append([x|bit for x in C[:-1]])
            out.append(C+[C[-1]|bit])
        chains=out
    return chains

def check_scd(n):
    chains=ordered_scd(n)
    assert len(chains)==comb(n,n//2)
    flat=[x for C in chains for x in C]
    assert len(flat)==len(set(flat))==1<<n
    earlier=set()
    for C in chains:
        assert C[0].bit_count()+C[-1].bit_count()==n
        assert all(a&b==a and b.bit_count()==a.bit_count()+1 for a,b in zip(C,C[1:]))
        for a,b in zip(C,C[2:]):
            assert any(a&y==a and y&b==y and y not in (a,b) for y in earlier)
        earlier.update(C)
    return True

def odd_star_size(d):
    """Largest star among middle-level sets rainbow on balanced 3 blocks."""
    from itertools import product
    from math import prod
    assert d%2==1 and d>=9
    q,r=divmod(d,3)
    bs=[q+(i<r) for i in range(3)]
    m=d//2
    return max(sum(prod(comb(b-(i==g),k-(i==g))
                        for i,(b,k) in enumerate(zip(bs,ks)))
                   for ks in product(*[range(1,b) for b in bs])
                   if sum(ks)==m) for g in range(3))

def even_good_pairs(d):
    assert d%2==0
    groups=[d//3+(i<d%3) for i in range(3)]
    count=sum(comb(groups[0],a)*comb(groups[1],b)*comb(groups[2],c)
              for a,b,c in product(*(range(1,s) for s in groups)) if a+b+c==d//2)
    assert count%2==0
    return count//2

def star_union9():
    G=[a for a in range(512) if a.bit_count()==4
       and all(0<(a & (7<<(3*j))).bit_count()<3 for j in range(3))]
    assert len(G)==81
    return sum((-1)**(t.bit_count()+1)*2**sum(a&t==t for a in G)
               for t in range(1,512))

def check_toy_gluing():
    P=(7,56,192); Q=(6,25,224); U=201
    def base(parts):
        D=[a for a in range(256) if all(a&g and ((255^a)&g) for g in parts)]
        # Two selfdual upsets, concentrated on opposite singleton states
        # of the 2-element block.
        g=next(g for g in parts if g.bit_count()==2)
        x=g&-g;y=g^x
        F=[{a for a in D if a&x},{a for a in D if a&y}]
        reps=[a for a in D if a<(255^a)]
        ranks=[]
        for i in range(8):
            order=sorted(range(2),key=lambda j:tuple(bool((a if a in F[j] else 255^a)&(1<<i)) for a in reps))
            ranks.append([order.index(j) for j in range(2)])
        return ranks
    A=base(P);B=base(Q);ranks=[];colors=[]
    for i in range(8):
        ranks.append([x+(2 if U>>i&1 else 0) for x in A[i]]+
                     [x+(0 if U>>i&1 else 2) for x in B[i]])
        colors.append([next(j for j,g in enumerate(P) if g>>i&1)]*2+
                      [next(j for j,g in enumerate(Q) if g>>i&1)]*2)
    assert check_variable_embedding(ranks,colors)==(80,8)

def main():
    assert lambda_next(6)==1422564
    assert check_gluing_masks()[0]==783558
    u8,nodes=lambda8_upper()
    z=star_union9()
    assert z==618474403306 and z>u8+1
    D6,D7=certify_d6_d7()
    h=lambda x:x*(x+1)//2
    assert h(h(D6))<2**90 and even_good_pairs(10)==90
    assert even_good_pairs(12)==396 and 360<396
    assert h(h(D7))<2**164 and odd_star_size(11)==164
    assert D7**16<2**690 and odd_star_size(13)==690
    table=[]
    for d in range(14,20):
        L=even_good_pairs(d) if d%2==0 else odd_star_size(d)
        W=comb(d-2,(d-2)//2)
        assert 2**L>3**W
        table.append((d,L))
    assert Fraction(551,320)>Fraction(5,3)
    assert Fraction(20,11)*(1-Fraction(1,64)-4*Fraction(11,20)**7)>Fraction(5,3)
    assert 3**3<2**5
    for n in range(13):assert check_scd(n)
    check_toy_gluing()
    print('lambda7 =',1422564)
    print('lambda8 upper =',u8,'over',nodes,'triple families')
    print('D6,D7 =',D6,D7)
    print('d8 base =',783558,'; d9 stars =',z)
    print('middle/star exponents d14..19:',table)
    print('All certificates passed, including an actual 80-point mixed embedding.')

if __name__=='__main__':main()
