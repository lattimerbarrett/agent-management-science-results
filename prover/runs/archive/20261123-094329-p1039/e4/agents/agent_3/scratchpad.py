import sympy as s
from pathlib import Path
# Universal-in-n calculation: remaining coordinates enter by independent |z_j|^4.
x,y,u,v,t=s.symbols('x y u v t', real=True)
a,b=s.symbols('a b', nonnegative=True)
q=(x*x+y*y)**2+(u*u+v*v)**2-(x*x+y*y)*(u*u+v*v)
assert s.expand((a*a+b*b-a*b)-s.Rational(1,2)*(a*a+b*b)-s.Rational(1,2)*(a-b)**2)==0
# Euler's identity proves nonzero gradient on q_n=1 in all dimensions.
assert s.expand(sum(w*s.diff(q,w) for w in (x,y,u,v))-4*q)==0
# Complex tangent vector e_2 at p=(1,0,...), and its Levi value.
p={x:1,y:0,u:0,v:0}
assert s.diff(q,u).subs(p)==0 and s.diff(q,v).subs(p)==0
L22=s.simplify((s.diff(q,u,2)+s.diff(q,v,2))/4)
assert L22.subs(p)==-1
assert q.subs(p)==1
assert s.diff(q,x).subs(p)==4
# q_n(t*z)=t^4 q_n(z), guaranteeing connected starshaped sublevel.
assert s.expand(q.subs({x:t*x,y:t*y,u:t*u,v:t*v}, simultaneous=True)-t**4*q)==0
out='''Verified universal quartic candidate q_n=|z1|^4+|z2|^4-|z1z2|^2+sum_{j>=3}|zj|^4.\nq_n >= (|z1|^4+|z2|^4)/2+sum_{j>=3}|zj|^4.\nEuler identity grad(q_n).radial=4q_n proves boundary regularity.\nAt p=(1,0,...), e2 tangent and Levi=-1.\nK_n={q_n<=1} is bounded closure of connected smooth domain and NOT pseudoconvex.\nNO Oka-complement assertion is established.\n'''
Path('workspace/agent3_quartic_checks.py').write_text(Path('scratchpad.py').read_text())
Path('workspace/agent3_quartic_checks.txt').write_text(out)
print(out)
# Exact universal Levi matrix repair for a C^2 boundary point.
alpha,beta=s.symbols('alpha beta', positive=True)
c_re,c_im,d=s.symbols('c_re c_im d', real=True)
A=((c_re*c_re+c_im*c_im)/alpha+alpha-d)/(2*beta*beta)
H=s.Matrix([[alpha,c_re+s.I*c_im],[c_re-s.I*c_im,d]])
Hfixed=H+s.Matrix([[0,0],[0,2*A*beta*beta]])
assert s.simplify(Hfixed.det()-alpha*alpha)==0
assert Hfixed[0,0]==alpha
print('Boundary Levi repair: first principal minor alpha>0; determinant alpha^2>0, verified symbolically.')
# Fully rational local psh-bump certificate for the explicit quartic in C^2.
a0,b0,c0,d0=s.symbols('a0 b0 c0 d0', real=True)
coords=(a0,b0,c0,d0)
qq=s.expand(q.subs({x:1+a0,y:b0,u:c0,v:d0}, simultaneous=True))
rr=1-qq
phi=s.expand(rr+rr**2-s.Rational(1,4)*sum(k*k for k in coords))
def levi(expr,i,j):
    xi,yi=coords[2*i:2*i+2]
    xj,yj=coords[2*j:2*j+2]
    return s.expand((s.diff(expr,xi,xj)+s.diff(expr,yi,yj)+s.I*s.diff(expr,xi,yj)-s.I*s.diff(expr,yi,xj))/4)
HH=s.Matrix(2,2,lambda i,j:levi(phi,i,j))
origin=dict.fromkeys(coords,0)
assert HH.subs(origin)==s.diag(s.Rational(15,4),s.Rational(3,4))
R=s.Rational(1,1000)
def cube_bound(poly):
    return sum(abs(coef)*R**sum(powers) for powers,coef in s.Poly(s.expand(poly),*coords).terms())
# Entrywise bounds on the entire cube, which contains the radius-R ball.
B11=cube_bound(HH[0,0]-s.Rational(15,4))
B22=cube_bound(HH[1,1]-s.Rational(3,4))
B12=cube_bound(s.re(HH[0,1]))+cube_bound(s.im(HH[0,1]))
assert s.Rational(15,4)-B11-B12>0
assert s.Rational(3,4)-B22-B12>0
assert cube_bound(rr)<s.Rational(1,2)
# An explicit exterior point where the max bump uses phi rather than constant.
delta=R**2/1000
pt={a0:delta,b0:0,c0:0,d0:0}
level=-R**2/8
assert rr.subs(pt)<0
assert level<phi.subs(pt)<0
print('Explicit quartic psh bump certified on ball radius',R)
print('Gershgorin positive lower bounds:',s.Rational(15,4)-B11-B12,s.Rational(3,4)-B22-B12)
Path('workspace/agent3_quartic_checks.py').write_text(Path('scratchpad.py').read_text())
