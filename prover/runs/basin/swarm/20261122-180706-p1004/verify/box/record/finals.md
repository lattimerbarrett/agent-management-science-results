# agent_1: last reply

Put
\[
c_g=\log\!\left(\frac{\sqrt{g_+}+\sqrt{g_-}}
{\sqrt{g_+}-\sqrt{g_-}}\right).
\]
In particular, \(c_g>0\).

The answer is
\[
\boxed{
(\gamma,\kappa)=
\begin{cases}
\left(2w,\;4\sqrt{c_g\,w(1-2w)}\right),&0<w<\frac12,\\[2mm]
(1,0),&w\geq\frac12.
\end{cases}}
\]

The constants \(L,\alpha,\beta,d\) affect the constants and logarithmic factors in the risk bounds, but, apart from \(w=(\alpha+\beta)/d\), do not affect this ordered pair.

Here is a proof. The polynomial-estimation details matter: using just one spatial resolution does not give the stated square-root-logarithmic constant.

## 1. Bounds that will be proved

For \(0<w<1/2\), write
\[
H=2\sqrt{c_gw(1-2w)}.
\]
We prove that, for some fixed positive constants \(C,c,B\),
\[
c\,n^{-2w}e^{-2H\sqrt{\log n}}
\ \leq\ R_n\
\leq C(\log n)^B n^{-2w}e^{-2H\sqrt{\log n}}.             \tag{1}
\]
For \(w\geq1/2\), we prove
\[
\frac cn\leq R_n\leq \frac{C(\log n)^B}{n}.               \tag{2}
\]
All constants in the proof may depend on the fixed class parameters.

These inequalities imply the answer, including its assertion at \(w=1/2\).

## 2. Two polynomial facts

Set
\[
l=g_-,\qquad h=g_+,\qquad
\rho=\frac{\sqrt h-\sqrt l}{\sqrt h+\sqrt l}.
\]
Thus \(0<\rho<1\) and \(c_g=\log(1/\rho)\).

### 2.1 Sharp approximation and moment annihilation

With \(c=(h+l)/2\) and \(r=(h-l)/2\), the Chebyshev expansion is
\[
\frac1u=\frac1{\sqrt{lh}}
\left\{1+2\sum_{j=1}^{\infty}(-\rho)^j
T_j\left(\frac{u-c}{r}\right)\right\},
\qquad l\leq u\leq h.                                   \tag{3}
\]
Consequently, there are polynomials \(p_m\), of degree at most \(m\), such that
\[
\sup_{u\in[l,h]}|p_m(u)-u^{-1}|\leq C\rho^m.              \tag{4}
\]

The matching dual identity is just as important. Define the signed measure
\[
\int F(u)\,d\sigma_m(u)
=\frac{(-1)^m}{\pi}\int_0^\pi
 F(c+r\cos t)\cos(mt)\,dt.
\]
For \(m\geq2\),
\[
\int u^j\,d\sigma_m(u)=0\quad(0\leq j<m),\qquad
\int\frac{d\sigma_m(u)}u=\frac{\rho^m}{\sqrt{lh}}.         \tag{5}
\]
Also \(\|\sigma_m\|_{\rm TV}\leq1\).

For completeness, (3) follows from
\[
\frac{1-\rho^2}{1+2\rho\cos t+\rho^2}
=1+2\sum_{j\geq1}(-\rho)^j\cos(jt)
\]
and the identities
\[
c+r\cos t=\frac{\sqrt{lh}}{1-\rho^2}
(1+2\rho\cos t+\rho^2).
\]
Orthogonality of the cosine functions gives (5).

### 2.2 Matrix versions with uniformly controlled derivatives

We will use fixed-dimensional real symmetric matrices with eigenvalues in \([l,h]\). Formula (3), applied to a matrix, approximates its inverse.

A slightly more general fact will be useful. A product of a fixed number of entries of inverses of such matrices has polynomial approximations \(Q_m\), of total degree at most \(m\), satisfying
\[
\|Q_m-Q\|\leq C(m+1)^b\rho^m,                            \tag{6}
\]
where \(b,C\) are fixed.

These approximations also have a uniform analytic bound: on a fixed complex neighborhood of the allowed real matrices,
\[
|Q_m|\leq C\quad\text{for every }m.                      \tag{7}
\]
Here and below the matrix dimensions are fixed.

Here are details ensuring that (7) does not hide a degree-dependent loss. Expand each inverse entry using (3), multiply the expansions, and retain terms whose total Chebyshev degree is at most \(m\). The discarded terms are bounded by
\[
C\sum_{j>m}(j+1)^b\rho^j
\leq C'(m+1)^b\rho^m.
\]
Choose \(1<R<1/\rho\). On a sufficiently small fixed complex neighborhood of the real symmetric matrices in question,
\[
\left\|T_j\left(\frac{G-cI}{r}\right)\right\|\leq C_RR^j.
\]
This follows from the matrix Cauchy formula on a Bernstein ellipse of parameter \(R\): the resolvents are uniformly bounded there. The multiplied series is therefore absolutely bounded by a convergent series with terms \(C(j+1)^b(\rho R)^j\). This proves (7).

In particular, Cauchy estimates imply that for all \(s\geq0\),
\[
\frac1{s!}|D^sQ_m[z_1,\ldots,z_s]|
\leq C^{s+1}\prod_i\|z_i\|.                             \tag{8}
\]
The constants are independent of \(m\). The same conclusion holds after multiplication by any fixed-degree polynomial in bounded moment variables.

## 3. An unbiased polynomial-estimation lemma

We record the variance bound used for the upper bound.

Partition \(D\) into \(k\) equal cubes of volume \(v=1/k\). In each cube, let \(Z\) be a vector of a fixed number of bounded local features of \((X,A,Y)\), multiplied by the cube indicator and divided by \(v\). Its mean \(\mu_C\) thus consists of normalized local moments.

Suppose
\[
\Phi(P)=\sum_C vF_C(\mu_C),                               \tag{9}
\]
where each \(F_C\) is a polynomial of degree at most \(D_0\). Assume the \(F_C\)'s have a common bounded analytic extension to a fixed neighborhood of all their allowed moment vectors.

Replace every product of \(j\) expectations in (9) by its unbiased average over \(j\) distinct observations. This defines a measurable unbiased estimator \(\widehat\Phi\). For \(D_0=O(\log n)\),
\[
\operatorname{Var}(\widehat\Phi)
 \leq \sum_{s=1}^{D_0}
 \frac{C^s k^{s-1}}{\binom ns}.                          \tag{10}
\]
Consequently,
\[
\operatorname{Var}(\widehat\Phi)
\leq \frac{CD_0}{n}
 \max\left\{1,\left(\frac{CD_0k}{n}\right)^{D_0-1}\right\}. \tag{11}
\]
If \(CD_0k/n\leq1/2\), the sharper bound \(C/n\) holds.

To prove this, the order-\(s\) canonical kernel in the Hoeffding decomposition is the canonicalization of
\[
\frac1{s!}D^s\Phi(\mu)[Z_1,\ldots,Z_s].
\]
Before canonicalization this is zero unless all \(s\) arguments fall in the same cube. Bound (8), bounded features, and \(g\leq g_+\) show that its squared \(L^2\)-norm is at most \(C^sk^{s-1}\). Canonicalization is an orthogonal projection and cannot increase that norm. Orthogonality of the Hoeffding components gives (10).

For \(D_0=O(\log n)\),
\[
\binom ns^{-1}\leq \frac{2s!}{n^s},\qquad 1\leq s\leq D_0
\]
for all large \(n\). Summing the resulting geometric upper bound proves (11) and its sharper version.

This lemma requires no smoothness of \(g\).

## 4. Local polynomial projection increments

Choose an integer polynomial degree
\[
p\geq \max(r_\alpha,r_\beta),
\]
and let \(V_j\) be the functions that are polynomials of total degree at most \(p\) on each cube of the dyadic partition with
\[
k_j=2^{jd}
\]
cubes. Let \(\Pi_j\) denote orthogonal projection in \(L^2(g)\), and put
\[
\theta_j=\langle\Pi_ja,\Pi_jb\rangle_g,\qquad
\theta=\int abg.
\]

Taylor approximation under the stated Hölder definition, followed by the minimizing property of projection, gives
\[
\|a-\Pi_ja\|_{L^2(g)}\leq Ck_j^{-\alpha/d},\qquad
\|b-\Pi_jb\|_{L^2(g)}\leq Ck_j^{-\beta/d}.
\]
Thus
\[
|\theta-\theta_j|\leq Ck_j^{-w}.                         \tag{12}
\]

We next construct polynomial approximations to each increment
\(\theta_j-\theta_{j-1}\) whose bias retains the factor \(k_{j-1}^{-w}\).

### 4.1 The residual-numerator identity

Fix a parent cube \(C\), of volume \(v\), and use coordinates normalized to that cube. Let the fine basis consist of orthonormal polynomial bases on its \(2^d\) children. Its dimension is fixed.

Write
\[
G= v^{-1}\int_C \phi\phi^\top g,\quad
h_a=v^{-1}\int_C \phi ag,\quad
h_b=v^{-1}\int_C \phi bg.
\]
Let \(E\) embed the coarse polynomial space into the fine space, and set
\[
G_c=E^\top GE,\qquad h_{a,c}=E^\top h_a,\qquad
h_{b,c}=E^\top h_b.
\]
All eigenvalues of \(G,G_c\) lie in \([l,h]\).

Put \(q=\dim(G_c)\) and
\[
R_a=\det(G_c)h_a-GE\,\operatorname{adj}(G_c)h_{a,c},
\]
with \(R_b\) defined similarly. The contribution of \(C\) to the projection increment is exactly
\[
v\,
\frac{R_a^\top G^{-1}R_b}{\det(G_c)^2}.                 \tag{13}
\]

Indeed,
\[
\frac{R_a}{\det(G_c)}
=h_a-GEG_c^{-1}E^\top h_a,
\]
the fine moment vector of the residual after coarse projection. Formula (13) follows by the orthogonal decomposition of the nested projection spaces.

Crucially, \(R_a=0\) whenever \(a\) is a coarse polynomial. Subtracting a Taylor polynomial on the parent cube therefore gives
\[
\|R_a\|\leq Ck_{j-1}^{-\alpha/d},\qquad
\|R_b\|\leq Ck_{j-1}^{-\beta/d}.                         \tag{14}
\]

### 4.2 Polynomial approximation of the increment

The matrix
\[
G^{-1}\det(G_c)^{-2}
=G^{-1}\{\det(G_c^{-1})\}^2
\]
has entries that are sums of products of \(2q+1\) inverse-matrix entries. Apply Section 2.2 and replace it in (13) by its degree-\(m\) polynomial approximation.

The resulting approximation to the entire increment is a polynomial functional, of degree at most
\[
D_0=m+2q+2.
\]
By (6) and (14), its bias is bounded by
\[
Ck_{j-1}^{-w}(m+1)^b\rho^m.                             \tag{15}
\]
By (7), it satisfies the analytic boundedness assumption of Section 3, uniformly in \(m,j\). Hence it has an unbiased estimator with variance bounded by (10)–(11), using \(k=k_{j-1}\).

The initial term \(\theta_0\) is handled directly by polynomial approximation of \(G^{-1}\). It has the same conclusions, with \(k=1\).

We have proved the following usable construction:

> At each resolution of complexity \(k\), an increment has an estimator with bias at most
> \[
> Ck^{-w}(m+1)^b e^{-c_gm},
> \]
> degree at most \(m+C\), and variance satisfying (10)–(11).

## 5. Upper bound below the elbow

Assume \(0<w<1/2\), and write
\[
N=\log n,\qquad H=2\sqrt{c_gw(1-2w)}.
\]
Choose large fixed constants \(A,M\), in that order, and set
\[
\delta=e^{-wN-H\sqrt N}N^M.                             \tag{16}
\]
Choose the last dyadic resolution \(J\) so that
\[
k_J^{-w}\asymp\delta.
\]

For an increment of complexity \(k\), including the initial term with \(k=1\), use
\[
m(k)=
\left\lceil
\frac{wN+H\sqrt N-(M-A)\log N-w\log k}{c_g}
\right\rceil.                                         \tag{17}
\]
For all sufficiently large \(n\), these integers are positive and \(O(N)\).

By (15),
\[
|\text{bias at this resolution}|
\leq C\delta N^{b-A}.
\]
There are \(O(N)\) resolutions. Taking \(A>b+3\), summing the biases, and using (12), gives total bias \(O(\delta)\).

It remains to check the variances, including their leading stretched-exponential constant.

Put \(x=\log(k/n)\), and \(D_0=m(k)+C\). From (17),
\[
D_0\leq
\frac{H\sqrt N-wx-(M-A)\log N}{c_g}+C.                  \tag{18}
\]

If \(k\leq n/N^{B_0}\), with a sufficiently large fixed \(B_0\), then \(D_0\leq CN\) and the sharper part of (11) gives variance \(C/n=o(\delta^2)\).

For the remaining resolutions, \(x\geq-B_0\log N\), so \(D_0=O(\sqrt N)\). Bound (11) gives
\[
\log\operatorname{Var}
\leq -N+O(\log N)+
\max\{0,(D_0-1)(x+\log(CD_0))\}.                        \tag{19}
\]
For \(-B_0\log N\leq x\leq0\), the last term is
\(O(\sqrt N\log N)=o(N)\), again giving \(o(\delta^2)\).

For \(x\geq0\), combine (18) with \(\log(CD_0)\leq C_1\log N\). Completing the square bounds the last term in (19) by
\[
\frac{\{H\sqrt N-(M-A-wC_1)\log N+O(1)\}^2}
{4wc_g}.
\]
The leading term is
\[
\frac{H^2}{4wc_g}N=(1-2w)N.                             \tag{20}
\]
By taking \(M\) sufficiently large, the next term is a negative constant times \(\sqrt N\log N\). Thus every variance is \(O(\delta^2)\).

Sum the increment estimators, and subtract the result from the empirical mean of \(AY\). The squared \(L^2\) triangle inequality costs at most the square of the number of resolutions. The empirical mean contributes \(O(1/n)\). Consequently,
\[
R_n\leq C N^{B}e^{-2wN-2H\sqrt N}.                      \tag{21}
\]
This proves the upper half of (1).

## 6. Upper bound at and above the elbow

Suppose \(w\geq1/2\). Choose a sufficiently large fixed \(B_0\), and stop at a resolution satisfying
\[
k_J\asymp n^{1/(2w)}N^{-B_0}.
\]
Then
\[
k_J^{-w}\asymp n^{-1/2}N^{B_0w}.
\]
At complexity \(k\), choose
\[
m(k)=\left\lceil
\frac{\frac12N-w\log k+C\log N}{c_g}
\right\rceil,
\]
where \(C\) is large enough to absorb the polynomial factor in (15).

All degrees are \(O(N)\), all resolutions satisfy \(k\leq n/N^{B_0}\) eventually, and their variances are \(O(1/n)\). The summed biases and the truncation error are \(n^{-1/2}\) times a fixed power of \(N\). Hence
\[
R_n\leq Cn^{-1}N^B.                                    \tag{22}
\]

## 7. Lower bound below the elbow

We now prove the lower half of (1). This also explains why the constant in (20) is sharp.

### 7.1 Smooth regression bumps and irregular densities

Use a partition into \(k=M^d\) equal cubes \(C_j\), and let \(\varphi_j\) be rescaled copies of a fixed nonzero \(C^\infty\) bump supported strictly inside each cube.

For latent variables \(u_j\in[l_n,h_n]\) and signs \(R_j,S_j\in\{-1,1\}\), define
\[
a(x)=a_0k^{-\alpha/d}\frac{R_j}{u_j}\varphi_j(x),\qquad
b(x)=b_0k^{-\beta/d}\frac{S_j}{u_j}\varphi_j(x)
\quad(x\in C_j),                                       \tag{23}
\]
where \(a_0,b_0>0\) are sufficiently small fixed constants.

The standard rescaling calculation for a smooth compactly supported bump gives, uniformly in the latent variables,
\[
a\in\mathcal H^\alpha(L),\qquad b\in\mathcal H^\beta(L).
\]
This calculation also applies to integer smoothness under the question's convention: the derivatives of order \(t-1\) have Lipschitz constant bounded after multiplication by the amplitude \(k^{-t/d}\). The functions extend by zero to \(U\). Taking \(a_0,b_0\) smaller if necessary ensures \(|a|+|b|\leq1/2\).

Start with an unnormalized density equal to \(u_j\) on \(C_j\). Write
\[
\bar u=k^{-1}\sum_j u_j
\]
and normalize it to \(g(x)=u_j/\bar u\). Given \(X=x\), take \(A,Y\in\{-1,1\}\) with probabilities
\[
P(A=s,Y=t\mid X=x)=\frac14\{1+sa(x)+tb(x)\}.             \tag{24}
\]
These probabilities are positive, the conditional means are \(a,b\), and \(E(AY\mid X)=0\).

Let \(B_\varphi=\int_{[0,1]^d}\varphi^2>0\). The target is
\[
\psi=-a_0b_0B_\varphi\,k^{-w}\,
\frac{k^{-1}\sum_jR_jS_j/u_j}{\bar u}.                   \tag{25}
\]

Take
\[
l_n=g_-+\frac1N,\qquad h_n=g_+-\frac1N
\]
for large \(n\). If \(\bar u\) is sufficiently close to \(1\), the normalized \(g\) satisfies the required density bounds.

### 7.2 Two moment-matching priors

Apply (5) on \([l_n,h_n]\), and denote its parameters by \(\rho_n,c_n=\log(1/\rho_n)\). Then
\[
c_n=c_g+O(N^{-1}).                                     \tag{26}
\]

Let \(\nu_n\) be the arcsine probability measure on that interval. Choose a fixed small \(\epsilon>0\) and a probability measure
\[
\mu_n=\epsilon\nu_n+\frac12\delta_1+
 \left(\frac12-\epsilon\right)\delta_{z_n}
\]
having mean \(1\). Explicitly,
\[
z_n=1+\frac{\epsilon(1-(l_n+h_n)/2)}{1/2-\epsilon}.
\]
A sufficiently small fixed \(\epsilon\) puts \(z_n\) strictly inside \([l_n,h_n]\), uniformly for large \(n\).

Under both priors, take the \(u_j\)'s independently from \(\mu_n\). Conditional on \(u_j\), give the signs the distribution
\[
P_\pm(R_j=r,S_j=s\mid u_j)
=\frac14\left\{1\pm \epsilon_0rs
      \frac{d\sigma_m}{d\mu_n}(u_j)\right\},             \tag{27}
\]
with a small fixed \(\epsilon_0>0\). Since \(\mu_n\geq\epsilon\nu_n\), these are valid probabilities. The derivative is zero at the atom \(1\), so the signs there are independent.

By (5),
\[
E_\pm(R_jS_j/u_j)
=\pm\frac{\epsilon_0\rho_n^m}{\sqrt{l_nh_n}}.            \tag{28}
\]

### 7.3 An informative experiment with a collision bound

The following experiment is more informative than a Poisson sample from the unnormalized law.

In each cube independently, generate a Poisson number of attempts of mean \(n'h_n/k\), where \(n'\) is a sufficiently large fixed multiple of \(n\). Each attempt has a uniform position in the cube and is either:

* rejected, with probability \(1-u_j/h_n\); or
* accepted with marks \(A=s,Y=t\), with probability
\[
\frac{u_j+s\,a_0k^{-\alpha/d}R_j\varphi_j(x)
+t\,b_0k^{-\beta/d}S_j\varphi_j(x)}{4h_n}.
\]

Accepted observations form precisely a Poisson process with intensity \(n'\) times the unnormalized law.

Conditional on \(M\) attempts in a cube, its likelihood is a polynomial in \(u_j,R_j,S_j\). The difference between the two sign priors retains only monomials odd in both \(R_j\) and \(S_j\). Such monomials:

1. contain the factor \(a_0b_0k^{-w}\);
2. have degree at most \(M-2\) in \(u_j\).

By moment annihilation, the two mixture likelihoods therefore agree exactly whenever \(M\leq m+1\).

For larger \(M\), the absolute likelihood difference is at most
\(C^Mk^{-w}\), relative to the common counting-and-position reference measure. The atom \(u=1\), of mass at least \(1/2\), gives a lower bound \(c^M\) for the denominator likelihood: both rejection and all four acceptance probabilities are bounded below there.

It follows that the one-cube chi-squared divergence is at most
\[
Ck^{-2w}\sum_{M\geq m+2}\frac{(Cn/k)^M}{M!}
\leq Ck^{-2w}(Cn/k)^{m+2},                             \tag{29}
\]
when \(n/k\) is sufficiently small. Independence across cubes gives
\[
\chi^2(\mathbb P_+,\mathbb P_-)
\leq
\exp\{Ck^{1-2w}(Cn/k)^{m+2}\}-1.                       \tag{30}
\]

### 7.4 Choosing the parameters

Put
\[
t_*=\sqrt{\frac{c_g(1-2w)}w},
\]
and choose \(k=M^d\) with
\[
\log k=N+t_*\sqrt N+o(1).
\]
Choose
\[
m=
\left\lceil
\frac{(1-2w)\log k}{\log(k/(Cn))}
\right\rceil+C_0.                                     \tag{31}
\]
The fixed constants can be chosen so that (30) tends to zero. Moreover,
\[
m=\frac{1-2w}{t_*}\sqrt N+O(1).                         \tag{32}
\]
Equations (26), (28), and (32) imply that the target separation has order
\[
\begin{aligned}
k^{-w}\rho_n^m
&=\exp\left\{-wN-
 \left(wt_*+\frac{c_g(1-2w)}{t_*}\right)\sqrt N+O(1)\right\}\\
&=\exp\{-wN-H\sqrt N+O(1)\}.                            \tag{33}
\end{aligned}
\]
The last equality is the elementary minimization
\[
\min_{t>0}\left\{wt+\frac{c_g(1-2w)}t\right\}
=2\sqrt{c_gw(1-2w)}=H.                                \tag{34}
\]

### 7.5 Normalization, concentration, and return to fixed sample size

The \(u_j\)'s are bounded, independent, and have mean \(1\). Hence
\[
P(|\bar u-1|>c/N)\leq 2e^{-c'k/N^2}=o(1).
\]
On the complementary event, \(g=u_j/\bar u\) satisfies the required bounds.

Also, the variance of \(k^{-1}\sum_jR_jS_j/u_j\) is \(O(1/k)\), whereas its squared mean has order \(\rho_n^{2m}\). Since
\[
k\rho_n^{2m}=\exp\{N+O(\sqrt N)\}\longrightarrow\infty,
\]
(25) concentrates under the two priors in disjoint intervals separated by a constant times (33).

Condition each prior on these high-probability density and target-concentration events. This changes the data distributions in total variation by \(o(1)\). Thus the two conditioned priors are supported on the required class, have separated targets, and their informative-experiment distributions have total variation bounded away from \(1\).

Finally, accepted observations, in random order, are iid from the normalized law. Choose \(n'\) as a large enough fixed multiple of \(n\); the chance of having fewer than \(n\) accepted observations is \(e^{-cn}\), uniformly. Any estimator based on \(n\) observations could therefore be applied in the informative experiment, with only an exponentially small additional risk.

The two-prior testing inequality now gives
\[
R_n\geq c\,e^{-2wN-2H\sqrt N},                          \tag{35}
\]
as claimed.

## 8. Parametric lower bound

For every choice of the fixed parameters, the class contains the submodel
\[
g=1,\qquad
P(A=s,Y=t\mid X)=\frac14(1+\tau st).
\]
Here \(a=b=0\), so every Hölder requirement is satisfied, and
\(\psi=\tau\).

Testing \(\tau=\pm c/\sqrt n\) gives
\[
R_n\geq c'/n.                                         \tag{36}
\]
Together with (22), this proves (2).

## 9. Computational checks

The following Python was run successfully. It checks the exact projection identity, the sharp Chebyshev/dual identities, the saddle-point algebra, the polynomial-estimation variance identity in an exactly enumerable example, and the likelihood degree cancellation underlying (29).

The numerical checks supplement, rather than replace, the uniform arguments above.

```python
import math
import numpy as np
import sympy as sp
from scipy.integrate import quad
from numpy.polynomial.chebyshev import chebval

# 1. Exact residual-numerator / projection-increment identity.
a, b, c, x, y, z, t = sp.symbols("a b c x y z t")
G = sp.Matrix([[a, b], [b, c]])
E = sp.Matrix([1, 0])
ha, hb = sp.Matrix([x, y]), sp.Matrix([z, t])
Gc = (E.T * G * E)[0]

Ra = Gc * ha - G * E * x
Rb = Gc * hb - G * E * z

difference = (
    (ha.T * G.inv() * hb)[0] - x*z/Gc
    - (Ra.T * G.inv() * Rb)[0] / Gc**2
)
assert sp.simplify(difference) == 0
assert sp.simplify(Gc*(G*E) - G*E*Gc) == sp.zeros(2, 1)
print("Projection and annihilation identities: PASS")

# 2. Sharp inverse expansion and moment-annihilating dual.
for lo, hi in [(0.2, 3.0), (0.8, 1.3), (0.01, 8.0)]:
    mid, rad = (lo + hi)/2, (hi - lo)/2
    rho = (np.sqrt(hi)-np.sqrt(lo))/(np.sqrt(hi)+np.sqrt(lo))

    for m in [2, 3, 8, 15]:
        integral = quad(
            lambda q: np.cos(m*q)/(mid + rad*np.cos(q)),
            0, np.pi, epsabs=1e-11
        )[0] / np.pi
        assert abs(integral - (-rho)**m/np.sqrt(lo*hi)) < 1e-10

        for j in range(m):
            moment = quad(
                lambda q: ((mid+rad*np.cos(q))/hi)**j*np.cos(m*q),
                0, np.pi, epsabs=1e-11
            )[0] / np.pi
            assert abs(moment) < 1e-10

    degree = 200
    coefficients = np.r_[
        1.0, 2*(-rho)**np.arange(1, degree+1)
    ] / np.sqrt(lo*hi)
    grid = np.linspace(lo, hi, 1001)
    error = np.max(np.abs(
        chebval((grid-mid)/rad, coefficients) - 1/grid
    ))
    tail_bound = (
        2/np.sqrt(lo*hi) * rho**(degree+1)/(1-rho)
    )
    assert error <= tail_bound + 2e-11

print("Chebyshev approximation and exact dual moments: PASS")

# 3. Exact sharp saddle point and matching quadratic maximum.
w, cg, X = sp.symbols("w cg X", positive=True)
H = 2*sp.sqrt(w*cg*(1-2*w))
tstar = sp.sqrt(cg*(1-2*w)/w)
objective = w*X + cg*(1-2*w)/X

assert sp.simplify(sp.diff(objective, X).subs(X, tstar)) == 0
assert sp.simplify(objective.subs(X, tstar) - H) == 0
assert sp.simplify(H**2/(4*w*cg) - (1-2*w)) == 0
print("Sharp saddle-point algebra: PASS")

# 4. Exact polynomial U-statistic variance by finite enumeration.
# F(p)=p^D; unbiased estimator is choose(K,D)/choose(n,D).
for n in [8, 12, 20]:
    for D in range(1, min(6, n)+1):
        p = 0.37
        variance = 0.0
        for k in range(n+1):
            probability = math.comb(n, k)*p**k*(1-p)**(n-k)
            estimate = (
                math.comb(k, D)/math.comb(n, D) if k >= D else 0.0
            )
            variance += probability*(estimate-p**D)**2

        hoeffding_formula = sum(
            math.comb(D, s)**2
            * p**(2*(D-s)) * (p*(1-p))**s
            / math.comb(n, s)
            for s in range(1, D+1)
        )
        assert abs(variance-hoeffding_formula) < 1e-13

print("Polynomial-estimator variance identity: PASS")

# 5. Attempt-likelihood cancellation.
# Odd-odd sign terms must contain both regression amplitudes,
# leaving degree at most M-2 in u.
u, R, S, aa, bb = sp.symbols("u R S aa bb")
factors = [
    u + aa*R + bb*S,
    3-u,
    u - aa*R + bb*S,
    u + aa*R - bb*S,
    3-u,
]
polynomial = sp.Poly(sp.prod(factors), R, S)
odd_odd = sum(
    coefficient
    for (i, j), coefficient in polynomial.terms()
    if i % 2 == 1 and j % 2 == 1
)

assert sp.degree(odd_odd, u) <= len(factors)-2
assert sp.rem(odd_odd, aa, aa) == 0
assert sp.rem(odd_odd, bb, bb) == 0
print("Likelihood moment-cancellation algebra: PASS")

# Example numerical values.
cg_value = np.log(
    (np.sqrt(2)+np.sqrt(0.5))/(np.sqrt(2)-np.sqrt(0.5))
)
for w_value in [0.05, 0.15, 0.25, 0.40, 0.49, 0.50, 0.80]:
    gamma = min(2*w_value, 1)
    kappa = (
        4*np.sqrt(cg_value*w_value*(1-2*w_value))
        if w_value < 0.5 else 0.0
    )
    print(f"w={w_value:.2f}: gamma={gamma:.6f}, "
          f"kappa={kappa:.6f}")
```

All five groups of assertions passed.

## 10. Uniqueness and conclusion

Bounds (1)–(2) give the requested logarithmic expansion. To see uniqueness, suppose two pairs had the asserted property. Subtracting their expansions gives
\[
(\gamma_1-\gamma_2)\log n
+(\kappa_1-\kappa_2)\sqrt{\log n}
=O(\log\log n).
\]
Division first by \(\log n\), and then by \(\sqrt{\log n}\), proves equality of both coordinates.

Thus the stated ordered pair is proved for every allowed set of fixed parameters and every \(w>0\), including the boundary \(w=1/2\). Nothing remains unresolved for the requested expansion.