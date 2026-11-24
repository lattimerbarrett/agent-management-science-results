Fix an integer \(n\geq5\). Define \(\mathcal E_n\subseteq\{2,4,6,\ldots\}\) as follows. An even integer \(\beta\geq2\) belongs to \(\mathcal E_n\) if the following property holds for every choice of data \((M,g,P,f_0)\) satisfying these assumptions:

- \((M,g)\) is a smooth connected compact \(n\)-dimensional Riemannian manifold without boundary, and its scalar curvature is nonnegative everywhere.
- \(P\in M\) has a coordinate neighborhood with coordinates \(x\), centered at \(P\), in which \(g_{ij}=\delta_{ij}\).
- \(f_0\in C^\infty(M,\mathbb R)\), with \(f_0(P)=0\) and \(f_0<0\) on \(M\setminus\{P\}\). In the specified coordinates,
  \[
  f_0(x)=-Q_\beta(x)+O(|x|^{\beta+1}),
  \]
  where \(Q_\beta:\mathbb R^n\to\mathbb R\) is a polynomial satisfying \(Q_\beta(tx)=t^\beta Q_\beta(x)\) for every \(t>0\), and \(Q_\beta(x)>0\) whenever \(x\neq0\).

The required property is that there exists \(\varepsilon>0\), allowed to depend on these data, such that for every constant \(0<\lambda<\varepsilon\), the equation
\[
-\Delta_g u=(f_0+\lambda)u^{(n+2)/(n-2)}\qquad\text{on }M
\]
has no smooth solution satisfying \(u>0\) everywhere. Here \(\Delta_g=\operatorname{div}_g\nabla_g\), so it equals \(\sum_i\partial_{x_i}^2\) in the specified flat coordinates.

Determine \(\mathcal E_n\) explicitly as a function of \(n\).

The answer was proved recently, so it is not an open problem: your task is to find it and prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at an answer that settles less than the question asks (a partial or conditional answer, "not known") is not acceptable, and neither is conceding: when an approach fails, try another.

Proving it means showing that the answer is right in every case the question covers, and that no other answer is.

Stop only when your proof is complete. When you stop, write in that response what you proved, and what is left.