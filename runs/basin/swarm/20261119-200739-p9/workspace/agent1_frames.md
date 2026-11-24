# Fixed finite row frames cannot yield non-scalar sharpness

Let M be any measurable invertible root (polar decomposition identifies its norm and pairwise characteristic with the positive root of W=(M* M)^(p/2)). Suppose M(x)=D(x)T_j on each of N measurable phases, with D positive diagonal and T_j fixed invertible.

For a fixed nonzero v, u_v=|M^{-*}v|^{-p} has scalar Ap characteristic at most the matrix characteristic A: indeed |M(y)^{-*}v|/|M(x)^{-*}v| is at most ||M(x)M(y)^{-1}||, and the exact nested integrals give the assertion. Also u_v |<f,v>|^p <= |Mf|^p pointwise by Cauchy-Schwarz.

For v_jk=T_j* e_k, on phase j one has |M^{-*}v_jk|=1/d_k, hence u_v_jk=d_k^p. Scalar Hilbert Ap estimates, componentwise commutation, and l2/lp equivalence give
||MHf||_p^p <= C_p sum_jk ||H<f,v_jk>||_Lp(u_v_jk)^p <= C_p (2N) A^(p S(p)) ||Mf||_p^p,
where S(p)=max(1,1/(p-1)). No constants depend on the directions or conditioning of T_j.

Dual roots M^{-*}=D^{-1}T_j^{-*} have the same number N of fixed row frames. Applying the result at q and using characteristic duality gives the additional N^(1/q) factor. Thus
||H||_Lp(W) <= C_p N^min(1/p,1/q) A^S(p).

If the candidate F(p)=1+1/[p(p-1)] is sharp along weights of characteristic A, these weights must use at least order A^min(1,1/(p-1)) fixed row frames (up to constants). In particular binary h, or any uniformly bounded number of h-values, cannot attain F(p). This is an obstruction only, not an exact-beta proof.
