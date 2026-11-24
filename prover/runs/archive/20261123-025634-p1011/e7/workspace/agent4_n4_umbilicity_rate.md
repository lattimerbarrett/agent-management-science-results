# Dimension-four umbilicity rate under isolated-simple blowup

This lemma proves umbilicity at an isolated-simple blowup limit using energy-norm modulation. It does NOT prove the full local Pohozaev nonnegativity required for compactness.

## Hypotheses

Let u_i be positive solutions on one fixed positive-Yamabe LCF manifold, p_i boundary blowup centers, M_i=u_i(p_i)→infinity, epsilon_i=M_i^−1 (n4). Assume local bubble convergence and isolated-simple strong decay through one fixed physical radius r0:

u_i(x)<=C M_i^−1 dist(x,p_i)^−2,
|∇u_i(x)|<=C M_i^−1 dist(x,p_i)^−3

outside a fixed multiple of epsilon_i and inside2r0. Flatten the metric conformally nearp_i and use a uniformly controlled local Möbius normalization to arrange H(p_i)=0. In the corresponding Euclidean graph chart its quadratic term is f2_i=(1/2)A_i[z,z], trA_i=0, with uniformly bounded higher jets.

## Conclusion

|A_i|² log(1/epsilon_i) is bounded. In particular II°(p_i)→0.

## Proof

1. Cut u_i off inside the physical r0-ball. Core bubble convergence and the strong gradient decay give H¹ closeness to a cut-off standard bubble: after rescaling, the gradient tail outside radiusR is bounded by C∫_R^infinity r^−3dr, uniformlyi. The lower-order and boundary form terms tend to zero. By finite-dimensional modulation choose a nearby center and scale delta_i, delta_i/epsilon_i→1 and center displacemento(epsilon_i), so

v_i=chi u_i=W_i+psi_i, psi_i Q-orthogonal to all bubble Jacobi modes, ||psi_i||H1=o(1).

This is the usual elementary implicit function theorem: the limiting Gram matrix of the bubble derivatives is positive definite. The changed A_i has the same limit and the same eventual logarithmic rate, since its changeiso(epsilon_i).

2. Let Phi_i be the physical quadratic correction constructed in agent4_n4_log_proof.md, and D_i=f2_i U_t. In graph pullback coordinates the material correction is B_i=D_i+Phi_i. It obeys

|B_i|<=C|A_i|(1+r)^−1,
|DB_i|<=C|A_i|(1+r)^−2,

and the first linear graph residual is cancelled exactly. Cut it off at R_i=r0/delta_i and transfer delta_i B_i back to the physical domain. Project off the finite-dimensional kernel and call the result b_i. Then

||b_i||H1<=C delta_i |A_i| sqrt(logR_i)+O(delta_i).

The projection changes the model by O(delta_i² logR_i), because its Euclidean angular projection is zero and the metric error paired with a Jacobi mode has normO(delta_i sqrt(logR_i)). This is o(delta_i), hence harmless below.

3. The corrected model m_i=W_i+b_i has full energy-dual residual O(delta_i), uniformlyi. Here are the required radial estimates, not just qualitative smallness:

* The cut-off B_i commutator has normO(1) on its outer annulus, since B_i~r^−1 and DB_i~r^−2; multiplying bydelta_i givesO(delta_i).
* The graph error beyond its quadratic first variation isO(delta_i²r²). Applied toDU~r^−3 or to the first correction it gives bulk coefficientsbounded byCdelta_i²r^−1, whose L² norm throughR_i isO(delta_i²R_i)=O(delta_i r0).
* The rescaled mean curvature isO(delta_i²r) becauseH(p_i)=0. Its boundary source againstU has dual trace normO(delta_i²R_i)=O(delta_i r0), and againstdelta_i B_i has normO(delta_i³R_i²)=O(delta_i r0²).
* Nonlinear remainder3U(delta_i B_i)² has L^{4/3} normO(delta_i²); the cubic remainder has normO(delta_i³(logR_i)^{3/4})=o(delta_i).

Higher metric terms are absorbed by the small fixed physical r0. Exactly the same estimates hold after bounded conformal normalizations.

4. The actual cut-off solution v_i has residualO(delta_i), supported only in its fixed physical outer annulus. The uniform projected inverse from agent4_uniform_inverse_proof.md and the small nonlinear Lipschitz constant on an o(1)H¹-ball therefore give

||v_i−m_i||H1<=C delta_i.

Indeed subtract their projected equations, invert the bubble linearization, and absorb its nonlinear derivative perturbation, which tends to zero. No annular pointwise approximation is used here.

5. Write x_i=|A_i|sqrt(logR_i). Let Z_i be the scale Jacobi mode with fixed physical cutoff. Its full linearized residual satisfies

||E''(W_i)Z_i||H*<=C delta_i(1+x_i).

The quadratic graph term contributesdelta_i|A_i|sqrt(logR_i) by the radial integral∫r^−1dr; the higher jets contributeO(delta_i) by the same estimates in step3. The actual cutoff residual paired withZ_i isO(delta_i²), because both u_i andZ_i and their gradients areO(delta_i) on the fixed physical outer annulus.

The nonlinear difference between v_i andm_i, paired withZ_i, isO(delta_i²(1+x_i)): n4 has cubic nonlinearity, and its derivative perturbation isO(||b_i||+||v_i−m_i||) in the energy-dual estimate. Combining with step4 yields

|E'(m_i)[Z_i]|<=C delta_i²(1+x_i).

6. The explicitly constructed model has scale energy

E(m_delta)=E0−(pi²/30)|A_i|² delta² log(1/delta)+O(delta²),

with a uniformly C¹-controlled remainder after differentiation bylogdelta. This follows from the exact graph energy: the sole logarithm is the quadratic Jacobi energy from agent4_n4_log_proof.md; every cubic/higher coefficient has the radial powers listed in step3 and givesO(delta²) after integration to r0/delta. The cutoff annulus givesO(delta²). The same power bounds apply after one logdelta derivative. The difference between the full logscale derivative ofm_delta andZ_delta has normO(delta |A_i|sqrt(logR)+delta), so pairing it with the O(delta)model residual changes the result by at mostCdelta²(1+x_i). Hence

(pi²/15)|A_i|² delta_i² logR_i <= C delta_i²(1+x_i).

Dividing bydelta_i² gives c x_i²<=C(1+x_i), forcingx_i bounded. This proves the rate and the vanishing conclusion.

## Explicit remaining gap

The estimate above controls the error only byO(1+x_i) after dividing the Pohozaev scale bydelta_i². Sincex_i may tend to a nonzero finite value, it does NOT establish the sharp nonnegative limiting Pohozaev sign. A further sectorwise/weighted remainder argument is necessary for that sign and for the ultimate positive-mass contradiction.
