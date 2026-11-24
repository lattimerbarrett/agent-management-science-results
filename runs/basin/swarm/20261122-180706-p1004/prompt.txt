Fix an integer \(d\geq1\), numbers \(\alpha,\beta,L>0\), and known constants \(0<g_-<1<g_+<\infty\), all independent of the sample size. Put \(D=[0,1]^d\) and \(U=(-1,2)^d\).

For \(t>0\), set \(r_t=\lceil t\rceil-1\) and \(\eta_t=t-r_t\). Define \(\mathcal H^t(L)\) to consist of restrictions to \(D\) of functions \(f\in C^{r_t}(U)\) satisfying
\[
\sum_{|\nu|\leq r_t}\|D^\nu f\|_{\infty,U}
+\max_{|\nu|=r_t}\sup_{\substack{x,y\in U\\x\ne y}}
\frac{|D^\nu f(x)-D^\nu f(y)|}{\|x-y\|_2^{\eta_t}}
\leq L.
\]
Here \(\nu\in\mathbb N_0^d\) is a multi-index, \(|\nu|\) is its total order, \(D^\nu\) is the corresponding partial derivative, and \(\|h\|_{\infty,U}=\sup_{x\in U}|h(x)|\).

Let \(\mathcal P\) be the class of probability laws of \((X,A,Y)\) such that \(X\in D\) has an unknown Lebesgue density \(g\) satisfying \(g_-\leq g(x)\leq g_+\) almost everywhere, \(|A|,|Y|\leq1\) almost surely, and the conditional means admit versions
\[
a(x)=\mathbb E(A\mid X=x)\in\mathcal H^\alpha(L),\qquad
b(x)=\mathbb E(Y\mid X=x)\in\mathcal H^\beta(L).
\]
No regularity is imposed on \(g\), and the conditional joint law of \((A,Y)\) given \(X\) is otherwise unrestricted. From \(n\) independent observations with common law \(P\in\mathcal P\), the target is
\[
\psi(P)=\mathbb E_P\{\operatorname{Cov}_P(A,Y\mid X)\}
=\mathbb E_P(AY)-\int_D a(x)b(x)g(x)\,dx.
\]
Define the minimax squared-error risk
\[
R_n=\inf_{T_n}\sup_{P\in\mathcal P}
\mathbb E_{P^{\otimes n}}\bigl[(T_n-\psi(P))^2\bigr],
\]
where the infimum is over all measurable estimators based on the observations; estimators may use the fixed class parameters but not the unknown functions \(a,b,g\).

Writing \(w=(\alpha+\beta)/d\), determine the unique ordered pair \((\gamma,\kappa)\), as a function of the fixed parameters and for all \(w>0\), such that
\[
\log R_n=-\gamma\log n-\kappa\sqrt{\log n}+O(\log\log n)
\qquad(n\to\infty).
\]
All logarithms are natural, and the implicit constant may depend on the fixed class parameters.

The answer was proved recently, so it is not an open problem: your task is to find it and prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at an answer that settles less than the question asks (a partial or conditional answer, "not known") is not acceptable, and neither is conceding: when an approach fails, try another.

Proving it means showing that the answer is right in every case the question covers, and that no other answer is.

Stop only when your proof is complete. When you stop, write in that response what you proved, and what is left.