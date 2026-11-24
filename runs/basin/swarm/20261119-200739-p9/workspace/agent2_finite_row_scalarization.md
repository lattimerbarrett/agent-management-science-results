# Finite row-direction scalarization (proved)

Let M be any invertible matrix root, W=(M* M)^(p/2), and A=[W]Ap. Assume R is partitioned into N measurable phases E_j and on each phase M(x)=D(x) T_j, where T_j are fixed invertible 2x2 matrices and D(x) is positive diagonal. The T_j may depend on A or other parameters: constants below do not depend on their directions or condition numbers.

For every nonzero fixed v define u_v(x)=|M(x)^(-*)v|^(-p). Agent_1 observed the stronger DIRECT bound:
u_v(x)^(1/p)/u_v(y)^(1/p)=|M(y)^(-*)v|/|M(x)^(-*)v|
<=||M(y)^(-*)M(x)*||=||M(x)M(y)^(-1)||.
Taking the exact mixed averages from the problem gives [u_v]Ap<=A, with no duality constant or lemma needed.
For every f, Cauchy gives u_v |<f,v>|^p <= |Mf|^p.

Put v_jk=T_j*e_k. On E_j, M^(-*)v_jk=D^(-1)e_k, so u_vjk=d_k^p. By l2/lp norm equivalence,
int |MHf|^p <= C_p sum_jk int_Ej d_k^p |H<f,v_jk>|^p
<=C_p sum_jk int u_vjk |H<f,v_jk>|^p.
Apply the scalar sharp weighted Hilbert estimate to each scalar pairing, then use the pointwise Cauchy inequality:
||H||Lp(W) <= C_p (2N)^(1/p) A^max(1,1/(p-1)).
This invokes the ordinary scalar sharp Hilbert theorem but no matrix theorem beyond our proved duality lemma.

In particular triangular roots M=[[d1,d1 h],[0,d2]] whose h takes a bounded number of values cannot give a super-scalar optimal exponent. Neither allowing the finitely many values to depend on A nor making their angles degenerate helps: the constant is independent of T_j. A lower construction must use a number of distinct row directions growing with the characteristic, or another non-finite-frame mechanism.

By applying the same proof to the dual root M^(-*)=D^(-1)T_j^(-*) and using operator/characteristic duality, N^(1/p) can be improved to N^min(1/p,1/q), up to p-dependent constants. The lemma applies in particular to ANY root with K fixed values by choosing D=I,T_j=M_j. Thus all bounded-state constructions are excluded, not just triangular finite-h models.
