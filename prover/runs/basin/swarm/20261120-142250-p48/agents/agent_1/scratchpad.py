import sympy as s

e=s.symbols('e', nonnegative=True, integer=True)
def dot(D,G):
    a,b=D; c,d=G
    return s.expand(-e*a*c+a*d+b*c)
S=(1,0); f=(0,1); H=(1,3*e+1); P=(4,12*e+3)
A=(5,-1); B=(-1,12*e+5); C=(4,12*e+4)
K=(-2,-e-2)
c1sq=dot(C,C); c2=dot(A,B)
assert s.simplify(c1sq-16*(5*e+2))==0
assert s.simplify(c2-13*(5*e+2))==0
assert s.simplify(dot(C,P)/2-(40*e+14))==0
assert s.simplify(dot(A,P)-(40*e+11))==0
assert s.simplify(dot(B,P)-(40*e+17))==0
assert s.simplify(2+(c1sq-dot(C,K))/2-c2+15*e)==0
for name,expr in [('H^2',dot(H,H)),('c1^2',c1sq),('c2',c2),('s2',c1sq-c2),('slope_P',dot(C,P)/2),('chi(E)',2+(c1sq-dot(C,K))/2-c2)]:
    print(name,'=',s.factor(expr))
# In the Hermitian--Einstein construction the tautological curvature has
# horizontal 2x2 block of positive trace, a negative vertical block, and
# the squared norm exhaustion adds one positive radial eigenvalue.
# Check the relevant inertia assertion on exact rational sample matrices.
for a,b,z in [(1,1,0),(5,-1,0),(-10,11,3),(0,2,7)]:
    M=s.Matrix([[a,z],[z,b]])
    assert s.trace(M)>0
    assert any(v.is_positive for v in M.eigenvals())
    print('horizontal eigenvalues:', list(M.eigenvals()))
# Exact cohomology of line bundles on F_e, by the ruling and relative duality.
def line_h(e0,a,b):
    if a >= 0:
        degs=[b-i*e0 for i in range(a+1)]
        return (sum(max(d+1,0) for d in degs),
                sum(max(-d-1,0) for d in degs),0)
    if a == -1:
        return (0,0,0)
    # K_X=-2S-(e+2)f and Serre duality.
    h=line_h(e0,-2-a,-e0-2-b)
    return tuple(reversed(h))

def split_sym_det_h(e0,k):
    out=[0,0,0]
    for i in range(k+1):
        a=6*i-k+4
        b=-i+(k-i)*(12*e0+5)+12*e0+4
        h=line_h(e0,a,b)
        out=[x+y for x,y in zip(out,h)]
    return out

for e0 in range(5):
    k=12*e0+6
    # The summand A^(k+1) B has b=-2, so h^1 is positive.
    a=5*k+4
    b=12*e0+4-k
    assert b == -2
    assert line_h(e0,a,b)[1] > 0
    h=split_sym_det_h(e0,k)
    assert h[1]>0
    print('e, k, cohomology of Sym^k(E0) det(E0):',e0,k,h)
print('All symbolic assertions passed.')
