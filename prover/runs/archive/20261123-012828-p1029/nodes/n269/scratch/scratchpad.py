import itertools
import sympy as s
# Exact noncommuting positive contractions with sum <= I.
v=[s.Matrix([1,0]),s.Matrix([1,1]),s.Matrix([1,2])]
b=[(x*x.T)/s.Integer(12) for x in v]
I=s.eye(2); S=sum(b,s.zeros(2))
def psd2(A):
    return A==A.T and A[0,0]>=0 and A[1,1]>=0 and A.det()>=0
assert psd2(I-S)
ave=s.zeros(2)
for eps in itertools.product((-1,1),repeat=len(b)):
    T=sum((e*x for e,x in zip(eps,b)),s.zeros(2))
    assert psd2(I-T) and psd2(I+T)
    ave+=T*T/s.Integer(2**len(b))
assert ave==sum((x*x for x in b),s.zeros(2))
# Scalar trace checks only: not a proof for nonlinear quasitraces.
tr=lambda A:s.trace(A)/2
print('All signed sums are contractions: verified exactly.')
print('Rademacher square identity: verified exactly.')
print('sum tau(b_i)^2 =',sum(tr(x)**2 for x in b))
print('sum tau(b_i^2) =',sum(tr(x*x) for x in b))
print('tau((sum b_i)^2) =',tr(S*S))
print('These last scalar sums use a trace and do not establish quasitracial finite cotype.')
