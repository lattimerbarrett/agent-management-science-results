import math, itertools, collections, json, time
from fractions import Fraction
from pathlib import Path

def det(a):
    a=[row[:] for row in a]; n=len(a)
    if n==0:return 1
    sign=1; old=1
    for k in range(n-1):
        if not a[k][k]:
            j=next((j for j in range(k+1,n) if a[j][k]),None)
            if j is None:return 0
            a[k],a[j]=a[j],a[k];sign=-sign
        pivot=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                val=a[i][j]*pivot-a[i][k]*a[k][j]
                assert val%old==0
                a[i][j]=val//old
            a[i][k]=0
        old=pivot
    return sign*a[-1][-1]

def lcm_to(h):
    d=1
    for j in range(1,h+1):d=math.lcm(d,j)
    return d

def floor_log_int(s,b):
    # Exact, not floating point.
    lo=0;hi=s.bit_length()
    while lo+1<hi:
        k=(lo+hi)//2
        if pow(b,k)<=s:lo=k
        else:hi=k
    return lo

def check(n,literal=False):
    import sympy as sp
    edges=list(itertools.combinations(range(n),2));N=len(edges)
    H=n**(n-2);D=lcm_to(H);B=2**(N+1)
    terms=collections.Counter(); commute_counts=collections.Counter()
    regular_connected=0; all_tree_bound=True
    for mask in range(2**N):
        deg=[0]*n; adj=[[0]*n for _ in range(n)]
        for k,(i,j) in enumerate(edges):
            bit=(mask//2**k)-2*(mask//2**(k+1))
            assert bit in (0,1)
            if bit:adj[i][j]=adj[j][i]=1;deg[i]+=1;deg[j]+=1
        r=math.prod(1//(1+(deg[i]-deg[0])**2) for i in range(1,n))
        assert r==int(len(set(deg))==1)
        # Every summand with r=0 is zero. No determinant is needed for it.
        if not r:continue
        Q=[[-adj[i][j] if i!=j else deg[i] for j in range(n-1)] for i in range(n-1)]
        K=det(Q);assert 0<=K<=H
        q=1-1//(K+1)
        seen={0};front=[0]
        for i in front:
            for j in range(n):
                if adj[i][j] and j not in seen:seen.add(j);front.append(j)
        assert q==int(len(seen)==n)
        if not q:continue
        regular_connected+=1
        Qb=[row[:] for row in Q]
        Qb[0][0]+=1;Qb[1][1]+=1;Qb[0][1]-=1;Qb[1][0]-=1
        F=det(Qb)-K;assert F>0 and D%K==0
        e=n*deg[0]*(D//K)*F
        terms[e]+=1
        c=Fraction(n*deg[0]*F,K)
        assert e==D*c
        commute_counts[str(c)]+=1
        # Independent hitting-time equations at targets 0 and 1.
        ht=[]
        for target,start in [(0,1),(1,0)]:
            vs=[i for i in range(n) if i!=target]
            M=sp.Matrix([[deg[i] if i==j else -adj[i][j] for j in vs] for i in vs])
            rhs=sp.Matrix([deg[i] for i in vs])
            sol=M.inv()*rhs
            ht.append(sol[vs.index(start)])
        assert Fraction(ht[0]+ht[1])==c
    assert 0<sum(terms.values())<=2**N<B
    # Sparse base-B integer: exact representation of S, avoiding enormous zero runs.
    leading=max(terms)
    assert 1<=terms[leading]<B
    # Since the sum has <B monomials, B^leading <= S < B^(leading+1).
    formula_value=Fraction(leading,D)
    assert formula_value==max(Fraction(k) for k in commute_counts)
    if literal:
        S=sum(coeff << ((N+1)*e) for e,coeff in terms.items())
        assert (S.bit_length()-1)//(N+1)==leading  # exact floor(log_B(S))
        print('literal_bits',n,S.bit_length(),flush=True)
    return dict(n=n,regular_connected=regular_connected,terms=len(terms),value=str(formula_value),D_digits=len(str(D)),commute_counts=dict(commute_counts))

if __name__=='__main__':
    Path('workspace/agent4_explicit_check.py').write_text(Path(__file__).read_text())
    out=[]
    for n in range(3,7):
        start=time.time();row=check(n,literal=n<=4);row['seconds']=round(time.time()-start,3);out.append(row);print(row,flush=True)
    Path('workspace/agent4_explicit_check.json').write_text(json.dumps(out,indent=2))
