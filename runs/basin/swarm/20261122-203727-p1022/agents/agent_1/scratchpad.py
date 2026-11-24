import itertools
import sympy as s
from math import comb

N=6
pairs=list(itertools.combinations(range(N),2))
D=len(pairs)
idx={p:i for i,p in enumerate(pairs)}

def wedge(a,b):
    return s.Matrix([a[i]*b[j]-a[j]*b[i] for i,j in pairs])

# A nondegenerate bivector and a projective transformation moving its line.
J=s.zeros(N)
for i in range(0,N,2):
    J[i,i+1]=1; J[i+1,i]=-1
G=s.diag(2,1,1,1,1,1)
J2=G*J*G.T
v=s.Matrix([J[i,j] for i,j in pairs])
v2=s.Matrix([J2[i,j] for i,j in pairs])
assert J.det()==1 and J.rank()==6
assert s.Matrix.hstack(v,v2).rank()==2
print('bivector rank:',J.rank(),'; distinct parameter lines: verified')

# Universal skew matrices belonging to W wedge V have rank <= 2 dim(W).
# For dim W=2, all 5-minors vanish identically (not just at samples).
a=s.symbols('a')
bs=s.symbols('b:8')
B=s.Matrix(2,4,bs)
M=s.BlockMatrix([[s.Matrix([[0,a],[-a,0]]), B],[-B.T,s.zeros(4)]]).as_explicit()
five=list(itertools.combinations(range(6),5))
assert all(s.expand(M.extract(I,K).det())==0 for I in five for K in five)
assert M.rank()==4
print('universal rank bound for W wedge V: all 36 five-minors are zero')

# Global sections of the dual exterior Euler complex.
# Lambda^2 V* -> V* tensor V* -> Sym^2 V*.
sympairs=list(itertools.combinations_with_replacement(range(N),2))
si={p:i for i,p in enumerate(sympairs)}
A=s.zeros(N*N,D)
for col,(i,j) in enumerate(pairs):
    A[i*N+j,col]=1; A[j*N+i,col]=-1
S=s.zeros(len(sympairs),N*N)
for i in range(N):
    for j in range(N):
        S[si[tuple(sorted((i,j)))],i*N+j]=1
assert S*A==s.zeros(len(sympairs),D)
assert A.rank()==D and S.rank()==len(sympairs)
assert D+len(sympairs)==N*N
print('dual Euler global-section complex dimensions/ranks:',(D,N*N,len(sympairs)),(A.rank(),S.rank()))

# Cech line-bundle cohomology dimensions on P^5 used for H^0(Lambda^2 Q).
def h_line(n,t,q):
    if q==0 and t>=0: return comb(n+t,n)
    if q==n and t<=-n-1: return comb(-t-1,n)
    return 0
for t in [-1,-2]:
    assert all(h_line(5,t,q)==0 for q in range(6))
print('O(-1), O(-2) on P^5: acyclic by the line-bundle formula')

# Check the finite linear-algebra test implying End(Lambda^2 Q)=C.
# Preservation of e_i wedge V forces every off-diagonal entry to vanish.
allowed=[]
for row,p in enumerate(pairs):
    for col,q in enumerate(pairs):
        if all(i in p for i in q): allowed.append((row,col))
assert allowed==[(i,i) for i in range(D)]
# Preservation of (e_i+e_j) wedge V forces adjacent eigenvalues equal.
relations=[]
for i,j in pairs:
    for k in range(N):
        if k in (i,j): continue
        row=[0]*D
        row[idx[tuple(sorted((i,k)))]]=1
        row[idx[tuple(sorted((j,k)))]]=-1
        relations.append(row)
R=s.Matrix(relations)
assert R.rank()==D-1
assert R.nullspace()==[s.ones(D,1)]
print('endomorphism test: off-diagonal entries vanish; diagonal relation rank:',R.rank())

# Splitting and rank arithmetic.
n=5
f_rank=comb(n,2)
pos=n-1
zero=comb(n-1,2)-1
e_rank=pos+zero
assert (f_rank,e_rank,pos,zero)==(10,9,4,5)
assert e_rank<2*n
print('E rank and splitting multiplicities:',e_rank,(pos,zero),'; rank < 2n:',e_rank<2*n)

# Weyl-dimension check of the irreducible homogeneous building blocks
# in the small-rank classification table (not a proof of that theorem).
def weyl_dim(lam):
    ans=s.Integer(1)
    for i in range(len(lam)):
        for j in range(i+1,len(lam)):
            ans*=s.Rational(lam[i]-lam[j]+j-i,j-i)
    return int(ans)
expected={2:{(0,0),(1,0),(2,0)},
          3:{(0,0,0),(1,0,0),(1,1,0)},
          4:{(0,0,0,0),(1,0,0,0),(1,1,0,0),(1,1,1,0)}}
for n in (2,3,4):
    bound=2*n-1
    found={lam for tail in itertools.product(range(bound),repeat=n-1)
           if all(tail[i]>=tail[i+1] for i in range(n-2))
           for lam in [tail+(0,)] if weyl_dim(lam)<=bound}
    assert found==expected[n]
    print('GL(%d) normalized highest weights of dimension <= %d:'%(n,bound),
          sorted((lam,weyl_dim(lam)) for lam in found))

# Describe, rather than pretend to verify, the external classification input.
print('Classification of arbitrary uniform bundles in dimensions 2,3,4 is an external theorem, not a finite computation.')
