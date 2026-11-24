import sympy as s
from pathlib import Path
x,y,z,X,Y,Z,a,M,r=s.symbols('x y z X Y Z a M r', nonzero=True)
H=s.Matrix([a*y+M*x*x,a*z+M*y*y,a*x])
xinv=Z/a
yinv=(X-M*xinv*xinv)/a
zinv=(Y-M*yinv*yinv)/a
Hi=s.Matrix([xinv,yinv,zinv])
assert all(s.simplify(expr-target)==0 for expr,target in zip(H.subs({x:xinv,y:yinv,z:zinv}, simultaneous=True),[X,Y,Z]))
assert s.simplify(H.jacobian([x,y,z]).det()-a**3)==0
A=H.jacobian([x,y,z]).subs({x:0,y:0,z:0})
assert A**3==a**3*s.eye(3)
# For a=1/2,M>=2,r>=2, r_next>=M*r²-a*r>2*r.
# At M=2,a=1/2,r=2+t the strict lower bound factor is positive.
t=s.symbols('t',nonnegative=True)
lower=s.expand((2*r*r-s.Rational(1,2)*r-2*r).subs(r,2+t))
assert all(c>0 for c in s.Poly(lower,t).all_coeffs())
# Set first-entry M=2+(4R+4)/delta², R>=1, delta>0.
# Then M*delta²-aR = 2delta²+3.5R+4 > max(2,2aR).
R,d=s.symbols('R d',positive=True)
entry=s.simplify((2+(4*R+4)/d**2)*d**2-s.Rational(1,2)*R)
assert s.simplify(entry-(2*d**2+s.Rational(7,2)*R+4))==0
Path('workspace/agent2_outer_approx.md').write_text(r'''## Outer approximation lemma (proved)
Suppose n>=3 and K is the closure of a bounded domain with C-infinity pseudoconvex boundary. Then K has a decreasing neighborhood basis K_epsilon of compact domains with smooth boundary having a strictly positive tangential Levi direction at each point.

Choose a smooth signed-distance defining function rho in a fixed collar of boundary K, negative on K. Compactness, smoothness, and pseudoconvexity imply a constant C with
L_rho(z;v) >= -C rho(z)||v||²
for all z in the outer collar and v in ker(partial rho(z)). To see this, project z to its nearest boundary point q; rho(z) is the signed distance. The tangent hyperplanes and Levi matrices differ by O(rho(z)); projecting v to ker(partial rho(q)) changes it by O(rho(z))||v||. Apply nonnegativity at q and absorb the uniform errors.

Fix A>C and set psi_epsilon(z)=rho(z)-epsilon exp(-A||z||²) in the collar. For sufficiently small epsilon, its zero set is a unique small positive outward normal graph over boundary K, since its outward normal derivative is uniformly positive. Define K_epsilon to be K plus the part of the outer collar where psi_epsilon<=0. These are smooth compact connected domains, decrease to K as epsilon decreases to zero, and form a neighborhood basis.

At a boundary point z of K_epsilon, rho(z)=epsilon exp(-A||z||²). The complex subspace
E_z=ker(partial rho(z)) intersect ker(partial ||z||²)
has dimension at least n-2>=1. Every nonzero v in E_z is complex tangent to psi_epsilon=0. Direct differentiation gives
L_{-exp(-A||z||²)}(v)=exp(-A||z||²)[A||v||²-A²|sum bar(z_j)v_j|²].
The final term vanishes on E_z, so
L_{psi_epsilon}(v)>=epsilon exp(-A||z||²)(A-C)||v||²>0.

The exteriors C^n minus K_epsilon increase to C^n minus K. Hence any theorem asserting Oka for holes with one strictly positive tangential Levi direction would imply the desired universal sufficiency in every n>=3, since increasing unions of Oka domains are Oka directly by CAP compactness. No such global theorem is proved in this note.
''')
print('PASS generalized Henon inverse/Jacobian/attracting linear part/escape-cone bounds')
Path('workspace/agent2_codim2_basin.py').write_text(Path(__file__).read_text())
