Let
\[
F=(f_1,f_2,f_3)=(y,zy-x^2,z^2+x^2y+zy^2+x^3),\qquad f=f_1f_2f_3.
\]
Consider the parameter hyperplane
\[
H=\{(s_1,s_2,s_3)\in\mathbb C^3:2s_1+6s_2+8s_3+27=0\}.
\]
For \(s\in H\), write \(\beta=s_2+1\) and \(\gamma=s_3+1\). Let \(U\subset H\) consist of the parameters satisfying
\[
\beta,\ \gamma,\ \beta+\gamma+\tfrac32,\ \beta+2\gamma+\tfrac32,\ 2(\beta+\gamma+1)\notin\mathbb Z.
\]

Let \(a,c\) be independent indeterminates, put
\[
Q_2=c-a^{-1},\qquad Q_3=c^2+c+a^{-1},
\]
and define the localization
\[
R=\mathbb C[a,a^{-1},c,c^{-1},Q_2^{-1},Q_3^{-1},(c+a^{-1})^{-1}].
\]
Write \(\Omega_R^j\) for the algebraic differential \(j\)-forms over \(\mathbb C\), with exterior differential \(d\). For each \(s\in U\), set
\[
\theta_s=-\frac{27}{2}\frac{da}{a}+s_2\frac{dQ_2}{Q_2}+s_3\frac{dQ_3}{Q_3},
\qquad
\mathcal H_s=\frac{\Omega_R^2}{\{d\eta+\theta_s\wedge\eta:\eta\in\Omega_R^1\}},
\]
where the quotient is taken as a complex vector space.

For an independent formal variable \(b\), define a complex-linear map \(J_s:\mathbb C[x,y,z]\to\mathcal H_s\) by
\[
J_s(\psi)=\left[-a^3[b^{18}]\left(\psi(ab^3,ab^2,a^2b^4c)\left(1+\frac{a^{-1}b}{Q_3}\right)^{s_3}\right)\,da\wedge dc\right].
\]
Here \([b^{18}]\) denotes coefficient extraction in \(R[[b]]\), the outer brackets denote the class in \(\mathcal H_s\), and formal powers are interpreted by
\[
(1+T)^{s_3}=\sum_{n\ge0}\frac{s_3(s_3-1)\cdots(s_3-n+1)}{n!}T^n,
\]
with empty product equal to \(1\). Define
\[
W_s=\operatorname{span}_{\mathbb C}\{J_s(f\psi):\psi\in\mathbb C[x,y,z]\}\subseteq\mathcal H_s.
\]
Let \(\mathcal E\) be the Zariski closure in \(\mathbb C^3\) of
\[
\{s\in U:W_s\ne\mathcal H_s\}.
\]
What is the reduced Gröbner basis of the vanishing ideal \(I(\mathcal E)\subset\mathbb C[s_1,s_2,s_3]\) for the lexicographic monomial order \(s_1\succ s_2\succ s_3\)?

The answer was proved recently, so it is not an open problem: your task is to find it and prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at an answer that settles less than the question asks (a partial or conditional answer, "not known") is not acceptable, and neither is conceding: when an approach fails, try another.

Proving it means showing that the answer is right in every case the question covers, and that no other answer is.

Stop only when your proof is complete. When you stop, write in that response what you proved, and what is left.