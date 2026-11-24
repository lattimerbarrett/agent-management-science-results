"""Exact rational finite-row graph compatibility checks.
These check algebraic steps of the CONDITIONAL normal-amplification theorem,
not existence of an infinite AW* amplification.
"""
import sympy as s
from itertools import combinations

def psd(A):
    assert A==A.T
    n=A.rows
    # Sylvester criterion for positive semidefiniteness: all principal minors.
    for k in range(1,n+1):
        for ix in combinations(range(n),k):
            assert A.extract(ix,ix).det()>=0

r=2; N=3
X=[s.Matrix([[1,1],[0,1]])/6,
   s.Matrix([[1,0],[1,-1]])/7,
   s.Matrix([[0,1],[-1,1]])/8]
I=s.eye(r)
S=sum((x*x.T for x in X),s.zeros(r))
psd(I-S)
Ps=[]
for n in range(1,N+1):
    T=s.Matrix.hstack(*X[:n])
    V=s.Matrix.vstack(s.eye(n*r),s.zeros((N-n)*r,n*r),T)
    P=V*(V.T*V).inv()*V.T
    assert P*P==P and P.T==P
    E=s.diag(*([1]*(n*r)+[0]*((N-n)*r)))
    psd(P[:N*r,:N*r]-E/2)
    D=s.diag(*([s.Integer(2)]*(N*r)+[s.Rational(2,3)]*r))
    psd(D-P)
    Ps.append(P)
for n in range(N):
    for m in range(n,N):
        assert Ps[n]*Ps[m]==Ps[n]
P=Ps[-1]
a=P[:N*r,:N*r]; b=P[:N*r,N*r:]
c=P[N*r:,:N*r]; d=P[N*r:,N*r:]
assert d-c*a.inv()*b==s.zeros(r)
assert c*a.inv()==s.Matrix.hstack(*X)
assert (c*a.inv())*(c*a.inv()).T==S
print('Exact PSD, graph nesting, Schur residual, recovery and row-sum checks passed')
