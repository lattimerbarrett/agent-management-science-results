#1 agent_1: An exact answer can be given by a **finite determinantal formula**. This avoids any genericity assumptions on \(b\): the ranks in the formula are taken **after substituting the given coefficient vector**. In particular, zero components and special algebraic relations between components require no exceptions.

The matrices below have \(O(g^2)\) rows, have explicitly specified entries in \(\mathbb Q[b_0,\ldots,b_{r-1}]\), and involve no surface-cohomology computations.

## 1. The formula

Put
\[
N=4g-3,\qquad B=4g,
\]
and introduce formal variables \(t,w\). Define
\[
s(t)=(1-t^{4g+2})^{1/2},\qquad
a(t)=-\frac12t^{-2g+2}s(t),
\]
and
\[
P(t,w)=1-k\,t^k\phi_b(t)w^k.
\]
Only powers \(w^0,\ldots,w^{N-1}\) will be used.

For \(M\geq0\), let \(\mathcal B(M)\) be the following finite list of Laurent series:
\[
\boxed{\quad
\mathcal B(M)=
 \{t^{-2i}:2i\leq M\}
 \ \cup\
 \{t^{-2i-2g-1}s(t):2i+2g+1\leq M\}.
\quad}                                                     \tag{1}
\]

Here are the three matrices appearing in the answer. A column specified by a Laurent series means its vector of coefficients in the stated row set.

### The matrix \(A_O\)

Its rows are indexed by
\[
(m,e),\qquad 0\leq m<N,\quad -B-3m\leq e<0.
\]
For every \(0\leq n<N\) and \(f\in\mathcal B(4n+B)\), include the column
\[
\boxed{\quad
[w^mt^e]\bigl(f(t)t^nw^nP^{-n/k}\bigr).
\quad}                                                     \tag{2}
\]

### The matrix \(A_L\)

Its row set is the same as that of \(A_O\). For every \(0\leq n<N\) and
\(f\in\mathcal B(4n+B-2g+2)\), include the column
\[
\boxed{\quad
[w^mt^e]\bigl(f(t)a(t)t^nw^nP^{1-n/k}\bigr).
\quad}                                                     \tag{3}
\]

### The matrix \(A_S\)

There are two kinds of rows:
\[
\begin{aligned}
(h,m,e)&:\quad 0\leq m<N,\quad 1-B-3m\leq e<0,\\
(v,m,e)&:\quad 0\leq m<N,\quad -B-3m\leq e<0.
\end{aligned}
\]
Its columns are the coefficient vectors of the following pairs, the first component supplying the \(h\)-rows and the second the \(v\)-rows:

* for \(f\in\mathcal B(4n+B)\),
  \[
  \boxed{\quad
  \left(0,\ f(t)t^nw^nP^{1-n/k}\right);
  \quad}                                                   \tag{4}
  \]
* for \(f\in\mathcal B(4n+B-2g+1)\),
  \[
  \boxed{\quad
  \left(
  f(t)a(t)t^nw^nP^{-n/k},\
  f(t)a(t)t^nw^nP^{-n/k}
       \left(-t^{-1}-t^k\phi_b'(t)w^k\right)
  \right).
  \quad}                                                   \tag{5}
  \]

In (2)–(5), discard powers \(w^N,w^{N+1},\ldots\). Thus every requested coefficient is obtained by a finite binomial expansion.

The answer is
\[
\boxed{\displaystyle
\Delta_b
 =4g-3+\operatorname{rank}_{\mathbb C}A_S(b)
       -\operatorname{rank}_{\mathbb C}A_O(b)
       -\operatorname{rank}_{\mathbb C}A_L(b).
}                                                          \tag{6}
\]

This is a finite determinantal formula as a function of \(g\) and the entire vector \(b\). If desired, “rank” in (6) can equivalently be replaced by “the largest order of a nonzero minor,” with value zero for a zero matrix. Consequently (1)–(6) specify the answer using just finitely many explicitly given polynomials and their zero/nonzero values.

For illustration, exact evaluation gives
\[
\begin{array}{c|c|r|rrr}
g&b&\Delta_b&h^1(\mathcal O)&h^1(S)&h^1(L)\\ \hline
2&(1)&0&3&10&7\\
3&(1)&0&7&31&24\\
4&(1,0)&0&12&62&50\\
4&(0,1)&-1&11&61&49\\
5&(1,0)&0&20&107&87\\
5&(0,1)&-1&18&104&85\\
7&(0,0,1)&-2&35&221&184
\end{array}
\]
The formula, not this table, covers all vectors.

## 2. Proof

### 2.1 A uniform finite-neighborhood bound

Write \(I=\mathcal I_E\). Since \(I/I^2\simeq\mathcal O_E(p)\), the associated graded pieces are
\[
\begin{aligned}
I^n/I^{n+1}&\simeq\mathcal O_E(np),\\
I^nL/I^{n+1}L&\simeq\Theta_E(np).
\end{aligned}                                             \tag{7}
\]
For the logarithmic tangent bundle, restriction to \(E\) gives
\[
0\longrightarrow\mathcal O_E
 \longrightarrow S|_E
 \longrightarrow\Theta_E
 \longrightarrow0.
\]
Hence
\[
0\longrightarrow\mathcal O_E(np)
 \longrightarrow I^nS/I^{n+1}S
 \longrightarrow\Theta_E(np)
 \longrightarrow0.                                      \tag{8}
\]

If \(n\geq N=4g-3\), both line bundles in (8) have vanishing \(H^1\): indeed
\[
\deg\Theta_E(np)=n-2g+2>2g-2.
\]
The same applies to (7).

It follows, successively on all finite neighborhoods, that
\[
H^1\!\left(E,\ I^NF/I^{N+j}F\right)=0
\quad(j\geq1),\qquad F=\mathcal O,S,L.
\]
The theorem on formal functions then gives
\[
R^1f_*(I^NF)=0.
\]
Here this higher direct image is supported at the singular point, so vanishing of its completion implies its vanishing. Since the representative downstairs is Stein,
\[
H^1(X,I^NF)=0.
\]
Also \(H^2(X,I^NF)=0\), because the fibers of \(f\) have dimension at most one. Therefore
\[
\boxed{\quad
H^1(X,F)\simeq H^1(X,F/I^NF),
\qquad F=\mathcal O,S,L.
\quad}                                                     \tag{9}
\]

Thus the single bound \(N=4g-3\) works for all \(b\), including every degeneration of its components.

### 2.2 The transition matrices on that neighborhood

On \(C_g\setminus\{p\}\), use the nowhere-zero vector field
\[
\delta x=z,\qquad
\delta z=\frac{2g+1}{2}x^{2g}.
\]
In the parameter \(t\),
\[
\delta=a(t)\partial_t,\qquad
a(t)=-\frac12t^{-2g+2}s(t).                                \tag{10}
\]

Put \(y=y_U\) and \(w=y_W\). Inverting the prescribed gluing gives
\[
y=twP^{-1/k},\qquad P=1-kt^k\phi_b(t)w^k.                 \tag{11}
\]

Use the logarithmic frames
\[
H=\delta\big|_{y\ {\rm fixed}},\qquad V=y\partial_y
\]
on the first chart, and
\[
h=\partial_t\big|_{w\ {\rm fixed}},\qquad v=w\partial_w
\]
on the second chart. Direct differentiation of the gluing gives
\[
V=P\,v
\]
and
\[
H=a\,h+
a\left(-t^{-1}-t^k\phi_b'(t)w^k\right)v.                 \tag{12}
\]
In particular,
\[
H\wedge V=aP\,h\wedge v.                                 \tag{13}
\]

Combining (11)–(13), the transition images of \(y^n\), \(y^nV\),
\(y^nH\), and \(y^nH\wedge V\) are exactly the series in
(2)–(5). This proves the asserted transition formulas, including the derivative term in (5).

### 2.3 The coefficient ring on the punctured curve

The functions regular away from \(p\) form
\[
R=\mathbb C[x,z]/(z^2-x^{2g+1}+1).
\]
Every element has a unique expression
\[
A(x)+zB(x).
\]
The pole orders of the indicated monomials are
\[
\operatorname{pole}_p(x^i)=2i,\qquad
\operatorname{pole}_p(x^iz)=2i+2g+1.                       \tag{14}
\]
Their expansions at \(p\) give exactly (1).

For completeness, cohomology here can be computed by the principal-parts presentation
\[
H^1(C,\mathcal F)
 =
\frac{\mathbb C((t))^d}
     {\mathbb C[[t]]^d+G(t)R^d},                         \tag{15}
\]
where \(G\) is the transition matrix for the finite-rank bundle obtained by pushing \(F/I^NF\) to \(C\). In this application \(d=N\) or \(2N\).

One way to justify (15) without an algebraicity assumption on the original analytic surface is to observe that the entries of \(G\) are meromorphic at \(p\). Its lattice lies between
\(t^q\mathbb C[[t]]^d\) and \(t^{-q}\mathbb C[[t]]^d\) for some \(q\). It therefore defines a vector bundle by finitely many principal-part conditions at \(p\). This bundle is algebraic, its analytic realization is the given bundle, and the usual principal-parts sequence gives (15).

After quotienting by \(\mathbb C[[t]]^d\), the target of (15) consists simply of finite negative Laurent polynomials, in each fiber degree and each component.

### 2.4 Why the displayed finite matrices compute the whole quotient

This is the key finiteness check: it explains why no omitted high-pole columns can introduce extra relations.

Set
\[
d=2g-1.
\]
Every monomial of \(\phi_b\) has exponent at least \(-d\). Consequently the coefficient of \(w^{\ell k}\) in any power of \(P\) has \(t\)-valuation at least
\[
\ell(k-d).
\]
We have
\[
4k\geq d.                                                \tag{16}
\]
Indeed \(k=g-\lfloor(g+2)/3\rfloor\), and the inequality follows immediately, or by checking the three residue classes of \(g\).

For \(A_O\), a column beginning in degree \(n\), with coefficient of pole order at most \(4n+B\), can have in degree \(m=n+\ell k\) no exponent below
\[
-B-3n+\ell(k-d)\geq-B-3m,
\]
by (16). Thus every retained \(O\)-column lies entirely in the retained row window.

The same calculation applies to \(L\), accounting for
\(\operatorname{ord}_t(a)=-2g+2\), and gives its stated pole bound
\(4n+B-2g+2\).

For \(S\), the horizontal window starts one exponent higher. The bound
\(4n+B-2g+1\) gives precisely that horizontal window; multiplication by
\(-t^{-1}\) reaches precisely the vertical window. The other vertical term,
\(-t^k\phi_b'w^k\), satisfies the same inequality (16). So all retained
\(S\)-columns also lie inside their retained row windows.

Now quotient the complete principal-parts target by these finite row windows. The omitted columns map **isomorphically** to the omitted rows:

* in a fixed fiber degree, their leading exponents run through all omitted exponents, each once;
* this uses (14) and the fact that every integer at least \(2g\) is a pole order in \(R\);
* all remaining terms have higher \(t\)-exponent;
* transition terms never decrease fiber degree;
* for \(S\), eliminate the horizontal component first, then the vertical one.

The leading coefficients are nonzero. Elimination is finite: there are only \(N\) fiber degrees, and each principal part contains only finitely many negative powers.

Equivalently, decomposing columns and rows into retained and omitted parts, the full map has block form
\[
\begin{pmatrix}
A_F&*\\
0&T_F
\end{pmatrix},
\]
where \(T_F\) is an isomorphism. Hence its cokernel is the cokernel of \(A_F\).

Together with (9) and (15), this proves
\[
\boxed{\quad
h^1(X,F)=\#\operatorname{rows}(A_F)-\operatorname{rank}(A_F),
\qquad F=\mathcal O,S,L.
\quad}                                                     \tag{17}
\]

### 2.5 Taking the alternating sum

Let
\[
Q=BN+\frac{3N(N-1)}2.
\]
The row counts are
\[
\#A_O=Q,\qquad \#A_L=Q,\qquad \#A_S=2Q-N.
\]
Substitution in (17) yields
\[
\Delta_b
=N+\operatorname{rank}A_S-\operatorname{rank}A_O
  -\operatorname{rank}A_L,
\]
which is (6).

No step used any nonvanishing condition on an individual \(b_j\). Indeed the proof also works for the excluded zero vector.

## 3. Executable exact Python

The following is Python using SageMath. It constructs precisely the matrices above and computes their exact ranks. The optional field `K` can be any suitable exact Sage field; for example, rational coefficients use `QQ`, algebraic coefficients can use a number field, and symbolic coefficients can use a rational-function field.

The square-root truncation is deliberately generous. All omitted terms have exponent too large to contribute to any requested negative coefficient.

```python
from sage.all import *

def matrices(g, b, K=QQ, N=None, B=None, D=3):
    r = (g + 2) // 3
    k = g - r
    assert len(b) == r

    b = list(map(K, b))
    N = 4*g - 3 if N is None else N
    B = 4*g if B is None else B

    R = LaurentPolynomialRing(K, 't')
    t = R.gen()

    # More than enough terms for every requested negative coefficient.
    T = 20*g + 20*N + 10*B
    s = sum(
        (K(binomial(QQ(1)/2, j)) * (-1)**j
         * t**(j*(4*g+2))
         for j in range(T//(4*g+2) + 1)),
        R.zero()
    )
    a = -t**(-2*g+2) * s / 2
    phi = sum(
        (b[j] * t**(-(2*g-1-2*j)) for j in range(r)),
        R.zero()
    )
    u = -k * t**k * phi       # P = 1 + u*w^k
    deriv = t**k * phi.derivative()

    def basis(M):
        return (
            [t**(-2*i) for i in range(M//2 + 1)]
            +
            [t**(-2*i-2*g-1)*s
             for i in range(max(0, (M-2*g-1)//2 + 1))]
        )

    result = {}

    for kind in ['O', 'S', 'L']:
        comps = ['h', 'v'] if kind == 'S' else ['q']
        rows = {}

        for c in comps:
            for m in range(N):
                for e in range(-B-D*m + int(c == 'h'), 0):
                    rows[c, m, e] = len(rows)

        cols = []

        for typ in (['H', 'V'] if kind == 'S' else [kind]):
            c = {'H': 'h', 'V': 'v'}.get(typ, 'q')

            for n in range(N):
                cap = n + B + D*n + {
                    'H': -2*g+1,
                    'L': -2*g+2
                }.get(typ, 0)

                for f in basis(cap):
                    col = {}

                    def put(poly, component, degree):
                        for e, value in poly.dict().items():
                            i = rows.get((component, degree, e))
                            if i is not None:
                                col[i] = col.get(i, K.zero()) + value

                    for ell in range((N-1-n)//k + 1):
                        m = n + ell*k
                        alpha = (
                            (1 if typ in ['V', 'L'] else 0)
                            - QQ(n)/k
                        )
                        pol = (
                            f * t**n
                            * K(binomial(alpha, ell))
                            * u**ell
                        )

                        if typ in ['H', 'L']:
                            pol *= a

                        put(pol, c, m)

                        if typ == 'H':
                            put(-pol/t, 'v', m)
                            if m+k < N:
                                put(-pol*deriv, 'v', m+k)

                    cols.append(col)

        entries = {
            (i, j): value
            for j, col in enumerate(cols)
            for i, value in col.items()
            if value
        }
        result[kind] = matrix(
            K, len(rows), len(cols), entries, sparse=True
        )

    return result


def delta(g, b, K=QQ, **options):
    A = matrices(g, b, K, **options)
    h = {
        name: M.nrows() - M.rank()
        for name, M in A.items()
    }
    answer = h['O'] - h['S'] + h['L']

    # Independently check the row-count cancellation in formula (6).
    N = options.get('N', 4*g-3)
    assert answer == (
        N + A['S'].rank() - A['O'].rank() - A['L'].rank()
    )
    return answer, h
```

Here are executable checks, including vanishing components, larger principal-part windows, and larger infinitesimal neighborhoods:

```python
for g in range(2, 7):
    r = (g+2)//3
    vectors = (
        [[int(i == j) for i in range(r)] for j in range(r)]
        + [[i+2 for i in range(r)]]
    )

    for b in vectors:
        value = delta(g, b)
        assert delta(g, b, B=4*g+2) == value
        assert delta(g, b, N=4*g-1) == value
        print(g, b, value)

print("All checks passed")
```

I ran these checks successfully. I also checked the split vector \(b=0\) against the independent Serre-duality counts
\[
\sum_{n\geq0}h^0\!\left(\mathcal O_E((2g-2-n)p)\right),
\qquad
\sum_{n\geq0}h^0\!\left(\mathcal O_E((4g-4-n)p)\right),
\]
using the pole semigroup (14), and checked the sparse rank computations against a separate exact SymPy implementation.

Thus (1)–(6), with the executable implementation above, determine the exact answer for **every** allowed \(g\) and **every** allowed coefficient vector \(b\). No exceptional-vector or genericity case remains unresolved.