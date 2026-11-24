# A discrete logarithmic barrier at an interior 2s-support cycle family

Assume the general spectral reduction and Lyapunov identities. Suppose an orbit, after its last coordinate annihilation, has omega set contained in the relative interior of one fixed face S with exactly 2s spectral nodes. Then no initially nonzero outside coordinate can have limiting two-step multiplier -1.

Proof. Write C=H_infinity^2 and Delta_S(z)=product_{i in S}(z-lambda_i). On every omega cycle, the monic degree-s polynomials P,Q obey P Q=Delta_S+C. There are only finitely many monic factor pairs; continuity and connectedness of the even omega set therefore imply p_{2k}->P and p_{2k+1}->Q (with these labels possibly swapped for the other parity). Set R_k=p_k p_{k+1}, C_k=H_k H_{k+1}. Thus R_k->R=Delta_S+C, C_k<=C, and R_k-R has degree at most 2s-1.

The assumed interior containment gives w_{k,i}>=a>0 eventually for all i in S. Let mu=lambda_j be an outside node with R(mu)=-C, and let L_i(mu) be the degree-(2s-1) Lagrange interpolation coefficients on S. Then sum L_i=1 and, exactly,

 R_k(mu)+C = sum_{i in S} L_i(mu)[R_k(lambda_i)-C].

Define the strictly positive quantity

 I_k=|y_{k,j}| product_{i in S}|y_{k,i}|^{L_i(mu)}.

It is well-defined after the last annihilation. Exact two-step multiplication gives

 log I_{k+2}-log I_k = log|R_k(mu)| + sum_i L_i(mu)log|R_k(lambda_i)| -2log C_k.

Set g_k=C-C_k>=0 and delta_ki=R_k(lambda_i)-C. Taylor expansion around C and -C, using the exact interpolation identity to cancel all linear delta terms, gives

 log I_{k+2}-log I_k >= 2 log(C/C_k)-B sum_i delta_ki^2.

But delta_ki=C_k(M_ki-1)-g_k, where y_{k+2,i}=M_ki y_{k,i}. Since all active weights exceed a,

 sum_i delta_ki^2 <= B1 ||y_{k+2}-y_k||^2+B2 g_k^2.

For large k the positive linear term 2log(C/C_k) absorbs B2 g_k^2. Hence

 log I_{k+2}-log I_k >= -B3 ||y_{k+2}-y_k||^2.

Square summability of the two-step residual increments gives a finite lower bound for log I along either parity. On the other hand every outside weight tends to zero, while all factors |y_{k,i}|, i in S, stay bounded above and below. Thus I_k->0, a contradiction.

This theorem is conditional on the entire omega set lying in the relative interior of one 2s-support face. It does not rule out transitions through lower-support faces or establish universal convergence. It nevertheless rules out all proposed counterexamples consisting of a compact interior full-2s cycle polytope plus nonzero -1 inactive modes.
