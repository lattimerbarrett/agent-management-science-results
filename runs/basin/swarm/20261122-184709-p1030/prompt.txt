Let \(h\ge 2\) and \(s\ge 1\) be integers, and set
\[
a=1+4h^2,\qquad p=2as-2h,\qquad q=p+a,\qquad r=p+\frac{p^2+1}{a}.
\]
Let \(Y_{h,s}=\Sigma(p,q,r)\) be the Brieskorn integral homology sphere. Explicitly, it is the boundary of
\[
\{(z_1,z_2,z_3)\in\mathbb C^3:z_1^p+z_2^q+z_3^r=\eta\}\cap B^6_\epsilon,
\]
where \(B^6_\epsilon\) is the closed ball of radius \(\epsilon\), \(\epsilon>0\) is sufficiently small, and the nonzero complex number \(\eta\) is sufficiently small relative to \(\epsilon\). Give this boundary the orientation induced by the complex surface.

Work over \(\mathbb F=\mathbb Z/2\mathbb Z\), and ignore absolute gradings in the minus-flavour Heegaard Floer homology. Define the nonnegative integer multiplicities \(m_\ell=m_\ell(h,s)\) by its elementary-divisor decomposition
\[
HF^-(Y_{h,s};\mathbb F)\cong\mathbb F[U]\oplus
\bigoplus_{\ell\ge1}\left(\mathbb F[U]/(U^\ell)\right)^{\oplus m_\ell}.
\]
Only finitely many \(m_\ell\) are nonzero. For a formal indeterminate \(t\), define the torsion-multiplicity polynomial
\[
P_{h,s}(t)=\sum_{\ell\ge1}m_\ell t^\ell\in\mathbb Z[t],
\]
so its coefficients are integer multiplicities, not elements of \(\mathbb F\). Put
\[
L=\max\bigl(\{0\}\cup\{\ell\ge1:m_\ell>0\}\bigr),\qquad d=\min\{h,s+1\},
\]
and retain the \(d\) consecutive degree positions ending at \(L\):
\[
Q_{h,s}(t)=\sum_{\substack{\ell\ge1\\L-d<\ell\le L}}m_\ell t^\ell.
\]
Determine \(Q_{h,s}(t)\) explicitly as a function of \(h,s,t\), including its exponents and integer coefficients.

The answer was proved recently, so it is not an open problem: your task is to find it and prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at an answer that settles less than the question asks (a partial or conditional answer, "not known") is not acceptable, and neither is conceding: when an approach fails, try another.

Proving it means showing that the answer is right in every case the question covers, and that no other answer is.

Stop only when your proof is complete. When you stop, write in that response what you proved, and what is left.