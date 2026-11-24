"""Exact independent certificates for the complete upper/lower argument."""
from math import factorial, comb
from itertools import combinations
from fractions import Fraction

def mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return c

def poly(roots):
    p=[1]
    for r in roots:p=mul(p,[r,1])
    return p

def rem(a,p):
    a=list(a)
    while len(a)>=len(p):
        q=a[-1]; shift=len(a)-len(p)
        for i,c in enumerate(p):a[i+shift]-=q*c
        a.pop()
    return a+[0]*(len(p)-1-len(a))

def lower_certificate(k):
    roots=tuple(range(1,2*k-1)); P=poly(roots)
    M=factorial(2*k-1); T=2*M*M+2
    pairs=list(combinations(range(k),2))
    S=[[0]*k for _ in range(k)]
    for e,(i,j) in enumerate(pairs):S[i][j]=T**e;S[j][i]=-T**e
    count=0
    # Every possible complementary factorization, exact integer arithmetic.
    for choice in combinations(roots,k-1):
        U=poly(choice); V=poly([r for r in roots if r not in choice])
        assert mul(U,V)==P and all(x>0 for x in U+V)
        assert max(U+V)<=M
        wedge=[U[i]*V[j]-U[j]*V[i] for i,j in pairs]
        assert any(wedge) and max(map(abs,wedge))<=2*M*M
        h=sum(a*b for a,b in zip(U,V)); a=sum(c*T**e for e,c in enumerate(wedge))
        assert h>0 and a!=0
        count+=1
    # Build every REAL symmetric form in B, using exact integers.
    n=2*k; forms=[]
    remainders=[[rem([0]*(i+j)+[1],P) for j in range(k)] for i in range(k)]
    for ell in range(2*k-2):
        R=[[remainders[i][j][ell] for j in range(k)] for i in range(k)]
        Hr=[[0]*n for _ in range(n)]; Hi=[[0]*n for _ in range(n)]
        for i in range(k):
            for j in range(k):
                Hr[i][j]=R[i][j];Hr[i+k][j+k]=-R[i][j]
                Hi[i][j+k]=Hi[i+k][j]=R[i][j]
        forms.extend([Hr,Hi])
    I=[[int(i==j) for j in range(n)] for i in range(n)]
    Q=[[0]*n for _ in range(n)]
    for i in range(k):
        for j in range(k):Q[i][j+k]=-S[i][j];Q[i+k][j]=S[i][j]
    forms=[I]+forms+[Q]
    assert len(forms)==2*n-2
    assert all(H[i][j]==H[j][i] for H in forms for i in range(n) for j in range(n))
    L=1+max(sum(map(abs,row)) for H in forms for row in H)
    K=[I]+[[[L*int(i==j)+H[i][j] for j in range(n)] for i in range(n)] for H in forms[1:]]
    # Strict diagonal dominance with positive diagonal certifies PD exactly.
    assert all(A[i][i]>sum(abs(A[i][j]) for j in range(n) if j!=i) for A in K for i in range(n))
    print('lower: k=',k,'factorizations=',count,'forms=',len(K),'PD: exact')
    return K

def upper_certificate(s):
    n=2**(s-1);j=2*n-2;d=3*n-2
    # Lucas theorem gives coefficient binom(j,r) mod 2 iff r's bits lie in j.
    terms=[(j+r,2*j-r) for r in range(j+1) if r&~j==0 and j+r<=d and 2*j-r<=d]
    assert terms==[(d-2,d),(d,d-2)]
    # Independent exact binomial coefficients, no Lucas assumption for this test.
    direct=[(j+r,2*j-r) for r in range(j+1) if comb(j,r)%2 and j+r<=d and 2*j-r<=d]
    assert direct==terms
    print('upper: s=',s,'d=',d,'surviving monomials=',terms)

if __name__=='__main__':
    from pathlib import Path
    Path('workspace/agent1_complete_checks.py').write_text(Path(__file__).read_text())
    for s in range(3,11):upper_certificate(s)
    for k in [2,4,8]:lower_certificate(k)
