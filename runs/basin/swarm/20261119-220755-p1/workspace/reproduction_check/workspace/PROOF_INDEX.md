# Sharp threshold for nonconvergence of even residual directions

**The answer is 4.** This is a computer-assisted existence proof for the upper bound;
the convergence proof for s<=3 is analytic. No numerical orbit is itself treated as proof.

## Reading order and scope

The assembled appendix COMPLETE_PROOF.md contains all the mathematical notes below,
in the stated order. Its individual notes use the notation in the final response.
For s=1, the general total-variation theorem immediately gives |T|<=2, and
normalization plus orthogonality uniquely determine weights on T; this is the
same minimal-support argument used for s=2,3.

1. General spectral dynamics and polynomial finite variation: agent4_tv_lemma.md.
2. Negative-neutral bound p_z=O((L-N)^2): agent3_negative_weight_bound.md.
3. Exact and robust extreme-root turning: agent3_root_turning_lemma.md,
   agent1_robust_extreme_root.md.
4. Complete s=2 proof: agent2_s2_convergence_proof.md.
5. The s=3 all-strata proof: agent3_s3_complete_convergence.md.
   Its supporting algebra and lemmas are agent2_s3_logmoment.md,
   agent1_s3_canonical_identities.md, agent3_virtual_root_lemma.md,
   agent4_virtual_probe_degenerate.md, agent2_strict_left_deflation.md,
   agent3_single_negative_edge_closure.md. Common roots of f,g are permitted.
6. Upper-bound analytic expansion: agent2_normal_form_proof.md.
7. Periodic-orbit validation theorem: agent1_floquet_tube_theorem.md.
8. Passage from the hyperbolic periodic ODE orbit to the exact restarted map:
   agent4_parabolic_lifting_theorem.md.

## Reproduce calculations

From the directory containing workspace/, run:

    python workspace/run_final_checks.py

This executes exact symbolic/rational checks, high-precision finite orbit checks,
and an independent exact audit of all 2897 directed-interval records (including
SHA256, exact dyadic tiling of all 2000 Hermite pieces, positivity, nonconstancy,
and the contraction budget). Numerical root-turning tests are supplementary,
not a substitute for the Rayleigh-quotient proof.

To regenerate *every directed interval enclosure*, without using cached chunks:

    python workspace/run_final_checks.py --full

This uses two workers, Sage RealIntervalField(300), exact rational Sturm
isolation of the algebraic spectral parameters, interval automatic differentiation,
and local polynomial numerator transformations. It takes about ten minutes.
The output directory final_recomputed_certificate must not already exist.

## Exact upper-bound parameters

S=(-3,-1,0,1,2,3), Q=(x+18/25)(x-17/10), N=3/50.
Let rho_0<...<rho_7 be the eight roots of P6*Q+N.
The quartic f has roots with indices (0,3,5,6); g has (1,2,4,7).
The two extra nodes are roots with indices (1,6) of P6*Q+2N.
Use all eight nodes shifted by +4 as the diagonal SPD matrix.
The initial positive weights are supplied by the proved parabolic lifting theorem.

## Validated orbit and seed data

- agent2_floquetframe_m072.npz is an *exact dyadic* Hermite seed, not an assumed
  solution. Its SHA256 is
  44d3bcc35e4cc85012075b1937825851e4f95b5878c5b6000bfbf866f1f0ab3b.
- agent4_interval_blowup.py implements the algebraic interval field and derivatives.
- agent4_floquet_pointwise.py implements the full defect and variational enclosures.
- agent4_periodic_pointwise_certificate.py runs the 300-bit interval validation.
- agent4_pointwise_certificate_chunks_v2/ contains the 200 certified chunk files,
  covering 2897 accepted intervals, and summary.json.
- agent2_certificate_post_audit.py independently checks all cached records exactly.
- agent2_floquet_budget_check_v2.py checks a conservative *rational* contraction
  budget: Fbar<9.553571e-6<1e-5=alpha*rho, Lip<0.141826<1/6.

All base weights and both exterior rescaled weights are strictly positive
throughout the validated tube; two phase slices have disjoint theta intervals.
Consequently the validated orbit is nonconstant, positive, and normally hyperbolic.

The continuation/BVP numerical search is not a hypothesis of the proof.
Only the explicitly stored dyadic seed and its verified interval enclosures are used.
