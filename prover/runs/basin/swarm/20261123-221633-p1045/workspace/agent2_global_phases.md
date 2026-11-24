# Global first and last phases
This extends `agent2_twin.md`; $a=\alpha/c$, $b=1/c$, where a hypothetical
counterexample coefficient $c$ is larger than the proposed upper bound.

## B-support triangle existence (agent 4)
Assume $0<a\le b<1/2$, $a<1/4$, $\sqrt a+\sqrt b<1$.
Let $s=|R|$, $\beta=1-s$. Recall $R$ is a red clique and $s\le a$.
If $s=0$, triangle-freeness of the red support gives by Mantel and Cauchy
$Q\ge2P^2$, hence $b\ge1-2P+Q\ge1/2$, impossible.
Suppose $s>0$ and the red support on $B$ is triangle-free. Put
\[
 C=\int_{R\times B}W^2\le s(a-s),\quad
 D=\int_{R\times B}W\le\sqrt{s\beta C},\quad
 P=\int_{B^2}W,\quad Q=\int_{B^2}W^2.
\]
Mantel and Cauchy yield $Q\ge2P^2/\beta^2$. Integrating blue-light row norms
on $B$ gives
\[
b\beta\ge\beta-2P+Q-2D+C
\ge\beta-\beta^2/2+C-2\sqrt{s\beta C}.
\]
The final expression is decreasing in $C$ throughout
$0\le C\le s(a-s)<s\beta$. Set $q=\sqrt{(a-s)/\beta}\le u=\sqrt a<1/2$.
It follows that
\[
b\ge\tfrac12+s(\tfrac12+q^2-2q).
\]
Let $u_0=1-1/\sqrt2$. If $u\le u_0$, this is at least $1/2$.
If $u\ge u_0$, since $s\le u^2$ and the bracket at $u$ is nonpositive,
\[
b\ge\tfrac12+u^2(\tfrac12+u^2-2u)\ge(1-u)^2,
\]
because the last difference is
$(u^2-1)(2u^2-4u+1)/2\ge0$. Either conclusion contradicts the hypotheses.
Thus the B-support contains a red triangle.

## Universal triangle inequality
For its three rows $g_1,g_2,g_3$, write $x_i=g_i(z)$.
For $0\le\lambda\le2$ put $h=\lambda$ (the k=3 case of the clique identity).
Pointwise
\[
\sum_i(1-x_i)^2+\lambda\sum_{i<j}x_ix_j\ge\frac{3\lambda}{1+\lambda}.
\]
After integration, $3b+3\lambda a\ge3\lambda/(1+\lambda)$, or
\[
b+\lambda a\ge\lambda/(1+\lambda),\qquad0\le\lambda\le2.
\]
In particular $b+2a\ge2/3$.

## First phase: $0<\alpha\le1/6$
Suppose $c>2$. Then $b<1/2$ and $a<1/12$;
$\sqrt a+\sqrt b<\sqrt{1/12}+\sqrt{1/2}<1$.
The triangle existence lemma applies, but
$b+2a=(1+2\alpha)/c< (1+2/6)/2=2/3$, a contradiction.
The elementary two-blue-clique construction gives the matching lower
bound $c\ge2$. Therefore $c(\alpha)=2$ here, including $\alpha=1/6$.

## Last phase: $1/4\le\alpha\le1$
Suppose $c>(1+\sqrt\alpha)^2$. Then $b<1/2$,
$a<\alpha/(1+\sqrt\alpha)^2\le1/4$, and
$\sqrt a+\sqrt b<1$. Thus a B-triangle exists. Its $\lambda=2$ inequality
and $a=\alpha b$ imply
\[
a\ge\frac{2\alpha}{3+6\alpha}\ge\frac19.
\]
Hence $\lambda=a^{-1/2}-1\in[0,2]$ is admissible. The same triangle
inequality gives $b\ge(1-\sqrt a)^2$, contradicting
$\sqrt a+\sqrt b<1$. Homogeneous random colorings give the matching lower
bound. Therefore $c(\alpha)=(1+\sqrt\alpha)^2$ for $1/4\le\alpha\le1$,
including $\alpha=1/4$.

The interval $(1/6,1/4)$ remains unproved globally; only the all-blue-light
case currently has the sharp upper bound there.
