# agent_1: last reply

Put
\[
\alpha_*=\frac{52-16\sqrt3}{121}=0.2007205543710575\ldots .
\]
Then the answer is
\[
\boxed{
c(\alpha)=
\begin{cases}
2,&0<\alpha\le \dfrac16,\\[2mm]
\dfrac{\bigl(\sqrt{3-2\alpha}+2\sqrt\alpha\bigr)^2}{3},
   &\dfrac16<\alpha<\alpha_*,\\[3mm]
(1+\sqrt\alpha)^2,&\alpha_*\le\alpha\le1.
\end{cases}}
\]
The adjacent formulas agree at both transition points. In particular, the middle formula is also valid at either endpoint.

The principal difficulty is the upper bound in the intermediate interval. We prove the requisite inequality below, rather than assume a sharp book-Ramsey theorem.

## 1. A kernel formulation

We use the standard compactness theorem for graphons: a sequence of finite graphs has a cut-convergent subsequence, and the density of each fixed graph is continuous under this convergence.

For a symmetric measurable \(W:[0,1]^2\to[0,1]\), write
\[
C_R(x,y)=\int_0^1W(x,z)W(y,z)\,dz,
\quad
C_B(x,y)=\int_0^1(1-W(x,z))(1-W(y,z))\,dz.
\]
We say that \(W\) has book bounds \(a,b\) if, almost everywhere,
\[
W(x,y)>0\implies C_R(x,y)\le a,\qquad
W(x,y)<1\implies C_B(x,y)\le b.                 \tag{1}
\]

Here is why this formulation applies. Suppose colorings on \(N_j\) vertices have no red \(B_{m_j}\) or blue \(B_{n_j}\), where
\[
\frac{m_j}{N_j}\longrightarrow a,\qquad
\frac{n_j}{N_j}\longrightarrow b.
\]
For every fixed positive integer \(k\), their red adjacency kernels satisfy
\[
t(B_k,W_j)
=\int W_j(x,y)C_{R,j}(x,y)^k\,dx\,dy
\le \left(\frac{m_j-1}{N_j}\right)^k\int W_j.
\]
Pass to a graphon limit, then let \(k\to\infty\). This gives the red implication in (1); the blue implication follows identically. The discrepancy on the diagonal squares of the finite kernels has measure \(1/N_j\), so the blue limit is \(1-W\).

We shall prove the following sharp inequality.

### Kernel lemma
Suppose \(W\) satisfies (1), and
\[
0<a\le b<\frac12,\qquad \sqrt a+\sqrt b<1.
\]
Set
\[
u_*=\frac4{\sqrt3}-2,\qquad A=u_*^2.
\]
Then necessarily
\[
a<A,\qquad
b\ge f(a):=1+2a-4\sqrt{\frac a3}.              \tag{2}
\]

## 2. Preliminary structure

For a vertex \(x\), let
\[
q_R(x)=\int W(x,z)^2\,dz,\qquad
q_B(x)=\int(1-W(x,z))^2\,dz.
\]

### 2.1. The two vertex types

Almost every vertex satisfies
\[
q_R(x)\le a\quad\hbox{or}\quad q_B(x)\le b.    \tag{3}
\]
Indeed, otherwise some positive-measure set has both inequalities violated by a fixed margin. The space of \(L^2\) row functions is separable, so a positive-measure subset has all its rows arbitrarily close in \(L^2\). Every pair in that subset then has both common-neighborhood integrals exceeding the corresponding bounds, contradicting (1).

The alternatives in (3) are disjoint: Minkowski’s inequality gives
\[
1=\|W(x,\cdot)+(1-W(x,\cdot))\|_2
 \le\sqrt{q_R(x)}+\sqrt{q_B(x)}.
\]

Let \(R\) be the first type and \(B\) the second, and put \(s=|R|\). The set \(R\) is a red clique almost everywhere. To see this, take red rows \(p,q\) of two vertices in \(R\), and put
\[
h=\frac{p+q}{2},\quad k=\frac{p-q}{2},\quad
v=\int h,\quad t=\sqrt a<\frac12.
\]
Then \(v\le t\) and \(\|h\|_2^2+\|k\|_2^2\le t^2\), so
\[
\begin{aligned}
\langle1-p,1-q\rangle
&=1-2v+\|h\|_2^2-\|k\|_2^2\\
&\ge1-2v+2v^2-t^2
 \ge(1-t)^2>b.
\end{aligned}
\]
Thus their connecting edge must be red. Consequently
\[
s\le a,\qquad
\int_B\int_R W(v,r)^2\,dr\,dv\le s(a-s).      \tag{4}
\]

### 2.2. A clique inequality

If \(k\) vertices in \(B\) form a red-support clique, then
\[
b+ra\ge\frac r{1+r}\qquad(0\le r\le k-1).    \tag{5}
\]
For completeness, put \(\lambda=2r/(k-1)\in[0,2]\). For arbitrary real \(z_i\),
\[
\sum_i(1-z_i)^2+\lambda\sum_{i<j}z_i z_j
\ge \frac{kr}{1+r}.
\]
This follows by first replacing \(\sum z_i^2\) by \((\sum z_i)^2/k\), then completing a square. Apply it to the \(k\) red rows and integrate.

The red support on \(B\) is \(K_4\)-free. Otherwise (5) with \(k=4,r=3\) implies \(a>1/12\). We may then choose
\[
r=\frac1{\sqrt a}-1<3
\]
in (5), obtaining \(b\ge(1-\sqrt a)^2\), contrary to the hypothesis.

## 3. Selecting three useful rows

Put
\[
h(v)=\int_R W(v,r)^2\,dr.
\]
Greedily choose a minimum-\(h\) vertex \(v_1\) in \(B\), remove its red-support nonneighbors \(A_1\), choose a minimum-\(h\) vertex in the remaining common neighborhood, and continue.

Since the support on \(B\) is \(K_4\)-free, this process stops after at most three choices. Write
\[
g_i=W(v_i,\cdot),\qquad x_i=|A_i|,\qquad h_i=h(v_i).
\]
The sets \(A_i\) partition \(B\), and
\[
g_i=0\ \hbox{on }A_i,\qquad
\sum_i x_i h_i\le s(a-s),\qquad x_i\le b.     \tag{6}
\]

Essential infima need not be attained. Rigorously, choose \(\varepsilon\)-essential minimizers, avoiding the null exceptional fibers in (1). The middle inequality in (6) then has an added \(+\varepsilon\). All estimates below are continuous in finitely many bounded moments, so passing to a subsequence and then letting \(\varepsilon\downarrow0\) gives the stated inequalities. We henceforth suppress these vanishing errors.

There cannot be just one choice, since then \(b\ge|B|=1-s>3/4\).

There cannot be just two choices either. If \(s=0\), their summed blue row bounds immediately give \(2b\ge1\). Otherwise put
\[
H=\int_R(g_1^2+g_2^2),\qquad m=\int_R(g_1+g_2).
\]
Because \(x_1+x_2=1-s\) and \(x_i\le b\), (6) gives
\[
H\le\frac{s(a-s)}{1-s-b}.
\]
Writing
\[
q^2=\frac{a-s}{2(1-s-b)}\le a=u^2,
\]
Cauchy–Schwarz and the summed blue bounds yield
\[
2b\ge1+s-2\sqrt{2sH}+H
   \ge1+s(1-4u+2u^2).                       \tag{7}
\]
If \(u\le1-1/\sqrt2\), this contradicts \(b<1/2\). Otherwise \(s\le a\) implies
\[
b\ge\frac12+a\left(\frac12+a-2u\right)\ge(1-u)^2,
\]
because the difference in the last inequality is
\[
\frac{(u^2-1)(2u^2-4u+1)}2\ge0.
\]
Again this is a contradiction.

Thus three rows are selected. Applying (5) to their triangle shows \(a>1/12\). If \(a\ge1/9\), its optimizing choice \(r=1/\sqrt a-1\le2\) contradicts the hypothesis again. Hence
\[
\frac1{12}<a<\frac19.                       \tag{8}
\]

## 4. The adaptive three-row inequality

This section supplies the intermediate-range upper bound.

Write \(u=\sqrt a\), so \(1/\sqrt{12}<u<1/3\), and set
\[
\begin{gathered}
t=2\sqrt3u,\quad
\kappa=3-\frac{2\sqrt3-3}{u},\quad
\ell=\frac4t-2,\quad K=3-t,\\
c_0=3-\frac{\sqrt3-1}{u},\qquad
\ell_i=\frac4{t+\kappa h_i}-2.
\end{gathered}
\]
On this interval,
\[
\frac43<\kappa<\frac53,\qquad c_0>0,\qquad
0\le\ell_i\le2.                             \tag{9}
\]
For the last assertion, \(h_i\le s\le a\le1/9\), so
\[
1\le t+\kappa h_i
 \le\frac2{\sqrt3}+\frac5{27}<2.
\]

Let
\[
M_i=\int_R g_jg_k,\qquad \{i,j,k\}=\{1,2,3\}.
\]
On \(A_i\), the coordinate \(g_i\) vanishes. The elementary inequality
\[
1+(1-x)^2+(1-y)^2+\lambda xy
 \ge3-\frac4{2+\lambda}\qquad(0\le\lambda\le2)       \tag{10}
\]
therefore gives, after integrating and using (1) and (6),
\[
3b\ge
(1-s)K-\kappa s(a-s)
-a\sum_i\ell_i+\sum_i\ell_iM_i
+\int_R\sum_i(1-g_i)^2.                     \tag{11}
\]
The exact square identity behind (10) is
\[
\frac{2+\lambda}{4}
 \left(x+y-\frac4{2+\lambda}\right)^2
+\frac{2-\lambda}{4}(x-y)^2.
\]

If \(s=0\), (11) immediately gives \(b\ge f(a)\). Assume \(s>0\), and let \(\mathbb E_R\) denote normalized expectation on \(R\). Put
\[
G=g_1+g_2+g_3,\qquad
Q=\mathbb E_R(g_1^2+g_2^2+g_3^2),
\]
and define the nonnegative quantity
\[
\mathcal E=
\mathbb E_R\left[
 \frac{(G-3u)^2}{3u}
 +c_0\left(g_1^2+g_2^2+g_3^2-\frac{G^2}{3}\right)
\right].                                   \tag{12}
\]

A rearrangement of (11) gives
\[
3b-3f(a)\ge
s\mathcal E+3su(u_*-u)+\kappa s^2-P,         \tag{13}
\]
where, with \(H=h_1+h_2+h_3=sQ\),
\[
P=\sum_i\left[
 \frac{\kappa^2h_i^2}{3(t+\kappa h_i)}
 +\frac{4\kappa h_iM_i}{t(t+\kappa h_i)}
\right].
\]
We now verify
\[
s\mathcal E+\kappa s^2-P\ge0.                \tag{14}
\]

### 4.1. Bounding the error \(P\)

Since \(M_i\le(h_j+h_k)/2\), put
\[
A_0=\frac{\kappa^2}{3t},\qquad B_0=\frac{2\kappa}{t^2}.
\]
Then
\[
P\le A_0\sum h_i^2+B_0\left(H^2-\sum h_i^2\right).
\]
Here \(B_0\ge A_0\), \(A_0\le25/27\), and \(B_0\le10/3\). Thus
\[
P\le\frac{A_0+2B_0}{3}H^2
 \le\frac{205}{81}s^2Q^2.                  \tag{15}
\]

### 4.2. A useful bound on \(Q\)

For \(0\le x_i\le1/2\), \(\sum x_i=1-s\), and \(0\le r_i\le1\),
\[
\sum_i x_ir_i\ge\left(\frac12-s\right)
                  \left(\sum_i r_i-1\right).       \tag{16}
\]
One quick proof is to minimize the left side over the weight polytope. Its vertices are permutations of \((1/2,1/2-s,0)\), where (16) is immediate.

Apply (16) to \(r_i=g_i(r)^2\), integrate over \(R\), and use (6). It follows that
\[
Q\le1+\frac{a-s}{1/2-s}\le1+2a\le\frac{11}{9}.       \tag{17}
\]

### 4.3. The remaining scalar estimate

Let
\[
k=\frac1{\sqrt3u}-1>0.
\]
Expanding (12) and applying Jensen gives
\[
\mathcal E\ge k(\mathbb E_RG)^2-2\mathbb E_RG+c_0Q+3u
             \ge-\frac1k+c_0Q+3u.           \tag{18}
\]
For \(Q\ge18/25\), this implies
\[
\mathcal E-\frac Q4\ge J(u),
\quad
J(u)=3u-\frac1k+\frac{18}{25}\left(c_0-\frac14\right)>0.       \tag{19}
\]
Indeed,
\[
J''(u)=
-\frac6{(1-\sqrt3u)^3}
-\frac{36(\sqrt3-1)}{25u^3}<0,
\]
and its values at \(u=1/\sqrt{12}\) and \(u=1/3\) are respectively
\[
\frac{97\sqrt3-167}{50}>0,\qquad
\frac{232-133\sqrt3}{50}>0.
\]

Combining (9) and (15), the left side of (14), divided by \(s\), is at least
\[
\mathcal E+s\left(\frac43-\frac{205}{81}Q^2\right).
\]
This is nonnegative if \(Q\le\sqrt{108/205}\). Otherwise
\[
Q>\sqrt{108/205}>\frac{18}{25},
\]
so (17)–(19), together with \(s\le1/9\), give the lower bound
\[
\frac Q4-\frac19\left(\frac{205}{81}Q^2-\frac43\right)>0.
\]
This last quadratic is concave in \(Q\); at the endpoints of
\([18/25,11/9]\) its values are
\[
\frac{1231}{6750},\qquad \frac{7943}{236196}.
\]
This proves (14).

Consequently (13) becomes
\[
b\ge f(a)+su(u_*-u).                        \tag{20}
\]
If \(u\le u_*\), it gives \(b\ge f(a)\). If \(u\ge u_*\), use \(s\le1\) and
\[
f(a)+u(u_*-u)=(1-u)^2
\]
to obtain \(b\ge(1-u)^2\), a contradiction. Thus \(u<u_*\), proving the kernel lemma.

## 5. The Ramsey upper bound

Define
\[
C_3(\alpha)=
\frac{\bigl(\sqrt{3-2\alpha}+2\sqrt\alpha\bigr)^2}{3},
\qquad
C_R(\alpha)=(1+\sqrt\alpha)^2,
\]
and let \(C>\max\{2,C_3(\alpha),C_R(\alpha)\}\).

If infinitely many colorings on \(\lfloor Cn\rfloor\) vertices avoided the required books, Section 1 would produce a kernel with
\[
a=\frac{\alpha}{C},\qquad b=\frac1C.
\]
These parameters meet the kernel lemma’s hypotheses. Its conclusion gives
\[
1\ge C+2\alpha-4\sqrt{\frac{\alpha C}{3}}.
\]
Setting \(y=\sqrt C\) and solving this quadratic inequality yields
\[
C\le
\left(\frac{2\sqrt\alpha+\sqrt{3-2\alpha}}{\sqrt3}\right)^2
=C_3(\alpha),
\]
a contradiction. Therefore
\[
\limsup_{n\to\infty}
\frac{r(B_{\lceil\alpha n\rceil},B_n)}n
\le\max\{2,C_3(\alpha),C_R(\alpha)\}.          \tag{21}
\]

## 6. Matching constructions

All three terms in (21) are attained asymptotically.

* **The term \(2\).** Take two blue cliques of size \(n+1\), with every cross-edge red. There is no red triangle and no blue \(B_n\).

* **The random term.** Color each edge red independently with
  \[
  p=\frac{\sqrt\alpha}{1+\sqrt\alpha}.
  \]
  Expected red and blue book sizes are \(p^2N+O(1)\) and \((1-p)^2N+O(1)\). For
  \(N=(C_R(\alpha)-\varepsilon)n\), both are below the forbidden sizes by a linear margin.

* **The three-part construction.** Partition the vertices into three equal parts. Make every within-part edge blue, and color cross-edges independently red with probability
  \[
  p=\frac{3\sqrt\alpha}
          {\sqrt{3-2\alpha}+2\sqrt\alpha}.
  \]
  A red edge has expected red book size \(p^2N/3+O(1)\). The largest expected blue book size is
  \[
  \frac{1+2(1-p)^2}{3}N+O(1),
  \]
  attained by a within-part blue edge. For a cross-part blue edge the expectation is smaller by \(p^2N/3+O(1)\).
  The identities
  \[
  C_3(\alpha)\frac{p^2}{3}=\alpha,\qquad
  C_3(\alpha)\frac{1+2(1-p)^2}{3}=1
  \]
  show that \(N=(C_3(\alpha)-\varepsilon)n\) works.

In both random constructions, conditional on the color of a proposed spine, its page indicators are independent. Hoeffding’s inequality and a union bound over \(O(N^2)\) spines give failure probability \(O(N^2)e^{-\Omega(n)}\). Thus suitable colorings exist. The ceiling in \(\lceil\alpha n\rceil\) does not affect these linear-margin arguments.

Together with (21), this proves existence of the limit and
\[
c(\alpha)=\max\{2,C_3(\alpha),C_R(\alpha)\}.   \tag{22}
\]

Finally, \(C_3(\alpha)=2\) exactly at \(\alpha=1/6\), while
\[
C_3(\alpha)-C_R(\alpha)
=\frac{\sqrt\alpha}{3}
 \left(4\sqrt{3-2\alpha}-6-\sqrt\alpha\right).
\]
The expression in parentheses is strictly decreasing and vanishes at
\[
\sqrt\alpha=\frac{4\sqrt3-2}{11},
\]
giving \(\alpha=\alpha_*\). This establishes the displayed piecewise answer, including its endpoints.

## 7. Executable checks

The following Python uses exact SymPy algebra for the identities and sign certificates in the proof. It also constructs a finite three-part coloring and **exhaustively checks every edge’s monochromatic book size**. The latter is an implementation check, not a substitute for the concentration proof.

```python
import sympy as S
import random, math

rt = S.sqrt(3)
u, s, D = S.symbols("u s D", positive=True)
h = S.symbols("h1:4", nonnegative=True)
m = S.symbols("m1:4", nonnegative=True)

a = u*u
t = 2*rt*u
kap = 3-(2*rt-3)/u
lam = 4/t-2
K = 3-t
ustar = 4/rt-2
c0 = 3-(rt-1)/u
li = [4/(t+kap*z)-2 for z in h]
H, M = sum(h), sum(m)

# Exact master rearrangement (13).
P = sum(
    kap**2*h[i]**2/(3*(t+kap*h[i]))
    + 4*kap*h[i]*m[i]/(t*(t+kap*h[i]))
    for i in range(3)
)
f = 1+2*a-4*u/rt
g = (1-u)**2
lower = ((1-s)*K-kap*s*(a-s)-a*sum(li)
         + sum(li[i]*m[i] for i in range(3))
         + 3*s-2*D+H)
Eint = lam*(H+2*M)/2-2*D+c0*H+3*u*s
assert S.factor(
    lower-3*f-Eint-3*u*(ustar-u)*s-kap*s*s+P
) == 0
assert S.simplify(g-f-u*(ustar-u)) == 0
assert S.simplify(1+kap/3-lam/2-c0) == 0

# Parameter ranges.
lo, hi = 1/(2*rt), S.Rational(1, 3)
assert S.simplify(kap.subs(u, lo)-S.Rational(4, 3)) > 0
assert S.simplify(S.Rational(5, 3)-kap.subs(u, hi)) > 0
assert 2-2/rt-S.Rational(5, 27) > 0
assert S.simplify(c0.subs(u, lo)) > 0
assert (S.Rational(25, 27)+2*S.Rational(10, 3))/3 \
       == S.Rational(205, 81)

# The scalar certificate (19).
k = lam/2
J = 3*u-1/k+S.Rational(18, 25)*(c0-S.Rational(1, 4))
assert S.simplify(
    S.diff(J, u, 2)
    + 6/(1-rt*u)**3
    + S.Rational(36, 25)*(rt-1)/u**3
) == 0
assert S.simplify(J.subs(u, lo)-(97*rt-167)/50) == 0
assert S.simplify(J.subs(u, hi)-(232-133*rt)/50) == 0
assert (97*rt-167)/50 > 0
assert (232-133*rt)/50 > 0

Q = S.symbols("Q", real=True)
assert S.Rational(108, 205) > S.Rational(18, 25)**2
F = Q/4-S.Rational(205, 729)*Q*Q+S.Rational(4, 27)
assert S.diff(F, Q, 2) < 0
assert F.subs(Q, S.Rational(18, 25)) \
       == S.Rational(1231, 6750) > 0
assert F.subs(Q, S.Rational(11, 9)) \
       == S.Rational(7943, 236196) > 0

# The two-root factorization.
v = S.symbols("v", real=True)
B = S.Rational(1, 2)+v*v*(S.Rational(1, 2)+v*v-2*v) \
    -(1-v)**2
assert S.simplify(
    B-(v*v-1)*(2*v*v-4*v+1)/2
) == 0

# Page and clique square identities.
x, y, L = S.symbols("x y L")
page = 1+(1-x)**2+(1-y)**2+L*x*y-(3-4/(2+L))
sos = ((2+L)/4*(x+y-4/(2+L))**2
       +(2-L)/4*(x-y)**2)
assert S.factor(page-sos) == 0

for ks in (2, 3, 4):
    z = S.symbols("z:"+str(ks))
    Z = sum(z)
    rr = L*(ks-1)/2
    lhs = sum((1-v)**2 for v in z) \
        + L*sum(z[i]*z[j]
                for i in range(ks) for j in range(i))
    rhs = (ks*rr/(1+rr)
           +(1-L/2)*sum((v-Z/ks)**2 for v in z)
           +(1+rr)/ks*(Z-ks/(1+rr))**2)
    assert S.factor(lhs-rhs) == 0

# Construction identities and exact transitions.
z = S.symbols("z", positive=True)  # sqrt(alpha)
ct = (S.sqrt(3-2*z*z)+2*z)**2/3
pt = 3*z/(S.sqrt(3-2*z*z)+2*z)
assert S.simplify(ct*pt**2/3-z*z) == 0
assert S.simplify(ct*(1+2*(1-pt)**2)/3-1) == 0
pr, cr = z/(1+z), (1+z)**2
assert S.simplify(cr*pr**2-z*z) == 0
assert S.simplify(cr*(1-pr)**2-1) == 0

alpha_star = S.simplify(ustar**2/(1-ustar)**2)
assert S.simplify(alpha_star-(52-16*rt)/121) == 0
al = S.symbols("al", positive=True)
c3 = 1+2*al/3+4*S.sqrt(al*(3-2*al))/3
assert S.simplify(c3.subs(al, S.Rational(1, 6))-2) == 0
assert S.simplify(
    c3.subs(al, alpha_star)-(1+S.sqrt(alpha_star))**2
) == 0

print("ALL EXACT SYMBOLIC CHECKS PASSED")
print("alpha* =", alpha_star, "=", S.N(alpha_star, 16))

# Construct a finite coloring, then check EVERY colored edge.
N, alpha, n = 600, .2, 500
rng = random.Random(8675309)
p = 3*math.sqrt(alpha)/(math.sqrt(3-2*alpha)+2*math.sqrt(alpha))
red = [0]*N
for i in range(N):
    for j in range(i+1, N):
        if i % 3 != j % 3 and rng.random() < p:
            red[i] |= 1 << j
            red[j] |= 1 << i

mask = (1 << N)-1
blue = [mask ^ red[i] ^ (1 << i) for i in range(N)]
maxbooks = []
for rows in (red, blue):
    largest = 0
    for i in range(N):
        edges = rows[i] & ~((1 << (i+1))-1)
        while edges:
            bit = edges & -edges
            j = bit.bit_length()-1
            largest = max(largest, (rows[i] & rows[j]).bit_count())
            edges -= bit
    maxbooks.append(largest)

assert maxbooks[0] < math.ceil(alpha*n)
assert maxbooks[1] < n
print("Finite exhaustive check:", N, maxbooks,
      "forbidden:", math.ceil(alpha*n), n)
```

Its output includes
```text
ALL EXACT SYMBOLIC CHECKS PASSED
alpha* = 52/121 - 16*sqrt(3)/121 = 0.2007205543710575
Finite exhaustive check: 600 [88, 317] forbidden: 100 500
```

# agent_2: last reply

The full proof is now complete and independently audited.

The resulting coefficient is
\[
c(\alpha)=
\begin{cases}
2,&0<\alpha\le \frac16,\\[2mm]
\dfrac{\bigl(\sqrt{3-2\alpha}+2\sqrt\alpha\bigr)^2}{3},
&\frac16<\alpha<\dfrac{52-16\sqrt3}{121},\\[3mm]
(1+\sqrt\alpha)^2,
&\dfrac{52-16\sqrt3}{121}\le\alpha\le1.
\end{cases}
\]
Adjacent formulas agree at both transition points.

My independent exact-check script is `workspace/agent2_finite_audit.py`. It verifies the adaptive finite-lemma identities, all numerical-constant bounds through exact algebra, the endpoint/discriminant checks, and the random-branch comparison. Both it and `workspace/agent3_greedy_certificate.py` ran successfully.

The corrected complete upper-bound proof is in `workspace/agent3_greedy_proof.md`; no mathematical gap remains identified.

# agent_3: last reply

Proved the lower constructions and the sharp mixed-type upper-bound lemma, completing the team’s proof. The resulting coefficient is
\[
c(\alpha)=
\begin{cases}
2,&0<\alpha\le \frac16,\\[2mm]
\dfrac{\bigl(\sqrt{3-2\alpha}+2\sqrt\alpha\bigr)^2}{3},
&\frac16<\alpha<\dfrac{52-16\sqrt3}{121},\\[3mm]
(1+\sqrt\alpha)^2,
&\dfrac{52-16\sqrt3}{121}\le\alpha\le1.
\end{cases}
\]
Adjacent formulas agree at both transition points.

The proof and exact computational certificates are in:
- `workspace/agent3_greedy_proof.md`
- `workspace/agent3_greedy_certificate.py`
- `workspace/agent3_lower.py`
- `workspace/agent3_finitecheck.py`

Agents 2 and 4 independently audited the key mixed-type inequality and its exact algebra. No mathematical gaps remain known; agent 1 is assembling the complete exposition and integrated Python.

# agent_4: last reply

Full proof independently audited and complete.

Confirmed:
\[
c(\alpha)=
\begin{cases}
2,&0<\alpha\le \frac16,\\[2mm]
\dfrac{(\sqrt{3-2\alpha}+2\sqrt\alpha)^2}{3},
&\frac16<\alpha<\dfrac{52-16\sqrt3}{121},\\[3mm]
(1+\sqrt\alpha)^2,
&\dfrac{52-16\sqrt3}{121}\le\alpha\le1.
\end{cases}
\]
Adjacent formulas agree at both transition points.

I independently verified the complete mixed-type greedy upper-bound argument, including the simplified all-range certificate in `workspace/agent1_finite_certificate.py`, and reran its exact symbolic checks successfully. Lower constructions, concentration estimates, and exhaustive finite-example checks also passed.

No mathematical gaps remain; agent_1 is assembling the final proof and runnable Python.