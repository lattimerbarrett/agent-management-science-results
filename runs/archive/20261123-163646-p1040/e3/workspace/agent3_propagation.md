# Explicit propagation of the rank-three quartic witness

Assume the quartic word $w_4\in\gamma_4(\mathrm{IA}_3)\cap\mathcal A_5(3)$ constructed and checked in `agent4_rank3.md`. Under the homomorphism to the free product of three involutions, followed by the characteristic-two Magnus homomorphism

$$a\mapsto1+A,\quad b\mapsto1+B,\quad c\mapsto1+C,$$

into the degree-completion of

$$R=\mathbf F_2\langle A,B,C\rangle/(A^2,B^2,C^2),$$

its degree-four initial term is

$$P_4=ABAC+ABCA+ABCB+ACAB+ACBA+BABC+BACA+BACB+BCAB+BCBA+CABA+CBAB.$$

The involutions corresponding to $B,C$ are the images of $K_{12},K_{21}$, respectively. Define recursively

$$w_{r+1}=\begin{cases}[w_r,K_{12}],&r\text{ even},\\[w_r,K_{21}],&r\text{ odd}.\end{cases}$$

Then $w_r\in\gamma_r(\mathrm{IA}_3)\cap\mathcal A_{r+1}(3)$: the lower-central assertion is definitional; the Andreadakis assertion follows inductively from $[\mathcal A_s,\mathcal A_t]\subseteq\mathcal A_{s+t}$, starting with $w_4\in\mathcal A_5$ and $K_{ij}\in\mathcal A_1$.

Let $v_4=ABAC$, and append $B,C,B,C,\ldots$ to obtain $v_r$ of length $r$. We claim that the coefficient of $v_r$ in the degree-$r$ initial term $P_r$ of the image of $w_r$ is one. This is true at $r=4$. If the next letter is $X\in\{B,C\}$, the commutator expansion gives

$$P_{r+1}=P_rX+XP_r.$$

The right-appended word $v_rX$ is nonzero in $R$ because $X$ differs from the last letter of $v_r$. In $P_rX$, its coefficient is exactly that of $v_r$ in $P_r$, namely one. It has initial letter $A$, so it cannot occur in $XP_r$. Thus the claim follows by induction.

Consequently the image of $w_r$ does not lie in $1+I^{r+1}$, where $I=(A,B,C)$, whereas every image of $\gamma_{r+1}(\mathrm{IA}_3)$ does lie there. Therefore

$$w_r\notin\gamma_{r+1}(\mathrm{IA}_3)\qquad(r\ge4).$$

This proves the strictness half for rank three in every degree. No center-freeness theorem, stabilization assertion, finite computation, or characteristic-zero logarithm is being used in the induction. The independent exact characteristic-two polynomial checker `agent3_propagation.py` confirms the initial polynomial and the explicit coefficient witnesses for every $4\le r\le30`; the induction proves all degrees.
