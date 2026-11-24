from functools import lru_cache
from itertools import combinations, product
from math import comb
from fractions import Fraction
import gc, random, time, json

# Independent sets in the comparability graph count antichains.
# Adding disjointness conflicts counts intersecting antichains.
def count_families(n, intersecting):
    vals=list(range(1 if intersecting else 0,1<<n))
    adj=[sum(1<<i for i,b in enumerate(vals)
             if a&b in (a,b) or (intersecting and a&b==0)) for a in vals]
    @lru_cache(8000000)
    def rec(mask):
        if not mask:return 1
        m=mask;isolated=0;best=-1;vertex=None
        while m:
            bit=m&-m;m-=bit;i=bit.bit_length()-1
            deg=(adj[i]&mask).bit_count()
            if deg==1:isolated|=bit
            if deg>best:best=deg;vertex=i
        if isolated:return (1<<isolated.bit_count())*rec(mask&~isolated)
        if best<=6:
            component=0;boundary=mask&-mask
            while boundary:
                component|=boundary;neighbors=0;m=boundary
                while m:
                    bit=m&-m;m-=bit;neighbors|=adj[bit.bit_length()-1]
                boundary=neighbors&mask&~component
            if component!=mask:return rec(component)*rec(mask^component)
        return rec(mask&~(1<<vertex))+rec(mask&~adj[vertex])
    answer=rec((1<<len(vals))-1)
    rec.cache_clear();gc.collect()
    return answer

def groups_of(sizes):
    ans=[];offset=0
    for s in sizes:
        ans.append(((1<<s)-1)<<offset);offset+=s
    return ans

def split(A,groups):return all(A&G and G&~A for G in groups)

def mvalue(d):
    sizes=sorted([d//3+(j<d%3) for j in range(3)])
    groups=groups_of(sizes)
    m=0
    # Inclusion-exclusion for k-subsets containing point 0 and splitting all groups.
    for choices in product((-1,0,1), repeat=3):
        inc=1;exc=0;sign=1
        for G,v in zip(groups,choices):
            if v==0:inc|=G;sign=-sign
            elif v==1:exc|=G;sign=-sign
        if inc&exc:continue
        k=d//2-inc.bit_count();rem=d-(inc|exc).bit_count()
        if 0<=k<=rem:m+=sign*comb(rem,k)
    return m

def eight_certificate():
    r=8;full=(1<<r)-1;parts=[]
    for pair in combinations(range(r),2):
        A=sum(1<<i for i in pair)
        rem=[i for i in range(r) if not A>>i&1]
        for triple in combinations(rem,3):
            B=sum(1<<i for i in triple);C=full^A^B
            if B<C:parts.append((A,B,C))
    subsets=[sum(1<<i for i in c) for c in combinations(range(r),4) if 0 in c]
    subsets=[209,101,39,169,53,89,165,77,177,83,147,141,27,23,51,113,225,105,149,163,57,15,153,71,43,99,85,201,195,197,29,75,45,135,139]
    assert len(set(subsets))==35 and all(A&1 and A.bit_count()==4 for A in subsets)
    def cover(A):return sum(1<<i for i,p in enumerate(parts) if all(A&G for G in p))
    queries=[(cover(A),cover(full^A)) for A in subsets]
    @lru_cache(None)
    def solve(S,j):
        assert S
        if j==len(queries):return 1
        a,b=queries[j];A=S&a;B=S&b
        if not A or not B:return solve(S,j+1)
        return solve(A,j+1)+solve(B,j+1)
    ans=solve((1<<len(parts))-1,0)
    print('d=8 query order:',subsets,flush=True)
    assert len(parts)==280 and ans==1932672
    return ans

def nine_certificate():
    G=groups_of([3,3,3]);sets=[sum(1<<i for i in c) for c in combinations(range(9),4)]
    P=[[A for A in sets if split(A,G) and (A&G[j]).bit_count()==2] for j in range(3)]
    assert list(map(len,P))==[27]*3
    verts=P[0]+P[1]
    adj=[{j for j,B in enumerate(verts) if not A&B}for A in verts]
    remaining=set(range(54));components=[]
    while remaining:
        C={next(iter(remaining))}
        while True:
            D=C|set().union(*(adj[i] for i in C))
            if C==D:break
            C=D
        components.append(C);remaining-=C
    assert len(components)==9
    assert all(len(C)==6 and all(len(adj[i])==2 for i in C)for C in components)
    z=P[2][0];neighbors={i for i,A in enumerate(verts)if not A&z}
    assert len(neighbors)==4
    assert sorted(len(C&neighbors)for C in components)==[0]*5+[1]*4
    # Count independent sets of a 6-cycle and a 5-path directly.
    cycle_edges={(i,(i+1)%6)for i in range(6)}
    def independent_count(n,edges):
        return sum(all(not(mask>>a&1 and mask>>b&1)for a,b in edges)for mask in range(1<<n))
    assert independent_count(6,cycle_edges)==18
    assert independent_count(5,{(i,i+1)for i in range(4)})==13
    return 18**9+13**4*18**5

def eleven_certificate():
    G=groups_of([3,4,4]);sets=[sum(1<<i for i in c)for c in combinations(range(11),5)]
    valid=[A for A in sets if split(A,G)]
    A=[s for s in valid if s&1];B=[s for s in valid if not s&1 and s&2]
    assert len(A)==164 and len(B)==116
    assert max(sum(not a&b for a in A)for b in B)<=6
    return Fraction(2**164*65**116,64**116)

# Rigorous interval arithmetic is used only to certify upper bounds on roots.
def finite_container_checks():
    from sage.all import RealIntervalField, QQ
    RF=RealIntervalField(100);bits=16;den=1<<bits
    @lru_cache(None)
    def root_log_upper(D16):
        if D16==0:return den
        D=RF(D16)/16
        lo=0;hi=den
        while hi-lo>1:
            mid=(lo+hi)//2;q=RF(mid)/den
            value=(RF(2)**(q*D))*(RF(2)**q-1)
            if value.lower()>=1:hi=mid
            else:lo=mid
        q=RF(hi)/den
        assert ((RF(2)**(q*D))*(RF(2)**q-1)).lower()>=1
        return hi
    B=1024
    margins=[]
    for n in range(18,100):
        w=comb(n,n//2);N=(1<<n)-2*n-2
        alpha=n//2+1;beta=comb((n+1)//2+1,2)
        bins=(B*(N-w)+w-1)//w
        total=0
        for j in range(bins):
            # x=(B+j)/B; degree lower bounds rounded down to multiples of 1/16.
            a=16*alpha*j//B
            b=(32*beta*(j-B))//(B+j)
            c=16*beta*(j-2*B)//B
            total+=root_log_upper(max(a,b,c,0))
        upper=Fraction(2*n+2+w)+Fraction(w*total,B*den)
        m=mvalue(n+2)
        assert m>upper,(n,m,upper)
        margins.append((n,float(Fraction(m, w)-upper/w)))
    # Certified constants for the uniform n>=100 estimate.
    assert (RF(2).log()>RF(69)/100)
    assert RF(100).log()<RF(461)/100
    assert RF(300).log()<RF(571)/100
    bound=Fraction(2,69)*(Fraction(571,100)+Fraction(571,100)**2/2)
    bound+=Fraction(8,6900)*(3*Fraction(461,100)+Fraction(9,2)*Fraction(461,100)**2)
    assert bound<Fraction(77,100)
    assert Fraction(2*101**2,2**100)<Fraction(1,1000)
    assert (2-Fraction(4,103))*(1-5*Fraction(3,5)**33)>Fraction(19,10)
    print('Container checks n=18,...,99 passed; minimum margin:', min(margins,key=lambda x:x[1]),flush=True)
    return margins

if __name__=='__main__':
    t=time.time()
    l7=count_families(6,True);print('lambda(7) =',l7,flush=True)
    l8=count_families(7,True);print('lambda(8) =',l8,flush=True)
    D7=count_families(7,False);print('Dedekind(7) =',D7,flush=True)
    assert (l7,l8,D7)==(1422564,229809982112,2414682040998)
    C8=eight_certificate();C9=nine_certificate();C11=eleven_certificate()
    assert C8>l7+1 and C9>l8+1
    for n in range(8,18):
        upper=D7**(1<<(n-7))
        if n==9:assert C11>upper+1
        else:assert 2**mvalue(n+2)>upper+1
    print('Small-d constructions passed.',flush=True)
    margins=finite_container_checks()
    json.dump({'lambda7':l7,'lambda8':l8,'D7':D7,'C8':C8,'C9':C9,'margins':margins},open('verified_results.json','w'))
    print('All computational certificates passed in',time.time()-t,'seconds',flush=True)
