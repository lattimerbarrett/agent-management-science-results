# Local mixed-root absorption lemma
Assume the typed graphon setup of `agent2_twin.md`, with $s=|R|$, $\beta=1-s$.
Let $a=u^2$ satisfy $1/12<a<(4/\sqrt3-2)^2$, and set
$\lambda=2/\sqrt{3a}-2\in(0,2)$,
$H=1-4/[3(2+\lambda)]=1-2u/\sqrt3$.
Suppose the red-support triangles on $B$ admit a probability distribution
whose average vertex marginal is at most $(1+\delta)/\beta$ relative to
Lebesgue measure. (In particular, $\delta=0$ is a fractional triangle factor.)

For each triangle $T=(y_1,y_2,y_3)$ and an R-root $z$, set
$x_i=W(z,y_i)$, $m=(x_1+x_2+x_3)/3$, and
$v=(\sum x_i^2)/3-m^2\ge0$. Its normalized triangle dual cost is
\[
F_T(z)=\frac13\left[\sum_i(1-x_i)^2+\lambda\sum_{i<j}x_ix_j\right]
=1-2m+(1+\lambda)m^2+(1-\lambda/2)v.
\]
By the marginal bound and the R-row norm condition,
$\mathbb E_T[(\sum x_i^2)/3]\le A=(1+\delta)(a-s)/\beta$.
The minimum expected dual cost under this L2 constraint, provided
$\sqrt A\le1/(1+\lambda)$, is
$\Phi(A)=1-2\sqrt A+(1+\lambda)A$.
To see this directly, discard the nonnegative variance term and use
$\mathbb E m\le\sqrt{\mathbb E m^2}\le\sqrt A$; the scalar quadratic is
strictly decreasing on $[0,1/(1+\lambda)]$.

At $\delta=0$, $A\le a$ and
\[
\Phi(a)-H=u(4/\sqrt3-2-u)>0.
\]
Hence for a sufficiently small positive $\delta$ (depending on $a$), every
R-root has expected normalized triangle cost strictly bigger than $H$.
On B-coordinates the K4-free support gives the exact sparse triangle
inequality, whose normalized cost is at least $H$.
Averaging this over T and all coordinates yields
\[
b+\lambda a\ge\beta H+s\Phi(A)\ge H,
\]
strictly if $s>0$. Therefore $b\ge1+2a-4\sqrt{a/3}$.

This is a complete sufficient condition, not a general purification proof:
an arbitrary feasible B-support need not have the required nearly uniform
triangle factor. It does prove local optimality near the balanced three-pod
extremizer, since in strong L2 its three cross support densities tend to 1,
and conditioning uniform independent pod samples on forming a red triangle
then gives the needed marginal domination with $\delta\to0$.
