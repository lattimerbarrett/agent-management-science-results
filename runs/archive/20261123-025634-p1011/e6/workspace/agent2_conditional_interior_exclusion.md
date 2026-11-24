# Conditional exclusion of an isolated interior peak approaching the boundary

This is a conditional lemma, not the missing compactness theorem.

Let n>=3. Suppose domains Omega_i converge in C^2_loc to the upper half-space,
positive smooth v_i solve
    Delta v_i + eta_i n(n-2) v_i^((n+2)/(n-2)) = 0,
where eta_i -> 0, and their Robin boundary coefficients converge to zero.
Assume v_i -> G in C^2_loc away from e_n (including C^1 boundary convergence),
G>0, G has a nonremovable isolated singularity at e_n, and no other
singularities occur in the whole upper half-space. Then these hypotheses are
inconsistent.

Proof. G is harmonic and has zero normal derivative on the boundary plane.
Even reflection extends it to a positive harmonic function on
R^n \ {e_n,-e_n}. Bocher's theorem gives equal positive singular coefficients
a at the two poles. Subtracting a|y-e_n|^(2-n)+a|y+e_n|^(2-n) leaves an entire
harmonic function H. Since G>=0, H is bounded below outside a large ball; it
is bounded below on the ball by continuity. Liouville's theorem makes H a
constant. Thus G is the two-image Green model plus a constant.

For each 0<r<1, the sphere S_r(e_n) lies in Omega_i for all sufficiently large i.
The translation stress vector for direction k is
    T_k(v)= (partial_k v) grad v
            - e_k (|grad v|^2/2 - eta_i (n-2)^2 v^(2n/(n-2))/2).
It has zero divergence by the PDE. Since v_i is smooth in B_r(e_n), its flux
through S_r(e_n) is zero. C^2 convergence and eta_i ->0 imply that the harmonic
translation stress flux of G through that sphere is zero.

For G=a|y-e_n|^(2-n)+h(y), h smooth harmonic near e_n, the flux equals
    (2-n) a |S^(n-1)| partial_k h(e_n).
Indeed expand grad G into its radial singular part and regular part and let
r -> 0; the two mixed angular terms cancel and only the constant regular
gradient survives. Flux is independent of r by harmonicity.
For the image Green model,
    partial_n h(e_n)=a(2-n)2^(1-n).
Consequently its normal translation flux is
    (n-2)^2 a^2 |S^(n-1)| 2^(1-n)>0,
a contradiction.

Application framework (not an extraction theorem): in flat local charts let
alpha_i=u_i(p_i), eps_i=alpha_i^(-2/(n-2)), and let d_i=dist(p_i,boundary).
If eps_i/d_i ->0 and d_i ->0, rescale
    v_i(y)=alpha_i d_i^(n-2)u_i(q_i+d_i y),
where q_i is a nearest boundary point and p_i=q_i+d_i e_n.
Then eta_i=(eps_i/d_i)^2 and the Robin coefficient is O(d_i).
The usual isolated-simple estimate
    u_i(x)<=C alpha_i^(-1)|x-p_i|^(2-n)
outside C eps_i, together with eps_i-scale standard-bubble convergence,
provides the compact convergence and a nonremovable pole above. Establishing
those estimates for arbitrary blow-up sequences remains a separate missing
analytic step.
