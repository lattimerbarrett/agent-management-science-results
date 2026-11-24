import sympy as s

# Normal coordinates for a strictly pseudoconvex boundary point.
# The tangential Levi entry is lam>0, the complex-normal derivative a>0.
lam, a = s.symbols('lam a', positive=True)
x, y, c = s.symbols('x y c', real=True)
A = ((x*x+y*y)/lam + s.sqrt(c*c+1) + 1)/(2*a*a)
H = s.Matrix([[lam, x+s.I*y], [x-s.I*y, c+2*A*a*a]])
det = s.simplify(H.det())
expected = lam*(c+s.sqrt(c*c+1)+1)
assert s.simplify(det-expected) == 0
# sqrt(c^2+1)>|c|, hence both principal minors are positive.
assert s.expand((c*c+1)-c*c) == 1
print('First principal minor:', H[0,0])
print('Second principal minor:', det)
print('The identity (c^2+1)-c^2=1 certifies sqrt(c^2+1)>|c|.')

# Taylor/Levi identity for adding A*r^2, at a boundary point r=0.
z, zb, w, wb, AA = s.symbols('z zb w wb AA')
r = a*(w+wb)+lam*z*zb+(x+s.I*y)*z*wb+(x-s.I*y)*w*zb+c*w*wb
rnew = r+AA*r*r
coords, bars = [z,w], [zb,wb]
Hnew = s.Matrix(2,2,lambda j,k:s.diff(rnew,coords[j],bars[k]).subs({z:0,zb:0,w:0,wb:0}))
Hexpected = s.Matrix([[lam,x+s.I*y],[x-s.I*y,c+2*AA*a*a]])
assert s.simplify(Hnew-Hexpected) == s.zeros(2)
print('Verified the Hessian identity for r + A*r^2.')
