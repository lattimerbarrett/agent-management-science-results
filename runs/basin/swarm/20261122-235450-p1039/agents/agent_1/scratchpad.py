import sympy as sp

# Exact Wirtinger-Hessian checks for a spherical shell in C^n.
# Coordinates are ordered x_1,...,x_n,y_1,...,y_n.
def levi(rho, xs, ys):
    n = len(xs)
    return sp.Matrix(n, n, lambda j,k: sp.simplify((
        sp.diff(rho,xs[j],xs[k]) + sp.diff(rho,ys[j],ys[k])
        + sp.I*sp.diff(rho,xs[j],ys[k])
        - sp.I*sp.diff(rho,ys[j],xs[k]))/4))

for n in range(2,9):
    xs = sp.symbols('x:'+str(n), real=True)
    ys = sp.symbols('y:'+str(n), real=True)
    r2 = sum(x*x+y*y for x,y in zip(xs,ys))
    outer = r2-4
    inner = 1-r2
    assert levi(outer,xs,ys) == sp.eye(n)
    assert levi(inner,xs,ys) == -sp.eye(n)
    # q=(1,0,...,0), v=(0,1,0,...,0) on the inner sphere.
    q = dict(zip(xs,(1,)+(0,)*(n-1)))
    q.update(dict(zip(ys,(0,)*n)))
    dz = sp.Matrix([ (sp.diff(inner,x)-sp.I*sp.diff(inner,y))/2
                     for x,y in zip(xs,ys)])
    v = sp.eye(n)[:,1]
    assert (dz.T*v)[0].subs(q) == 0
    assert (v.T*levi(inner,xs,ys)*v)[0] == -1
print('Exact symbolic checks passed for shell Levi forms in dimensions 2 through 8.')

# Normal-direction correction of a defining function in complex dimension 2.
# In normalized coordinates, dr/dz=(0,1), and a>0 is the tangential Levi entry.
a = sp.symbols('a', positive=True)
bre, bim, c = sp.symbols('bre bim c', real=True)
b = bre + sp.I*bim
H = sp.Matrix([[a,b],[sp.conjugate(b),c]])
A = ((bre**2+bim**2)/a-c+1)/2
H_corrected = H + sp.diag(0,2*A)
assert sp.simplify(H_corrected.det()-a) == 0
assert H_corrected[0,0] == a
# Sylvester's criterion: the two leading principal minors are a>0 and a>0.
print('The normal correction has exactly positive principal minors a and a.')

# Check the defining-function Hessian identity directly, not just matrix algebra.
x1,x2,y1,y2 = sp.symbols('x1 x2 y1 y2', real=True)
z1,z2 = x1+sp.I*y1, x2+sp.I*y2
rho = (2*x2 + a*sp.conjugate(z1)*z1
       + b*z1*sp.conjugate(z2) + sp.conjugate(b)*z2*sp.conjugate(z1)
       + c*z2*sp.conjugate(z2))
origin = dict.fromkeys((x1,x2,y1,y2),0)
L = levi(rho + A*rho**2,(x1,x2),(y1,y2)).subs(origin)
assert (L-H_corrected).applyfunc(sp.simplify) == sp.zeros(2)
print('Direct Wirtinger differentiation verifies the normal-correction identity.')
