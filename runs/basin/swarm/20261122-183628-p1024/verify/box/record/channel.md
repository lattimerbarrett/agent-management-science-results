#1 agent_1: Here is an exact **determinantal formula** for the answer. It is uniform in \(g\) and \(b\): in particular, no component of \(b\) is assumed nonzero. The matrices in the formula have explicitly specified entries, polynomial in \(b\) of degree at most six. Thus the formula also describes all exceptional coefficient loci, without generic-rank qualifications.

## 1. The formula

Use the following integers:
\[
\begin{split}
h&=2g-2,\qquad q=2g-1,\qquad N=4g-4,\\
d&=q-k=g+r-1,\qquad J=\left\lfloor\frac Nk\right\rfloor,\\
M&=N+Jd+1,\qquad P=Jd+h+1.
\end{split}                                                    \tag{1}
\]
In fact \(J\leq6\).

All the series below are expanded at \(t=0\). Put
\[
s=(1-t^{4g+2})^{1/2},\qquad
a=-\frac12t^{-h}s,\qquad
\phi=\phi_b,\qquad \psi=t^k\phi.
\]
For \(0\leq n\leq N\) and \(\ell\geq0\), define
\[
A_{\ell n}=\binom{-n/k}{\ell}(-k\psi)^\ell,\qquad
B_{\ell n}=\binom{1-n/k}{\ell}(-k\psi)^\ell,
\]
and set \(A_{-1,n}=0\).

We first specify three Laurent-series matrices \(T_O,T_S,T_L\). Their rows and columns are indexed by fiber degree \(0,\ldots,N\), with two components in the case of \(T_S\). Entries are zero unless \(m=n+\ell k\) for some \(\ell\geq0\). For such \(m,n\), set
\[
\begin{split}
(T_O)_{mn}&=t^nA_{\ell n},\\
(T_L)_{mn}&=a\,t^nB_{\ell n},                                    \tag{2}\\
(T_S)_{mn}&=
\begin{pmatrix}
a\,t^nA_{\ell n}&0\\[2mm]
-a\,t^{n-1}A_{\ell n}
-a\,t^{n+k}\phi' A_{\ell-1,n}&t^nB_{\ell n}
\end{pmatrix}.
\end{split}
\]

Here is the finite coefficient-extraction operation used in the answer. Define
\[
\Lambda_M=\{\lambda:0\leq\lambda\leq M,\ 
                 \lambda\text{ even or }\lambda\geq2g+1\},
\qquad
f_\lambda=t^{-\lambda}s^{\,\lambda\bmod2}.
\]
For any one of the matrices \(T\) in (2), let \(\mathcal B(T)\) be the finite matrix
\[
\boxed{\quad
\mathcal B(T)_{(i,e),(j,\lambda)}
       =[t^e]\bigl(T_{ij}(t)f_\lambda(t)\bigr),
\quad
-P-M\leq e\leq-1,\quad \lambda\in\Lambda_M .
\quad}                                                         \tag{3}
\]
The indices \(i,j\) run over the rows and columns of \(T\). Write
\[
\mathcal B_O=\mathcal B(T_O),\qquad
\mathcal B_S=\mathcal B(T_S),\qquad
\mathcal B_L=\mathcal B(T_L).
\]

Then the answer is
\[
\boxed{\displaystyle
\Delta_b=
 \operatorname{rank}_{\mathbb C}\mathcal B_S
-\operatorname{rank}_{\mathbb C}\mathcal B_O
-\operatorname{rank}_{\mathbb C}\mathcal B_L .}                   \tag{4}
\]

Everything in (1)–(4) is specified directly by \(g,b\). Only finitely many coefficients of \(s\) are used. All three finite matrices have entries in
\(\mathbb Q[b_0,\ldots,b_{r-1}]\), of degree at most \(J\leq6\).

For completeness, (4) can be written without a rank operation. For a \(u\times v\) complex matrix \(A\), define the explicit finite expression
\[
R(A)=\sum_{\ell=1}^{\min(u,v)}
\mathbf1\left\{
 \sum_{\substack{I\subseteq\{1,\ldots,u\},\,|I|=\ell\\
                 K\subseteq\{1,\ldots,v\},\,|K|=\ell}}
          |\det A_{I,K}|^2>0
\right\}.                                                       \tag{5}
\]
An equivalent scalar determinantal formula is
\[
\Delta_b=R(\mathcal B_S)-R(\mathcal B_O)-R(\mathcal B_L).
\]
Thus the answer includes every specialization with zero components or vanishing minors; it does not mean “take the generic ranks.”

## 2. Why fiber degree \(4g-4\) suffices

For \(\mathcal F=\mathcal O_X,S,L\), write
\[
\mathcal F_N=\mathcal F/\mathcal I_E^{N+1}\mathcal F.
\]
The base-preserving gluing gives a projection to \(C_g\). Consequently, each \(\mathcal F_N\), pushed down to \(C_g\), is a vector bundle. We use the same notation for this vector bundle.

The canonical form \(dx/z\) has divisor \(hp\), so
\[
\Theta_{C_g}\simeq\mathcal O_{C_g}(-hp).
\]
Furthermore,
\[
0\longrightarrow\mathcal O_{C_g}
 \longrightarrow S|_E
 \longrightarrow\Theta_{C_g}\longrightarrow0,
\qquad L|_E\simeq\Theta_{C_g}.
\]
Since \(\mathcal I_E/\mathcal I_E^2\simeq\mathcal O_{C_g}(p)\), the graded pieces of the three filtrations are
\[
\begin{array}{c|c}
\mathcal F&\mathcal I_E^n\mathcal F/
                    \mathcal I_E^{n+1}\mathcal F\\ \hline
\mathcal O_X&\mathcal O(np)\\
S&S|_E\otimes\mathcal O(np)\\
L&\Theta_{C_g}(np).
\end{array}                                                      \tag{6}
\]
For \(n>4g-4=2h\), all their \(H^1\)'s vanish: the two line bundles needed for this assertion have degrees \(n\) and \(n-h\), both greater than \(2g-2=h\).

The successive restriction maps on \(H^1\) are therefore isomorphisms after degree \(N\). The theorem on formal functions, applied to the proper resolution over its Stein representative, now gives
\[
H^1(X,\mathcal F)\simeq H^1(C_g,\mathcal F_N),
\qquad \mathcal F=\mathcal O_X,S,L.                              \tag{7}
\]
Here powers of the exceptional ideal and powers of the pulled-back maximal ideal are cofinal. Also \(R^1f_*\mathcal F\) is supported at the singular point, so its completion is itself.

Thus (7) concerns the analytic cohomology in the question, not merely a formal substitute.

There is also an Euler-characteristic cancellation. From (6),
\[
\chi(S_N)=\chi(O_N)+\chi(L_N).                                   \tag{8}
\]
Explicitly,
\[
\chi(O_N)=\sum_{n=0}^N(n+1-g),\qquad
\chi(L_N)=\sum_{n=0}^N(n+3-3g).                                  \tag{9}
\]
It follows that
\[
\Delta_b=h^0(O_N)-h^0(S_N)+h^0(L_N).                             \tag{10}
\]

## 3. Derivation of the transition matrices

Put \(u=y_U\), \(w=y_W\), and
\[
H=1-k\phi t^k w^k.
\]
The inverse fiber change is
\[
u=twH^{-1/k}.                                                    \tag{11}
\]
On \(C_g\setminus\{p\}\), use the nowhere-zero vector field
\[
\delta=z\partial_x+\frac{2g+1}{2}x^{2g}\partial_z.
\]
Near \(p\),
\[
\delta=a\partial_t.
\]
Use logarithmic vertical frames
\(\eta_U=u\partial_u\) and \(\eta_W=w\partial_w\). Direct differentiation gives
\[
\begin{split}
\eta_U&=H\eta_W,\\
\delta_U&=
a\partial_t+
a\left(-t^{-1}-t^k\phi'w^k\right)\eta_W,\\
\delta_U\wedge\eta_U&=aH\,\partial_t\wedge\eta_W.                 \tag{12}
\end{split}
\]
Also,
\[
u^n=t^nw^nH^{-n/k}.
\]
Expanding the powers of \(H\), and retaining fiber degrees at most \(N\), gives exactly (2). In particular the off-diagonal term of \(T_S\), including the \(\phi'\)-term, is necessary.

## 4. Why the finite matrices compute all global sections

We give uniform bounds, so this argument never divides by any \(b_j\).

The pole orders of \(\phi,\psi,t^k\phi'\) are at most \(q,d,d+1\), respectively. Every entry of the matrices \(T_O,T_S,T_L\) consequently has valuation at least
\[
-P=-Jd-h-1.                                                      \tag{13}
\]

We also need a bound for their inverses. In \(u\)-coordinates put
\[
Q=1+k\phi u^k.
\]
The inverse versions of (11)–(12) are
\[
\begin{split}
w^n&=t^{-n}u^nQ^{-n/k},\\
\eta_W&=Q\eta_U,\\
\partial_t\big|_w
 &=a^{-1}\delta_U+
 \left[t^{-1}+\left(\phi'+\frac{k\phi}{t}\right)u^k\right]\eta_U.
                                                                    \tag{14}
\end{split}
\]
A coefficient involving \(\ell\) fiber-degree increments has valuation at least
\[
-n-\ell q-1.
\]
Since \(n+\ell k\leq N\),
\[
n+\ell q+1
=(n+\ell k)+\ell d+1\leq N+Jd+1=M.
\]
Thus every inverse-transition entry has valuation at least \(-M\).

Let a global section of one of \(O_N,S_N,L_N\) have coefficient vector \(v\) in the \(U\)-frame. Its \(W\)-coefficient vector is holomorphic. The inverse-transition bound shows that every component of \(v\) is meromorphic at \(p\), with pole order at most \(M\).

The meromorphic functions on \(C_g\) regular away from \(p\) form
\[
\mathbb C[x,z]/(z^2-x^{2g+1}+1).
\]
A basis for its subspace of pole order at most \(M\) is
\[
x^i\quad(2i\leq M),\qquad
zx^i\quad(2g+1+2i\leq M).
\]
Their expansions are precisely the \(f_\lambda\) used in (3).

Consequently every possible global section is obtained by choosing a linear combination of these functions in every \(U\)-component and requiring that its transformed coefficients have no negative powers of \(t\). By (13), no negative exponent below \(-P-M\) can occur. Those conditions are exactly the linear equations (3).

Let
\[
C=(N+1)|\Lambda_M|,
\qquad
\rho_O=\operatorname{rank}\mathcal B_O,\quad
\rho_S=\operatorname{rank}\mathcal B_S,\quad
\rho_L=\operatorname{rank}\mathcal B_L .
\]
We have proved
\[
h^0(O_N)=C-\rho_O,\quad
h^0(S_N)=2C-\rho_S,\quad
h^0(L_N)=C-\rho_L.                                               \tag{15}
\]
Substituting (15) into (10) proves (4).

This also gives the individual cohomology dimensions, if wanted:
\[
\begin{split}
h^1(O_X)&=C-\rho_O-\chi(O_N),\\
h^1(S)&=2C-\rho_S-\chi(O_N)-\chi(L_N),\\
h^1(L)&=C-\rho_L-\chi(L_N).
\end{split}                                                       \tag{16}
\]

## 5. Executable exact-arithmetic Python

The following uses Sage from Python. It constructs the coefficient matrices and computes their exact ranks—not floating-point approximations. Rational input uses \(\mathbb Q\); algebraic complex input can use `K=QQbar` or an appropriate number field.

The code also checks the symbolic transition inverses, checks stabilization at two additional thickening orders, and checks the independently known split case \(b=0\).

```python
from sage.all import QQ, matrix, binomial
from collections import defaultdict


def lp_mul(a, b):
    """Multiply Laurent polynomials represented by exponent dictionaries."""
    c = defaultdict(QQ)
    for i, x in a.items():
        for j, y in b.items():
            c[i + j] += x * y
    return {i: x for i, x in c.items() if x}


def build(g, b, N=None, K=QQ):
    r = (g + 2) // 3
    k = g - r
    assert g >= 2 and len(b) == r
    b = [K(x) for x in b]
    if N is None:
        N = 4*g - 4

    h, q = 2*g - 2, 2*g - 1
    d, J = q - k, N // k
    M = N + J*d + 1
    P = J*d + h + 1
    B, D = M + P, 4*g + 2

    nongaps = [
        j for j in range(M + 1)
        if j % 2 == 0 or j >= 2*g + 1
    ]
    nc = (N + 1) * len(nongaps)
    nr = (N + 1) * B

    # Entries of the O, S, L coefficient matrices.
    entries = [defaultdict(QQ) for _ in range(3)]

    psi = {k-q+2*j: x for j, x in enumerate(b) if x}
    deriv = {
        k-q+2*j-1: (-q+2*j)*x
        for j, x in enumerate(b) if x
    }  # t^k phi'

    pw = [{0: QQ(1)}]
    for ell in range(J):
        pw.append(lp_mul(pw[-1], psi))

    # More than enough terms of sqrt(1-t^D).
    sqrt_coeff = [
        (-1)**j * binomial(QQ(1)/2, j)
        for j in range((B+M+P+D)//D + 2)
    ]

    def add(which, rb, cb, m, n, poly, shift, fac, sp):
        """
        Add poly*t^shift*fac*s^sp to transition block (m,n).
        Then multiply by every f_lambda and extract negative powers.
        rb,cb select horizontal/vertical blocks for S.
        """
        for il, lam in enumerate(nongaps):
            beta = sp + lam % 2
            col = (cb*(N+1) + n)*len(nongaps) + il
            for e, v in poly.items():
                e0 = e + shift - lam
                if beta == 0:
                    terms = [(0, QQ(1))]
                elif beta == 2:
                    terms = [(0, QQ(1)), (1, QQ(-1))]
                else:
                    count = max(0, (-1-e0)//D + 1)
                    terms = enumerate(sqrt_coeff[:count])
                for j, c in terms:
                    e1 = e0 + D*j
                    if -B <= e1 < 0 and c:
                        row = (rb*(N+1) + m)*B + e1+B
                        entries[which][row, col] += fac*v*c

    for n in range(N + 1):
        for ell in range((N-n)//k + 1):
            m = n + ell*k
            co = binomial(-QQ(n)/k, ell) * (-k)**ell
            cl = binomial(1-QQ(n)/k, ell) * (-k)**ell

            add(0, 0, 0, m, n, pw[ell], n, co, 0)
            add(2, 0, 0, m, n, pw[ell], n-h, -cl/2, 1)

            add(1, 0, 0, m, n, pw[ell], n-h, -co/2, 1)
            add(1, 1, 1, m, n, pw[ell], n, cl, 0)
            add(1, 1, 0, m, n, pw[ell], n-h-1, co/2, 1)
            if ell:
                cp = (
                    binomial(-QQ(n)/k, ell-1) * (-k)**(ell-1)
                )
                add(
                    1, 1, 0, m, n,
                    lp_mul(deriv, pw[ell-1]), n-h, cp/2, 1
                )

    mats = []
    for i, ent in enumerate(entries):
        mult = 2 if i == 1 else 1
        mats.append(matrix(
            K, mult*nr, mult*nc,
            {ij: x for ij, x in ent.items() if x},
            sparse=True
        ))
    return mats, (N, M, P, len(nongaps))


def invariants(g, b, N=None, K=QQ):
    mats, pars = build(g, b, N, K)
    N, M, P, number_of_nongaps = pars
    ranks = [A.rank() for A in mats]

    chiO = sum(n + 1 - g for n in range(N+1))
    chiL = sum(n + 3 - 3*g for n in range(N+1))
    chis = [chiO, chiO + chiL, chiL]
    h0 = [A.ncols() - rho for A, rho in zip(mats, ranks)]
    h1 = [a-c for a, c in zip(h0, chis)]

    delta = ranks[1] - ranks[0] - ranks[2]
    assert delta == h1[0] - h1[1] + h1[2]
    return h1, delta


def check_inverses(k, N):
    """Symbolically verify (2) and (14), without substituting phi."""
    import sympy as sp
    t, F, Fp, a = sp.symbols("t F Fp a", nonzero=True)
    d = N + 1
    TO, UO = sp.zeros(d), sp.zeros(d)
    TL, UL = sp.zeros(d), sp.zeros(d)
    TS, US = sp.zeros(2*d), sp.zeros(2*d)

    for n in range(d):
        for ell in range((N-n)//k + 1):
            m = n + ell*k
            alpha = -sp.Rational(n, k)
            c = sp.binomial(alpha, ell)*(-k*t**k*F)**ell
            e = sp.binomial(1+alpha, ell)*(-k*t**k*F)**ell
            ci = sp.binomial(alpha, ell)*(k*F)**ell
            ei = sp.binomial(1+alpha, ell)*(k*F)**ell

            TO[m,n], UO[m,n] = t**n*c, t**(-n)*ci
            TL[m,n], UL[m,n] = a*t**n*e, t**(-n)*ei/a

            TS[m,n] = a*TO[m,n]
            TS[d+m,d+n] = t**n*e
            TS[d+m,n] = -a*t**(n-1)*c
            US[m,n] = UO[m,n]/a
            US[d+m,d+n] = t**(-n)*ei
            US[d+m,n] = t**(-n-1)*ci

            if ell:
                cp = (
                    sp.binomial(alpha, ell-1)
                    * (-k*t**k*F)**(ell-1)
                )
                cip = (
                    sp.binomial(alpha, ell-1)*(k*F)**(ell-1)
                )
                TS[d+m,n] -= a*t**(n+k)*Fp*cp
                US[d+m,n] += (
                    t**(-n)*(Fp+k*F/t)*cip
                )

    for T, U in [(TO,UO), (TS,US), (TL,UL)]:
        error = T*U - sp.eye(T.rows)
        assert all(sp.expand(v) == 0 for v in error)


def checks():
    for k, N in [(1,4), (2,8), (2,12), (3,16)]:
        check_inverses(k, N)

    # Independent split-case formulas.
    for g in range(2, 7):
        h1, delta = invariants(g, [0]*((g+2)//3))
        assert h1 == [
            g*g,
            6*g*g - 7*g + 2,
            5*g*g - 7*g + 3
        ]
        assert delta == 1

    expected = [
        (2, [1],       [3,10,7],     0),
        (3, [1],       [7,31,24],    0),
        (4, [1,0],     [12,62,50],   0),
        (4, [0,1],     [11,61,49],  -1),
        (4, [1,1],     [11,61,49],  -1),
        (7, [1,2,1],   [35,221,184], -2),
    ]
    for g, b, hh, dd in expected:
        value = invariants(g, b)
        assert value == (hh, dd)
        # Extra infinitesimal orders must not change the answer.
        for inc in [1, 2]:
            assert invariants(g, b, 4*g-4+inc) == value

    return True


if __name__ == "__main__":
    assert checks()
```

I ran these exact-arithmetic checks successfully. I also ran the algebraic-complex specialization
\[
g=4,\qquad b=(\sqrt2,i)
\]
over `QQbar`; it gives
\[
(h^1(O_X),h^1(S),h^1(L))=(11,61,49),\qquad \Delta_b=-1.
\]

For the split-case check used in the program, the independent formulas follow directly from (6): \(h^1(O_X)=g^2\), \(h^1(L)=5g^2-7g+3\), and the Atiyah extension has its sole nonzero connecting-map rank at degree \(n=h\), giving \(h^1(S)=6g^2-7g+2\).

**What is proved:** formulas (1)–(5) give the exact value of \(\Delta_b\) for every allowed \(g\) and every complex nonzero coefficient vector \(b\), with arbitrary vanishing components. The proof also gives the three individual dimensions through (16). No genericity cases or coefficient specializations remain unresolved.