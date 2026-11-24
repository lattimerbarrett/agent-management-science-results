# Conditional dimension reduction (NOT a complete solution)

Let (T) denote the unverified global assertion: for n>=3, the exterior of every smooth compact domain whose boundary has at least n-2 strictly positive tangential Levi eigenvalues everywhere is Oka.

If (T) holds, the following proved geometric arguments give S containing every n>=3 and N={2}.

1. If K is pseudoconvex and n>=3, the outer defining functions psi_epsilon=rho-epsilon exp(-A|z|^2) give decreasing smooth compact neighborhoods K_epsilon of K. On their boundaries rho=epsilon exp(-A|z|^2). Uniform smoothness gives L_rho(v)>=-C rho |v|^2 for rho>=0 and v in ker partial rho. On the common tangent space E=ker partial rho intersect ker partial |z|^2, dimension at least n-2, L_psi(v)>=epsilon exp(-A|z|^2)(A-C)|v|^2>0. Choose A>C. Thus (T) makes each exterior Oka. Their increasing union is C^n\K and is Oka directly from CAP, because each compact image f(Q) lies in one member.

2. For n>=3 take rho=(|z|^2-1)^2+||w||^2-2, z in C and w in C^{n-1}. The domain rho<=0 is smooth, compact, connected and strictly star-shaped. On each boundary, w-orthogonal tangent directions give n-2 positive Levi eigenvalues. At z=0, ||w||=1, the z direction is tangent with Levi -2, so K is not pseudoconvex. Assertion (T) would make its exterior Oka, excluding every n>=3 from N.

3. Independently of (T), 2 belongs to N: a negative tangential Levi eigenvalue of K gives a strictly pseudoconvex exterior boundary point. A holomorphic local peak glues to a bounded nonconstant continuous psh function on the exterior. CAP and bounded-subharmonic Liouville on C prohibit this. Full proof is in agent2_necessity.md.

The remaining universal S question would then be exactly whether 2 belongs to S. Neither this question nor (T) has been settled by the team.
