from fractions import Fraction as Q
from math import gcd
from itertools import combinations
import random
import sympy as sp

def newton_vertices(support):
    # The reduced support is finite here. The output is the exact lower hull.
    d = {}
    for x,y in support:
        if x >= 1 and y >= 1:
            d[x] = min(y,d.get(x,y))
    pts=[]; best=None
    for x,y in sorted(d.items()):
        if best is None or y < best:
            pts.append((Q(x),Q(y))); best=y
    hull=[]
    def cross(o,a,b):
        return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    for z in pts:
        while len(hull)>=2 and cross(hull[-2],hull[-1],z)<=0:
            hull.pop()
        hull.append(z)
    if not hull: raise ValueError('empty reduced support')
    return hull

def exceptional_description(V):
    V=list(V); L=V[0]; R=V[-1]
    return {'isolated_vertices': [v for v in V if v[0]!=v[1]],
            'vertical_half_open': ((L[0],L[1]),(L[0],L[0])) if L[1]<L[0] else None,
            'horizontal_half_open': ((R[0],R[1]),(R[1],R[1])) if R[0]<R[1] else None}

def exceptional(V,z):
    a,b=map(Q,z); AL,BL=V[0]; AR,BR=V[-1]
    return ((a,b) in V and a!=b) or (a==AL and BL<=b<AL) or (b==BR and AR<=a<BR)

def boundary_samples(V):
    out=set(V)
    for (A,B),(C,D) in zip(V,V[1:]):
        for t in (Q(1,7),Q(1,2),Q(6,7)):
            out.add((A+t*(C-A),B+t*(D-B)))
    AL,BL=V[0]; AR,BR=V[-1]
    for t in (Q(1,3),Q(1),Q(3),Q(20)):
        out.add((AL,BL+t)); out.add((AR+t,BR))
    out.add((AL,max(AL,BL))); out.add((max(AR,BR),BR))
    return out

def support_value(V,j,k):
    return min(a*j+b*k for a,b in V)

rng=random.Random(7183)
polys=[]
# Exhaust all subsets of sizes 1..5 of the 3x3 grid, and randomized larger supports.
grid=[(i,j) for i in range(1,4) for j in range(1,4)]
for n in range(1,6):
    for supp in combinations(grid,n): polys.append(newton_vertices(supp))
for _ in range(350):
    polys.append(newton_vertices([(rng.randint(1,24),rng.randint(1,24)) for _ in range(20)]))
polys=list(dict.fromkeys(tuple(v) for v in polys))
checks=0
for V in polys:
    # Verify each hull vertex admits a strictly positive exposing normal.
    for i,(a,b) in enumerate(V):
        # Normal (1,q); lower and upper admissible q.
        lo=Q(0) if i==0 else (a-V[i-1][0])/(V[i-1][1]-b)
        hi=None if i==len(V)-1 else (V[i+1][0]-a)/(b-V[i+1][1])
        q=lo+1 if hi is None else (lo+hi)/2
        assert q>0 and all(a+q*b<c+q*d for c,d in V if (c,d)!=(a,b))
        checks+=1
    for a,b in boundary_samples(V):
        # Supporting weights and the universal W <= 1 inequality.
        for j,k in ((1,1),(1,7),(9,2),(3,11)):
            assert support_value(V,j,k)<=a*j+b*k
            checks+=1
        # The exact finite-type inequality, for every compact face and all
        # possible multiplicities 1 <= m <= gcd(horizontal span,vertical span).
        for (A,B),(C,D) in zip(V,V[1:]):
            ell=gcd(int(C-A),int(B-D))
            u=(C-A)/ell; v=(B-D)/ell
            const=v*A+u*B
            assert const>=u+v+ell*u*v
            assert a+b>=2+ell*min(u,v)>=ell+2
            for m in range(1,ell+1):
                assert a+b>=m+2
                # Precisely the forbidden p's of the finite-type input.
                if a+b==m+2 and (a==1 or b==1):
                    assert exceptional(V,(a,b))
                checks+=1
        if not exceptional(V,(a,b)):
            # The complete list of successful summation mechanisms.
            edge=any((a,b) not in (P,R) and
                     (a-P[0])*(R[1]-P[1])==(b-P[1])*(R[0]-P[0]) and
                     P[0]<a<R[0] for P,R in zip(V,V[1:]))
            diagonal_vertex=(a,b) in V and a==b
            horizontal=b==V[-1][1] and a>V[-1][0] and a>=b
            vertical=a==V[0][0] and b>V[0][1] and b>=a
            assert edge or diagonal_vertex or horizontal or vertical
            checks+=1

# Exact symbolic scaling and randomized-sign obstruction.
a,b,X,Y=sp.symbols('a b X Y',positive=True)
p=(a+b)/a; s=1/(a+b)
assert sp.simplify(a*s-1/p)==0
assert sp.simplify(-1+b*s+1/p)==0
assert sp.simplify(s-(1-1/p)/b)==0
assert sp.simplify(sp.Rational(1,2)-1/p-(b-a)/(2*(a+b)))==0

# The fixed-offset L2 incidence matrix really has uniformly bounded degrees:
# h increases by >=1 in each coordinate. Check all offsets in a finite box.
max_degree=0
for V in polys:
    rows={}; cols={}
    for j in range(1,21):
        for k in range(1,21):
            n=support_value(V,j,k)
            rows[(j,n)]=rows.get((j,n),0)+1
            cols[(k,n)]=cols.get((k,n),0)+1
    deg=max(max(rows.values()),max(cols.values()))
    assert deg==1
    max_degree=max(max_degree,deg)

print('distinct Newton polygons:',len(polys))
print('exact geometric/type/scaling checks:',checks)
print('maximum exact-frequency row/column degree:',max_degree)
for supp in [[(1,1)],[(2,5)],[(5,2)],[(2,7),(4,4),(8,2)],[(1,5),(5,1)]]:
    V=newton_vertices(supp)
    print('V =',V,'; E =',exceptional_description(V))
