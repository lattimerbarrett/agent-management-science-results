import itertools
import sympy as S

K = [S.Matrix(a) for a in [
 [[12,6,-15,4],[6,-15,-6,-11],[-15,-6,3,3],[4,-11,3,0]],
 [[-3,5,7,5],[5,-13,5,3],[7,5,7,3],[5,3,3,9]],
 [[-15,10,3,-4],[10,14,-8,2],[3,-8,1,-3],[-4,2,-3,0]],
 [[6,-2,-5,7],[-2,-4,0,-9],[-5,0,9,-5],[7,-9,-5,-11]]]]
assert all(A == A.T and S.trace(A) == 0 for A in K)
assert S.Matrix.hstack(*(A.reshape(16,1) for A in K)).rank() == 4
x,y,z = S.symbols('x y z')
triples = list(itertools.combinations(range(4),3))
def minors(c):
    M = sum((a*A for a,A in zip(c,K)), S.zeros(4))
    return [M.extract(I,J).det() for I in triples for J in triples]
G = S.groebner(minors([x,y,z,1]),x,y,z)
p = S.Poly(G.polys[-1].as_expr(),z)
assert not (p.as_expr().free_symbols - {z})
assert p.degree() == 10
seq = [S.Poly(f,z) for f in S.sturm(p.as_expr(),z)]
def signs_at_infinity(negative):
    return [int(S.sign(q.LC())) * (-1 if negative and q.degree()%2 else 1) for q in seq]
def variations(a):
    return sum(u != v for u,v in zip(a,a[1:]))
a,b = signs_at_infinity(True),signs_at_infinity(False)
assert variations(a) == variations(b) == 5
assert p.count_roots(-S.oo,S.oo) == 0
print('Sturm signs at -infinity:',a)
print('Sturm signs at +infinity:',b)
for c,gens in [([x,y,1,0],(x,y)),([x,1,0,0],(x,)),([1,0,0,0],(x,))]:
    assert list(S.groebner(minors(c),*gens)) == [1]
print('All three patches at infinity have ideal (1).')

# Compute six positive definite forms spanning K-perp.
E=[]
for i in range(4):
    for j in range(i,4):
        M=S.zeros(4);M[i,j]=M[j,i]=1;E.append(M)
C=S.Matrix([[S.trace(A*B) for B in E] for A in K])
assert C.rank()==4
forms=[S.eye(4)]
for v in C.nullspace():
    A=sum((v[i]*E[i] for i in range(10)),S.zeros(4))
    if S.Matrix.hstack(*(B.reshape(16,1) for B in forms+[A])).rank()>len(forms):
        forms.append(A)
assert len(forms)==6
spd=[forms[0]]
for A in forms[1:]:
    c=1+max([S.Integer(0)]+[sum(abs(A[i,j]) for j in range(4) if j!=i)-A[i,i] for i in range(4)])
    spd.append(A+c*S.eye(4))
assert all(A[i,i]>sum(abs(A[i,j]) for j in range(4) if j!=i) for A in spd for i in range(4))
assert all(S.trace(A*B)==0 for A in spd for B in K)
assert S.Matrix.hstack(*(A.reshape(16,1) for A in spd)).rank()==6
print('Six independent positive definite forms constructed and verified.')

def upper_certificate(s):
    assert s>=3
    j=(1<<s)-2
    m=j//2
    d=3*m+1
    k=m-1
    assert k & ~j == 0 # Lucas: binomial(j,k) is odd
    assert (j+k,2*j-k)==(d-2,d)
    return d
for s in range(3,11):
    print('s =',s,'D_s =',upper_certificate(s))
# Exact parity checks independent of the bit formula, at manageable sizes.
for s in range(3,10):
    j=(1<<s)-2;m=j//2
    assert S.binomial(j,m-1)%2==1
