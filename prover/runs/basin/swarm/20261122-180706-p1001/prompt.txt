All rings below are commutative with identity, and an integral domain is required to satisfy \(1\ne0\). For each integral domain \(D\), let \(K=\operatorname{Frac}(D)\) be its field of fractions, let \(X\) be one indeterminate over \(K\), and define the ring of integer-valued polynomials by
\[
\operatorname{Int}(D)=\{f\in K[X]:f(a)\in D\text{ for every }a\in D\}.
\]
For any ring \(A\), its Krull dimension \(\dim A\) is the supremum of the lengths \(r\) of strict chains of prime ideals \(\mathfrak p_0\subsetneq\mathfrak p_1\subsetneq\cdots\subsetneq\mathfrak p_r\).

Determine explicitly the complete set
\[
\mathcal S=\bigl\{(\dim D[X],\dim\operatorname{Int}(D)):\ D\text{ is an integral domain and both displayed dimensions are finite}\bigr\}
\]
as a subset of \(\mathbb Z_{>0}^{\,2}\), where \(\mathbb Z_{>0}\) denotes the positive integers.

The answer was proved recently, so it is not an open problem: your task is to find it and prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at an answer that settles less than the question asks (a partial or conditional answer, "not known") is not acceptable, and neither is conceding: when an approach fails, try another.

Proving it means showing that the answer is right in every case the question covers, and that no other answer is.

Stop only when your proof is complete. When you stop, write in that response what you proved, and what is left.