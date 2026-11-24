For each \(d\in\{2,3\}\), let \(X_{n,d}\) consist of \(n\) independent points uniformly distributed in \([0,1]^d\), using ordinary Euclidean distance without periodic boundary conditions. At parameter \(a\geq0\), define the Čech complex by
\[
\mathcal C_a(X_{n,d})=\left\{\sigma\subseteq X_{n,d}:\bigcap_{x\in\sigma}\overline B(x,\sqrt a)\neq\varnothing\right\},
\]
where \(\overline B(x,r)\) is the closed Euclidean ball of radius \(r\). Compute persistent homology in degree one over the field \(\mathbb F_2\) of two elements. Let \(D_{n,d}\) be the multiset of birth–death pairs \((b,\delta)\) of all positive-length intervals, so \(0<b<\delta<\infty\); zero-length intervals are discarded, multiplicities are retained, and no death-time cutoff is imposed.

Assign to each pair the reduced coordinate
\[
s(b,\delta)=\sqrt{\tfrac12\log(\delta/b)},
\]
with natural logarithms. Writing \(m_{n,d}=|D_{n,d}|\), define the empirical probability measure
\[
\widehat\mu_{n,d}=\frac1{m_{n,d}}\sum_{(b,\delta)\in D_{n,d}}\delta_{s(b,\delta)}
\]
when \(m_{n,d}>0\), where \(\delta_x\) denotes unit point mass at \(x\); when \(m_{n,d}=0\), set \(\widehat\mu_{n,d}=\delta_1\).

You may assume that \(\widehat\mu_{n,d}\) converges weakly in probability to a deterministic probability measure \(\mu_d\) on \([0,\infty)\), meaning that its integrals against bounded continuous functions converge in probability to those of \(\mu_d\). You may also assume that the distribution function \(F_d(t)=\mu_d([0,t])\) has an expansion
\[
F_d(t)=c_dt+q_dt^2+o(t^2)\qquad(t\downarrow0),\qquad c_d>0.
\]
Define
\[
K_d=\frac12+\frac{q_d}{c_d^2},
\]
which is unchanged by multiplying the reduced coordinate by a positive constant, or equivalently by additively centering its logarithm. Determine the exact ordered pair \((K_2,K_3)\).

The answer was proved recently, so it is not an open problem: your task is to find it and prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at an answer that settles less than the question asks (a partial or conditional answer, "not known") is not acceptable, and neither is conceding: when an approach fails, try another.

Proving it means showing that the answer is right in every case the question covers, and that no other answer is.

Stop only when your proof is complete. When you stop, write in that response what you proved, and what is left.