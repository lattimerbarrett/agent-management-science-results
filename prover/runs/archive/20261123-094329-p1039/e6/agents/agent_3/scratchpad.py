from pathlib import Path
import sympy as s
u,t=s.symbols('u t')
H=s.Matrix([t,16*t*t-u/4])
J=H.jacobian([u,t])
assert s.simplify(J.det())==s.Rational(1,4)
assert set(J.subs({u:0,t:0}).eigenvals())=={s.I/2,-s.I/2}
W=s.symbols('W', positive=True)
escape_excess=16*W**2-W/4-W
assert s.factor(escape_excess)==W*(64*W-5)/4
v=s.symbols('v', nonnegative=True)
assert s.simplify((escape_excess-s.Rational(59,4)*W).subs(W,1+v)-16*v*(v+1))==0
# If each of two normal coordinates is bounded by eps*R and eps=d/(4R),
# then squared distance to the safe plane is at most d²/8 < d².
d,R=s.symbols('d R',positive=True)
eps=d/(4*R)
assert s.simplify(2*(eps*R)**2)==d*d/8
assert s.simplify(d*d-2*(eps*R)**2)==7*d*d/8
print('H determinant:',s.factor(J.det()))
print('H eigenvalues at 0:',list(J.subs({u:0,t:0}).eigenvals()))
print('Escape excess:',s.factor(escape_excess))
print('Two-horn distance margin:',s.simplify(d*d-2*(eps*R)**2))
Path('workspace/agent3_horn_check.py').write_text(Path(__file__).read_text().split(chr(10)+"Path('workspace/agent3_horn_check.py')")[0]+'\n')
notes=r'''# Strong domination does not suffice for necessity (n >= 4)

Let K be any compact subset of C^n and p outside K. Suppose there is an affine
complex plane L through p of codimension two, disjoint from K. For n>=4 there
is a Fatou--Bieberbach domain D through p contained in C^n minus K.

Proof. Apply an affine unitary map so p=0 and L={t1=t2=0}, with coordinates
(u1,u2,u3,...,u_(n-2),t1,t2). Let d=dist(K,L)>0 and
R=max(1,max_K |u1|,max_K |u2|). Put eps=d/(4R).
The polynomial automorphism H(u,t)=(t,16t^2-u/4) has an attracting fixed point
0 (eigenvalues +/-i/2). Its attracting basin B is biholomorphic to C^2 by the
standard attracting-basin theorem. Moreover B avoids the forward-escaping
cone |t|>max(|u|,1): writing W=|t|, one has
  |16t^2-u/4| >=16W^2-|u|/4 >16W^2-W/4 >W,
and the new first coordinate has modulus W. The cone is invariant and W grows
geometrically. Hence B lies in |t|<=max(|u|,1).
Scale only the second coordinate by eps, obtaining B_eps inside
  |t|<=eps*max(|u|,1).
Use B_eps in the pairs (u1,t1),(u2,t2) and take a product with C^(n-4).
This is a Fatou--Bieberbach domain through 0. If a point of K belonged to it,
then |t1|,|t2|<=eps R=d/4, so dist(point,L)^2<=d^2/8<d^2, a contradiction.

Application to the nonpseudoconvex quartic example:
  K={||g||^2+|w|^4-|w|^2<=1}, g in C^(n-1).
At p=(g0,w0) outside K, set A=1-|w0|^4+|w0|^2.
If g0 != 0, take L={w=w0, <g,g0>=||g0||^2}.
Cauchy--Schwarz gives ||g||>=||g0||>sqrt(A) when A>=0;
if A<0 the fiber contains no obstacle anyway. Thus L avoids K and has
complex dimension n-2. If g0=0, A<0, so take any affine hyperplane in the
whole obstacle-free fiber w=w0 through p.
Therefore every point of the quartic exterior has a Fatou--Bieberbach
neighborhood for n>=4, despite the negative boundary Levi eigenvalue.
It is in particular strongly dominable everywhere.

This DOES NOT establish that the exterior is Oka. It disproves a proposed
necessity reduction to static strong domination (in dimensions n>=4).
All escape and distance inequalities were checked in agent3_horn_check.py.
'''
Path('workspace/agent3_horn_notes.md').write_text(notes)
import runpy
runpy.run_path('workspace/agent3_horn_check.py')
