from pathlib import Path
text=r'''SUPPORT-NORM LEMMA (agent_2, checked proof)

Let p:V->B be a holomorphic vector bundle of rank 2 over a complex surface.
Let Omega be an open neighborhood of its zero section with compact closure, and
suppose its boundary is smooth and has a smooth defining function r, Omega={r<0},
whose Levi form on the complex tangent to the boundary has at least two strictly
negative eigenvalues. Define
  F(x,xi) = max{|xi(v)| : v in closure(Omega) intersect V_x}.
Then F is continuous, is a genuine complex norm in each dual fibre, and log F is
plurisubharmonic on V* minus its zero section (with value -infinity at zero).

PROOF.
The compact zero section has a uniform small tube contained in Omega, and Omega
is bounded in a fixed smooth metric. Thus c|xi| <= F(x,xi) <= C|xi|. Triangle and
complex homogeneity are immediate. Compactness of closure(Omega) gives upper
semicontinuity.

Fix xi!=0 and a maximizing v0 over x0; v0 is a boundary point. Multiply xi by a
constant phase so xi(v0)=F(x0,xi)>0. The real supporting halfspace Re xi(v)>F is
disjoint from closure(Omega)_x0. We claim d_v r(v0)!=0. Otherwise, on each real
vertical direction w with Re xi(w)>0, r(v0+t w)>=0 for small positive t. Since its
first vertical derivative is zero, its real vertical Hessian is nonnegative on
these w, hence by evenness and continuity on every real vertical vector. The
vertical complex 2-plane is then a semipositive subspace for the Levi form of r,
and lies in the boundary complex tangent. It must intersect a negative complex
2-plane there (the boundary complex tangent has dimension 3), a contradiction.
Thus d_v r!=0. The implicit function theorem gives interior points in nearby
fibres arbitrarily close to v0. This proves lower semicontinuity, hence continuity.

Work in holomorphic local coordinates and test log F on an affine complex line
 t -> (x(t),xi(t)) in V*. If x(t) is constant, log F is the supremum of the locally
uniformly upper bounded subharmonic functions log|xi(t)(v)| for fixed v in the
compact fibre body, and continuity gives subharmonicity. Otherwise x(t) is an
immersion. Suppose a smooth function phi touches log F from above at t0 and
phi_{t bar t}(t0)<0. Choose a maximizing v0. On the complex 3-fold parametrized by
(t,v), the pulled-back boundary r=0 is smooth at (t0,v0), because d_v r!=0. Its
complex tangent has dimension 2 and intersects a negative 2-plane of the ambient
boundary complex tangent (dimension 3) in dimension at least 1. Thus its Levi
form has a strictly negative direction.

On the other hand put rho(t,v)=log|xi(t)(v)|-phi(t). This is smooth near the contact
point, since xi(t0)(v0)!=0, and has nonzero vertical derivative. Locally {r<0} is
contained in {rho<=0}, and their boundaries touch at (t0,v0). Hence
 d rho = lambda d r, lambda>0,
and on their common complex tangent
 Levi(rho) <= lambda Levi(r).
This standard tangency inequality follows by taking the real second derivative
of rho along any curve in r=0: rho has a local maximum zero on that boundary.
But log|xi(t)(v)| is pluriharmonic where nonzero, so
 Levi(rho) = -phi_{t bar t}|dt|^2 >= 0.
Consequently Levi(r) is semipositive on that entire complex tangent, contradicting
the negative direction just obtained. Thus every upper test has nonnegative
Laplacian. The standard upper-test characterization of continuous subharmonic
functions gives subharmonicity along every affine complex line. Hence log F is
plurisubharmonic. The extension across xi=0 with value -infinity is psh because
of the two-sided comparison with log|xi|. QED.

EXTRACTION FROM A 3-POSITIVE EXHAUSTION.
Identify a punctured neighborhood of the removed section in P(O+E) with a
punctured neighborhood of zero in E using [1:v]. Proper sublevels imply psi->+
infinity uniformly as v->0 over the compact base: otherwise a sequence tending
to the removed section would lie in a compact sublevel of U. Choose epsilon>0
and a regular value c greater than psi on epsilon/2<=|v|<=epsilon and greater than
psi on the compact exceptional set. Then
 Omega = zero section union {0<|v|<epsilon, psi([1:v])>c}
is a bounded tube with smooth compact boundary, disjoint from that exceptional
set. On its boundary r=c-psi has at least three negative Levi eigenvalues in
ambient dimension 4, hence at least two on its complex tangent hyperplane. The
lemma produces a continuous convex homogeneous dual norm F with log F psh.
'''
Path('workspace/agent2_support_lemma.txt').write_text(text)
print('Saved complete support-norm lemma and exhaustion-to-tube argument.')
