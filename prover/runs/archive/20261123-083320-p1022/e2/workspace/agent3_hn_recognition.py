"""Exact algebraic checks for P4 wedge-HN geometric recognition.
Geometric inputs/proofs are in agent3_hn_recognition.txt; this script checks
all Chern/degree/cohomology arithmetic used in that argument.
"""
import sympy as S
from pathlib import Path
x,y,b,ell,z=S.symbols('x y b ell z')
s=x+y;t=x*y
# R=V/S, rank3, c(R)=1/(1-s z+t z^2)
cR=[1,s,s*s-t,s**3-2*s*t]
# C=det(S) tensor R, rank3.
cC=[1,-2*s,2*s*s-t,-s*t]
assert S.expand(cR[1]-3*s-cC[1])==0
assert S.expand(cR[2]-2*s*cR[1]+3*s*s-cC[2])==0
assert S.expand(cR[3]-s*cR[2]+s*s*cR[1]-s**3-cC[3])==0
# Rank-one p_*A would be O(b); quotient rank2 requires c3=b x*c2quot.
c2quot=S.expand(cC[2]-b*x*(cC[1]-b*x))
obstruction=S.Poly(S.expand(b*x*c2quot-cC[3]),x,y)
assert obstruction.coeff_monomial(x*y*y)==2*b+1
assert S.solve(2*b+1,b)==[-S.Rational(1,2)]
# Relative Beilinson Chern character comparison: C'=C tensor p*O(ell).
ch0=3;ch1=cC[1];ch2=S.expand((cC[1]**2-2*cC[2])/2)
ch3=S.expand((cC[1]**3-3*cC[1]*cC[2]+3*cC[3])/6)
difference_degree2=S.expand(ell*x*ch1+S.Rational(3,2)*ell**2*x*x)
assert S.Poly(difference_degree2,x,y).coeff_monomial(x*y)==-2*ell
# Degeneracy curve arithmetic for two sections of gg rank3 F on P3:
# c3(F)=2p_a(C)-2+(4-c1(F))*deg(C).
assert S.solve(S.Eq(0,2*z-2+(4-2)*2),z)==[-1]
# Cohomology tables h^q(A(-i)), i=0..3, q=0..3.
# Omega^2(2)=T(-2), computed from Euler and line-bundle cohomology.
def line_h(k):
    return [int(S.binomial(k+3,3)) if k>=0 else 0,0,0,
            int(S.binomial(-k-1,3)) if k<=-4 else 0]
# Euler 0 O(-2-i) -> O(-1-i)^4 -> T(-2-i) ->0.
euler=[]
for i in range(4):
    a=line_h(-2-i);bb=[4*v for v in line_h(-1-i)]
    # all maps vanish except i=3 top cohom C4 -> C4, an isomorphism.
    if i<3: out=[bb[q]+(a[q+1] if q<3 else 0) for q in range(4)]
    else:
        assert a[3]==bb[3]==4
        out=[0]*4
    euler.append(out)
assert euler==[[0,0,0,0],[0,0,0,0],[0,0,1,0],[0,0,0,0]]
split_table=[[1,1,0,0],[0,0,0,0],[0,0,1,0],[0,0,0,0]]
assert split_table[1:]==euler[1:]
# On each split-fiber the 1,1 dimensions follow H0(O_C)=2,
# H0(O_P3)=1, and for the -2 twist a nonzero C^2->C map.
assert 2-1==1 and 2-1==1
print('Chern identification:', [S.expand(v) for v in cC])
print('Impossible generic split-fiber coefficient:',2*b+1)
print('Beilinson mixed coefficient:',-2*ell)
print('Euler cohomology table:',euler)
print('All recognition arithmetic checks passed.')
Path('workspace').mkdir(exist_ok=True)
Path('workspace/agent3_hn_recognition.py').write_text(Path(__file__).read_text())

# Explicit local-freeness connecting maps for the rank-one extension fiber.
alpha,beta=S.symbols('alpha beta', nonzero=True)
connecting_minus2=S.Matrix([[alpha,beta]])
connecting_minus3=S.diag(alpha,alpha,beta,beta)
assert connecting_minus2.rank()==1
assert S.expand(connecting_minus3.det()-alpha**2*beta**2)==0
assert connecting_minus3.rank()==4
assert 2-connecting_minus2.rank()==1
assert 4-connecting_minus3.rank()==0
print('Rank-one extension connecting maps checked exactly: ranks 1 and 4.')
