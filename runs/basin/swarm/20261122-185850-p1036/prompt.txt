Fix an integer \(n\ge2\). Write \(|E|\) for the \(n\)-dimensional Lebesgue measure of a measurable set, let \(B(x,r)=\{y\in\mathbb R^n:|y-x|<r\}\), and put \(B_1=B(0,1)\). For every nonempty bounded convex open set \(\Omega\subset\mathbb R^n\), let \(\lambda_1(\Omega)\le\lambda_2(\Omega)\) be the first two eigenvalues of the Dirichlet Laplacian \(-\Delta\), counted with multiplicity. Define
\[
\delta(\Omega)=\frac{\lambda_2(B_1)}{\lambda_1(B_1)}-\frac{\lambda_2(\Omega)}{\lambda_1(\Omega)},\qquad r_\Omega=\left(\frac{|\Omega|}{|B_1|}\right)^{1/n},
\]
and define the Fraenkel asymmetry by
\[
\mathcal A(\Omega)=\inf_{x\in\mathbb R^n}\frac{|\Omega\mathbin\Delta B(x,r_\Omega)|}{|\Omega|},
\]
where \(E\mathbin\Delta F=(E\setminus F)\cup(F\setminus E)\). Determine explicitly the set
\[
\mathscr P_n=\left\{p>0:\ \exists\,c_{n,p}>0\text{ such that }\delta(\Omega)\ge c_{n,p}\mathcal A(\Omega)^p\text{ for every nonempty bounded convex open }\Omega\subset\mathbb R^n\right\}.
\]
The constant \(c_{n,p}\) may depend on \(n\) and \(p\), but not on \(\Omega\).

The answer was proved recently, so it is not an open problem: your task is to find it and prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at an answer that settles less than the question asks (a partial or conditional answer, "not known") is not acceptable, and neither is conceding: when an approach fails, try another.

Proving it means showing that the answer is right in every case the question covers, and that no other answer is.

Stop only when your proof is complete. When you stop, write in that response what you proved, and what is left.