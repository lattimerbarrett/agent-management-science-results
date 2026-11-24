# Uniform projected inverse for a concentrating boundary bubble

This standard analytic lemma is proved here because it is a genuine global ingredient absent from the earlier spectral calculations. It does not give quantitative reduced-energy remainders or a scale critical point.

## Set-up

One may conformally normalize so that R_g>0 and H_g=0, but this is not necessary. Work directly in the given metric, which is useful for Euclidean graph domains. Let

Q(v,w)=∫M(∇v·∇w+c_n R_g v w)+2c_n∫∂M H_g v w, H=H¹(M),
a=n(n−2), p=(n+2)/(n−2).

Then Q is an equivalent Hilbert norm on H. Indeed λ1>0 gives λ1||v||²_L2<=Q(v,v), while the bounded curvature and trace interpolation give Q(v,v)>=(1/2)||∇v||²−C||v||²_L2; combining proves coercivity in H¹. Fix a small Fermi radius r0 uniform over boundary centers ξ. Let χ be a smooth radial cutoff, equal to 1 in radius r0/2 and supported in radius r0. Set

U(z)=(1+|z|²)^{−(n−2)/2},
W_{δ,ξ}(F_ξ(δz))=χ(δz)δ^{−(n−2)/2}U(z).

Let Z0=(n−2)U/2+z·∇U and Zj=∂_jU for j=1,...,n−1, and let K^α_{δ,ξ} be the corresponding cut-off rescalings. Let Kδ be their span and Πδ its Q-orthogonal projection. Define Tδ by

Q(Tδv,φ)=pa∫M Wδ^{p−1}vφ,

and Aδ=Πδ^perp(Id−Tδ)|_{Kδ^perp}.

## Theorem

There are δ0>0 and C<∞, independent of ξ∈∂M and 0<δ<δ0, such that Aδ is invertible and ||Aδ^{-1}||<=C.

## Proof

1. The rescaled Fermi metrics tend in C²_loc to the Euclidean halfspace metric, uniformly in ξ. The cut-off kernel Gram matrix converges to the positive definite matrix ∫_{R^n_+}∇Zα·∇Zβ. Also

||(Id−Tδ)K^αδ||_H→0.

Here are explicit cutoff estimates. The slowest Jacobi mode satisfies |Z|<=C(1+|z|)^{2−n}, |∇Z|<=C(1+|z|)^{1−n}. Hence cutting it off at rescaled radius R has D^{1,2} error <=C R^{−(n−2)/2}; the same bound applies to the cutoff-gradient annulus. For any fixed η<r0/2, the Fermi metric differs from Euclidean by O(η) on the physical η-ball. Testing against an H-unit vector and splitting there gives a geometric error <=Cη+C(δ/η)^{(n−2)/2}. The nonlinear-potential cutoff error is bounded by Hölder, using ||U^{p−1}||_{L^{n/2}(|z|>R)}<=C R^{−2}. The interior lower-order term is <=C||Kδ||_L2, with norms O(δ^{1/2}) for n3, O(δ sqrt|logδ|) for n4, O(δ) for n>=5. The boundary curvature term is <=C||Kδ||_{L²(∂M)}, which is O(sqrt(δ|logδ|)) for n3 and O(sqrtδ) for n>=4, by the trace theorem for the test vector. All constants are uniform in ξ. First let δ→0, then η→0. The Gram convergence follows by the same estimates. This proves the stated kernel residual and controls every physical cutoff error.

2. If the estimate failed, choose δ_i→0, ξ_i, v_i∈K_i^perp with ||v_i||_Q=1 and ||A_i v_i||_Q→0. Write (Id−T_i)v_i=r_i+Σ c_iα K_iα, with r_i→0 in H. Testing against K_iβ and using self-adjointness gives

Σ c_iα Q(K_iα,K_iβ)=Q(v_i,(Id−T_i)K_iβ)=o(1).

The Gram limit makes every c_iα→0. Thus the full residual (Id−T_i)v_i tends to zero in H.

3. Passing weakly in H gives v_i⇀v. For a fixed smooth test φ the potential term tends to zero: outside a fixed small boundary ball the weight W_i^{p−1} tends uniformly to zero; inside the ball Hölder bounds it by C||φ||_{L^{2n/(n−2)}(ball)}, which tends to zero with the ball radius. Therefore Q(v,φ)=0, so v=0.

4. Rescale at (ξ_i,δ_i): V_i(z)=δ_i^{(n−2)/2}v_i(F_{ξ_i}(δ_i z)). Local weak compactness gives V_i⇀V in D^{1,2}(R^n_+) and locally strongly in L². Rescaling the weak equation yields

−ΔV=pa U^{p−1}V, ∂νV=0.

Orthogonality against K_iα passes to ∫∇V·∇Zα=0; tails vanish by Cauchy-Schwarz and the finite Dirichlet norms of Zα.

The halfspace linearized kernel is exactly span{Z0,...,Z_{n−1}}. Indeed, divide V by U and use conformal covariance: the resulting equation on a round hemisphere of radius 1/2 is −Δw=4n w with Neumann boundary. The conformal energy identity puts w in H¹; the missing stereographic boundary point has zero H¹ capacity. Even reflection across the equator identifies this eigenspace with the even degree-1 spherical harmonics, precisely n dimensions. Thus the stated orthogonality forces V=0.

5. It follows that the potential energy vanishes. Inside |z|<R this follows from local strong L² convergence. Outside,

∫_{M\B_{Rδ_i}(ξ_i)}W_i^{p−1}v_i² <= C (∫_{|z|>R}U^{2n/(n−2)})^{2/n},

by Hölder and the uniform Sobolev norm of v_i. This bound tends to zero as R→∞. Hence ∫W_i^{p−1}v_i²→0. Testing the full residual against v_i now gives

1−pa∫W_i^{p−1}v_i²=o(1),

a contradiction.

6. For each fixed δ, Tδ is compact on H, because Wδ is smooth bounded and H¹ embeds compactly into L² on the compact manifold. Thus Aδ is self-adjoint Fredholm of index zero on Kδ^perp. The proved lower bound implies bijectivity, completing the proof.

## Consequence: a small projected nonlinear correction

Let S:H*→H be the Q-Riesz solution map. The cut-off bubble residual

rδ=Πδ^perp[Wδ−S(a Wδ^p)]

tends to zero in H, by exactly the same local-rescaling/tail argument. For the nonlinearity (u_+)^p, the Sobolev/Hölder estimates give uniformly

||N(φ)−N(ψ)||_{H*} <= C (||φ||_H+||ψ||_H)^min(1,p−1) ||φ−ψ||_H

on a small H-ball (with the usual harmless bounded-W factor when p>=2). The uniform inverse and contraction mapping therefore give a unique small φδ∈Kδ^perp, ||φδ||_H<=C||rδ||_H, solving the projected nonlinear equation. This does NOT make the kernel residual vanish. It also supplies no sharp rate or C² reduced-energy expansion.

If a parameter choice kills the kernel residual, the resulting actual solution is nonnegative by testing its equation against its negative part and using positivity of Q; the strong maximum principle makes a nonzero solution strictly positive.

## Explicit limits of this lemma

The physical cutoff radius may also shrink: if ρ_i→0 and δ_i/ρ_i→0, compare the fixed-radius and ρ_i-cutoff bubbles and Jacobi modes. Their H¹ difference is <=C(δ_i/ρ_i)^{(n−2)/2}; the potential difference in L^{n/2} is <=C(δ_i/ρ_i)². Gram matrices and kernel projections therefore differ by o(1), and the inverse survives by operator-norm perturbation. Thus the lemma applies to bubbles supported inside individual shrinking gluing patches.

The estimates are uniform over a C²-compact family of smooth metrics on one fixed compact manifold, provided λ1 is uniformly bounded below by a positive number and uniform boundary collar/Fermi radii exist. If uniform inversion failed, take a C²-convergent subsequence of the metrics and repeat the contradiction proof, using the uniformly coercive Q forms. All cutoff estimates above depend only on these common geometric bounds. In particular, for one fixed final C∞ graph-glued domain, moving centers through infinitely many bumps cause no loss whatsoever: the boundary is compact and smooth, so the needed common constants exist. A family of sufficiently small C³ boundary-graph changes pulled back by smooth collar diffeomorphisms is covered whenever its resulting metrics form such a C²-compact family.

The theorem proves a qualitative global inverse and small projected correction on a fixed positive-Yamabe manifold. It does not control the correction sharply relative to an arbitrarily tiny engineered shape-Hessian well; that requires quantitative weighted estimates. It does not prove nonlinear gluing, n>=7 existence, or low-dimensional compactness.
