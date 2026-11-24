import sympy as s
from pathlib import Path
x1,y1,x2,y2=s.symbols('x1 y1 x2 y2',real=True)
vars=[x1,y1,x2,y2]
rho=(x1*x1+y1*y1-2)**2+x2*x2+y2*y2-s.Rational(1,4)
def dz(f,j):
    return (s.diff(f,vars[2*j])-s.I*s.diff(f,vars[2*j+1]))/2
def dzbar(f,j):
    return (s.diff(f,vars[2*j])+s.I*s.diff(f,vars[2*j+1]))/2
L=s.simplify(s.Matrix(2,2,lambda j,k:dzbar(dz(rho,j),k)))
assert L==s.diag(4*(x1*x1+y1*y1)-4,1)
# Smoothness: complex gradient vanishing forces z2=0 and z1=0 or |z1|²=2.
# rho at those candidate critical loci has values 15/4 and -1/4.
assert rho.subs({x1:0,y1:0,x2:0,y2:0})==s.Rational(15,4)
r=s.symbols('r',real=True)
rho_rad=(r-2)**2-s.Rational(1,4)
assert rho_rad.subs(r,2)==-s.Rational(1,4)
assert s.solve(rho_rad,r)==[s.Rational(3,2),s.Rational(5,2)]
assert (4*r-4).subs(r,s.Rational(3,2))==2
# Boundary outer circle z2=0, |z1|²=5/2 lies in K; disk hull includes origin outside K.
assert rho_rad.subs(r,s.Rational(5,2))==0
print('Exact Levi matrix:',L)
print('Radial interval:',s.solve_univariate_inequality(rho_rad<=0,r))
print('Minimum complex Hessian eigenvalues on K: >=2, 1')
print('Critical rho values:',s.Rational(15,4),-s.Rational(1,4),'(both nonzero)')
print('rho(0)=',rho.subs({x1:0,y1:0,x2:0,y2:0}))
Path('workspace/agent3_nonpoly_check.py').write_text(Path(__file__).read_text().split(chr(10)+'# Analytic-disc certificate',1)[0])
