# Twin-row structural lemma
Let $W:[0,1]^2\to[0,1]$ be a symmetric measurable red kernel. Write
$C_R(x,y)=\int W(x,z)W(y,z)dz$ and
$C_B(x,y)=\int(1-W(x,z))(1-W(y,z))dz$.
Assume $C_R\le a$ a.e. on $\{W>0\}$ and $C_B\le b$ a.e. on $\{W<1\}$.

For almost every $x$, either $q_R(x)=\int W(x,z)^2dz\le a$ or
$q_B(x)=\int(1-W(x,z))^2dz\le b$.
Indeed if both inequalities fail by $\epsilon$ on a positive-measure set,
separability of $L^2$ gives a positive-measure subset on which all rows are
within $\delta$ of one another. For sufficiently small $\delta$, both inner
products exceed their bounds for every pair in this subset (outside null
sets). No value $W(x,y)\in[0,1]$ is compatible with that.

Assume $\sqrt a+\sqrt b<1$ and $a\le1/4$. The light-red and light-blue
classes $R,B$ are disjoint: a light-red row has red degree at most $\sqrt a$,
while a light-blue row has red degree at least $1-\sqrt b$.

Moreover $W=1$ a.e. on $R\times R$. For two light-red rows $f,g$, put
$h=(f+g)/2$, $k=(f-g)/2$, $r=\int h$, $t=\sqrt a$.
Then $\|h\|^2+\|k\|^2\le t^2$, $r\le t$, and
\[
\langle1-f,1-g\rangle
=1-2r+\|h\|^2-\|k\|^2
\ge1-2r+2r^2-t^2
=(1-t)^2+2(t-r)(1-t-r)\ge(1-t)^2>b.
\]
Thus the pair cannot be blue. In particular $s=|R|\le a$.

If $R$ has full measure, put $p=\int W\le\sqrt a=t$.
The Goodman identity and red book bound imply
\[
b\ge\frac{1-3p+3p^2-ap}{1-p}\ge(1-t)^2,
\]
where the second difference equals
$-(p-t)(3p+t-2)/(p-1)\ge0$ for $p\le t\le1/2$.
So $B$ has positive measure above the random curve.

These statements do **not** imply $R$ is null: mixed examples above the
random curve exist. Sharp middle/high phase upper bounds still require a
separate mixed-type optimization theorem.
