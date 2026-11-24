import sympy as s
from pathlib import Path
# Symbolic Levi certificate for rho=(|z1|^2+|z2|^2-1)^2+sum |w_j|^2-eps.
# Audited independently together with the shared outer-approximation argument.
x1,y1,x2,y2,u,v,eps=s.symbols('x1 y1 x2 y2 u v eps',real=True)
xs=[x1,x2,u]; ys=[y1,y2,v]
a=x1*x1+y1*y1+x2*x2+y2*y2
rho=(a-1)**2+u*u+v*v-eps
Dz=lambda f,j:(s.diff(f,xs[j])-s.I*s.diff(f,ys[j]))/2
Db=lambda f,j:(s.diff(f,xs[j])+s.I*s.diff(f,ys[j]))/2
g=s.Matrix([Dz(rho,j) for j in range(3)])
L=s.Matrix(3,3,lambda j,k:s.expand(Db(Dz(rho,j),k)))
z=s.Matrix([x1+s.I*y1,x2+s.I*y2]); w=u+s.I*v
# holomorphic tangent vector, nonzero at every boundary point for eps<1/4
T=s.Matrix([s.conjugate(w)*z[0],s.conjugate(w)*z[1],-2*(a-1)*a])
assert s.expand((g.T*T)[0])==0
levi=s.expand((T.T*L*s.conjugate(T))[0])
expected=(4*a-2)*a*(u*u+v*v)+4*(a-1)**2*a*a
assert s.expand(levi-expected)==0
# Inner equator at epsilon=1/16 and z=(sqrt(3)/2,0),w=0.
subs={x1:s.sqrt(3)/2,y1:0,x2:0,y2:0,u:0,v:0,eps:s.Rational(1,16)}
assert s.simplify(rho.subs(subs))==0
assert L.subs(subs)==s.diag(1,s.Rational(-1,2),1)
assert g.subs(subs)[1:]==[0,0]
print('Verified tangent identity and Levi formula: (4a-2)*a*|w|^2+4*(a-1)^2*a^2.')
print('At inner equator epsilon=1/16 Levi matrix=',L.subs(subs))
print('Tangential directions z2 and w have Levi eigenvalues -1/2 and +1.')
# Extra dimensions add +1 diagonal Levi entries and no cross terms.
Path('workspace').mkdir(exist_ok=True)
# Simpler ball-fiber domain in C^3: z in C, w in C^2.
b=x1*x1+y1*y1
rho2=(b-1)**2+x2*x2+y2*y2+u*u+v*v-2
L2=s.Matrix(3,3,lambda j,k:s.expand(Db(Dz(rho2,j),k)))
assert L2==s.diag(4*b-2,1,1)
# Exact algebraic regularity certificate: rho2=0 and all real first derivatives have no solution.
all_real=[x1,y1,x2,y2,u,v]
grad_ideal=s.groebner([rho2]+[s.diff(rho2,xx) for xx in all_real],*all_real)
assert list(grad_ideal)==[s.Integer(1)]
ss,tt,lam=s.symbols('ss tt lam',real=True)
rad=lambda ss,tt:(ss-1)**2+tt-2
assert s.expand(rad(lam*ss,lam*tt)-(lam*rad(ss,tt)+(1-lam)*rad(0,0)-ss**2*lam*(1-lam)))==0
print('Verified empty critical-boundary ideal (Groebner basis [1]) and star-shaped identity.')
q={x1:0,y1:0,x2:1,y2:0,u:0,v:0}
assert rho2.subs(q)==0
assert s.Matrix([Dz(rho2,j) for j in range(3)]).subs(q)==s.Matrix([0,1,0])
assert L2.subs(q)==s.diag(-2,1,1)
# v=(0,-w2,w1) is a complex tangent and has positive Levi for w != 0.
T2=s.Matrix([0,-(u-s.I*v),x2-s.I*y2])
g2=s.Matrix([Dz(rho2,j) for j in range(3)])
assert s.expand((g2.T*T2)[0])==0
assert s.expand((T2.T*L2*s.conjugate(T2))[0]-(x2*x2+y2*y2+u*u+v*v))==0
print('Verified simpler rho2=(|z|^2-1)^2+||w||^2-2 has Levi diag(4|z|^2-2,1,1).')
print('At (z,w1,w2)=(0,1,0), tangent eigenvalues are -2 and +1.')
# Hénon escape check showing a FB attracting basin can avoid the torus tube.
M=s.Integer(10); alpha=s.Rational(1,10)
lo=s.Rational(3,4); hi=s.Rational(5,4)
first_lower=M*lo-alpha*s.sqrt(hi)
assert first_lower>2
assert s.sqrt(hi)<2
R=s.symbols('R',real=True,positive=True)
# For R>=2 and |w|<=|z|=R, |10z²-.1w| >= (10R-.1)R>2R.
assert (M*R-alpha-2).subs(R,2)>0
assert (s.Matrix([[0,-alpha],[1,0]])**2)==-alpha*s.eye(2)
print('Verified Hénon escape: torus tube enters invariant cone |z|>max(2,|w|).')
# Exact outer-perturbation Hessian used in agent2's weak -> one-positive reduction.
A=s.symbols('A',positive=True,real=True)
S=sum(xx*xx+yy*yy for xx,yy in zip(xs,ys))
h=-s.exp(-A*S)
Lh=s.Matrix(3,3,lambda j,k:Db(Dz(h,j),k))
Z=s.Matrix([xx+s.I*yy for xx,yy in zip(xs,ys)])
claimed=s.exp(-A*S)*(A*s.eye(3)-A*A*s.conjugate(Z)*Z.T)
assert (Lh-claimed).applyfunc(s.simplify)==s.zeros(3)
print('Verified Levi(-exp(-A||Z||^2))=exp(-A||Z||^2)*(A I-A^2 conjugate(Z) Z^T).')
# Holomorphic change used to strongly dominate a rational-hull point of the worm.
U,D=s.symbols('U D')
G=s.Matrix([-D*s.exp(2*s.I*U),s.exp(U)])
assert s.simplify(G.jacobian([U,D]).det()-s.exp((1+2*s.I)*U))==0
assert G.subs({U:s.pi/2,D:1})==s.Matrix([1,s.exp(s.pi/2)])
ff,gg,c,u0=s.symbols('ff gg c u0')
P=s.Matrix([u0+ff,1+c*s.exp((u0+ff)**2)*gg])
assert s.simplify(P.jacobian([ff,gg]).det()-c*s.exp((u0+ff)**2))==0
print('Verified Gaussian-strip map and worm-cover Jacobians and target point exactly.')
Path('workspace/agent4_levi_certificate.py').write_text(Path(__file__).read_text())
Path('workspace/agent4_worm_domination.md').write_text(r'''# Explicit entire domination of a rational-hull point of the worm
Let the worm be K={rho<=0}, rho=|z|^2-2Re(z exp(-it))+eta(t), t=log|w|^2,
with eta>=0 and eta(t)>1 outside a bounded interval [2a,2b].
Use a Hénon basin parametrization Psi=(f,g):C^2 -> Omega, Psi(0)=0, with
|g|<=max(|f|,2). Its existence and invertible derivative are proved in the shared basin notes.

Set u0=pi/2, A=max(|a|,|b|), B=exp(A^2)*(A+u0+3), c=1/(4B),
U=u0+f, Delta=1+c exp(U^2)g.
If a<=Re U<=b, writing U=X+iY gives
|exp(U^2)g| <= exp(A^2) exp(-Y^2)*(A+u0+2+|Y|) <= B,
since exp(-Y^2)<=1 and |Y| exp(-Y^2)<=1.
Thus Re Delta>=3/4 on this strip. Outside this strip eta(2Re U)>1.

Define H=(Z,W)=(-Delta exp(2iU), exp U).
Inside the strip, with t=2Re U,
rho(H)=|Delta|^2 exp(-4Im U)+2Re(Delta)exp(-2Im U)+eta(t)>0.
Outside the strip eta(t)>1 implies rho(H)>0 from the original squared-disc expression.
Hence H is entire with image in C^2 minus K.

At source0, U=pi/2 and Delta=1, so H(0)=(1,exp(pi/2)), the explicit point in
rational hull(K) from agent3_worm_geometry.md.
The map (f,g)->(U,Delta) has Jacobian c exp(U^2), and (U,Delta)->(Z,W)
has Jacobian exp((1+2i)U). Both are everywhere nonzero.
Thus det DH(0)!=0. In fact H is locally biholomorphic everywhere.

This disproves the proposed statement that a nondegenerate entire map omitting compact K
in C^2 must omit the rational hull of K. It DOES NOT prove that the entire worm exterior is Oka.
The Gaussian change-of-coordinate Jacobian and the target point are checked in agent4_levi_certificate.py.
''')
Path('workspace/agent4_mixed_example.md').write_text(r'''# Explicit smooth compact mixed-Levi hole
For n>=3 split (z,w) in C x C^{n-1} and let
rho=(|z|^2-1)^2+||w||^2-2,
Omega={rho<0}, K={rho<=0}.

Boundedness: |z|^2<=1+sqrt(2), ||w||^2<=2 on K. Nonemptiness: rho(0,0)=-1.
Smooth boundary: partial_z rho=2(|z|^2-1) conjugate(z), partial_w rho=conjugate(w).
A zero gradient requires w=0 and z=0 or |z|=1, where rho=-1 or -2, never0.
Every rho=0 point is a boundary point by regularity, so K=closure(Omega).

Connectedness: K and Omega are star-shaped about0. Put s=|z|^2,t=||w||^2,u=lambda^2 in [0,1]. Then
rho(lambda z,lambda w)=u rho(z,w)+(1-u)rho(0,0)-s^2 u(1-u).
For rho(z,w)<0 the RHS is negative; hence Omega is connected.

Levi matrix (holomorphic coordinates z,w): diag(4|z|^2-2,1,...,1).
If w!=0, choose a nonzero v_w with sum conjugate(w_j)v_j=0 (possible since n-1>=2), and v_z=0.
This vector is complex tangent and its Levi value is ||v_w||^2>0.
If w=0, all pure w directions are tangent and have positive Levi value.
Thus every boundary point has a strictly positive tangential Levi direction.

At q=(z,w)=(0,1,0,...,0), rho=0 and complex tangency is v_{w_1}=0.
The z direction is tangent with Levi value -2, while w_2 is tangent with value+1.
Consequently K is not pseudoconvex in the orientation of the problem.

The code agent4_levi_certificate.py verifies the complex derivatives, tangent identities,
Levi signature, and auxiliary constructions exactly with SymPy.
THIS FILE DOES NOT CLAIM THAT THE COMPLEMENT IS OKA; a global Oka theorem is still needed.
''')
