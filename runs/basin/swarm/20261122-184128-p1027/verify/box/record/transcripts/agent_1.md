# agent_1: the whole run

[user message]
Let \(\mathbb N=\{0,1,2,\ldots\}\), and let \(m,n\) be positive integers with \(\gcd(m,n)=1\). Set
\[
d=m^2+n(2m+1),\qquad (a_0,a_1,a_2,a_3,a_4)=\bigl(0,nm,n(m+1),n(2m+1),d\bigr),
\]
and let \(A=\{a_0,a_1,a_2,a_3,a_4\}\).

For each integer \(h\ge0\), let \(hA\) be the set of sums of exactly \(h\) elements of \(A\), with repetitions allowed and \(0A=\{0\}\). Define the additive semigroups
\[
S_1=\left\{\sum_{i=0}^4u_i a_i:u_i\in\mathbb N\right\},\qquad
S_2=\left\{\sum_{i=0}^4u_i(d-a_i):u_i\in\mathbb N\right\}.
\]
For \(j=1,2\), let their conductors be
\[
c_j=\min\{c\in\mathbb N:c+\mathbb N\subseteq S_j\}.
\]
Define the sumsets regularity \(\sigma(A)\) to be the least \(h_0\in\mathbb N\) such that, for every integer \(h\ge h_0\), both \(hd\ge c_1+c_2\) and
\[
hA=\{x\in\mathbb Z:0\le x\le hd,\ x\in S_1,\ hd-x\in S_2\}
\]
hold. The inequality \(hd\ge c_1+c_2\) is part of this definition, even when the displayed set equality holds at earlier levels.

Let \(P=\mathbb C[x_0,x_1,x_2,x_3,x_4]\), with \(\deg x_i=1\), and let \(\varphi:P\to\mathbb C[s,t]\) be the algebra homomorphism \(x_i\mapsto s^{a_i}t^{d-a_i}\), where \(s,t\) are independent variables. Give \(R_A=P/\ker\varphi\) its quotient grading. If its minimal graded free \(P\)-resolution has modules
\[
F_i=\bigoplus_jP(-j)^{\beta_{i,j}},
\]
where the generator of \(P(-j)\) has degree \(j\), define
\[
\operatorname{reg}(A)=\max\{j-i:\beta_{i,j}\ne0\}.
\]
Thus this is the regularity of the coordinate ring, not its defining ideal.

Determine the exact function \(\Delta(m,n)=\sigma(A)-\operatorname{reg}(A)\) for every coprime positive pair \((m,n)\).

The answer was proved recently, so it is not an open problem: your task is to find it and prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at an answer that settles less than the question asks (a partial or conditional answer, "not known") is not acceptable, and neither is conceding: when an approach fails, try another.

Proving it means showing that the answer is right in every case the question covers, and that no other answer is.

Stop only when your proof is complete. When you stop, write in that response what you proved, and what is left.

## response 1
[tool call: read_scratchpad]

[tool result]
```
(scratchpad.py is empty)
```

## response 2
[tool call: write_scratchpad]
content:
```
from math import gcd,ceil

def calc(m,n,detail=False):
 d=m*m+n*(2*m+1)
 K=(d-1)*(2*m+1)
 L=[0]+[10**18]*K
 front=[[] for _ in range(d)]
 for k in range(K+1):
  if k:
   L[k]=1+min(L[k-a] for a in (m,m+1,2*m+1) if a<=k)
  h=L[k]
  if h>=d: continue
  q,r=divmod(n*k,d)
  b=h-q-(r>0)
  if r and (not front[r] or b<front[r][-1][1]): front[r].append((q,b))
 T=0;G=0
 for f in front[1:]:
  if len(f)==1:G=max(G,sum(f[0])+1)
  for (q,b),(qq,bb) in zip(f,f[1:]):T=max(T,qq+b)
 c1=max([0]+[r+f[0][0]*d for r,f in enumerate(front) if r])-d+1
 c2=max([0]+[d-r+f[-1][1]*d for r,f in enumerate(front) if r])-d+1
 H=(c1+c2+d-1)//d
 reg=max(T,G);sig=max(T,H)
 return (sig-reg,sig,reg,T,G,H,c1,c2,front) if detail else (sig-reg,sig,reg)

if __name__=='__main__':
 for m in range(1,13):
  print('m=',m,[(n,calc(m,n)) for n in range(1,13) if gcd(m,n)==1])

```

[tool result]
```
Wrote scratchpad.py (28 lines).
```

## response 3
[tool call: run_scratchpad]

[tool result]
```
[exit code 1, 0.1s]
--- stdout ---
m= 1 [(1, (-1, 0, 1)), (2, (-1, 1, 2)), (3, (-1, 2, 3)), (4, (-1, 3, 4)), (5, (-1, 4, 5)), (6, (-1, 5, 6)), (7, (-1, 6, 7)), (8, (-1, 7, 8)), (9, (-1, 8, 9)), (10, (-1, 9, 10)), (11, (-1, 10, 11)), (12, (-1, 11, 12))]

--- stderr ---
Traceback (most recent call last):
  File "scratchpad.py", line 28, in <module>
    print('m=',m,[(n,calc(m,n)) for n in range(1,13) if gcd(m,n)==1])
                     ^^^^^^^^^
  File "scratchpad.py", line 10, in calc
    L[k]=1+min(L[k-a] for a in (m,m+1,2*m+1) if a<=k)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ValueError: min() iterable argument is empty

```

## response 4
[tool call: edit_scratchpad]
old_string: min(L[k-a] for a in (m,m+1,2*m+1) if a<=k)
new_string: min((L[k-a] for a in (m,m+1,2*m+1) if a<=k),default=10**18)

[tool result]
```
Edited scratchpad.py (1 replacement).
```

## response 5
[tool call: run_scratchpad]

[tool result]
```
[exit code 0, 0.1s]
--- stdout ---
m= 1 [(1, (-1, 0, 1)), (2, (-1, 1, 2)), (3, (-1, 2, 3)), (4, (-1, 3, 4)), (5, (-1, 4, 5)), (6, (-1, 5, 6)), (7, (-1, 6, 7)), (8, (-1, 7, 8)), (9, (-1, 8, 9)), (10, (-1, 9, 10)), (11, (-1, 10, 11)), (12, (-1, 11, 12))]
m= 2 [(1, (-1, 1, 2)), (3, (0, 4, 4)), (5, (0, 6, 6)), (7, (0, 8, 8)), (9, (0, 10, 10)), (11, (0, 12, 12))]
m= 3 [(1, (-1, 2, 3)), (2, (0, 4, 4)), (4, (0, 6, 6)), (5, (0, 7, 7)), (7, (0, 9, 9)), (8, (0, 10, 10)), (10, (0, 12, 12)), (11, (0, 13, 13))]
m= 4 [(1, (-1, 3, 4)), (3, (0, 6, 6)), (5, (0, 8, 8)), (7, (0, 10, 10)), (9, (0, 12, 12)), (11, (0, 14, 14))]
m= 5 [(1, (-1, 4, 5)), (2, (0, 6, 6)), (3, (0, 7, 7)), (4, (0, 8, 8)), (6, (0, 10, 10)), (7, (1, 12, 11)), (8, (1, 13, 12)), (9, (1, 14, 13)), (11, (1, 16, 15)), (12, (1, 17, 16))]
m= 6 [(1, (-1, 5, 6)), (5, (1, 11, 10)), (7, (1, 13, 12)), (11, (1, 17, 16))]
m= 7 [(1, (-1, 6, 7)), (2, (0, 8, 8)), (3, (0, 9, 9)), (4, (1, 11, 10)), (5, (1, 12, 11)), (6, (1, 13, 12)), (8, (1, 15, 14)), (9, (1, 16, 15)), (10, (1, 17, 16)), (11, (1, 18, 17)), (12, (1, 19, 18))]
m= 8 [(1, (-1, 7, 8)), (3, (0, 10, 10)), (5, (1, 13, 12)), (7, (1, 15, 14)), (9, (1, 17, 16)), (11, (2, 20, 18))]
m= 9 [(1, (-1, 8, 9)), (2, (0, 10, 10)), (4, (1, 13, 12)), (5, (1, 14, 13)), (7, (1, 16, 15)), (8, (2, 18, 16)), (10, (2, 20, 18)), (11, (2, 21, 19))]
m= 10 [(1, (-1, 9, 10)), (3, (1, 13, 12)), (7, (2, 18, 16)), (9, (2, 20, 18)), (11, (2, 22, 20))]
m= 11 [(1, (-1, 10, 11)), (2, (0, 12, 12)), (3, (1, 14, 13)), (4, (1, 15, 14)), (5, (1, 16, 15)), (6, (2, 18, 16)), (7, (2, 19, 17)), (8, (2, 20, 18)), (9, (2, 21, 19)), (10, (2, 22, 20)), (12, (2, 24, 22))]
m= 12 [(1, (-1, 11, 12)), (5, (1, 17, 16)), (7, (2, 20, 18)), (11, (3, 25, 22))]

--- stderr ---
(empty)
```

## response 6
[tool call: edit_scratchpad]
old_string:
```
for m in range(1,13):
  print('m=',m,[(n,calc(m,n)) for n in range(1,13) if gcd(m,n)==1])
```
new_string:
```
for m,n in [(1,3),(2,3),(3,2),(5,2),(5,7),(6,5),(8,11),(12,11),(15,2),(15,4),(15,7),(15,16),(20,21)]:
  v=calc(m,n,True);d=m*m+n*(2*m+1)
  print(m,n,'d',d,'v',v[:-1], 'c1+c2 - (m+n-1)d',v[6]+v[7]-(m+n-1)*d)
```

[tool result]
```
Edited scratchpad.py (1 replacement).
```

## response 7
[tool call: run_scratchpad]

[tool result]
```
[exit code 0, 0.1s]
--- stdout ---
1 3 d 10 v (-1, 2, 3, 0, 3, 2, 18, 0) c1+c2 - (m+n-1)d -12
2 3 d 19 v (0, 4, 4, 0, 4, 4, 42, 16) c1+c2 - (m+n-1)d -18
3 2 d 23 v (0, 4, 4, 0, 4, 4, 34, 38) c1+c2 - (m+n-1)d -20
5 2 d 47 v (0, 6, 6, 0, 6, 6, 86, 164) c1+c2 - (m+n-1)d -32
5 7 d 102 v (1, 12, 11, 0, 11, 12, 746, 384) c1+c2 - (m+n-1)d 8
6 5 d 101 v (1, 11, 10, 0, 10, 11, 550, 470) c1+c2 - (m+n-1)d 10
8 11 d 251 v (2, 20, 18, 0, 18, 20, 3116, 1694) c1+c2 - (m+n-1)d 292
12 11 d 419 v (3, 25, 22, 0, 22, 25, 5632, 4466) c1+c2 - (m+n-1)d 880
15 2 d 287 v (0, 16, 16, 0, 16, 16, 706, 3794) c1+c2 - (m+n-1)d -92
15 4 d 349 v (1, 19, 18, 0, 18, 19, 1884, 4662) c1+c2 - (m+n-1)d 264
15 7 d 442 v (2, 23, 21, 0, 21, 23, 4116, 5964) c1+c2 - (m+n-1)d 798
15 16 d 721 v (4, 34, 30, 0, 30, 34, 14160, 9870) c1+c2 - (m+n-1)d 2400
20 21 d 1261 v (5, 45, 40, 0, 40, 45, 33180, 23560) c1+c2 - (m+n-1)d 6300

--- stderr ---
(empty)
```

## response 8
[tool call: edit_scratchpad]
old_string:
```
for m,n in [(1,3),(2,3),(3,2),(5,2),(5,7),(6,5),(8,11),(12,11),(15,2),(15,4),(15,7),(15,16),(20,21)]:
  v=calc(m,n,True);d=m*m+n*(2*m+1)
  print(m,n,'d',d,'v',v[:-1], 'c1+c2 - (m+n-1)d',v[6]+v[7]-(m+n-1)*d)
```
new_string:
```
m,n=3,2
 d=m*m+n*(2*m+1)
 v=calc(m,n,True)
 pts={(r+f[0][0]*d,sum(f[0])+1) for r,f in enumerate(v[-1]) if r}
 pts.add((0,0))
 for u in range(m+n+1):
  for v in range(m+n+1):
   if u*v: continue
   W=[w for w in range(m+n+1) if (n*(m*u+(m+1)*v+(2*m+1)*w),u+v+w) in pts]
   if W:print(u,v,W)
```

[tool result]
```
Edited scratchpad.py (1 replacement).
```

## response 9
[tool call: run_scratchpad]

[tool result]
```
[exit code 0, 0.0s]
--- stdout ---
0 0 [0, 1, 2, 3, 4]
0 1 [0, 1, 2, 3]
0 2 [0, 1, 2]
0 3 [0, 1]
0 4 [0]
1 0 [0, 1, 2, 3]
2 0 [0, 1, 2]
3 0 [0, 1]

--- stderr ---
(empty)
```

## response 10
[reasoning summary]
**Evaluating high differences in variables**

I’m working through how to handle high differences, particularly when u-v is greater than or equal to m plus one. I need to subtract m plus one from u, which should be greater than or equal to zero, and then add m to v. The end goal is to ensure h is less than or equal to u-1 while preserving k. It looks like if v is much larger than u, low absolute values can still reduce things, even if they cross. I'll keep repeating this until any imbalances are addressed outside the ends.

[reasoning summary]
**Considering code efficiency**

I think the for each loop isn't necessary in the final code, but the tool runs on a finite grid. With values for m and n up to 10, perhaps it's coprime and yields around 63. I wonder about the maximum d — maybe it's around 271? For H20, we get around 5000 sets with about 100k each in manageable loops. Betti selection may involve a dozen. I should create the code from scratch, ensuring it retains previous calculations. A full rewrite seems needed!

[message]
The key structure is that this ring is free over the polynomial ring generated by the two endpoint variables. This gives the sumset equality at every level, so \(\sigma(A)\) is governed entirely by the conductor inequality. I’ll prove that freeness, then check the resulting formulas against direct semigroup, sumset, and Koszul-homology computations.

[tool call: write_scratchpad]
content:
```
from math import gcd
from heapq import heappush, heappop
from itertools import combinations
from fractions import Fraction
from functools import lru_cache

def ceildiv(a,b):
    return -((-a)//b)

def answer(m,n):
    assert m>0 and n>0 and gcd(m,n)==1
    d=m*m+n*(2*m+1)
    M=m+n-1
    c1=n*(2*m+1)*M-d+1
    c2=(m-1)*(d-m-1)
    sig=ceildiv(c1+c2,d)
    delta=ceildiv((n-2)*m*m-(3*m+2)*n+2,d)
    assert sig-M==delta
    return delta,sig,M,c1,c2

def reduce_pair(m,n,u,v):
    # b_(u,v) = x0^p x4^q b_(U,V), with b of degree max(u,v).
    p=q=0
    while True:
        old=max(u,v)
        if u-v>m:
            u,v=u-m-1,v+m
            p+=old-max(u,v)
        elif v-u>m:
            u,v=u+m+1,v-m
            p+=old-max(u,v)
        elif old>=m+n:
            if u>=v:
                u,v=u-m-n,v-n
            else:
                u,v=u-n+1,v-m-n
            q+=1
            p+=old-max(u,v)-1
        else:
            return u,v,p,q
        assert min(u,v,p,q)>=0

def apery(gens,d):
    # Independent shortest-path computation of the Apéry set modulo d.
    dist=[None]*d
    dist[0]=0
    heap=[(0,0)]
    while heap:
        x,r=heappop(heap)
        if dist[r]!=x: continue
        for a in gens:
            y=x+a; s=y%d
            if dist[s] is None or y<dist[s]:
                dist[s]=y
                heappush(heap,(y,s))
    assert all(x is not None for x in dist)
    return dist

def qrank(A):
    if not A or not A[0]: return 0
    A=[[Fraction(x) for x in row] for row in A]
    r=0
    for c in range(len(A[0])):
        pivot=next((i for i in range(r,len(A)) if A[i][c]),None)
        if pivot is None: continue
        A[r],A[pivot]=A[pivot],A[r]
        z=A[r][c]
        A[r]=[x/z for x in A[r]]
        for i in range(r+1,len(A)):
            z=A[i][c]
            if z: A[i]=[x-z*y for x,y in zip(A[i],A[r])]
        r+=1
        if r==len(A): break
    return r

@lru_cache(None)
def koszul_homology(code):
    # code records which of the 32 subsets of five generators occur.
    V=[[s for s in range(32) if (code>>s)&1 and s.bit_count()==i]
       for i in range(6)]
    ranks=[0]*7
    for i in range(1,6):
        rows={s:j for j,s in enumerate(V[i-1])}
        mat=[[0]*len(V[i]) for _ in V[i-1]]
        for j,s in enumerate(V[i]):
            for k,b in enumerate(b for b in range(5) if (s>>b)&1):
                face=s^(1<<b)
                assert face in rows
                mat[rows[face]][j]=(-1)**k
        ranks[i]=qrank(mat)
    hom=tuple(len(V[i])-ranks[i]-ranks[i+1] for i in range(6))
    assert min(hom)>=0
    return hom

def direct_betti(A,sumsets,J):
    subset_size=[s.bit_count() for s in range(32)]
    subset_sum=[sum(A[i] for i in range(5) if (s>>i)&1) for s in range(32)]
    betti={}
    for j in range(J+1):
        for x in sumsets[j]:
            code=0
            for s in range(32):
                i=subset_size[s]
                if i<=j and x-subset_sum[s] in sumsets[j-i]:
                    code|=1<<s
            for i,b in enumerate(koszul_homology(code)):
                if b: betti[i,j]=betti.get((i,j),0)+b
    return betti

def check(m,n,with_betti=False):
    delta,sigma,M,c1,c2=answer(m,n)
    d=m*m+n*(2*m+1)
    A=[0,n*m,n*(m+1),n*(2*m+1),d]
    D=[(u,v) for u in range(M+1) for v in range(M+1) if abs(u-v)<=m]
    assert len(D)==d
    ab={}
    for u,v in D:
        alpha=n*(m*u+(m+1)*v)
        beta=max(u,v)*d-alpha
        assert alpha%d not in ab
        ab[alpha%d]=(alpha,beta,max(u,v))
    assert len(ab)==d and max(e for a,b,e in ab.values())==M
    for u in range(2*(m+n)+2):
        for v in range(2*(m+n)+2):
            U,V,p,q=reduce_pair(m,n,u,v)
            assert (U,V) in D
            assert max(u,v)==p+q+max(U,V)
            assert n*(m*u+(m+1)*v)==q*d+n*(m*U+(m+1)*V)
    ap1=apery(A,d)
    ap2=apery([d-a for a in A],d)
    for r,(alpha,beta,e) in ab.items():
        assert ap1[r]==alpha
        assert ap2[(-r)%d]==beta
    assert max(ap1)-d+1==c1
    assert max(ap2)-d+1==c2
    assert (sigma==0 or (sigma-1)*d<c1+c2) and sigma*d>=c1+c2
    J=max(sigma+1,M+5 if with_betti else M+2)
    S=[{0}]
    for h in range(1,J+1):
        S.append({x+a for x in S[-1] for a in A})
    for h in range(J+1):
        saturated={x for x in range(h*d+1)
                   if x>=ap1[x%d] and h*d-x>=ap2[(h*d-x)%d]}
        assert S[h]==saturated
        assert len(S[h])==sum(h-e+1 for a,b,e in ab.values() if e<=h)
    if with_betti:
        B=direct_betti(A,S,M+5)
        assert max(j-i for i,j in B)==M
        # Euler characteristic of the graded free resolution.
        for h in range(M+6):
            from math import comb
            predicted=sum((-1)**i*b*comb(h-j+4,4)
                          for (i,j),b in B.items() if j<=h)
            assert predicted==len(S[h])
        return B

if __name__=='__main__':
    count=0
    for m in range(1,11):
        for n in range(1,11):
            if gcd(m,n)==1:
                check(m,n)
                count+=1
    print('Direct Apéry, reduction, sumset and Hilbert-function checks:',count,'pairs')
    pairs=[(1,1),(1,3),(2,1),(2,3),(3,2),(3,4),(4,3),(5,2),(5,7),(8,11)]
    for m,n in pairs:
        B=check(m,n,True)
        print((m,n),'(delta,sigma,reg,c1,c2) =',answer(m,n),
              'Betti =',sorted(B.items()))
    print('All checks passed; distinct Koszul complexes:',koszul_homology.cache_info().currsize)

```

[tool result]
```
Wrote scratchpad.py (170 lines).
```

## response 11
[tool call: run_scratchpad]
timeout_seconds: 200

[tool result]
```
[exit code 1, 0.1s]
--- stdout ---
(empty)
--- stderr ---
Traceback (most recent call last):
  File "scratchpad.py", line 162, in <module>
    check(m,n)
  File "scratchpad.py", line 128, in check
    assert n*(m*u+(m+1)*v)==q*d+n*(m*U+(m+1)*V)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError

```

## response 12
[tool call: edit_scratchpad]
old_string:
```
            q+=1
            p+=old-max(u,v)-1
```
new_string:
```
            q+=n
            p+=old-max(u,v)-n
```

[tool result]
```
Edited scratchpad.py (1 replacement).
```

## response 13
[tool call: run_scratchpad]
timeout_seconds: 200

[tool result]
```
[exit code 0, 0.2s]
--- stdout ---
Direct Apéry, reduction, sumset and Hilbert-function checks: 63 pairs
(1, 1) (delta,sigma,reg,c1,c2) = (-1, 0, 1, 0, 0) Betti = [((0, 0), 1), ((1, 2), 6), ((2, 3), 8), ((3, 4), 3)]
(1, 3) (delta,sigma,reg,c1,c2) = (-1, 2, 3, 18, 0) Betti = [((0, 0), 1), ((1, 2), 3), ((1, 4), 3), ((2, 3), 2), ((2, 5), 6), ((3, 6), 3)]
(2, 1) (delta,sigma,reg,c1,c2) = (-1, 1, 2, 2, 6) Betti = [((0, 0), 1), ((1, 2), 1), ((1, 3), 7), ((2, 4), 12), ((3, 5), 5)]
(2, 3) (delta,sigma,reg,c1,c2) = (0, 4, 4, 42, 16) Betti = [((0, 0), 1), ((1, 2), 1), ((1, 3), 2), ((1, 5), 5), ((2, 4), 2), ((2, 6), 10), ((3, 7), 5)]
(3, 2) (delta,sigma,reg,c1,c2) = (0, 4, 4, 34, 38) Betti = [((0, 0), 1), ((1, 2), 1), ((1, 4), 2), ((1, 5), 7), ((2, 5), 2), ((2, 6), 14), ((3, 7), 7)]
(3, 4) (delta,sigma,reg,c1,c2) = (0, 6, 6, 132, 66) Betti = [((0, 0), 1), ((1, 2), 1), ((1, 4), 2), ((1, 7), 7), ((2, 5), 2), ((2, 8), 14), ((3, 9), 7)]
(4, 3) (delta,sigma,reg,c1,c2) = (0, 6, 6, 120, 114) Betti = [((0, 0), 1), ((1, 2), 1), ((1, 5), 2), ((1, 7), 9), ((2, 6), 2), ((2, 8), 18), ((3, 9), 9)]
(5, 2) (delta,sigma,reg,c1,c2) = (0, 6, 6, 86, 164) Betti = [((0, 0), 1), ((1, 2), 1), ((1, 6), 2), ((1, 7), 11), ((2, 7), 2), ((2, 8), 22), ((3, 9), 11)]
(5, 7) (delta,sigma,reg,c1,c2) = (1, 12, 11, 746, 384) Betti = [((0, 0), 1), ((1, 2), 1), ((1, 6), 2), ((1, 12), 11), ((2, 7), 2), ((2, 13), 22), ((3, 14), 11)]
(8, 11) (delta,sigma,reg,c1,c2) = (2, 20, 18, 3116, 1694) Betti = [((0, 0), 1), ((1, 2), 1), ((1, 9), 2), ((1, 19), 17), ((2, 10), 2), ((2, 20), 34), ((3, 21), 17)]
All checks passed; distinct Koszul complexes: 104

--- stderr ---
(empty)
```

## response 14
[message]
Put \(d=m^2+(2m+1)n\). Then the answer is
\[
\boxed{\displaystyle
\Delta(m,n)=
\left\lceil
\frac{(n-2)m^2-(3m+2)n+2}
     {m^2+(2m+1)n}
\right\rceil .}
\]

In fact, the two invariants individually are
\[
\boxed{\operatorname{reg}(A)=m+n-1}
\]
and
\[
\boxed{\displaystyle
\sigma(A)=
\left\lceil
\frac{n(2m+1)(m+n-1)+(m-2)d-m^2+2}{d}
\right\rceil .}
\]

We prove these statements for all the stated pairs, including \(m=1\) or \(n=1\), and then give executable checks using independent semigroup, sumset, and Koszul-homology computations.

## 1. A free module basis

Write \(R=R_A\), and use \(x_i\) also for its image in \(R\). Thus
\[
x_0=t^d,\qquad x_4=s^d,
\]
so
\[
B=\mathbb C[x_0,x_4]\subseteq R
\]
is a polynomial ring in two degree-one variables.

Set
\[
M=m+n-1.
\]
For \(u,v\in\mathbb N\), define
\[
b_{u,v}
=x_1^{\max(u-v,0)}
 x_2^{\max(v-u,0)}
 x_3^{\min(u,v)}.
\]
Its degree and its exponent of \(s\) are, respectively,
\[
e(u,v)=\max(u,v),\qquad
\alpha(u,v)=n\bigl(mu+(m+1)v\bigr).
\]
Its exponent of \(t\) is therefore
\[
\beta(u,v)=e(u,v)d-\alpha(u,v).
\]

Consider the finite set
\[
D=\{(u,v)\in\mathbb N^2: u,v\le M,\ |u-v|\le m\}.
\]

### Lemma
The elements \(b_{u,v}\), for \((u,v)\in D\), form a free \(B\)-basis of \(R\).

### Proof: spanning

Since \(a_1+a_2=a_3\), we have
\[
x_1x_2=x_0x_3.
\]
Consequently, every monomial in \(x_1,x_2,x_3\) is an \(x_0\)-multiple of some \(b_{u,v}\). It suffices to reduce arbitrary pairs \((u,v)\) to \(D\).

For this purpose put
\[
k(u,v)=mu+(m+1)v,\qquad H=\max(u,v).
\]
Two monomials in \(R\) are equal whenever they have the same degree and the same \(s\)-exponent.

First reduce the imbalance.

* If \(u-v>m\), replace
  \[
  (u,v)\longmapsto(u-m-1,v+m).
  \]
* If \(v-u>m\), replace
  \[
  (u,v)\longmapsto(u+m+1,v-m).
  \]

Both operations preserve \(k(u,v)\), keep the coordinates nonnegative, do not increase \(H\), and strictly decrease \(|u-v|\). If the new maximum is \(H'\), they give the identity
\[
b_{u,v}=x_0^{H-H'}b_{u',v'}.
\]

Once \(|u-v|\le m\), suppose \(H\ge m+n\).

* If \(u\ge v\), replace
  \[
  (u,v)\longmapsto(u-m-n,v-n).
  \]
  Both new coordinates are nonnegative because \(v\ge u-m\ge n\).
* If \(v>u\), replace
  \[
  (u,v)\longmapsto(u-n+1,v-m-n).
  \]
  Again both new coordinates are nonnegative, because \(u\ge v-m\ge n\).

In either case,
\[
k(u,v)-k(u',v')=d,
\qquad H'\le H-n.
\]
Thus
\[
b_{u,v}=x_0^{H-H'-n}x_4^n b_{u',v'}.
\]
The exponent of \(x_0\) is nonnegative.

Repeating these operations terminates: an imbalance operation decreases the lexicographic pair \((H,|u-v|)\), and an endpoint operation decreases \(H\). At termination the pair lies in \(D\). This proves spanning over \(B\).

### Proof: independence

Counting by the value of \(u-v\),
\[
\begin{aligned}
|D|
&=(M+1)+2\sum_{i=1}^{m}(M-i+1)\\
&=(2m+1)(M+1)-m(m+1)\\
&=m^2+(2m+1)n=d.
\end{aligned}
\]

Moreover,
\[
\gcd(nm,n(m+1),d)=1,
\]
because \(\gcd(n,d)=\gcd(n,m^2)=1\). Hence nonnegative combinations of \(nm\) and \(n(m+1)\) attain every residue modulo \(d\). The reductions above preserve the \(s\)-exponent modulo \(d\), so the \(d\) elements indexed by \(D\) attain all \(d\) residues. They therefore attain each residue exactly once.

Different basis candidates consequently have disjoint \(s\)-exponent residues modulo \(d\), whereas multiplication by \(B\) preserves those residues. Within one candidate, multiplication by the polynomial ring \(\mathbb C[s^d,t^d]\) is injective. Thus the spanning sum is direct:
\[
\boxed{\displaystyle
R=\bigoplus_{(u,v)\in D}B\,b_{u,v}.}
\]
This proves the lemma. \(\square\)

## 2. The regularity

The free decomposition shows that \(x_0,x_4\) is an \(R\)-regular sequence. It also shows that
\[
E=R/(x_0,x_4)R
\]
has vector-space basis given by the images of the \(b_{u,v}\), \((u,v)\in D\). Its highest nonzero degree is
\[
M,
\]
since all basis degrees are at most \(M\), and \((M,M)\in D\).

For completeness, this determines the regularity in exactly the convention of the question.

Tensoring the minimal graded \(P\)-resolution of \(R\) with
\[
Q=P/(x_0,x_4)=\mathbb C[x_1,x_2,x_3]
\]
preserves exactness because \(x_0,x_4\) is \(R\)-regular. The resulting resolution is minimal and has the same graded shifts. Thus
\[
\operatorname{reg}_P(R)=\operatorname{reg}_Q(E).
\]

The Koszul complex of \(E\) over \(Q\) gives
\[
\operatorname{Tor}_i^Q(E,\mathbb C)_j=0
\quad\text{if }j>M+i.
\]
On the other hand, any nonzero element of \(E_M\) is annihilated by all three variables. It gives a nonzero top Koszul-homology class in degree \(M+3\). Hence
\[
\operatorname{reg}_Q(E)=M.
\]
Therefore
\[
\boxed{\operatorname{reg}(A)=m+n-1.}
\]

## 3. The sumset equality holds at every level

Index the basis elements by their \(s\)-exponent residues \(r\pmod d\), writing their data as
\[
(\alpha_r,\beta_r,e_r),\qquad
\alpha_r+\beta_r=e_rd.
\]

The free-basis decomposition implies that the exponent pairs occurring in \(R\), in residue \(r\), are exactly
\[
(\alpha_r+qd,\ \beta_r+pd),
\qquad p,q\in\mathbb N.
\]

In particular:

* \(\alpha_r\) is the least element of \(S_1\) congruent to \(r\pmod d\);
* \(\beta_r\) is the least element of \(S_2\) congruent to \(-r\pmod d\).

Now suppose
\[
0\le x\le hd,\qquad x\in S_1,\qquad hd-x\in S_2.
\]
Choose \(r\equiv x\pmod d\). Then
\[
x=\alpha_r+qd,\qquad
hd-x=\beta_r+pd
\]
for some \(p,q\in\mathbb N\). Adding gives
\[
h=e_r+p+q.
\]
Thus \(x_4^qx_0^pb_r\) is a degree-\(h\) monomial with \(s\)-exponent \(x\), proving \(x\in hA\).

The converse follows immediately from the definitions. Hence, for **every** \(h\ge0\),
\[
\boxed{\displaystyle
hA=\{x:0\le x\le hd,\ x\in S_1,\ hd-x\in S_2\}.}
\]

The conductor inequality in the question is therefore the only restriction on \(\sigma(A)\):
\[
\boxed{\displaystyle
\sigma(A)=\left\lceil\frac{c_1+c_2}{d}\right\rceil .}
\]

## 4. Computing the conductors

If a numerical semigroup contains \(d\), and its least elements in the \(d\) residue classes are \(w_r\), its conductor is
\[
c=\max_r w_r-d+1.
\]
Indeed, the largest missing integer in residue \(r\), when nonnegative, is \(w_r-d\). This formula also gives \(c=0\) for \(\mathbb N\).

Our basis supplies precisely these least elements.

### The first conductor

Since \(u,v\le M\),
\[
\max_D\alpha(u,v)=n(2m+1)M,
\]
attained at \(u=v=M\). Thus
\[
\boxed{\displaystyle c_1=n(2m+1)M-d+1.}
\]

### The second conductor

If \(u\ge v\), then
\[
\beta(u,v)=m^2u+n(m+1)(u-v)
\le m^2M+nm(m+1).
\]
Equality holds at
\[
(u,v)=(M,M-m)=(M,n-1).
\]

If \(v\ge u\), then
\[
\beta(u,v)=m^2v+nm(v-u)
\le m^2M+nm^2,
\]
which is no larger. Consequently,
\[
\max_D\beta(u,v)
=m^2M+nm(m+1)
=m(d-m).
\]
Therefore
\[
\boxed{\displaystyle
c_2=m(d-m)-d+1=(m-1)(d-m-1).}
\]

It follows that
\[
c_1+c_2
=n(2m+1)M+(m-2)d-m^2+2.
\]
Since \(M\) is an integer,
\[
\Delta
=\left\lceil\frac{c_1+c_2-Md}{d}\right\rceil.
\]
Finally,
\[
c_1+c_2-Md
=(n-2)m^2-(3m+2)n+2,
\]
which proves the claimed formula.

## 5. Executable verification

The following is pure Python. It does more than evaluate the formulas:

1. It checks the reduction identities and basis residues.
2. It independently computes both Apéry sets by shortest paths.
3. It constructs actual sumsets and checks the equality at every tested level.
4. It checks the Hilbert function against the free-basis decomposition.
5. It computes graded Betti numbers directly from the five-generator Koszul complex, using exact rational ranks.

For the Betti checks, degrees through \(M+5\) cover every possible nonzero Betti number by the regularity bound proved above and the length-five Koszul complex.

```python
from math import gcd, comb
from heapq import heappush, heappop
from fractions import Fraction
from functools import lru_cache


def ceildiv(a, b):
    return -((-a) // b)


def answer(m, n):
    assert m > 0 and n > 0 and gcd(m, n) == 1
    d = m*m + n*(2*m + 1)
    M = m + n - 1
    c1 = n*(2*m + 1)*M - d + 1
    c2 = (m - 1)*(d - m - 1)
    sigma = ceildiv(c1 + c2, d)
    delta = ceildiv((n - 2)*m*m - (3*m + 2)*n + 2, d)
    assert sigma - M == delta
    return delta, sigma, M, c1, c2


def reduce_pair(m, n, u, v):
    # Certifies b_(u,v) = x0^p x4^q b_(U,V).
    p = q = 0
    while True:
        old = max(u, v)
        if u - v > m:
            u, v = u - m - 1, v + m
            p += old - max(u, v)
        elif v - u > m:
            u, v = u + m + 1, v - m
            p += old - max(u, v)
        elif old >= m + n:
            if u >= v:
                u, v = u - m - n, v - n
            else:
                u, v = u - n + 1, v - m - n
            q += n
            p += old - max(u, v) - n
        else:
            return u, v, p, q
        assert min(u, v, p, q) >= 0


def apery(gens, d):
    # Independent shortest-path calculation modulo d.
    dist = [None] * d
    dist[0] = 0
    heap = [(0, 0)]
    while heap:
        x, r = heappop(heap)
        if dist[r] != x:
            continue
        for a in gens:
            y = x + a
            s = y % d
            if dist[s] is None or y < dist[s]:
                dist[s] = y
                heappush(heap, (y, s))
    assert all(x is not None for x in dist)
    return dist


def qrank(A):
    """Exact rank over Q."""
    if not A or not A[0]:
        return 0
    A = [[Fraction(x) for x in row] for row in A]
    r = 0
    for c in range(len(A[0])):
        pivot = next(
            (i for i in range(r, len(A)) if A[i][c]), None
        )
        if pivot is None:
            continue
        A[r], A[pivot] = A[pivot], A[r]
        z = A[r][c]
        A[r] = [x / z for x in A[r]]
        for i in range(r + 1, len(A)):
            z = A[i][c]
            if z:
                A[i] = [x - z*y for x, y in zip(A[i], A[r])]
        r += 1
        if r == len(A):
            break
    return r


@lru_cache(None)
def koszul_homology(code):
    # Bit s of code records whether subset s of {0,...,4} occurs.
    V = [
        [s for s in range(32)
         if (code >> s) & 1 and s.bit_count() == i]
        for i in range(6)
    ]
    ranks = [0] * 7
    for i in range(1, 6):
        rows = {s: j for j, s in enumerate(V[i - 1])}
        mat = [[0] * len(V[i]) for _ in V[i - 1]]
        for j, s in enumerate(V[i]):
            bits = [b for b in range(5) if (s >> b) & 1]
            for k, b in enumerate(bits):
                face = s ^ (1 << b)
                assert face in rows
                mat[rows[face]][j] = (-1)**k
        ranks[i] = qrank(mat)

    hom = tuple(
        len(V[i]) - ranks[i] - ranks[i + 1]
        for i in range(6)
    )
    assert min(hom) >= 0
    return hom


def direct_betti(A, sumsets, J):
    # At multidegree (j,x), the Koszul basis consists of subsets F
    # such that x-sum(A[i] for i in F) lies in (j-|F|)A.
    sizes = [s.bit_count() for s in range(32)]
    sums = [
        sum(A[i] for i in range(5) if (s >> i) & 1)
        for s in range(32)
    ]
    betti = {}
    for j in range(J + 1):
        for x in sumsets[j]:
            code = 0
            for s in range(32):
                i = sizes[s]
                if i <= j and x - sums[s] in sumsets[j - i]:
                    code |= 1 << s
            for i, b in enumerate(koszul_homology(code)):
                if b:
                    betti[i, j] = betti.get((i, j), 0) + b
    return betti


def check(m, n, with_betti=False):
    delta, sigma, M, c1, c2 = answer(m, n)
    d = m*m + n*(2*m + 1)
    A = [0, n*m, n*(m + 1), n*(2*m + 1), d]

    D = {
        (u, v)
        for u in range(M + 1)
        for v in range(M + 1)
        if abs(u - v) <= m
    }
    assert len(D) == d

    ab = {}
    for u, v in D:
        alpha = n*(m*u + (m + 1)*v)
        beta = max(u, v)*d - alpha
        assert alpha % d not in ab
        ab[alpha % d] = (alpha, beta, max(u, v))
    assert len(ab) == d
    assert max(e for a, b, e in ab.values()) == M

    # Explicitly check reduction certificates on a finite grid.
    for u in range(2*(m + n) + 2):
        for v in range(2*(m + n) + 2):
            U, V, p, q = reduce_pair(m, n, u, v)
            assert (U, V) in D
            assert max(u, v) == p + q + max(U, V)
            assert (
                n*(m*u + (m + 1)*v)
                == q*d + n*(m*U + (m + 1)*V)
            )

    # Independent numerical-semigroup computations.
    ap1 = apery(A, d)
    ap2 = apery([d - a for a in A], d)
    for r, (alpha, beta, e) in ab.items():
        assert ap1[r] == alpha
        assert ap2[(-r) % d] == beta
    assert max(ap1) - d + 1 == c1
    assert max(ap2) - d + 1 == c2
    assert sigma*d >= c1 + c2
    assert sigma == 0 or (sigma - 1)*d < c1 + c2

    J = max(sigma + 1, M + 5 if with_betti else M + 2)
    S = [{0}]
    for h in range(1, J + 1):
        S.append({x + a for x in S[-1] for a in A})

    for h in range(J + 1):
        saturated = {
            x for x in range(h*d + 1)
            if x >= ap1[x % d]
            and h*d - x >= ap2[(h*d - x) % d]
        }
        assert S[h] == saturated
        assert len(S[h]) == sum(
            h - e + 1 for a, b, e in ab.values() if e <= h
        )

    if with_betti:
        B = direct_betti(A, S, M + 5)
        assert max(j - i for i, j in B) == M

        # Resolution Euler characteristic versus actual sumsets.
        for h in range(M + 6):
            predicted = sum(
                (-1)**i * b * comb(h - j + 4, 4)
                for (i, j), b in B.items() if j <= h
            )
            assert predicted == len(S[h])
        return B


if __name__ == "__main__":
    count = 0
    for m in range(1, 11):
        for n in range(1, 11):
            if gcd(m, n) == 1:
                check(m, n)
                count += 1
    print("Apéry/reduction/sumset/Hilbert checks:", count, "pairs")

    pairs = [
        (1, 1), (1, 3), (2, 1), (2, 3), (3, 2),
        (3, 4), (4, 3), (5, 2), (5, 7), (8, 11)
    ]
    for m, n in pairs:
        B = check(m, n, with_betti=True)
        print((m, n), answer(m, n),
              "computed regularity =", max(j-i for i, j in B))

    print("All checks passed.")
```

I ran these checks successfully: all \(63\) coprime pairs with \(1\le m,n\le10\), and the ten listed direct Betti computations. For example, the independently checked values include
\[
\begin{array}{c|c|r|r|r}
m&n&\sigma&\operatorname{reg}&\Delta\\ \hline
1&1&0&1&-1\\
2&3&4&4&0\\
5&7&12&11&1\\
8&11&20&18&2
\end{array}
\]

Thus the displayed ceiling formula is proved for every coprime positive pair \((m,n)\). Nothing remains unresolved.
