from fractions import Fraction
from itertools import combinations
from math import comb
import json, pathlib

def weyl_dimension(a):
    n = len(a) + 1
    d = Fraction(1)
    for i in range(n):
        for j in range(i+1,n):
            d *= Fraction(j-i + sum(a[i:j]),j-i)
    assert d.denominator == 1
    return int(d)

def low_irreducibles(n):
    # Weyl dimensions increase in each Dynkin coordinate. Once 2*omega_i
    # and omega_i+omega_j exceed cutoff, every weight of total height>=2
    # is excluded. In n=2, height 2 itself is included and height 3 excluded.
    e = [tuple(int(i==j) for i in range(n-1)) for j in range(n-1)]
    low = [((0,)*(n-1),1)]
    for a in e:
        d = weyl_dimension(a)
        assert d == comb(n,a.index(1)+1)
        if d < 2*n:
            low.append((a,d))
    for i in range(n-1):
        for j in range(i,n-1):
            a=tuple(e[i][k]+e[j][k] for k in range(n-1))
            d=weyl_dimension(a)
            if d<2*n:
                assert n==2 and a==(2,) and d==3
                low.append((a,d))
            else:
                assert d >= 2*n
    if n==2:
        assert weyl_dimension((3,))==4
    return low

results={str(n):low_irreducibles(n) for n in range(2,31)}
for n in range(5,31):
    assert len(results[str(n)])==3
for n in range(3,31):
    for k in range(n-1):
        a=tuple(2*int(j==k) for j in range(n-1))
        assert weyl_dimension(a)>=n*(n+1)//2
    for i,j in combinations(range(n-1),2):
        a=tuple(int(k==i)+int(k==j) for k in range(n-1))
        assert weyl_dimension(a)>=n*n-1
pathlib.Path('workspace/agent4_levi_checks.py').write_text(pathlib.Path(__file__).read_text())
p=pathlib.Path('workspace/agent4_levi_checks.json')
p.write_text(json.dumps(results,indent=2))
print('Verified exact rational Weyl dimensions and cutoff classification for 2<=n<=30.')
print('n=2:',results['2'])
print('n=3:',results['3'])
print('n=4:',results['4'])
print('n>=5 through 30: trivial, standard, dual only.')
print('Saved',p)

# Exact chain-homotopy check for the Koszul differential. This is the
# mechanism proving the exterior-Q H^1 vanishing used in gap splitting.
from collections import defaultdict

def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for first in range(total+1):
            for rest in compositions(total-first,length-1):
                yield (first,)+rest

def diff(basis):
    I, alpha = basis
    out = defaultdict(int)
    for s,i in enumerate(I):
        beta=list(alpha); beta[i]+=1
        out[(I[:s]+I[s+1:],tuple(beta))]+=(-1)**s
    return dict(out)

def homotopy(basis):
    I, alpha=basis
    out=defaultdict(int)
    for i,a in enumerate(alpha):
        if a and i not in I:
            sign=(-1)**sum(j<i for j in I)
            beta=list(alpha); beta[i]-=1
            out[(tuple(sorted(I+(i,))),tuple(beta))]+=sign*a
    return dict(out)

def compose(f,g,basis):
    out=defaultdict(int)
    for v,a in g(basis).items():
        for w,b in f(v).items(): out[w]+=a*b
    return out

checks=0
for m in range(2,7):
    for exterior_degree in range(m+1):
        for symmetric_degree in range(4):
            for I in combinations(range(m),exterior_degree):
                for alpha in compositions(symmetric_degree,m):
                    basis=(I,alpha)
                    out=compose(diff,homotopy,basis)
                    for w,a in compose(homotopy,diff,basis).items(): out[w]+=a
                    out[basis]-=exterior_degree+symmetric_degree
                    assert all(a==0 for a in out.values())
                    checks+=1
print('Verified d*kappa+kappa*d=(exterior_degree+symmetric_degree)*Id on',checks,'exact Koszul basis vectors.')
import sympy as sp
h,H=sp.symbols('h H')
for rank in range(1,21):
    aa=sp.symbols('a0:'+str(rank)); bb=sp.symbols('b0:'+str(rank))
    ch2=sp.expand(sum((aa[i]*h+bb[i]*H)**2 for i in range(rank))/2)
    assert ch2.coeff(H,2)==sum(b*b for b in bb)/2
print('Verified distinct-degree ch2 sum-of-squares coefficient for ranks1..20.')
pathlib.Path('workspace/agent4_levi_and_gap_checks.py').write_text(pathlib.Path(__file__).read_text())
