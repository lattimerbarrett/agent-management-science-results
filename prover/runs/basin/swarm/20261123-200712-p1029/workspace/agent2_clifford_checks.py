import sympy as s
from pathlib import Path
I2=s.eye(2)
X=s.Matrix([[0,1],[1,0]])
Y=s.Matrix([[0,-s.I],[s.I,0]])
Z=s.diag(1,-1)
def tensor_list(xs):
    out=s.Matrix([[1]])
    for x in xs:out=s.kronecker_product(out,x)
    return out
count=0
for r in range(1,5):
    gs=[]
    for k in range(r):
        gs.append(tensor_list([Z]*k+[X]+[I2]*(r-k-1)))
        gs.append(tensor_list([Z]*k+[Y]+[I2]*(r-k-1)))
    gs.append(tensor_list([Z]*r))
    I=s.eye(2**r)
    for i,g in enumerate(gs):
        assert g*g==I and g.H==g
        p=(I+g)/2
        assert p*p==p and s.trace(p)==2**(r-1)
        for h in gs[:i]:
            assert g*h+h*g==s.zeros(2**r)
            q=(I+h)/2
            assert (p+q-I)**2==I/2
            count+=1
assert 1+1/s.sqrt(2)<s.Rational(9,5)
print('Verified',count,'exact Clifford projection-pair identities; pair sum norm = 1+1/sqrt(2)<1.8.')
