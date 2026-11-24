For each even integer \(n\ge 2\), let \([n]=\{1,\ldots,n\}\). For every ordered pair \(i\ne j\) in \([n]\), draw \(U_{ij}\) independently from the uniform distribution on \([0,1]\). Participant \(i\) prefers \(j\) to \(k\) exactly when \(U_{ij}<U_{ik}\); these preferences are strict with probability one.

A perfect matching is a map \(M:[n]\to[n]\) satisfying \(M(M(i))=i\) and \(M(i)\ne i\) for every \(i\). It is stable if there are no distinct participants \(i,j\), with \(j\ne M(i)\), for which both
\[
U_{ij}<U_{i,M(i)}
\qquad\text{and}\qquad
U_{ji}<U_{j,M(j)}.
\]
Let \(P_n\) be the probability that at least one stable perfect matching exists. Determine the exact ordered pair \((\alpha,C)\in(0,\infty)^2\) such that
\[
\lim_{\substack{n\to\infty\\ n\text{ even}}} n^{\alpha}P_n=C.
\]

The answer was proved recently, so it is not an open problem: your task is to find it and prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at an answer that settles less than the question asks (a partial or conditional answer, "not known") is not acceptable, and neither is conceding: when an approach fails, try another.

Proving it means showing that the answer is right in every case the question covers, and that no other answer is.

Stop only when your proof is complete. When you stop, write in that response what you proved, and what is left.