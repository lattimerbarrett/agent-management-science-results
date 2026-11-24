For integers \(1\leq m\leq n\leq 3\), define the affine complex fourfold
\[
X_{m,n}=\operatorname{Spec}\!\left(
\frac{\mathbb C[a,b,u,v,p,q]}
{\bigl(p^2-uv,\ q^2-(u-4a^m)(v-4b^n)\bigr)}
\right).
\]
These varieties are normal and Gorenstein. A projective crepant resolution of \(X_{m,n}\) means a projective birational morphism \(f:Y\to X_{m,n}\) from a smooth complex variety such that \(K_Y=f^*K_{X_{m,n}}\) for compatible canonical divisors; projectivity is relative to \(X_{m,n}\), not necessarily over \(\mathbb C\).

Determine, as an explicit finite set of ordered pairs, the complete exceptional set
\[
\mathcal E=\bigl\{(m,n)\in\mathbb Z^2:1\leq m\leq n\leq3,\quad X_{m,n}\text{ admits no projective crepant resolution}\bigr\}.
\]

The answer was proved recently, so it is not an open problem: your task is to find it and prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at an answer that settles less than the question asks (a partial or conditional answer, "not known") is not acceptable, and neither is conceding: when an approach fails, try another.

Proving it means showing that the answer is right in every case the question covers, and that no other answer is.

Stop only when your proof is complete. When you stop, write in that response what you proved, and what is left.