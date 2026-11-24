# No second critical radius, conditional ONLY on local Pohozaev sign

This uses agent2_conditional_simple_estimate.md. Suppose p_i are isolated boundary
blowups with the standard bubble C2 profile, but a second critical radius r_i of
r^a average(u_i) tends to zero. The bubble profile gives r_i/eps_i->infinity.
Apply the conditional sharp estimate up to r_i (the endpoint derivative may be
zero; its proof only requires the corresponding nonpositive endpoint inequality).

Set W_i(y)=r_i^a u_i(p_i+r_i y), N_i=r_i^a M_i->infinity. Then

            N_i W_i(y)<=C|y|^(2-n), 0<|y|<=1.

The original isolation bound and annular Harnack extend this estimate to a fixed
annulus 1/2<=|y|<=2 (after fixing sufficiently small coordinate neighborhoods).
Standard elliptic compactness thus gives, after subsequence,

       N_i W_i -> h in C2_loc(B_2^+\{0}),
       Delta h=0, partial_n h=0, 0<h<=C|y|^(2-n).

The coefficient of the fundamental singularity is strictly positive. To see
this without assuming it, use the exact normalized scalar-flat/minimal flux:
the integral of A u_i^p on a fixed multiple R eps_i of the bubble scale is
>=c/M_i by bubble convergence. Nonnegativity then gives the same lower bound
for total outward flux at larger radii. Equivalently the fundamental coefficient
of h is >=c>0. The weak estimate from the sharp-bound proof gives tail mass
<=C R^(-2+p eta)/M_i, so in fact that coefficient is the standard bubble one.
Only strict positivity is needed.

Even reflection and Bocher's theorem give

                 h(y)=A|y|^(2-n)+b(y), A>0,

where b is harmonic and even across y_n=0 on B_2. Its hemispherical mean is
constant B=b(0). The second-critical-radius condition passes to the limit at
|y|=1, hence

  0=d/dr[r^a average(h)]_(r=1)=a(B-A),

so B=A>0.

For the harmonic half-sphere Pohozaev flux

 P(r,h)=int_(S_r^+)[a h h_r-r|grad h|^2/2+r h_r^2],

one has

       lim_(r->0)P(r,h)=-(n-2)^2 |S^(n-1)| A B/4<0.

Therefore ANY scale-uniform local theorem asserting nonnegative limiting
normalized flux at an isolated boundary blowup excludes the second radius.
This proves isolated blowups are simple CONDITIONAL ON THAT SIGN THEOREM.
No global compactness or sign theorem is claimed here.
