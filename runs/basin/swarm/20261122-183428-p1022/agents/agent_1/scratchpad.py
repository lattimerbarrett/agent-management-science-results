import sympy as s
from itertools import combinations
N=6
pairs=list(combinations(range(N),2))
W=s.zeros(N)
for i in range(0,N,2): W[i,i+1]=1; W[i+1,i]=-1
assert W.rank()==6
# Quotient by a representative non-isotropic or isotropic two-plane.
for U, expected in [([0,1],4),([0,2],2)]:
    rest=[i for i in range(N) if i not in U]
    assert W.extract(rest,rest).rank()==expected
# Universal factorization for a bivector supported in U wedge V.
u,v,a,b=[s.Matrix(s.symbols(f'{name}0:6')) for name in ['u','v','a','b']]
M=s.Matrix.hstack(u,v,a,b)
J=s.zeros(4); J[0,2]=J[1,3]=1; J[2,0]=J[3,1]=-1
assert M*J*M.T == u*a.T-a*u.T+v*b.T-b*v.T
# Such a matrix has rank at most 4, unlike W.
# Check the scalar-endomorphism argument: diagonal eigenvalues of wedge^2 V
# are identified by all (e_i+e_k) wedge e_j.
rows=[]
for i,j,k in __import__('itertools').permutations(range(N),3):
    row=[0]*len(pairs)
    row[pairs.index(tuple(sorted((i,j))))]=1
    row[pairs.index(tuple(sorted((k,j))))]-=1
    rows.append(row)
assert s.Matrix(rows).rank()==14
# Global sections in the exterior Euler complex.
monomials=list(combinations(range(N),2)) + [(i,i) for i in range(N)]
monomials=sorted(monomials)
mult=s.zeros(len(monomials),N*N)
alt=s.zeros(N*N,len(pairs))
for i in range(N):
    for j in range(N): mult[monomials.index(tuple(sorted((i,j)))),N*i+j]=1
for col,(i,j) in enumerate(pairs):
    alt[N*i+j,col]=1; alt[N*j+i,col]=-1
assert mult.rank()==21 and alt.rank()==15
assert mult*alt==s.zeros(21,15)
assert 36-mult.rank()==alt.rank()
# Explicit projective transformation changes the line of bivectors.
g=s.diag(2,1,1,1,1,1)
Wp=g*W*g.T
assert s.Matrix.hstack(s.Matrix(W).reshape(36,1),Wp.reshape(36,1)).rank()==2
# Exact resolution gives ch(E) = 14 - 6 exp(-h) + exp(-2h).
h=s.symbols('h')
ch=s.series(14-6*s.exp(-h)+s.exp(-2*h),h,0,6).removeO()
logc=sum((-1)**(k-1)*s.factorial(k-1)*ch.coeff(h,k)*h**k for k in range(1,6))
c=s.series(s.exp(logc),h,0,6).removeO().expand()
assert ch.coeff(h,0)==9
assert c.coeff(h,1)==4
print('rank(W) =',W.rank())
print('quotient bivector ranks for the two types of lines: 4, 2')
print('rank of simplicity constraints =',s.Matrix(rows).rank())
print('Euler global-section ranks =',alt.rank(),mult.rank())
print('Chern character =',ch)
print('Total Chern class through degree 5 =',c)
print('All assertions passed.')