import sympy as S
from math import prod
T,u,a,b,t,s=S.symbols('T u a b t s')
I=S.eye(2)
def bracket(X,Y): return X*Y-Y*X
def comm(X,Y): return (X*Y*X.inv()*Y.inv()).applyfunc(S.cancel)
def eq(X,Y): return all(S.cancel(x)==0 for x in X-Y)
def x(a):return S.Matrix([[1,a],[0,1]])
def y(b):return S.Matrix([[1,0],[b,1]])
def h(t):return S.diag(t,1/t)
# General derivation proof: Y is fixed, T=ad(Y), all maps Z[T]-linear.
D=S.diag(T,0); A=S.Matrix([[0,0],[T,0]]); B_u=S.Matrix([[0,-u],[0,0]])
assert eq(bracket(D,B_u), B_u.subs(u,T*u))
assert eq(bracket(D,bracket(A,B_u)),S.zeros(2))
# General exact group commutator and opposite-root Gauss factorization.
Dg=S.diag(t,1)
assert eq(comm(Dg,x(b)),x((t-1)*b))
d=1-a*b
assert eq(comm(x(a),y(b)),x(-a*a*b/d)*h(1/d)*y(a*b*b/d))
# Column-convention words in the Alexander representation.
for c in range(3,17):
    k=c-3
    B=x(-s)
    for _ in range(k):B=comm(S.diag(1+s,1),B)
    assert eq(B,x(-s**(k+1)))
    W=comm(S.diag(1+s,1),comm(y(s),B))
    # Each entry starts in degree >=c+1, some starts exactly there.
    vals=[]
    for z in W-I:
        num,den=S.fraction(S.cancel(z))
        assert den.subs(s,0)!=0
        if num!=0: vals.append(min(v[0][0] for v in S.Poly(num,s).terms()))
    assert min(vals)==c+1
    print('c=',c,': exact word and valuation checks passed')
# Check the proposed local fields have the required Eisenstein degrees.
z=S.symbols('z')
for c in range(3,65):
    odd=[p for p in S.factorint(c) if p!=2]
    if odd:
        p=min(odd); q=c//p
        f=S.Poly(sum((1+z**q)**j for j in range(p)),z)
        e=(p-1)*q
    else:
        p=2; q=c//4
        f=S.Poly(z**(2*q)-2*z**q+2,z)
        e=2*q
    assert f.degree()==e
    coeff=f.all_coeffs()
    assert coeff[0]==1 and all(int(v)%p==0 for v in coeff[1:])
    assert int(coeff[-1])%p**2!=0
    assert p*e//(p-1)==c
for p in [3,5,7,11,13,17,19]:
    f=S.cyclotomic_poly(p,z)
    N=int(S.resultant(f,1+(z-1)**(p-1),z))
    assert N%(p*p)==1+p
print('All exact checks passed; no numerical approximations used.')
