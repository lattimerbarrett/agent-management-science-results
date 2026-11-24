from pathlib import Path
import math
import sympy as sp

# Exact Walsh transform: quadrant masses -> constant and 3 sign correlations.
W=sp.Matrix([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]])
assert W*W.T == 4*sp.eye(4)
assert W.inv()*sp.Matrix([1,0,0,0]) == sp.ones(4,1)/4
# Flipping either hyperplane acts by the three nontrivial sign characters.
flip1=sp.zeros(4); flip2=sp.zeros(4)
for col,(a,b) in enumerate([(1,1),(1,-1),(-1,1),(-1,-1)]):
    signs=[(1,1),(1,-1),(-1,1),(-1,-1)]
    flip1[signs.index((-a,b)),col]=1
    flip2[signs.index((a,-b)),col]=1
assert W*flip1*W.inv()==sp.diag(1,-1,1,-1)
assert W*flip2*W.inv()==sp.diag(1,1,-1,-1)

# Symbolic degree/truncation arithmetic valid for every n>=3.
n=sp.symbols('n', integer=True, positive=True)
j=2*n; d=3*n+1; a=3*n-1; b=3*n+1
assert sp.expand(a+b-3*j)==0
assert sp.expand(a-j-(n-1))==0
assert sp.expand(b-j-(n+1))==0
assert sp.expand(d-a)==2 and sp.expand(d-b)==0

# Exact GF(2) polynomials as sets of exponents. XOR multiplication by 1+t^e.
def multiply_binomial_mod2(support,e):
    return support.symmetric_difference({u+e for u in support})

def check_s(s):
    j=(1<<s)-2; n=j//2; d=3*n+1
    # Frobenius factorization: (1+t)^j = product_{k=1}^{s-1}(1+t^(2^k)).
    support={0}
    for k in range(1,s):
        support=multiply_binomial_mod2(support,1<<k)
    # Verify full coefficient support independently by Lucas digit test.
    assert support == {i for i in range(j+1) if i & ~j == 0}
    target=n-1
    assert target==sum(1<<k for k in range(1,s-1))
    assert target in support
    # Two separate direct checks for moderate sizes only.
    if s<=10:
        assert {i for i in range(j+1) if math.comb(j,i)%2}==support
    a=j+target; b=2*j-target
    assert (a,b)==(3*n-1,3*n+1)
    assert a<=d and b<=d and a+b==3*j
    survivors=[(j+i,2*j-i) for i in support if j+i<=d and 2*j-i<=d]
    assert (a,b) in survivors
    return s,j,d,len(support),survivors

rows=[check_s(s) for s in range(3,17)]
for row in rows:
    print(row)
print('Exact Walsh, symbolic exponent, and GF(2) polynomial checks passed.')
Path('workspace').mkdir(exist_ok=True)
Path('workspace/agent3_upper_checks.py').write_text(Path(__file__).read_text())
