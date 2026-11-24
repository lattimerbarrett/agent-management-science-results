"""Exact rational cohomology/Lefschetz checks for S^2 x S^2."""
import sympy as s

# Basis 1,a,b,ab, with a^2=b^2=0 and integral(ab)=1.
basis = ((0,0),(1,0),(0,1),(1,1))
def multiply(u,v):
    out = [s.Integer(0)]*4
    for i, ci in enumerate(u):
        for j, cj in enumerate(v):
            e=tuple(basis[i][k]+basis[j][k] for k in (0,1))
            if max(e)<=1:
                out[basis.index(e)] += ci*cj
    return s.Matrix(out)
E=[s.eye(4)[:,i] for i in range(4)]
one,a,b,ab=E
assert multiply(a,a)==s.zeros(4,1)
assert multiply(b,b)==s.zeros(4,1)
assert multiply(a,b)==ab

# Poincare pairing: all degrees even, so no minus signs.
P=s.Matrix(4,4,lambda i,j:multiply(E[i],E[j])[3])
assert P==s.Matrix([[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]])
assert P*P==s.eye(4)
# The inverse pairing represents the diagonal's Poincare-dual class.
# Pull it back to the graph of a map isotopic to identity.
diagonal_pullback=s.zeros(4,1)
for i in range(4):
    for j in range(4):
        diagonal_pullback+=P.inv()[i,j]*multiply(E[i],E[j])
assert diagonal_pullback==4*ab
# Independent homological Lefschetz computation: b0=b4=1,b2=2.
betti={0:1,1:0,2:2,3:0,4:1}
lefschetz=sum((-1)**k*betti[k] for k in betti)
assert lefschetz==diagonal_pullback[3]==4
print('Verified ring, Poincare duality, diagonal pullback, Lefschetz number:',lefschetz)
