# Full finite-dimensional quartic-profile minimum for n>=32

This result concerns the exact quadratic shape functional only. It does NOT prove a nonlinear solution or an infinite-gluing counterexample.

Let d=n−1, P2(x)=x1²−x2², P4(x)=|x|²P2(x) on R^d. Transfer a graph h to the equatorial sphere by stereographic projection and its normal-distance conformal factor. Let Q be the positive quadratic form in the shape-Hessian lemma, omitting the universal positive factor α²/2. Define the sector constants A,B,C by

Q(P2,P2)=A ||P2||²_{L²(S^{d−1})},
Q(P2,P4)=B ||P2||²,
Q(P4,P4)=C ||P2||².

Then A,B,C>0, and agent2_quartic_all_dimensions_proof.md proves 4B²−3AC>0 for every n>=32 using exact gamma/telescoping certificates.

Normalize A=1 by dividing Q by A, and replace B,C accordingly. Let f=−P2+P4. At bubble center ξ and scale λ, its effective graph is f(ξ+λx)/λ, modulo affine functions (which are in the gauge kernel). At ξ=0, writing z=λ²,

Q(f(λ·)/λ)=||P2||²(z−2Bz²+Cz³).

The smaller scale critical point is

z−=(2B−sqrt(4B²−3C))/(3C)=1/(2B+sqrt(4B²−3C))>0.

There Q has negative scale second derivative. We prove its full translation Hessian is also negative definite, so −Q has a strict nondegenerate local minimum.

## Cubic constants in terms of A and B

Let q3 and qt be Q constants per angular L² norm on harmonic cubic graphs H3 and trace cubic graphs |x|²H1. Then, before normalizing A,

q3=((n−1)B−(n+3)A)/2,
qt=2(A+B)/(n−1).

Proof: in the Gegenbauer decomposition, the harmonic-cubic mode j has the same total equatorial degree and DtN multiplier as quadratic mode j+1. Their full summands have ratio (j+1)(j+n+3). For trace cubic mode j>=1 the corresponding quadratic mode is j−1, with ratio 4j(j+n)/(n−1)². The j=0 trace mode is gauge. The quadratic-sector coefficient ratio R_k=2(k+1)(k+n+1)/(n−1)−1 therefore converts both sums to the asserted linear combinations of A and B. These termwise ratios were checked symbolically for arbitrary n,j in agent4_mixed_spectral_exact.py.

## Translation Hessian

Write P2=x^T D x, D=diag(1,−1,0,...), T=tr(D²)=2, and a_i=D_ii. At ξ=0,

∂_{ξ_i}[f(ξ+λx)/λ] ≡ λ²∂_iP4,
∂²_{ξ_i}[f(ξ+λx)/λ] ≡ λ∂²_iP4

modulo affine gauge functions. Decompose

∂_iP4=H3_i+|x|²L_i,
H3_i=2x_iP2−4a_i|x|²x_i/(d+2),
L_i=2(d+4)a_i x_i/(d+2).

On the unit S^{d−1}, with normalized angular averages,

average(H3_i²)=8T/[d(d+2)(d+4)]+16a_i²/[(d+2)²(d+4)],
average(L_i²)=4(d+4)²a_i²/[d(d+2)²].

If S_i is the quadratic matrix of ∂²_iP4, then tr(D S_i)=2T+8a_i². Rotational invariance of the quadratic sector gives the coefficient of ξ_i² in Q, divided by |S^{d−1}|A, as

z²{q3 average(H3_i²)+qt average(L_i²)}+(−z+z²B)(4T+16a_i²)/[d(d+2)],

where q3,qt now are normalized by A as well.

For a_i=0 this equals a positive multiple of z(−1+z M0), where

M0=2(n+1)B/(n+3)−1 < 2B.

For a_i²=1 it similarly equals a positive multiple of z(−1+z M1), where

M1−2B=−(n−9)/(3(n−1))*(1+4B/(n+3)) < 0

for n>9. These simplifications are checked symbolically for arbitrary n in the code. At z=z−, both signs are strictly negative because z−=1/(2B+sqrt(4B²−3C)).

The profile is invariant under each coordinate reflection, so the translation Hessian is diagonal and the mixed translation/scale block vanishes. Thus Q has a strict nondegenerate maximum at (ξ,λ)=(0,sqrt(z−)); equivalently the actual negative shape energy has a strict nondegenerate local minimum.

Combining with the exact all-n>=32 discriminant certificate proves this finite-dimensional proposition for every integer n>=32. A separate exact rational enclosure of the n32 square root certifies the two translation signs as an independent check.

Remaining beyond this proposition: uniform nonlinear reduction on shrinking supports, C² control of its reduced-energy remainder, fixed smooth infinite gluing, all required solution bounds, n7 through n31 constructions, and all n3 through n6 compactness.
