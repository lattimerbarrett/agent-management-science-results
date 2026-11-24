# agent_1: last reply

Put
\[
\alpha_*=\frac{52-16\sqrt3}{121}.
\]
Then the limit exists, and
\[
\boxed{
c(\alpha)=
\begin{cases}
2,&0<\alpha\le \dfrac16,\\[1mm]
1+\dfrac{2\alpha}{3}+\dfrac43\sqrt{\alpha(3-2\alpha)},
 &\dfrac16<\alpha<\alpha_*,\\[1mm]
(1+\sqrt\alpha)^2,&\alpha_*\le\alpha\le1.
\end{cases}}
\]
Both adjacent expressions agree at the indicated endpoints.

Here is a proof, including the optimization needed for the middle regime. The Python at the end checks the algebraic identities and inequalities used in that optimization, and constructs finite colorings whose entire booksize tables are checked.

## 1. The density inequality behind the upper bound

Write
\[
\beta(a)=\min\left\{
\frac12,\quad 1+2a-4\sqrt{\frac a3},\quad(1-\sqrt a)^2
\right\},\qquad 0<a\le\frac14.
\]

We will prove the following density statement.

**Density theorem.** Let \(W:[0,1]^2\to[0,1]\) be symmetric and measurable. Set
\[
f_x(z)=W(x,z),\quad
R(x,y)=\langle f_x,f_y\rangle,\quad
Q(x,y)=\langle1-f_x,1-f_y\rangle.
\]
Suppose, almost everywhere,
\[
W(x,y)>0\Longrightarrow R(x,y)\le a,\qquad
W(x,y)<1\Longrightarrow Q(x,y)\le b.
\tag{2}
\]
If \(0<a\le1/4\), then \(b\ge\beta(a)\).

The inner products and norms in this proof are in \(L^2[0,1]\).

### 1.1 Classifying the rows

Almost every row satisfies at least one of
\[
\|f_x\|^2\le a,\qquad \|1-f_x\|^2\le b.
\tag{3}
\]
Indeed, otherwise a positive-measure set of rows violates both inequalities by a fixed positive margin. Separability of \(L^2\) gives a positive-measure subset contained in a sufficiently small \(L^2\)-ball. Every pair of rows in that subset then has both red inner product greater than \(a\) and blue inner product greater than \(b\). By (2), its edge would have to have \(W=0\) and \(W=1\), a contradiction.

Suppose henceforth that \(b<\beta(a)\). In particular,
\[
b<\frac12,\qquad \sqrt a+\sqrt b<1.
\tag{4}
\]
Thus the two classes in (3) are disjoint. Denote them by \(\mathcal R,\mathcal B\), with measures \(r,s=1-r\).

For nonnegative rows \(f,g\) of squared norm at most \(a\), put \(\sigma=\sqrt a\le1/2\) and \(d=\int g\le\sigma\). Cauchy–Schwarz gives
\[
\langle1-f,1-g\rangle
\ge1-d-\sigma\sqrt{1-2d+a}\ge(1-\sigma)^2.
\tag{5}
\]
For the second inequality, the function on the left of it is decreasing for \(0\le d\le\sigma\), so its minimum is at \(d=\sigma\).

By (2), (4), and (5), \(W=1\) almost everywhere on \(\mathcal R^2\). Consequently
\[
r\le a,\qquad
\int_{\mathcal B}q(x)\,dx\le r(a-r),
\quad q(x):=\int_{\mathcal R}W(x,z)^2\,dz.
\tag{6}
\]

### 1.2 A useful clique bound

Let \(f_1,\ldots,f_k\) be rows from \(\mathcal B\) whose pairwise red densities are positive. Their pairwise inner products are at most \(a\). Put \(c=1-b\), \(d_i=\int f_i\), and
\[
t=\frac{a+c}{2}.
\]
By (4),
\[
\sqrt a<t<1-\sqrt b\le d_i.
\]
Take \(\lambda_i=(d_i-t)^{-1}>0\) and \(L=\sum_i\lambda_i\). Since
\(\|f_i\|^2\le2d_i-c\),
\[
\begin{aligned}
(k+tL)^2
&=\left(\int\sum_i\lambda_i f_i\right)^2\\
&\le\left\|\sum_i\lambda_i f_i\right\|^2
\le aL^2+2L.
\end{aligned}
\]
Therefore
\[
(t^2-a)L^2+(2kt-2)L+k^2\le0.
\tag{7}
\]
But \(t>1/4\). Thus (7) excludes \(k\ge4\). If \(a\ge1/9\), then \(t>1/3\), so it also excludes \(k=3\).

### 1.3 A greedy partition

Choose a row \(f_1\) in \(\mathcal B\) whose \(q\)-value is within \(\delta>0\) of the essential infimum. Remove its red nonneighbors. Among the remaining common red neighbors, choose a row of nearly minimum \(q\), and repeat.

By (7), this stops after \(k\le3\) choices. The removed sets \(V_1,\ldots,V_k\) partition \(\mathcal B\), up to null sets. Writing \(\theta_i=|V_i|\), we have
\[
f_i=0\text{ on }V_i,\qquad
\sum_i\theta_iq(f_i)\le r(a-r)+\delta.
\tag{8}
\]
The chosen rows form a red clique.

If \(k\le2\), average their blue norm bounds with weights \(\theta_i/s\). Their contribution on \(\mathcal B\) is at least
\[
\frac{\sum_i\theta_i^2}{s}\ge\frac{s}{2}.
\]
Using (8) and Cauchy–Schwarz for the contribution on \(\mathcal R\), and then letting \(\delta\downarrow0\), gives
\[
b\ge \frac{s}{2}
+r\left(1-\sqrt{\frac{a-r}{s}}\right)^2
\ge \frac{s}{2}+r(1-\sqrt a)^2
\ge\min\left\{\frac12,(1-\sqrt a)^2\right\}.
\tag{9}
\]
This contradicts \(b<\beta(a)\).

Hence \(k=3\). If \(a\le1/12\), putting \(F=f_1+f_2+f_3\) yields
\[
3c\le\int(2F-F^2)+2\sum_{i<j}\langle f_i,f_j\rangle
\le1+6a\le\frac32,
\]
again a contradiction. If \(a\ge1/9\), a triangle is excluded by (7).

Only \(1/12<a<1/9\) remains. It is settled by the following lemma, proved in Section 4.

**Three-profile lemma.** Suppose \(1/12\le a\le1/9\), \(r\le a\), and a probability space is partitioned into
\(\mathcal R,V_1,V_2,V_3\), of measures \(r,\theta_1,\theta_2,\theta_3\). Suppose \(f_i:[0,1]\to[0,1]\) satisfy
\[
f_i=0\text{ on }V_i,\quad
\langle f_i,f_j\rangle\le a\ (i\ne j),\quad
\|1-f_i\|^2\le b,
\]
and
\[
\sum_i\theta_i\int_{\mathcal R}f_i^2\le r(a-r).
\tag{10}
\]
Then
\[
1-b\le
\max\left\{4\sqrt{\frac a3}-2a,\ 2\sqrt a-a\right\}.
\tag{11}
\]
The same conclusion holds with an error tending to zero if the right side of (10) has an added error tending to zero.

Applying this to (8) contradicts \(b<\beta(a)\). The density theorem follows.

## 2. From the density theorem to the Ramsey upper bound

Let \(C=C(\alpha)\) be the expression in the answer. Direct algebra gives
\[
a:=\frac{\alpha}{C}\le\frac14,
\qquad
\beta(a)=\frac1C.
\tag{12}
\]
For clarity, the two transitions in density coordinates are
\[
a=\frac1{12},\qquad
a_*=\left(\frac4{\sqrt3}-2\right)^2.
\]
They correspond respectively to
\[
\alpha=\frac16,\qquad
\alpha=\frac{a_*}{(1-\sqrt{a_*})^2}
=\frac{52-16\sqrt3}{121}.
\]

Fix \(\varepsilon>0\). Suppose that infinitely many colorings of
\[
K_{N_j},\qquad N_j=\lceil(C+\varepsilon)n_j\rceil,
\]
avoid both required books. Their red adjacency graphons have, after relabeling and taking a subsequence, a cut-limit \(W\).

Here are the compactness and counting facts being used. For each accuracy \(\eta\), refining a partition whenever its conditional-expectation approximation has cut error \(>\eta\) raises its \(L^2\)-energy by at least \(\eta^2\). Thus boundedly many refinements give a bounded-size step approximation. Diagonal subsequences of nested such approximations give cut compactness. Also, telescoping over edges gives continuity of each fixed finite graph's homomorphism density in cut distance.

For every fixed positive integer \(k\), the red book bound gives
\[
t(B_k,W_j)\le
\left(\frac{\lceil\alpha n_j\rceil-1}{N_j}\right)^k
\int W_j.
\]
Passing to the limit and then letting \(k\to\infty\) proves the red implication in (2), even with the enlarged bound \(a=\alpha/C\). The blue implication follows identically, with
\[
b=\frac1{C+\varepsilon}.
\]
(The finite blue adjacency graphon differs from \(1-W_j\) only on vertex-diagonal atoms, of total measure \(1/N_j\).)

But (12) gives \(b<\beta(a)\), contrary to the density theorem. Therefore, for all sufficiently large \(n\),
\[
r(B_{\lceil\alpha n\rceil},B_n)\le
\lceil(C+\varepsilon)n\rceil.
\tag{13}
\]

## 3. The lower-bound colorings

Fix \(\varepsilon>0\) and put \(N=\lfloor(C-\varepsilon)n\rfloor\).

### Constant regime

For \(0<\alpha\le1/6\), split the vertices into two nearly equal classes, color cross edges red, and internal edges blue. Red is triangle-free, while every blue book has at most
\(\lceil N/2\rceil-2<n\) pages.

### Three-part regime

For \(1/6<\alpha<\alpha_*\), partition into three nearly equal classes. Color internal edges blue and cross edges independently red with probability
\[
p=\sqrt{\frac{3\alpha}{C}}.
\]
The defining expression for \(C\) gives
\[
\frac{Cp^2}{3}=\alpha,\qquad
\frac{C[1+2(1-p)^2]}3=1.
\tag{14}
\]
A potential red spine has expected red codegree at most
\(\alpha N/C+1\). A blue internal spine has expected blue codegree at most \(N/C+1\). For a blue cross spine, the corresponding density is
\[
\frac{2(1-p)+(1-p)^2}{3}
\le\frac{1+2(1-p)^2}{3},
\]
so its expected blue codegree is at most \(N/C+2\).

### Homogeneous regime

For \(\alpha_*\le\alpha\le1\), independently color each edge red with probability
\[
p=\frac{\sqrt\alpha}{1+\sqrt\alpha}.
\]
Since \(C=(1+\sqrt\alpha)^2\), the red and blue expected codegrees are at most \(\alpha N/C\) and \(N/C\).

In both random constructions, conditional on a potential spine's color, its codegree is a sum of independent Bernoulli variables and deterministic terms. Every red mean is at most \(\alpha N/C+3\), and every blue mean at most \(N/C+3\). With
\[
t=\frac{\alpha\varepsilon n}{2C},
\]
both mean-plus-\(t\) quantities are below their forbidden thresholds for sufficiently large \(n\). Hoeffding and a union bound give failure probability at most
\[
2N^2\exp(-2t^2/N)=o(1).
\]
Thus an avoiding coloring exists.

At \(\alpha=1/6\), either the two-part or three-part construction works; at \(\alpha=\alpha_*\), either random construction works. Consequently,
\[
r(B_{\lceil\alpha n\rceil},B_n)>
\lfloor(C-\varepsilon)n\rfloor
\tag{15}
\]
for all sufficiently large \(n\).

Equations (13) and (15) prove the asserted limit.

## 4. Proof of the three-profile lemma

This section supplies the optimization left over from Section 1.

Put
\[
p=\sqrt{3a},\quad t=\frac{1-p}{p},\quad s=1-r,\qquad
g_3=\frac{4p}{3}-\frac{2p^2}{3},\quad
g_h=\frac{2p}{\sqrt3}-\frac{p^2}{3}.
\]
Thus
\[
\frac12\le p\le\frac1{\sqrt3},\qquad
\sqrt3-1\le t\le1.
\]
We seek a contradiction from \(c:=1-b>\max(g_3,g_h)\).

The cases \(p=1/2\) and \(r=0\) are immediate. The former follows from
\(3c\le1+6a\). For the latter, at most two profiles are nonzero at every point, and maximizing the resulting two-variable quadratic gives
\[
c\le2at+\frac{2p}{3}=g_3.
\]
Assume henceforth \(p>1/2\), \(r>0\).

### 4.1 A bound on every partition weight

Let \(F=\sum f_i\), \(H=F-1\), \(h=\|H\|\), \(q_i=\|f_i\|^2\), and \(d_i=\int f_i\). Define nonnegative deficits
\[
D_i=2d_i-q_i-c,\qquad e_{ij}=a-\langle f_i,f_j\rangle.
\]
Then
\[
h^2=1+6a-3c-\sum_iD_i-2\sum_{i<j}e_{ij}.
\tag{16}
\]
Moreover,
\[
q_i=c-4a+D_i+2\sum_{j\ne i}e_{ij}+2\langle f_i,H\rangle,
\]
so
\[
(\sqrt{q_i}-h)^2\le1+2a-2c.
\tag{17}
\]

Set
\[
B=1-\frac{8p}{3}+2p^2,\quad
E=1-\frac{2p}{3},\quad
D=1-2p+\frac{2p^2}{3}.
\]
Since \(c\ge g_3\), (16)–(17) imply
\[
\sqrt{q_i}\le 2p-1+\sqrt B.
\]
Also
\[
\sqrt B+\sqrt D\le\sqrt{2(B+D)}
\le\sqrt E-(2p-1).
\tag{18}
\]
The last inequality follows by squaring: the difference is
\[
2(2p-1)\left(\frac{3-p}{3}-\sqrt E\right)\ge0.
\]
All radicals here are nonnegative on the specified interval.

Thus \(\sqrt{q_i}\le\sqrt E-\sqrt D\le\sqrt c\). Since
\((u+c/u)/2\) decreases for \(u\le\sqrt c\),
\[
\frac{d_i}{\sqrt{q_i}}
\ge\frac{\sqrt{q_i}+c/\sqrt{q_i}}2\ge\sqrt E.
\]
But \(f_i=0\) on \(V_i\) gives \(d_i^2\le(1-\theta_i)q_i\). Hence
\[
\boxed{\theta_i\le\frac{2p}{3}.}
\tag{19}
\]

### 4.2 A quadratic dual inequality

For \(\tau,\nu\ge0\), subtract the pair constraints with weights
\(2\tau\theta_k\), where \(\{i,j,k\}=\{1,2,3\}\), from the average of the three row constraints. Then use (10).

Completing squares on the three \(V_i\) and on \(\mathcal R\) gives
\[
c\le 2a\tau s+
\sum_i\frac{2\theta_i}{3(1+3\tau\theta_i)}
+\frac r9\mathbf1^TM^{-1}\mathbf1+\nu r(a-r),
\tag{20}
\]
whenever the relevant quadratic forms are positive semidefinite. Here
\[
M_{ii}=\frac13+\nu\theta_i,\qquad
M_{ij}=\tau\theta_k\quad(i\ne j).
\]
For singular matrices below, the same bound follows directly by completing squares; their linear term is orthogonal to the kernel.

We use (20) in two cases.

### 4.3 Near-uniform partitions

Write \(x_i=\theta_i/s\), \(m=\max x_i\), and suppose
\[
m\le\frac1{3t}.
\tag{21}
\]
Choose
\[
\nu_0=\sqrt3-1+(\sqrt3-2)t,\qquad
\tau=\frac ts,\quad \nu=\frac{\nu_0}{s}.
\]
Put \(\delta=x-\mathbf1/3\). The two terms in (20) depending on \(x\) become
\[
s\,\mathcal B(x)+r\,\mathcal R(x),
\]
where
\[
\mathcal B(x)=\sum_i\frac{(2/3)x_i}{1+3tx_i},\qquad
\mathcal R(x)=\frac19\mathbf1^TM^{-1}\mathbf1,
\]
and now \(M\) has diagonal \(1/3+\nu_0x_i\) and off-diagonal \(tx_k\).

By strong concavity,
\[
\frac{2p}{3}-\mathcal B(x)\ge\frac t4\|\delta\|^2.
\tag{22}
\]

Here are explicit bounds for the other term. In the decomposition
\(\operatorname{span}(\mathbf1)\oplus\mathbf1^\perp\), the principal entry of \(M\) is
\[
A=\frac{1+t}{\sqrt3}\ge1,
\]
and its coupling vector is \((\nu_0-t)\delta/\sqrt3\).
The least eigenvalue of the perpendicular block is at least
\[
\ell(t)=
\frac{\sqrt3-1+(2\sqrt3-3)t-(\sqrt3-1)/t}{3}.
\tag{23}
\]
To see this, put \(d^2=1-3\sum_{i<j}x_ix_j\). The perpendicular eigenvalues are
\[
\frac{1+\nu_0-t}{3}\ \pm\ \frac{2t+\nu_0}{3}d.
\]
Condition (21) gives \(d\le1/t-1\), proving (23).

The Schur complement therefore gives
\[
\mathcal R(x)-\sqrt a
=\frac{\zeta}{3A(A-\zeta)},\qquad
0\le\zeta\le
\frac{(\nu_0-t)^2\|\delta\|^2}{3\ell(t)}.
\tag{24}
\]
The following rational estimates suffice:
\[
\begin{array}{c|cc}
& t\ge\sqrt3/2&t\le\sqrt3/2\\ \hline
\ell(t)&>9/100&>1/50\\
(\nu_0-t)^2&<29/100&<7/50\\
\|\delta\|^2&<2/125&<9/100\\
\zeta&<1/50&<21/100\\
(\mathcal R-\sqrt a)/\|\delta\|^2&<2/5&<1 .
\end{array}
\tag{25}
\]
These follow directly from (23), which is increasing in \(t\), and
\(\|\delta\|^2\le\frac23(1/t-1)^2\). Their exact radical comparisons are checked in the code below.

Equations (22)–(25) imply
\[
\mathcal R(x)-\sqrt a
\le8\left(\frac{2p}{3}-\mathcal B(x)\right).
\]
Since \(r/s\le1/8\), (20) is at most its value at \(x_i=1/3\). That value is
\[
\begin{aligned}
U&=2at+\frac{2ps}{3}+r\sqrt a+\frac{\nu_0r(a-r)}s\\
&=g_3+r(g_h-g_3)-\frac{\nu_0(1-a)r^2}{s}
\le\max(g_3,g_h).
\end{aligned}
\]
This is the desired contradiction.

### 4.4 Far partitions

Suppose \(m>1/(3t)\). By (19),
\[
\frac{p}{3(1-p)}\le m\le\frac{2p}{3s},
\qquad r\ge2p-1.
\tag{26}
\]
Choose
\[
\tau=\nu=\frac1{3sm}.
\]
The matrix in (20) is
\[
M=\frac I3+\frac{T_x}{3m},
\]
where \(T_x\) has diagonal \(x_i\) and off-diagonal \(x_k\).
Its eigenvalues are \(1,d,-d\), with \(d\le m\); hence \(M\) is positive semidefinite. Its row sums are constant, giving the \(\mathcal R\)-maximum \(m/(1+m)\).

Concavity in the other two partition weights now gives
\[
c\le J(r,m):=
\frac{2a+r(a-r)/s}{3m}
+\frac{m[s(5-3m)+3r]}{3(1+m)}.
\tag{27}
\]
We claim \(J\le g_3\) throughout (26).

Let \(A_0=2a+r(a-r)/s\), \(K_0=8-5r\). Then
\[
J_{mm}=\frac23\left(\frac{A_0}{m^3}-\frac{K_0}{(1+m)^3}\right)\ge0.
\]
Indeed \(A_0/K_0\ge p^2/12\), \(m\le3p/4\), and
\[
(4+3p)^3-324p=(3p-2)^2(3p+16)\ge0.
\]
It is therefore enough to check the two endpoints in (26).

Put \(y=2p-1\), \(z=r-y\). Then \(0\le y,z\le1/9\). Exact expansion gives
\[
g_3-J\!\left(r,\frac{p}{3(1-p)}\right)
=\frac{P_0}{12(2-y)(1-y)(1+y)(1-y-z)},
\]
\[
g_3-J\!\left(r,\frac{2p}{3s}\right)
=\frac{P_1}{12(1+y)(4-2y-3z)},
\]
where
\[
\begin{aligned}
P_0={}&y^2(y^4-12y^3+46y^2-60y+25)\\
&+yz(y^4-18y^3+100y^2-126y+43)\\
&+z^2(-6y^3+58y^2-58y+22),\\
P_1={}&y^2(2y^2-20y+50)+yz(y^2-82y+97)\\
&+z^2(-3y^2-102y+45-36z).
\end{aligned}
\]
Every parenthesized expression is positive on \([0,1/9]^2\): drop its positive terms and replace the variables in its negative terms by \(1/9\). Both denominators are positive. Thus \(J\le g_3\), completing the proof of the lemma.

Finally, an added error \(\eta\) in (10) adds only \(\nu\eta\) to (20). The choices above have uniformly bounded \(\nu\), so the error version used in the greedy argument follows.

## 5. Executable checks

This code was run successfully. The symbolic part uses **exact arithmetic only**. The finite examples are additional checks, not a substitute for the concentration proof.

```python
import sympy as S
Q = S.Rational
h = S.sqrt(3)
p,r,m,y,z,t = S.symbols('p r m y z t', real=True)
a=p*p/3; s=1-r
g3=4*p/3-2*p*p/3
gh=2*p/h-p*p/3
nu=1+(h-2)/p

# Uniform-value identity.
U=2*a*(1-p)/p+2*p*s/3+r*p/h+nu*r*(a-r)/s
assert S.simplify(U-g3-r*(gh-g3)+nu*(1-a)*r*r/s)==0

# Theta-cap radical identity.
H=2*p-1
E=1-2*p/3
B=1-8*p/3+2*p*p
D=1-2*p+2*p*p/3
assert S.simplify((S.sqrt(E)-H)**2-2*(B+D)
                 -2*H*((3-p)/3-S.sqrt(E)))==0
assert S.expand(E-D-g3)==0
assert S.expand((1-p/3)**2-E-p*p/9)==0

# Exact spectral identities.
x0,x1,L=S.symbols('x0 x1 L', real=True)
x=S.Matrix([x0,x1,1-x0-x1])
e2=x[0]*x[1]+x[0]*x[2]+x[1]*x[2]
d2=1-3*e2
T=S.Matrix([[x[0],x[2],x[1]],
            [x[2],x[1],x[0]],
            [x[1],x[0],x[2]]])
cp=T.charpoly()
assert S.factor(cp.as_expr().subs(cp.gen,L)
                -(L-1)*(L*L-d2))==0
nu0=h-1+(h-2)*t
M=S.eye(3)/3+nu0*S.diag(*x)+t*(T-S.diag(*x))
e=S.ones(3,1)/h
delta=x-S.ones(3,1)/3
assert S.simplify(M*e-(1+t)/h*e
                 -(nu0-t)/h*delta)==S.zeros(3,1)
P=S.Matrix([[1/S.sqrt(2),1/S.sqrt(6)],
            [-1/S.sqrt(2),1/S.sqrt(6)],
            [0,-2/S.sqrt(6)]])
C=S.simplify(P.T*M*P)
C0=(1+nu0-t)/3
K=2*t+nu0
assert S.simplify(S.trace(C)-2*C0)==0
assert S.simplify(C.det()-C0*C0+K*K*d2/9)==0
low=((h-1)+(2*h-3)*t-(h-1)/t)/3
assert S.simplify(low-C0+K*(1/t-1)/3)==0
assert S.simplify(low.subs(t,h/2)-1/(6*h))==0
assert S.simplify(low.subs(t,h-1)-(7-4*h)/3)==0

# Every rational estimate in the Schur-complement table.
checks=[
 h-1>Q(18,25),
 1/(6*h)>Q(9,100),
 (7-4*h)/3>Q(1,50),
 (4-2*h)**2<Q(29,100),
 (h-1)**2/4<Q(7,50),
 Q(2,3)*(2/h-1)**2<Q(2,125),
 (2-h)/3<Q(9,100),
 Q(29,100)*Q(2,125)/(3*Q(9,100))<Q(1,50),
 Q(7,50)*Q(9,100)/(3*Q(1,50))==Q(21,100),
 Q(29,100)/(9*Q(9,100)*Q(49,50))<Q(2,5),
 Q(7,50)/(9*Q(1,50)*Q(79,100))<1]
assert all(bool(v) for v in checks)

# Far-case convexity and both endpoint polynomial identities.
assert S.expand((4+3*p)**3-324*p
                -(3*p-2)**2*(3*p+16))==0
J=(2*a+r*(a-r)/s)/(3*m)+m*(s*(5-3*m)+3*r)/(3*(1+m))
A0=2*a+r*(a-r)/s
K0=8-5*r
assert S.simplify(S.diff(J,m,2)
                 -Q(2,3)*(A0/m**3-K0/(1+m)**3))==0
P0=(y*y*(y**4-12*y**3+46*y*y-60*y+25)
    +y*z*(y**4-18*y**3+100*y*y-126*y+43)
    +z*z*(-6*y**3+58*y*y-58*y+22))
P1=(y*y*(2*y*y-20*y+50)+y*z*(y*y-82*y+97)
    +z*z*(-3*y*y-102*y+45-36*z))
D0=12*(2-y)*(1-y)*(1+y)*(1-y-z)
D1=12*(1+y)*(4-2*y-3*z)
for mm,PP,DD in [
    (p/(3*(1-p)),P0,D0),(2*p/(3*s),P1,D1)]:
    diff=S.factor((g3-J.subs(m,mm))
                  .subs(r,2*p-1+z).subs(p,(1+y)/2))
    assert S.factor(diff-PP/DD)==0
assert all(v>0 for v in [
 25-Q(60,9)-Q(12,9**3),
 43-Q(126,9)-Q(18,9**3),
 22-Q(58,9)-Q(6,9**3),
 50-Q(20,9),97-Q(82,9),
 45-Q(3,81)-Q(102,9)-Q(36,9)])

# Exact transition conversions.
a0=(4/h-2)**2
b0=(1-S.sqrt(a0))**2
astar=(52-16*h)/121
assert S.simplify(a0/b0-astar)==0
assert S.simplify(1+2*a0-4*S.sqrt(a0/3)-b0)==0
assert S.simplify(1+Q(2,3)*Q(1,6)
    +Q(4,3)*S.sqrt(Q(1,6)*(3-2*Q(1,6)))-2)==0
print("All exact algebraic checks passed.")

# Actual finite colorings: compute EVERY edge's common-neighbor count.
import numpy as np
rng=np.random.default_rng(20260703)
alpha_star=float(astar)
for alpha in [0.1,1/6,0.18,alpha_star,0.25,0.5,1.0]:
    n=700
    eps=0.7
    if alpha<=1/6:
        CC=2.
    elif alpha<alpha_star:
        CC=1+2*alpha/3+4*np.sqrt(alpha*(3-2*alpha))/3
    else:
        CC=(1+np.sqrt(alpha))**2
    N=int(np.floor((CC-eps)*n))
    if alpha<=1/6:
        A=np.zeros((N,N),dtype=np.int32)
        k=N//2
        A[:k,k:]=1
        A[k:,:k]=1
    else:
        prob=(np.sqrt(3*alpha/CC) if alpha<alpha_star
              else np.sqrt(alpha)/(1+np.sqrt(alpha)))
        A=np.triu((rng.random((N,N))<prob).astype(np.int32),1)
        A+=A.T
        if alpha<alpha_star:
            for I in np.array_split(np.arange(N),3):
                A[np.ix_(I,I)]=0
    Blue=np.ones((N,N),dtype=np.int32)-np.eye(N,dtype=np.int32)-A
    RR=A@A
    BB=Blue@Blue
    red=int(RR[A==1].max(initial=0))
    blue=int(BB[Blue==1].max(initial=0))
    assert red<int(np.ceil(alpha*n)) and blue<n
    print(alpha,N,red,blue)
```

The finite-check output was:
```text
0.1                 910    0   453
0.16666666666666666 910    0   453
0.18                937  117   507
0.20072055437105754 977  134   530
0.25               1085  168   558
0.5                1549  335   617
1.0                2310  673   692
```
All assertions passed.

# agent_2: last reply

Completed and independently verified:

- All lower-bound constructions, concentration estimates, transition values, and endpoint cases.
- The mixed-triangle upper-bound lemma that closes the main gap.
- A self-contained exact Python certificate checking **1,020 nonnegative Bernstein coefficients**, with independent polynomial reconstruction and determinant checks. All four agents ran or audited it successfully.
- The alternative elementary middle-range proof and its endpoint polynomial identities.

Key files:
- `workspace/agent2_lower_proof.md`
- `workspace/lower_bound_checks.py`
- `workspace/agent2_mixed_triangle_lemma.md`
- `workspace/agent2_mixed_certificate.py`

The team’s proof is complete; agent_1 is assembling the final presentation.

# agent_3: last reply

The team’s proof is complete. I independently verified:

- the exact 1,020-coefficient Bernstein certificate closing the mixed-triangle case;
- its derivation from the graphon book constraints;
- the graphon reduction, greedy partition, upper-bound parameters, and limiting argument;
- the lead’s independent elementary proof of the difficult middle case.

All exact certificate checks passed. No mathematical gap remains; agent_1 is assembling the final exposition and executable verification code.

# agent_4: last reply

The team’s proof is now complete.

I independently verified the previously missing mixed-loop upper bound, including:
- Its derivation from the graphon constraints.
- Positivity of all denominator and quadratic-form terms.
- All **1,020 exact Bernstein coefficients**, with independent polynomial reconstruction.
- The graphon reduction, endpoint cases, and parameter normalization.

The lead is assembling the final proof and reproducible Python. No mathematical gap remains identified.