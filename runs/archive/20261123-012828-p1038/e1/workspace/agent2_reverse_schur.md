# Reverse-radii boundary inequality

This closes the only additional algebraic case needed when using the lower-halfspace full-mode Schur argument after swapping the two rings. It is a local Schur lemma, **not** a determinant/nonvanishing proof.

Suppose $0<|t|<B<r$, $0<k<1$, and set
\[
p=\sqrt{B^2-t^2},\quad q=\sqrt{r^2-t^2},\quad A=r-B,
\quad K=Bp+rq,\quad U=rp+Bq.
\]
For $C^2+S^2=1$ define
\[
s^2=p^2+r^2+k^2t^2-2rkBC,
\qquad G=K-k(UC+tAS).
\]
Then $G>A s$ strictly.

First $G>0$, because Cauchy--Schwarz and the exact identity
\[
K^2-U^2-t^2A^2=A^2((r+B)^2-t^2)>0
\]
give $G\ge K-k\sqrt{U^2+t^2A^2}>0$.

Write $h=|t|$, $B=h\cosh u$, $r=h\cosh v$, where $v>u>0$. Put
\[
\beta=\cosh(v-u)>1,\quad
\alpha=\cosh(u+v),\quad
L=\frac{\cosh((u+v)/2)}{\sinh((v-u)/2)}>0.
\]
Then $L^2=(\alpha+1)/(\beta-1)$ and
\[
\frac G{Ah}=L\beta-k(LC+\operatorname{sgn}(t)S),
\quad \frac{s^2}{h^2}=\alpha\beta+k^2-k(\alpha+\beta)C.
\]
Direct substitution, using $C^2+S^2=1$, yields
\[
\boxed{\frac{G^2-A^2s^2}{A^2t^2}
=(\beta-kC)\Big[L^2+1-k\big((L^2-1)C+2L\operatorname{sgn}(t)S\big)\Big].}
\]
Both factors are strictly positive: the first exceeds $1-k$, and the second is at least $(1-k)(L^2+1)$, since
$(L^2-1)^2+4L^2=(L^2+1)^2$.
Thus $G^2>A^2s^2$; since $G>0$ and $A,s>0$, the claim follows.

For $t=0$, $p=B$, $q=r$, and directly $G=s^2$, while
$s^2-A^2=2rB(1-kC)>0$. Hence again $G>A s$.

The companion Python file `agent2_reverse_schur.py` checks all four algebraic identities exactly with SymPy and tests the full unreduced inequality and factorization numerically at high precision.
