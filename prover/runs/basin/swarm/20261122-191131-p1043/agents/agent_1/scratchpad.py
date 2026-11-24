from fractions import Fraction as Q
from functools import lru_cache
import sympy as s

I = s.eye(4)
def O(b):
    a,b,c,d = b
    return s.Matrix([[a,-b,-c,-d],[b,a,-d,c],
                     [c,d,a,-b],[d,-c,b,a]])
Os = [O(b) for b in [(1,0,0,0),(0,1,0,0),
                     (0,0,1,0),(0,0,0,-1)]]
P = s.Matrix.vstack(*[I.row_join(B) for B in Os])/2
D = s.diag(*[s.Rational(1,i) for i in range(1,5) for _ in range(4)])
S = P.T*P
B = sum(Os, s.zeros(4))/4
assert S == I.row_join(B).col_join(B.T.row_join(I))
assert B*B.T == I/4
assert S.inv() == s.Rational(4,3)*I.row_join(-B).col_join((-B.T).row_join(I))
for j in (0,4):
    e = s.eye(8)[:,j]
    f = P*S.inv()*e
    assert P.T*f == e and (f.T*f)[0] == s.Rational(4,3)

# Polynomial verification of the quaternion identities used in the proof.
w = s.Matrix(4,4,lambda r,c:s.Symbol('w%d%d'%(r,c)))
Bs = [sum((w[r,i]*Os[i] for i in range(4)),s.zeros(4)) for r in range(4)]
assert s.expand((Bs[0]*Bs[1].T-Bs[0].T*Bs[1])[0,0]) == 0
delta = (Bs[0].T*Bs[1]*Bs[2].T*Bs[3] -
         Bs[0]*Bs[1].T*Bs[2]*Bs[3].T)[0,0]
assert s.expand(delta+2*w.det()) == 0

@lru_cache(None)
def K(q):
    x,y = q
    if x == 0:
        return [[Q(0)]*8 for _ in range(8)]
    ww = [Q(i*x*x,4*(i*x*x+y*y)) for i in range(1,5)]
    a = sum(ww)
    b = [[sum(ww[i]*int(Os[i][j,k]) for i in range(4))
          for k in range(4)] for j in range(4)]
    return [[(a if j==k else Q(0)) if j//4 == k//4 else
             (b[j][k-4] if j<4 else b[k][j-4])
             for k in range(8)] for j in range(8)]

# Independently verify the Fourier multiplier against the original P,D.
for q in [(0,0),(0,1),(1,0),(1,1),(1,2),(1,3),(-2,3)]:
    x,y=q
    expected = x*x*P.T*(x*x*s.eye(16)+y*y*D).inv()*P if q!=(0,0) else s.zeros(8)
    assert s.Matrix(K(q)) == expected

T = {(0,0):Q(1,2)}
for q in [(1,0),(0,1),(1,3)]:
    T[q] = T[(-q[0],-q[1])] = Q(1,12)

def propagate(U):
    V = {}
    for q,u in U.items():
        for r,t in T.items():
            z = (q[0]+r[0],q[1]+r[1])
            if z[0]==0:
                continue
            v = V.setdefault(z,[Q(0)]*8)
            for j in range(8):
                v[j] += t*u[j]
    return {q:[sum(a*b for a,b in zip(row,u)) for row in K(q)]
            for q,u in V.items()}

U = [{(0,0):[Q(j==i) for j in range(8)]} for i in (0,4)]
diffs = []
for n in range(2,6):
    U = [propagate(u) for u in U]
    coeff = [-sum(t*u.get((-q[0],-q[1]),[0]*8)[i]
                  for q,t in T.items()) for i,u in zip((0,4),U)]
    diffs.append(coeff[1]-coeff[0])
assert diffs == [0,0,0,Q(1,531372441600)]
print('Coefficients at orders 2,3,4,5:', diffs)

W = s.Matrix([[s.Rational(i,4*(i+r*r)) for i in range(1,5)]
              for r in (3,2,1,0)])
assert W.det() == s.Rational(3,51251200)
c = 8*W.det()/12**5
assert c == s.Rational(1,531372441600)
print('det(W) =', W.det())
print('(p,c) =', (5,c))
