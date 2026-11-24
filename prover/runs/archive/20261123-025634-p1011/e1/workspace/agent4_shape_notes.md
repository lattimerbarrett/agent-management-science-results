# Established hemisphere shape calculation; not a compactness proof

Let Ω be the round unit n-hemisphere, Σ its equator, V its volume,
a=4(n−1)/(n−2), q=2n/(n−2), b=(n−2)/n, R=n(n−1).
Consider Q(Ω,w)=[∫Ω(a|∇w|²+Rw²)+2∫Σ H w²]/(∫Ω w^q)^b.
For a normal graph deformation f of the equator and w=1+t v, assume
∫Σ f=0 and ∫Ω v=0. Reflection in Σ makes Vol(Ω_t)−V and
∫Σ_t H odd in t. Thus the pure shape second variation is zero.
H'f=−(ΔΣ+n−1)f and direct differentiation gives

V^b Q''=2a∫Ω(|∇v|²−n v²)+8∫Σ(H'f)v.

The quadratic form on v is nonnegative, kernel first Neumann spherical
harmonics. For f orthogonal to degrees 0 and 1, minimizing gives
(Δ+n)v=0, ∂νv=−(2/a)H'f. Write Λ for this equation's DN map.
Then

V^b Q''=−(8/a) <H'f,Λ^{-1}H'f>.

On equatorial spherical harmonics of degree L≥2,
μ_L=2 Γ(L/2)Γ((L+n+1)/2) / [Γ((L−1)/2)Γ((L+n)/2)] >0.
Hence the shape Hessian is diagonal and negative with eigenvalues
−(8/a)[(L−1)(L+n−1)]²/μ_L. Degrees 0,1 are Möbius kernels.
Derivation: the regular radial solution is sin(θ)^L times
2F1((L−1)/2,(L+n)/2;L+n/2;sin²θ); Gauss continuation at θ=π/2
has exponents 0,1/2, and the derivative/value ratio yields μ_L.

For Euclidean graph homogeneous term P_d, stereographic normal displacement
is η=2P_d/(1+r²), so at the omitted equatorial point η~ρ^(2−d).
Its H^(3/2) energy is finite for n>2d and logarithmic for n=2d.
This calculation alone does NOT give the Pohozaev scale-derivative sign.

Attempted next lemma fails numerically: let A_de be the positive quadratic
form given by the negative shape Hessian on compactified polynomial jets.
The scale derivative involves B_de=(d+e−2)A_de. For n=19, angular degree
ell=2, graph degrees d=2,4,6,8, all satisfying 2d<n, the normalized B has
one negative eigenvalue ≈−0.00117202234. Formula verification uses Jacobi
moments checked by independent quadrature and spectral cutoffs through
100000. This is numerical evidence, not a rigorous infinite-series-tail bound;
more importantly it is not a counterexample to the original theorem.

Files:
- agent4_shape_checks.py: symbolic coefficients plus numerical DN checks.
- agent4_jet_matrix.py: spectral Jacobi matrix construction.
- agent4_verify_negative.py: independent quadrature and cutoff stability.

The missing compactness steps are major: all-dimensional local blowup
Pohozaev control for arbitrary boundary, selection/simplicity, high-order
geometry/Green asymptotics, and applying a suitable positive-mass theorem.
No proof of those is supplied here.
