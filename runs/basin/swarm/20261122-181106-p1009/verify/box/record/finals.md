# agent_1: last reply

\[
\boxed{\displaystyle
(\alpha,C)=\left(\frac14,\,
\frac{2^{1/4}e\,\Gamma(3/4)}{\sqrt{\pi}}\right)}
\]
The constant is approximately \(2.234914123073541\).

Here is a proof. We use the **classical finite stable-permutation inclusion–exclusion theorem** for stable roommates, stated explicitly below. No asymptotic result about random stable roommates is assumed.

## 1. The finite stable-permutation sieve

For a permutation \(\sigma\) without fixed points, call \(\sigma\) stable if

1. every participant weakly prefers its successor \(\sigma(i)\) to its predecessor \(\sigma^{-1}(i)\);
2. no pair \(i,j\) both strictly prefer each other to their respective predecessors.

For a 2-cycle, the first condition is automatic. A stable permutation consisting entirely of 2-cycles is precisely a stable perfect matching.

We use the following exact, finite combinatorial theorem, usually called the stable-permutation inclusion–exclusion theorem or sieve.

**Stable-permutation sieve.** For every strict preference profile,
\[
\mathbf 1_{\{\text{a stable perfect matching exists}\}}
=
\sum_{\substack{\sigma:\ \text{all cycles even}\\
                         \text{all cycles have length }\ge2}}
(-1)^{c_{\ge4}(\sigma)}
\mathbf 1_{\{\sigma\text{ is stable}\}},
\tag{1}
\]
where \(c_{\ge4}(\sigma)\) is the number of cycles of length at least four.

This is the classical finite identity underlying Mertens’s inclusion–exclusion formula. In particular, the sign is one minus sign **per long cycle**, not per vertex. We will need substantial cancellation in this identity.

Write
\[
p(\sigma)=\Pr(\sigma\text{ is stable}).
\]
Taking expectations in (1) gives
\[
P_n=\sum_\sigma(-1)^{c_{\ge4}(\sigma)}p(\sigma).
\tag{2}
\]

We next estimate \(p(\sigma)\) uniformly over **all** the permutations appearing here.

## 2. An integral for a stable permutation

Let \(m\) be the number of vertices in cycles of \(\sigma\) of length at least four. Let \(E_\sigma\) be the set of unordered pairs that are adjacent in its cycles.

Condition on
\[
x_i=U_{i,\sigma^{-1}(i)}.
\]
For each vertex in a long cycle, its successor score must be less than \(x_i\), contributing \(x_i\). For a nonadjacent unordered pair \(\{i,j\}\), the probability that it does not block is \(1-x_ix_j\). All the random variables used in these conditions are distinct. Consequently,
\[
p(\sigma)=
\int_{[0,1]^n}
\left(\prod_{i\text{ in long cycles}}x_i\right)
\prod_{\{i,j\}\notin E_\sigma}(1-x_ix_j)\,d\boldsymbol x.
\tag{3}
\]

Set
\[
\alpha_i=
\begin{cases}
1,&i\text{ is in a 2-cycle},\\
2,&i\text{ is in a long cycle},
\end{cases}
\qquad q=\sum_i\alpha_i=n+m.
\]
Define
\[
I(n,m)=
\int_{\mathbb R_+^n}e^{-(\sum_i x_i)^2/2}
       \prod_i x_i^{\alpha_i-1}\,d\boldsymbol x.
\]
Simplex integration gives
\[
I(n,m)=\frac{2^{q/2-1}\Gamma(q/2)}{\Gamma(q)}.
\tag{4}
\]

The estimate we need is
\[
\boxed{\quad
p(\sigma)=I(n,m)\left(e^{\mu(n,m)}+O(n^{-1})\right),
\quad}
\tag{5}
\]
uniformly over all even-cycle permutations, where
\[
\begin{split}
a&=\frac{2n+4m}{n+m+1},\\
b&=\frac{n+7m}{2(n+m+1)},\\
\mu(n,m)&=\frac a2+b-\frac{a^2}{4}.
\end{split}
\tag{6}
\]
All \(O\)-constants below are absolute unless indexed otherwise.

Here is a proof of that uniform estimate.

### 2.1 Exact moments for the reference measure

Normalize the integrand in (4) to a probability density, and denote its random vector by \(X\). If nonnegative integers \(r_i\) have total \(2d\), radial-simplex integration yields
\[
\mathbb E\prod_iX_i^{r_i}
=
\frac{\prod_i(\alpha_i)_{r_i}}
     {(q+1)(q+3)\cdots(q+2d-1)}.
\tag{7}
\]
Here \((u)_r=u(u+1)\cdots(u+r-1)\).

In particular, for any fixed total degree \(2d\),
\[
\mathbb E\prod_iX_i^{r_i}=O_d(n^{-d}).
\tag{8}
\]

We will also use a weighted version. Put \(Q=\sum_iX_i^2\). For fixed \(c>0\) and fixed \(\boldsymbol r\),
\[
\mathbb E\left[
\mathbf1_{\{X\in[0,1]^n\}}e^{cQ}
\prod_iX_i^{r_i}\right]
\le C_{c,\boldsymbol r}\,
\mathbb E\prod_iX_i^{r_i}.
\tag{9}
\]
To prove this, on the unit cube use
\[
e^{cX_i^2}\le1+(e^c-1)X_i^2.
\]
Expand the product over \(i\), and apply (7). Adding exponent two at a previously unused coordinate multiplies the numerator by at most \(6\), while supplying a new denominator factor at least \(q\). At the bounded number of already used coordinates, replace \(6\) by a constant depending only on \(\boldsymbol r\). The sum is bounded by a constant times
\[
(1+6(e^c-1)/q)^n=O_c(1).
\]
This proves (9).

### 2.2 Expanding the logarithm

Write
\[
B=\sum_{\{i,j\}\in E_\sigma}X_iX_j,
\qquad
H=\frac Q2+B-\frac{Q^2}{4}.
\]
Every vertex has degree at most two in \(E_\sigma\), so \(B\le Q\). Therefore
\[
H\le\frac32Q-\frac14Q^2\le\frac94.
\tag{10}
\]

The ratio of the integrands in (3) and (4), without the unit-cube indicator, is
\[
F(X)=e^{(\sum_iX_i)^2/2}
       \prod_{\{i,j\}\notin E_\sigma}(1-X_iX_j).
\]
On the event \(G=\{\max_iX_i\le1/2\}\), expansion of \(\log(1-z)\) gives
\[
\log F
=
H+\frac14\sum_iX_i^4
+\frac12\sum_{\{i,j\}\in E_\sigma}X_i^2X_j^2-R,
\]
where
\[
0\le R\le C\left(\sum_iX_i^3\right)^2.
\]
Thus
\[
|\log F-H|
\le C\left[
\sum_iX_i^4+
\sum_{\{i,j\}\in E_\sigma}X_i^2X_j^2+
\left(\sum_iX_i^3\right)^2\right].
\tag{11}
\]
Both \(\log F\) and \(H\) are at most \(3Q/2\). By (8)–(9), the expectation of \(e^{3Q/2}\) times the right side of (11), restricted to the cube, is \(O(n^{-1})\). Indeed, the three unweighted orders are respectively
\[
n\,O(n^{-2}),\qquad n\,O(n^{-2}),\qquad n^2O(n^{-3}).
\]

The discarded event is harmless. Formula (7) gives
\[
\Pr(G^c)\le 2^6\sum_i\mathbb EX_i^6=O(n^{-2}),
\]
and (9) gives the same bound with the cube-restricted weight \(e^{3Q/2}\). On the cube, \(F\le e^{3Q/2}\), while (10) bounds \(e^H\) everywhere. Hence
\[
\frac{p(\sigma)}{I(n,m)}
=\mathbb Ee^H+O(n^{-1}).
\tag{12}
\]

### 2.3 Concentration to the required accuracy

By (7),
\[
\mathbb EQ=a.
\]
There are \((n-m)/2\) edges between \(\alpha=1\) vertices and \(m\) edges between \(\alpha=2\) vertices. Thus
\[
\mathbb EB
=\frac{(n-m)/2+4m}{q+1}=b.
\]

We have, uniformly in \(\sigma\),
\[
\operatorname{Var}Q=O(n^{-1}),\qquad
\operatorname{Var}B=O(n^{-1}),\qquad
\mathbb E(Q-a)^4=O(n^{-1}).
\tag{13}
\]
For completeness, these orders follow directly from (7):

* For \(1\le j\le4\), expanding \(Q^j\), terms with distinct indices have total numerator \((2n+4m)^j+O_j(n^{j-1})\); terms with repeated indices contribute \(O_j(n^{j-1})\). Therefore
  \[
  \mathbb EQ^j=a^j+O_j(n^{-1}).
  \]
  This proves the first and third assertions.
* In \(B^2\), only \(O(n)\) ordered edge pairs share a vertex, because degrees are at most two. The remaining pairs give \(b^2+O(n^{-1})\) by (7). This proves the second assertion.

With \(\mu\) as in (6),
\[
H-\mu
=\frac{1-a}{2}(Q-a)+(B-b)-\frac14(Q-a)^2.
\]
Consequently,
\[
\mathbb E(H-\mu)=O(n^{-1}),\qquad
\mathbb E(H-\mu)^2=O(n^{-1}).
\]
Both \(H\) and \(\mu\) are bounded above by \(9/4\). Taylor’s theorem therefore gives
\[
\mathbb Ee^H=e^\mu+O(n^{-1}).
\]
Together with (12), this proves (5).

We also record the elementary bound
\[
\left|e^{\mu(n,m)}-e^{1/2}\right|
\le C\frac{m+1}{n}.
\tag{14}
\]
For example, substituting (6) gives
\[
\mu(n,m)=
\frac{3m^2+6mn+11m+n^2+3n}{2(m+n+1)^2},
\]
from which (14) follows for \(0\le m\le n\).

## 3. Summing the signed cycle counts

Put \(n=2N\), \(m=2k\), and define coefficients
\[
\begin{split}
b_k&=[w^k]\,e^{w/2}(1-w)^{1/2},\\
a_k&=[w^k]\,e^{-w/2}(1-w)^{-1/2}.
\end{split}
\tag{15}
\]
The exponential formula for labelled permutations shows that their signed and unsigned numbers with \(2k\) long-cycle vertices are respectively
\[
\frac{(2N)!}{2^{N-k}(N-k)!}\,b_k,
\qquad
\frac{(2N)!}{2^{N-k}(N-k)!}\,a_k.
\tag{16}
\]
Indeed, the signed generating function for the long cycles is
\[
\exp\left(-\sum_{\ell\ge2}\frac{w^\ell}{2\ell}\right)
=e^{w/2}(1-w)^{1/2}.
\]

Multiplying the common factor in (16) by \(I(2N,2k)\) gives
\[
A_{N,k}
=
\frac{\Gamma(N+1)\Gamma(N+1/2)}
     {\Gamma(N-k+1)\Gamma(N+k+1/2)}
=
\prod_{j=0}^{k-1}\frac{N-j}{N+j+1/2}.
\tag{17}
\]
In particular, \(A_{N,0}=1\).

For \(0\le k\le N\),
\[
A_{N,k}\le e^{-k^2/(4N)}.
\tag{18}
\]
This follows by applying \(\log(1-u)\le-u\) to each factor in (17).

The coefficients \(a_k\) are nonnegative, and coefficientwise
\[
e^{-w/2}(1-w)^{-1/2}\preceq(1-w)^{-1/2}.
\]
Hence \(a_k=O((k+1)^{-1/2})\), so (18) gives
\[
\sum_{k=0}^Na_kA_{N,k}=O(N^{1/4}).
\tag{19}
\]

Applying (5) in (2), and using (19) to sum its errors absolutely,
\[
P_{2N}
=
\sum_{k=0}^N b_kA_{N,k}e^{\mu(2N,2k)}
+O(N^{-3/4}).
\tag{20}
\]

## 4. The coefficient signs and their tail

Let
\[
B(w)=e^{w/2}(1-w)^{1/2}.
\]
Its derivative satisfies
\[
B'(w)=-\frac w2e^{w/2}(1-w)^{-1/2}.
\tag{21}
\]
The function on the right after \(-w/2\) has strictly positive coefficients. Therefore
\[
b_0=1,\qquad b_1=0,\qquad b_k<0\quad(k\ge2).
\]
The binomial coefficient asymptotic, convolved with \(e^{w/2}\), gives
\[
-b_k\sim
\frac{e^{1/2}}{2\sqrt\pi}\,k^{-3/2},
\qquad
|b_k|\le Ck^{-3/2}.
\tag{22}
\]
One can obtain this directly from (21): if
\[
h_j=[w^j]e^{w/2}(1-w)^{-1/2},
\]
then
\[
-b_k=\frac{h_{k-2}}{2k},
\qquad
h_j\sim\frac{e^{1/2}}{\sqrt{\pi j}}.
\]
The latter follows by convolution with the absolutely summable coefficients \(1/(2^r r!)\).

In particular \(\sum_k|b_k|<\infty\), and evaluating \(B(1)\) gives
\[
\sum_{k\ge0}b_k=0.
\tag{23}
\]

Equations (14), (18), and (22) imply
\[
\begin{split}
&\left|
\sum_{k=0}^Nb_kA_{N,k}
  \left(e^{\mu(2N,2k)}-e^{1/2}\right)
\right|\\
&\hspace{12mm}\le
\frac CN\left(1+\sum_{k=2}^Nk^{-1/2}e^{-k^2/(4N)}\right)
=O(N^{-3/4}).
\end{split}
\]
Thus (20) reduces to
\[
P_{2N}
=e^{1/2}\sum_{k=0}^Nb_kA_{N,k}
+O(N^{-3/4}).
\tag{24}
\]

This cancellation is why replacing the inclusion–exclusion sum by its absolute values would give the wrong answer.

## 5. The limiting integral

Extend \(A_{N,k}=0\) for \(k>N\). From (23),
\[
\sum_{k=0}^Nb_kA_{N,k}
=
\sum_{k\ge2}(-b_k)(1-A_{N,k}).
\tag{25}
\]
For fixed \(x>0\), (17) gives
\[
A_{N,\lfloor x\sqrt N\rfloor}\longrightarrow e^{-x^2}.
\tag{26}
\]
Indeed, uniformly for \(k=O(\sqrt N)\),
\[
\log A_{N,k}
=-\frac{k^2-k/2}{N}+O(k^3/N^2).
\]

There is also the useful global bound
\[
0\le1-A_{N,k}\le\min(k^2/N,1).
\tag{27}
\]
For \(k\le N\), use \(1-\prod r_j\le\sum(1-r_j)\) in (17); for \(k>N\), the bound is immediate.

Equations (22), (26), and (27) justify the Riemann-sum limit
\[
N^{1/4}\sum_{k=0}^Nb_kA_{N,k}
\longrightarrow
\frac{e^{1/2}}{2\sqrt\pi}
\int_0^\infty x^{-3/2}(1-e^{-x^2})\,dx.
\tag{28}
\]
To spell out domination, the contribution of \(k\le\delta\sqrt N\), after multiplication by \(N^{1/4}\), is \(O(\delta^{3/2})\); that of \(k\ge L\sqrt N\) is \(O(L^{-1/2})\). On the intervening compact interval, ordinary Riemann-sum convergence applies.

Integration by parts evaluates the integral:
\[
\begin{split}
\int_0^\infty x^{-3/2}(1-e^{-x^2})\,dx
&=4\int_0^\infty x^{1/2}e^{-x^2}\,dx\\
&=2\Gamma(3/4).
\end{split}
\]
Combining this with (24)–(28),
\[
P_{2N}
\sim
\frac{e\,\Gamma(3/4)}{\sqrt\pi}\,N^{-1/4}.
\]
Since \(N=n/2\),
\[
\boxed{\displaystyle
P_n\sim
\frac{2^{1/4}e\,\Gamma(3/4)}{\sqrt\pi}\,n^{-1/4}}
\qquad(n\to\infty,\ n\text{ even}).
\tag{29}
\]

The constant is strictly positive and finite. Consequently any smaller exponent gives limit zero, and any larger exponent gives limit \(+\infty\). This proves uniqueness of the requested ordered pair.

## 6. Executable checks

The following code was run. It does not merely print the proposed answer. It:

* exhaustively checks the pointwise finite sieve for all \(1296\) preference profiles on four participants;
* checks additional random profiles at \(n=6,8\);
* integrates the finite polynomials exactly, obtaining \(P_4\) and \(P_6\);
* checks the algebra for \(\mu\), the product formula, and its Gaussian bound;
* numerically checks the limiting integral;
* computes the cancellation-sensitive one-dimensional sum in (24).

Finite checks supplement, rather than replace, the uniform estimates above.

```python
import itertools
import math
from collections import defaultdict
from fractions import Fraction

import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.special import gamma


def even_permutations(n):
    out = []
    for p in itertools.permutations(range(n)):
        seen, cycles = set(), []
        for i in range(n):
            if i in seen:
                continue
            c, j = [], i
            while j not in seen:
                seen.add(j)
                c.append(j)
                j = p[j]
            cycles.append(c)

        if all(len(c) % 2 == 0 for c in cycles):
            inv = [0] * n
            for i, j in enumerate(p):
                inv[j] = i
            sign = (-1) ** sum(len(c) > 2 for c in cycles)
            matching = all(len(c) == 2 for c in cycles)
            out.append((p, inv, sign, matching))
    return out


def check_sieve(n, exhaustive=False, trials=1000):
    perms = even_permutations(n)
    choices = [
        list(itertools.permutations(j for j in range(n) if j != i))
        for i in range(n)
    ]
    rng = np.random.default_rng(293)

    if exhaustive:
        profiles = itertools.product(*choices)
    else:
        profiles = (
            [choices[i][rng.integers(len(choices[i]))]
             for i in range(n)]
            for _ in range(trials)
        )

    count = solvable = 0
    for profile in profiles:
        rank = np.zeros((n, n), dtype=int)
        for i, row in enumerate(profile):
            for k, j in enumerate(row):
                rank[i, j] = k

        signed_sum, has_matching = 0, False
        for p, inv, sign, matching in perms:
            if any(rank[i, p[i]] > rank[i, inv[i]]
                   for i in range(n)):
                continue

            blocked = any(
                rank[i, j] < rank[i, inv[i]]
                and rank[j, i] < rank[j, inv[j]]
                for i in range(n)
                for j in range(i + 1, n)
                if j != p[i] and j != inv[i]
            )
            if blocked:
                continue

            signed_sum += sign
            has_matching |= matching

        assert signed_sum == int(has_matching)
        count += 1
        solvable += has_matching

    print("sieve:", n, count, "profiles;", solvable, "solvable")


check_sieve(2, exhaustive=True)
check_sieve(4, exhaustive=True)
check_sieve(6, trials=3000)
check_sieve(8, trials=200)


# Exact integration of (3), by expanding its polynomial.
def exact_integral(cycles):
    n = sum(map(len, cycles))
    adjacent = set()
    initial_powers = [0] * n

    for c in cycles:
        for h, i in enumerate(c):
            adjacent.add(tuple(sorted((i, c[(h + 1) % len(c)]))))
            if len(c) > 2:
                initial_powers[i] = 1

    poly = {tuple(initial_powers): 1}
    for i in range(n):
        for j in range(i + 1, n):
            if (i, j) in adjacent:
                continue
            new = defaultdict(int, poly)
            for powers, coefficient in poly.items():
                p = list(powers)
                p[i] += 1
                p[j] += 1
                new[tuple(p)] -= coefficient
            poly = {p: c for p, c in new.items() if c}

    return sum(
        (Fraction(c, math.prod(r + 1 for r in p))
         for p, c in poly.items()),
        Fraction(0)
    )


P4 = (
    3 * exact_integral([[0, 1], [2, 3]])
    - 6 * exact_integral([[0, 1, 2, 3]])
)
P6 = (
    15 * exact_integral([[0, 1], [2, 3], [4, 5]])
    - 90 * exact_integral([[0, 1, 2, 3], [4, 5]])
    - 120 * exact_integral([[0, 1, 2, 3, 4, 5]])
)
assert P4 == Fraction(26, 27)
assert P6 == Fraction(181431847, 194400000)
print("exact P4 =", P4)
print("exact P6 =", P6)


# Symbolic checks.
n, m, w = sp.symbols("n m w", positive=True)
a = (2*n + 4*m) / (n + m + 1)
b = (n + 7*m) / (2*(n + m + 1))
mu = a/2 + b - a*a/4
mu_explicit = (
    3*m*m + 6*m*n + 11*m + n*n + 3*n
) / (2*(m+n+1)**2)
assert sp.simplify(mu - mu_explicit) == 0
assert sp.limit(mu.subs(m, 0), n, sp.oo) == sp.Rational(1, 2)

B = sp.exp(w/2) * sp.sqrt(1-w)
assert sp.simplify(
    sp.diff(B, w) + w*sp.exp(w/2)/(2*sp.sqrt(1-w))
) == 0


# Exact checks of (17) and finite checks of (18).
for N in range(1, 70):
    A = Fraction(1)
    for k in range(N + 1):
        if k:
            A *= Fraction(2*(N-k+1), 2*(N+k)-1)

        direct = (
            Fraction(math.factorial(2*N) * 2**(2*k), 2)
            * Fraction(
                math.factorial(N+k-1),
                math.factorial(N-k)
                * math.factorial(2*N+2*k-1)
            )
        )
        assert A == direct
        assert float(A) <= math.exp(-k*k/(4*N)) + 1e-14


# Check the limiting integral.
f = lambda x: x**(-1.5) * (-math.expm1(-x*x))
J = quad(f, 0, 1)[0] + quad(f, 1, np.inf)[0]
assert abs(J - 2*gamma(.75)) < 1e-9


# Stable evaluation of e^(1/2) sum b_k A_{N,k}.
# We use sum (-b_k)(1-A_{N,k}) plus the tail.
def model_probability(N):
    b_prev2, b_prev1 = 1.0, 0.0
    A, answer = 1.0, 0.0

    for k in range(2, N + 1):
        bk = ((k-1)*b_prev1 - 0.5*b_prev2) / k
        if k == 2:
            A = (N/(N+.5)) * ((N-1)/(N+1.5))
        else:
            A *= (N-k+1)/(N+k-.5)
        answer += (-bk) * (1-A)
        b_prev2, b_prev1 = b_prev1, bk

    # sum_{k=0}^N b_k is [w^N] e^(w/2)(1-w)^(-1/2).
    c_prev2, c_prev1 = 1.0, 1.0
    for k in range(2, N + 1):
        c_prev2, c_prev1 = (
            c_prev1,
            (k*c_prev1 - .5*c_prev2)/k
        )
    answer += c_prev1
    return math.exp(.5) * answer


C = 2**.25 * math.e * gamma(.75) / math.sqrt(math.pi)
print("C =", C)
for N in (100, 1000, 10000, 100000):
    p = model_probability(N)
    print(N, p, "scaled:", p*(2*N)**.25)

print("All checks passed.")
```

Some output from the run was
```text
exact P4 = 26/27
exact P6 = 181431847/194400000
C = 2.234914123073541

N          scaled model probability
100        2.3710778613022807
1000       2.2844828330637648
10000      2.251182629886616
100000     2.240115701639623
```

Thus the asymptotic probability, its positive constant, and the uniqueness of the exponent have been proved. Nothing remains to determine for the stated question.