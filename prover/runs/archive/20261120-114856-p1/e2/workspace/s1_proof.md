## Universal convergence for one-step blocks
Let the distinct active eigenvalues be $\lambda_1,\ldots,\lambda_m$, and write $u_i=P_i r_0/\|P_i r_0\|$. Every normalized residual belongs to the unit sphere in $\operatorname{span}\{u_i\}$. For $y=\sum c_i u_i$, put $\mu=\sum\lambda_i c_i^2$ and $v=\sum(\lambda_i-\mu)^2c_i^2$. A one-step exact minimization has step length $1/\mu$, so its normalized residual map is
$$T(y)=(\mu I-A)y/\sqrt v.$$
Nontermination implies $v(y_k)>0$.

For central moments $m_j=\sum c_i^2(\lambda_i-\mu)^j$, we have $m_1=0$, $m_2=v$, and
$$v(Ty)=m_4/v-(m_3/v)^2.$$
Consequently
$$v(Ty)-v(y)=\frac1v\sum_i c_i^2\left[(\lambda_i-\mu)^2-\frac{m_3}{v}(\lambda_i-\mu)-v\right]^2\ge0.$$
Variance is bounded on the finite spectrum, so $v(y_k)\to v_\infty\ge v(y_0)>0$. The map $T$ and the variance increment are continuous on a neighborhood of the orbit closure. Every cluster point has zero variance increment, and therefore is supported on the roots of a nonzero quadratic. Positive limiting variance excludes one-point support, so it has exactly two distinct active eigenvalues.

For any pair $a<b$, let the squared coefficient on $a$ be $p$. Its variance is $p(1-p)(b-a)^2=v_\infty$, which has at most two solutions for $p$. There are finitely many spectral pairs and finitely many coefficient sign choices; hence the complete normalized orbit has a finite cluster set. On a two-point support, $T$ exchanges the squared coefficients $p$ and $1-p$. Moreover $(\mu-a)(\mu'-a)=(\mu-b)(\mu'-b)=v$, so $T^2y=y$, including its signs.

It follows by compactness and continuity that $\|y_{k+2}-y_k\|\to0$. Finally, a bounded sequence with finite cluster set and increments tending to zero converges: otherwise, disjoint small balls about its finitely many cluster points would require infinitely many transitions through the complement, producing another cluster point. Apply this elementary observation to $y_{2k}$. Thus every nonterminating one-step orbit has a convergent even subsequence.

The symbolic identities are checked in `workspace/s1_checks.py`.
