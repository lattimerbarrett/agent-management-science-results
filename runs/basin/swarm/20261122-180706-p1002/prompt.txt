Let \(k\) be an arbitrary field. Define a ten-dimensional unital \(k\)-algebra \(A\) with basis
\[
e_1,e_2,z,a,b_1,b_2,w_1,w_2,u,v.
\]
The elements \(e_1,e_2\) are orthogonal idempotents with \(e_1+e_2=1\). Assign source and target labels by
\[
z:1\to1,\qquad a:1\to2,\qquad b_1,b_2,u:2\to1,\qquad w_1,w_2,v:2\to2.
\]
For a non-idempotent basis element \(d:i\to j\), impose \(e_i d=d=d e_j\), with its other products with the idempotents equal to zero. The only nonzero products of two non-idempotent basis elements are
\[
b_1z=w_1b_1=w_2b_2=u,\qquad b_2a=w_1^2=w_2^2=v.
\]
All other such products are zero, and multiplication is extended \(k\)-bilinearly.

For a finite-dimensional \(k\)-algebra \(B\) and a unital right \(B\)-module \(M\), let \(\operatorname{pd}_B M\) be the least length of a projective resolution of \(M\), or \(+\infty\) if no finite projective resolution exists. Define the right little and big finitistic dimensions by
\[
\operatorname{findim}B=\sup\{\operatorname{pd}_B M:M\text{ is finitely generated and }\operatorname{pd}_B M<\infty\},
\]
\[
\operatorname{Findim}B=\sup\{\operatorname{pd}_B M:M\text{ is any right }B\text{-module and }\operatorname{pd}_B M<\infty\}.
\]
These suprema take values in \(\mathbb Z_{\ge0}\cup\{+\infty\}\). Let \(A^{\mathrm{op}}\) be the algebra with the same underlying vector space as \(A\) and reversed multiplication. Determine, for every field \(k\), the exact ordered triple
\[
\bigl(\operatorname{findim}A,\operatorname{Findim}A,\operatorname{Findim}(A^{\mathrm{op}})\bigr).
\]

The answer was proved recently, so it is not an open problem: your task is to find it and prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at an answer that settles less than the question asks (a partial or conditional answer, "not known") is not acceptable, and neither is conceding: when an approach fails, try another.

Proving it means showing that the answer is right in every case the question covers, and that no other answer is.

Stop only when your proof is complete. When you stop, write in that response what you proved, and what is left.