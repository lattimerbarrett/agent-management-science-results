Work in ZFC. A directed subset of a poset is a nonempty subset in which every two elements have a common upper bound belonging to that subset. A chain means a nonempty totally ordered subset.

Let \(P\) range over all nonempty set-sized posets in which every directed subset has a supremum. For \(a,b\in P\), define two relations by
\[
a\ll_{\mathrm{ch}}b
\iff
\forall C\subseteq P\text{ a chain},\quad
b\leq\bigvee_P C\ \Longrightarrow\ \exists c\in C\ (a\leq c),
\]
\[
a\ll_{\mathrm{dir}}b
\iff
\forall D\subseteq P\text{ directed},\quad
b\leq\bigvee_P D\ \Longrightarrow\ \exists d\in D\ (a\leq d).
\]
For \(p\in P\), put \(I_P(p)=\{x\in P:x\ll_{\mathrm{ch}}p\}\). Restrict attention to posets satisfying the following approximation condition: for every \(p\in P\), there is a chain \(K_p\subseteq P\) such that
\[
I_P(p)=\downarrow_P K_p,
\qquad
\bigvee_P I_P(p)=p,
\]
where \(\downarrow_P K=\{x\in P:\exists k\in K\ (x\leq k)\}\).

For a nonempty poset \(S\), let \(\operatorname{cf}(S)\) be the least cardinality of a cofinal subset of \(S\): a subset \(T\subseteq S\) is cofinal when every \(s\in S\) lies below some \(t\in T\). The sets \(I_P(p)\) carry the order inherited from \(P\).

Determine exactly the collection of ordered pairs of cardinals
\[
\left\{
\bigl(\operatorname{cf}(I_P(a)),\operatorname{cf}(I_P(b))\bigr):
P\text{ satisfies all the conditions above},\quad
 a,b\in P,\quad
 a\ll_{\mathrm{ch}}b,\quad
 a\not\ll_{\mathrm{dir}}b
\right\}.
\]

The answer was proved recently, so it is not an open problem: your task is to find it and prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at an answer that settles less than the question asks (a partial or conditional answer, "not known") is not acceptable, and neither is conceding: when an approach fails, try another.

Proving it means showing that the answer is right in every case the question covers, and that no other answer is.

Stop only when your proof is complete. When you stop, write in that response what you proved, and what is left.