# Global convergence whenever the number of active distinct eigenvalues is at most s+2

This theorem holds for every restart length s, not only s<=3. Use the spectral reduction and Lyapunov identity from agent3_s1_proof.md. Let F be the normalized residual map and H the monic-polynomial residual norm. Let G=F^2. At every cluster point H=h>0, G(y)=y, and support has at least s+1 nodes. A support of <=s nodes terminates, so is absent in a nonterminating orbit.

If there are exactly s+1 nodes, barycentric orthogonality gives the reciprocal-involution map on squared weights, hence F^2(y)=y exactly (including signs; alternatively use the Lyapunov equality identity). Thus the even sequence is constant. A finite loss of a node from s+2 nodes reduces to this case, so assume the s+2 initial nodes all retain positive weights forever.

Put n=s+2, Delta(x)=prod_i(x-lambda_i), c_i=1/Delta'(lambda_i). Write q_k for the monic degree-s orthogonal polynomial under w_ki=y_ki^2 and H_k=H(y_k). There is a monic degree-one polynomial f_k(x)=x-t_k such that
  w_ki q_k(lambda_i)=H_k^2 c_i f_k(lambda_i).
To see this, the vector w_i q_i annihilates the s moment rows, and barycentric identities identify its two-dimensional nullspace with c_i times polynomials of degree<=1. The degree-one leading coefficient is H_k^2 because
  H_k^2=sum_i w_i q_i^2=sum_i c_i f_scaled(lambda_i)q_i
is the leading coefficient of f_scaled q, a degree n-1 polynomial. The degree of f_scaled is exactly one because H_k>0. The requirement that interpolation of q have degree<=s is sum_i c_i q_i=0, giving sum_i c_i^2 f_k(lambda_i)/w_i=0. Thus t_k is a weighted mean of the spectral nodes, with positive weights c_i^2/w_i; in particular it lies strictly inside their convex hull and never equals a node (otherwise q at that node would vanish and a residual coordinate would be lost).

Duality gives two exact identities:
  w_(k+2,i) / w_(k,i) is proportional to [f_(k+1)(lambda_i)/f_k(lambda_i)]^2;
  M_i(y_k):=G(y_k)_i/y_ki = (H_(k+1)/H_k) f_(k+1)(lambda_i)/f_k(lambda_i).
For the second, multiply the barycentric identities at k and k+1, and use w_(k+1,i)=w_ki q_k(lambda_i)^2/H_k^2.

We use the non-neutral minimal-support trapping lemma (agent4_trapping_lemma.md). Its proof is included here for completeness. If an even cluster point u has s+1 active nodes S and every outside multiplier differs from +1, choose a neighborhood where |M_j-1|>=c>0 outside S. Then sum_outside y_j^2 <= c^-2 ||G(y)-y||^2. On the face S, G's squared-weight map is the identity, so analyticity gives sum_active |G(y)_i^2-y_i^2| <= C sum_outside y_j^2. The total squared G-step sum is finite. Upon a sufficiently late visit to a smaller active-weight box around u, the remaining squared-step tail is too small to leave a larger active-weight box; inactive coordinates cannot cause exit since the last inside point and its successor have magnitude bounded by (1+c^-1)||G(y)-y||. Active signs remain fixed. Thus the orbit is trapped, outside weights sum finitely, and active weights have finite total variation, proving even convergence.

Now suppose, seeking a contradiction, the even sequence does not converge. Every even cluster point is either fully supported or has exactly n-1=s+1 active nodes. At a full-support cluster point all M_i=1 because G(u)=u. At a boundary cluster point the one outside multiplier must also equal +1, since otherwise the trapping lemma proves convergence. Active multipliers again equal +1. Consequently ALL M_i equal +1 at EVERY even cluster point. The same is true for odd cluster points (they are images under F of even cluster points, with the same two-cycle support and product multiplier). Compactness and continuity imply M_i(y_k)>0 for every i and every sufficiently large k.

The sign identity above now says f_(k+1)(lambda_i) and f_k(lambda_i) have the same sign at every spectral node. Since f_k is monic linear, t_k therefore remains forever in one fixed open spectral gap.

It remains to prove t_k monotone in that gap. Let nu_i=c_i^2/w_ki (normalization irrelevant); f_k is its monic degree-one orthogonal polynomial. The next dual polynomial f_(k+2) is degree-one orthogonal for nu_i f_k(lambda_i)^2/f_(k+1)(lambda_i)^2. If t_(k+1)<t_k, let c=t_(k+1) and S(c)=sum_i nu_i f_k(lambda_i)^2/(lambda_i-c). On the common gap S is strictly increasing and S(t_k)=sum_i nu_i f_k(lambda_i)=0. Thus S(c)<0. But S(c) is the numerator of the mean of x-c under nu_i f_k^2/f_(k+1)^2, so t_(k+2)<t_(k+1). The case t_(k+1)>t_k reverses both inequalities; equality forces equality thereafter. Hence t_k is monotone, bounded, converges to t, and has finite total variation.

For nodes lambda_i,lambda_l different from t, the exact ratio identity yields
  log(w_(k+2,i)/w_(k+2,l))-log(w_ki/w_kl)
  =2[log|lambda_i-t_(k+1)|-log|lambda_i-t_k|
      -log|lambda_l-t_(k+1)|+log|lambda_l-t_k|].
The right side is absolutely summable, because t_k has finite variation and stays away from these two nodes. Thus all even ratios of such weights tend to finite positive limits. If t equals a spectral node lambda_j, then w_kj tends to zero: otherwise a cluster two-cycle would have w_j>0 and barycentric identity q_j w_j=H^2 c_j f(lambda_j)=0, contradicting q_j q_next,j=h^2>0 on active nodes. Normalization now implies all even weights converge. On coordinates with positive limiting weight the even signs are eventually fixed because G-step lengths tend to zero. All other coordinates tend to zero. Therefore y_(2k) converges, contradicting the assumption.

Conclusion: every nonterminating orbit having at most s+2 initially active distinct eigenvalues has convergent normalized even residuals.
