# Conditional diagonal persistence lemma (not a PDE construction)

Let h parametrize smooth normal-graph perturbations of the unit sphere, with
small C^2 norm, and let Omega_h be the bounded Euclidean domain. Use a fixed
collar-extension diffeomorphism to pull the scalar-curvature/Robin equation
back to a reference ball. A positive solution is called nondegenerate when
the linearized Robin operator has trivial kernel.

**Persistence.** Each positive nondegenerate solution at h_0 extends uniquely
to nearby h in C^{4,alpha}, with C^{2,alpha} convergence of solutions. Indeed,
the PDE map takes C^{4,alpha} graph parameters and C^{2,alpha} positive
functions into C^{0,alpha}(M) x C^{1,alpha}(boundary). Its u-derivative is a
uniformly elliptic scalar Robin operator, Fredholm index zero. Trivial kernel
therefore gives an isomorphism; apply the Banach implicit-function theorem.
Positivity and a strict boundary-height lower bound persist by C^0 continuity.

**Diagonal lemma.** Suppose one can construct successively h_j with disjoint
new perturbation supports U_j and a nondegenerate positive solution v_j with
boundary maximum > j+1. Suppose the single-patch construction allows each
increment h_{j+1}-h_j arbitrarily small in every prescribed finite C^m norm,
while keeping its support in a fresh U_{j+1}. Then one can choose the sequence
so that its smooth limit h_infty has positive solutions with boundary maxima
>j for every j.

Proof. At stage j, prior solutions have continued to h_j by persistence.
Choose epsilon_j>0 so every parameter within epsilon_j in C^{4,alpha} admits
continuations of all first j solutions, maintaining their heights >1,...,j.
Set r_j <= min(epsilon_j/2, r_{j-1}/4, 2^{-j}). Demand that the next increment
have C^{4,alpha} norm <r_j/2, and C^j norm <2^{-j}. Also demand the analogous
C^m smallness for all m<=j (equivalently use the maximum of these norms).
Then h_j converges in every C^m. The tail distance from h_j is at most
r_j/2+r_j/8+...=2r_j/3<epsilon_j, so persistence applied directly at h_j
gives all first j solutions on h_infty. This proves the claim.

One must reserve an untouched spherical boundary region for all future
patches; otherwise a fixed lower bound on |II^circ| could obstruct an
arbitrarily C^2-small new bubble construction. Disjoint U_j accumulating at
p and perturbations flat relative to dist(U_j,p) ensure the limit is smooth
and agrees with the sphere to infinite order at p. These extra smallness
requirements are finite-stage conditions and fit the diagonal choice.

**Global hypotheses.** Sufficiently small C^2 graph perturbations retain
strict Euclidean mean convexity H>h_0>0. Their Robin quadratic energy is
int |du|^2 + (n-2)/(2(n-1)) int_boundary H u^2 and is coercive in L^2;
otherwise a normalized sequence with energy tending to zero converges to a
nonzero constant while its boundary term tends to zero, a contradiction.
Thus positive Yamabe type is retained. Euclidean domains are flat and hence
LCF. If the first patch has II^circ !=0 at a point untouched by later patches,
the final boundary is not umbilic and cannot be conformally equivalent to a
round hemisphere (umbilicity is conformally invariant).

This lemma is rigorous but CONDITIONAL. It does not prove the existence of
any one of the required nondegenerate high-peak single-patch solutions.


# Stronger packet-persistence variant: nondegenerate PDE solutions unnecessary

Suppose a single-patch LS construction gives a projected inverse uniformly
on a compact parameter ball K (scale bounded above/below, centers bounded),
and a C^1 reduced energy E_h on K, depending continuously on the domain h.
Assume E_h has a strict interior-versus-boundary energy gap:
min_boundary(K) E_h > E_h(z_0) for some interior z_0.
Then every sufficiently nearby domain retains this strict gap and projected
inverse; the reduced energy attains a minimum in the interior of K, giving
a true critical point and hence a PDE solution. All points of K correspond
to bubbles with boundary maxima at least a common positive constant times
epsilon^{-(n-2)/2}, so the height bound persists too. This is a robust solution
packet, even if no individual solution is nondegenerate or isolated.

The diagonal proof above applies to packet persistence neighborhoods instead
of implicit-function neighborhoods. In particular, a strict local MAXIMUM
of the positive shape quadratic Q and a UNIFORM C^0 asymptotic
E=E_0-C*epsilon^16*Q+o(epsilon^16), C>0, supply a stable local MINIMUM packet.
No C^2 parameter asymptotic or exact nondegeneracy is required. If one has
only an isolated saddle with nonzero Brouwer degree, uniform C^1 convergence
and finite-dimensional gradient degree give the analogous persistence.

# Positivity without a pointwise correction estimate

Carry out LS with A_g u=n(n-2)(u_+)^{(n+2)/(n-2)}, B_g u=0, A_g=-L_g.
If u is a nonzero weak solution, test by u_-=max(-u,0). Then
-E_g(u_-,u_-)=0, since (u_+)^p*u_-=0. Positivity of lambda_1 forces u_-=0.
Thus u>=0. Strong maximum principle yields strict interior positivity, and
Hopf's boundary lemma rules out a boundary zero: at such a zero, B_g u=0
would imply partial_nu u=0, contrary to Hopf. Thus u>0 on the compact closure,
and elliptic regularity yields smoothness. The solution is nonzero because
its bubble projection is bounded away from zero throughout K.
