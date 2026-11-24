Let \(\mathbb C_7\) be the completion of an algebraic closure of \(\mathbb Q_7\), with valuation \(v_7(7)=1\). For each integer \(r\geq1\), let \(\mathcal O_r=W(\mathbb F_{7^r})\) be the ring of integers in the unramified extension of \(\mathbb Q_7\) of degree \(r\), and let \(\operatorname{Tr}_r:\mathcal O_r\to\mathbb Z_7\) be its trace. For \(t\in\mathbb F_{7^r}\), write \([t]\) for its Teichmüller lift: \([0]=0\), and for \(t\ne0\), \([t]\) is the unique \((7^r-1)\)-st root of unity reducing to \(t\). Define the convergent Witt-ring-valued function
\[
 f_r(t)=[t]^{11}+\sum_{j=2}^{\infty}7^j[t]^{11\cdot7^j-19}.
\]
For each integer \(n\geq1\), choose a primitive \(7^n\)-th root of unity \(\zeta_{7^n}\in\mathbb C_7\), and define \(\chi_n:\mathbb Z_7\to\mathbb C_7^\times\) by \(\chi_n(z)=\zeta_{7^n}^{\,z\bmod7^n}\). Set
\[
 L_n(s)=\exp\!\left(\sum_{r=1}^{\infty}\frac{s^r}{r}\sum_{t\in\mathbb F_{7^r}}\chi_n\!\left(\operatorname{Tr}_r(f_r(t))\right)\right).
\]
For these data, \(L_n(s)\) is a polynomial. Define its characteristic series by the coefficientwise \(7\)-adically convergent product
\[
 C_n^*(s)=\prod_{j=0}^{\infty}(1-7^js)L_n(7^js)
          =\sum_{k=0}^{\infty}b_{n,k}s^k.
\]
Let \(N_n\) be the Newton polygon formed as the lower convex hull of
\[
 \bigl(k,\nu_n(b_{n,k})\bigr),\qquad k\in\mathbb Z_{\geq0},
 \qquad \nu_n=6\cdot7^{n-1}v_7,
\]
where the valuation of zero is \(+\infty\). Regard \(N_n(x)\) as the piecewise-linear ordinate of this polygon for real \(x\geq0\). Thus \(\nu_n(\zeta_{7^n}-1)=1\), and the factor \((1-s)\) is included in the polygon.

Define the adjacent-level agreement radius
\[
 \mathcal R_n=\sup\left\{R\geq0:\ N_n(x)=N_{n+1}(x)\text{ for every }x\in[0,R]\right\},
\]
with \(\mathcal R_n=+\infty\) when the two polygons agree on the entire half-line. Determine an explicit exact formula for \(\mathcal R_n\) for every integer \(n\geq1\).

The answer was proved recently, so it is not an open problem: your task is to find it and prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at an answer that settles less than the question asks (a partial or conditional answer, "not known") is not acceptable, and neither is conceding: when an approach fails, try another.

Proving it means showing that the answer is right in every case the question covers, and that no other answer is.

Stop only when your proof is complete. When you stop, write in that response what you proved, and what is left.