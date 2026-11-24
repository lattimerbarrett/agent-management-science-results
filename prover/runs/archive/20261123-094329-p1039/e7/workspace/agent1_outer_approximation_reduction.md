# Proved geometric reduction for the higher-dimensional sufficiency claim

Let K be the closure of a bounded connected smooth domain in C^n, with outward pseudoconvex boundary.
A smooth signed defining function rho exists on a compact boundary collar, rho<0 inside and rho>0 outside.

There is a constant C>=0 such that for every outside point p in a sufficiently thin collar and every v in ker(partial rho(p)),

    Levi_rho(p;v) >= -C rho(p) ||v||^2.                 (1)

Proof: the nearest-boundary projection p -> q(p) is smooth on a collar. Orthogonal projections P_p onto ker(partial rho(p)) are smooth. For unit v tangent at p, the vector v_q=P_q v differs from v by O(dist(p,bK))=O(rho(p)). Smoothness of the Hessian and compactness of bK give Levi_rho(p;v)=Levi_rho(q;v_q)+O(rho(p)). The first term is nonnegative.

Choose A>C, let u(z)=||z||^2 and phi=rho exp(Au). For v in ker(partial rho), the product rule gives

    Levi_phi(v)=exp(Au)[Levi_rho(v)+A rho ||v||^2
                         +A^2 rho |partial u(v)|^2].  (2)

Thus for rho>0 the Levi form of phi is positive definite on the (n-1)-dimensional complex subspace ker(partial rho). Its positive index is at least n-1.

For sufficiently small epsilon>0, partial phi is nonzero on phi=epsilon. Define K_epsilon to be K together with the outside collar phi<=epsilon. This is a compact smooth domain with connected interior: the new collar is attached along each component of the original boundary, and every collar component meets the original connected interior. Its boundary is phi=epsilon. Its complex tangent space intersects ker(partial rho) in dimension at least n-2. Therefore its tangential Levi form has at least n-2 positive eigenvalues everywhere.

The sets K_epsilon decrease to K as epsilon decreases to zero, so their complements increase to C^n minus K.

Increasing unions of Oka domains are Oka directly from CAP: for f near compact convex Q, the compact f(Q) lies in one member of the increasing cover; by continuity f maps a smaller neighborhood of Q into that member, and CAP there supplies the required entire approximation.

Consequently, the universal sufficiency claim for n>=3 would follow from an exterior Oka theorem for compact smooth domains with >=n-2 positive tangential Levi eigenvalues. This last analytic theorem is NOT proved here or asserted as verified.

The scalar product-rule identity (2) was checked independently with SymPy in agent1_outer_2convex_checks.py. Estimate (1), collar topology, eigenvalue index, and CAP increasing-union argument are mathematical proofs, not finite numerical tests.
