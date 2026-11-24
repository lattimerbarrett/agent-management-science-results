Let \(\omega=\{0,1,2,\ldots\}\), and write \(\overline X=\omega\setminus X\). Fix a standard effective enumeration \((W_e)_{e\in\omega}\) of all computably enumerable sets of pairs \((x,F)\), where \(x\in\omega\) and \(F\subseteq\omega\) is finite, using a computable coding of finite sets. Define
\[
\Gamma_e(B)=\{x:\exists F\subseteq B\text{ finite }\ ((x,F)\in W_e)\}.
\]
Write \(A\leq_e B\) if \(A=\Gamma_e(B)\) for some \(e\), and write \(A\equiv_e B\) if both \(A\leq_e B\) and \(B\leq_e A\). The enumeration degree of \(A\) is \(\mathbf d_e(A)=\{B:B\equiv_e A\}\). Define the skip of \(A\) by
\[
A^\diamond=\omega\setminus\{e:e\in\Gamma_e(A)\}.
\]
An enumeration degree \(\mathbf a\) is **total** if it contains a set \(B\) with \(\overline B\leq_e B\), and **cototal** if it contains a set \(B\) with \(B\leq_e\overline B\). It is **weakly cototal** if it contains a set \(B\) such that \(\mathbf d_e(\overline B)\) is total.

For each integer \(m\geq1\), a set belongs to \(\Sigma_m^0\), respectively \(\Pi_m^0\), if its membership relation can be expressed using \(m\) alternating blocks of quantifiers over \(\omega\), beginning with an existential, respectively universal, block, applied to a computable predicate. Dummy quantified variables are allowed, and no set parameters are allowed. Treat \(\Sigma\) and \(\Pi\) as labels, with \(\sigma_m^0\) denoting the corresponding class.

Determine the exact set
\[
\mathcal E=\left\{(\sigma,m)\in\{\Sigma,\Pi\}\times\{1,2,3,\ldots\}:\exists A\in\sigma_m^0\ \bigl[\mathbf d_e(A)\text{ is weakly cototal and }\mathbf d_e(A^\diamond)\text{ is not cototal}\bigr]\right\}.
\]

The answer was proved recently, so it is not an open problem: your task is to find it and prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at an answer that settles less than the question asks (a partial or conditional answer, "not known") is not acceptable, and neither is conceding: when an approach fails, try another.

Proving it means showing that the answer is right in every case the question covers, and that no other answer is.

Stop only when your proof is complete. When you stop, write in that response what you proved, and what is left.