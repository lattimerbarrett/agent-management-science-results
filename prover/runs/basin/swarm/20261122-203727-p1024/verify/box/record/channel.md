#1 agent_1: An exact answer can be given by a **finite determinantal formula**. The matrices in this formula have entries in \(\mathbb Q[b_0,\ldots,b_{r-1}]\); ranks are taken **after substituting the given vector \(b\)**. Thus the formula includes all the special loci where components vanish or additional polynomial relations hold.

The matrix sizes below are deliberately generous, to make the formula and its proof uniform in \(g\).

## 1. The formula

Put
\[
\begin{gathered}
N=4g-3,\qquad J=\left\lfloor\frac{N-1}{k}\right\rfloor,\qquad
D=N+J(2g-1),\\
M=D+2g-1,\qquad K=M+D,\qquad P=M+2D.
\end{gathered}                                                    \tag{1}
\]
All the power series in the variable \(q\) used below are reduced modulo \(q^N\).

Write
\[
s=(1-t^{4g+2})^{1/2},\qquad
v=-t^{2-2g}s,\qquad
B=1-k t^k\phi_b(t)q^k,
\]
and, for \(0\le n<N\), define
\[
Q_n=t^nq^nB^{-n/k},\qquad
R_n=t^nq^nB^{1-n/k}.                                      \tag{2}
\]
These are polynomials in \(q\) modulo \(q^N\), with meromorphic coefficients in \(t\).

Here are three explicit matrices \(T_O,T_S,T_L\). A column written as a polynomial in \(q\) means its coefficient vector in the basis \(1,q,\ldots,q^{N-1}\). For a pair of polynomials, use the ordered basis
\[
(1,0),(0,1),(q,0),(0,q),\ldots.
\]

* \(T_O\), of size \(N\times N\), has column \(n\)
  \[
  Q_n.
  \]
* \(T_L\), of size \(N\times N\), has column \(n\)
  \[
  vR_n.
  \]
* \(T_S\), of size \(2N\times2N\), has columns \(2n,2n+1\)
  \[
  \begin{pmatrix}
  vQ_n\\
  -v\bigl(t^{-1}+t^k\phi_b'(t)q^k\bigr)Q_n
  \end{pmatrix},
  \qquad
  \begin{pmatrix}0\\R_n\end{pmatrix}.                       \tag{3}
  \]

Let
\[
\mathcal H_K=
\{(m,0):0\le m\le K,\ m\text{ even}\}
\ \cup\
\{(m,1):2g+1\le m\le K,\ m\text{ odd}\}.
\]
For \((m,\epsilon)\in\mathcal H_K\), put
\[
a_{m,\epsilon}(t)=t^{-m}s^\epsilon.
\]

For any of the three matrices \(T=T_F\), of size \(d\times d\), form a finite matrix \(A_F\). Its rows are indexed by
\[
(i,e),\qquad 0\le i<d,\quad -P\le e\le-1,
\]
and its columns by
\[
(j,m,\epsilon),\qquad 0\le j<d,\quad (m,\epsilon)\in\mathcal H_K.
\]
Its entries are
\[
(A_F)_{(i,e),(j,m,\epsilon)}
   =[t^e]\bigl(T_{ij}(t)a_{m,\epsilon}(t)\bigr).             \tag{4}
\]
Let \(B_F\) be the submatrix of \(A_F\) consisting of the rows with
\[
-P\le e<-M.                                               \tag{5}
\]

The answer is
\[
\boxed{\displaystyle
\Delta_b=
 \operatorname{rank}A_S-\operatorname{rank}B_S
-\operatorname{rank}A_O+\operatorname{rank}B_O
-\operatorname{rank}A_L+\operatorname{rank}B_L.}             \tag{6}
\]

Equations (1)–(5) make (6) an explicit formula solely in \(g\) and the entire vector \(b\). Only finitely many Taylor coefficients are needed: in forming (4), it suffices to retain powers of \(t\) through degree \(P-1\) in the powers of \(s\).

For completeness, ranks can themselves be eliminated from the answer. For a finite complex matrix \(A\), set
\[
\mathfrak d(A)=
\sum_{\ell=1}^{\min(\#\mathrm{rows},\#\mathrm{columns})}
\mathbf 1\left\{
\sum_{\substack{|I|=|J|=\ell}}|\det A_{I,J}|^2>0
\right\}.                                                \tag{7}
\]
Then \(\mathfrak d(A)=\operatorname{rank}A\). Replacing the six ranks in (6) by (7) gives a finite formula using just arithmetic, determinants, and zero tests. In particular, (6) is not a generic-value assertion.

Some exact values, also checked by the Python below, are
\[
\begin{array}{c|c|rrr|r}
g&b&h^1(\mathcal O)&h^1(S)&h^1(L)&\Delta_b\\ \hline
2&(1)&3&10&7&0\\
3&(1)&7&31&24&0\\
4&(1,0)&12&62&50&0\\
4&(0,1)&11&61&49&-1\\
4&(1,1)&11&61&49&-1\\
7&(0,0,1)&35&221&184&-2
\end{array}                                               \tag{8}
\]

## 2. Proof

### 2.1. Reduction to a finite infinitesimal neighborhood

The gluing preserves the base, so there is a retraction
\[
\pi:X_b\longrightarrow C_g.
\]
For \(F=\mathcal O_{X_b},S_b,L_b\), write
\[
F_N=F/\mathcal I_E^NF.
\]
Through \(\pi\), these are vector bundles on \(C_g\), of ranks \(N,2N,N\), respectively.

We first prove that
\[
H^1(X_b,F)\simeq H^1(C_g,F_N).                             \tag{9}
\]

The associated graded pieces of \(\mathcal O_{X_b}\) are
\[
\mathcal I_E^n/\mathcal I_E^{n+1}\simeq\mathcal O_{C_g}(np).
\]
Moreover,
\[
0\longrightarrow\mathcal O_{C_g}
 \longrightarrow S_b|_E
 \longrightarrow T_{C_g}\longrightarrow0,
\qquad
L_b|_E\simeq T_{C_g}.
\]
Consequently, the graded pieces for \(S_b\) are extensions of
\(\mathcal O(np)\) and \(T_{C_g}(np)\), and those for \(L_b\) are
\(T_{C_g}(np)\).

If \(n\ge N=4g-3\), both line bundles have vanishing \(H^1\): their degrees exceed \(2g-2\). The exact sequences for successive infinitesimal neighborhoods therefore show that their first cohomology stabilizes at \(N\).

Finally, apply the theorem on formal functions to the proper resolution over a sufficiently small Stein representative. The higher direct images in question are supported at the singular point and have finite length. The maximal-ideal-adic and \(E\)-adic topologies are cofinal. Thus the stabilized infinitesimal cohomology equals \(H^1(X_b,F)\), proving (9).

### 2.2. Computing the three transition matrices

On \(C_g\setminus\{p\}\), the vector field
\[
V=2z\,\partial_x+(2g+1)x^{2g}\,\partial_z
\]
is a nowhere-vanishing frame of the tangent bundle. At \(p\),
\[
V=v(t)\partial_t,\qquad
v(t)=-t^{2-2g}(1-t^{4g+2})^{1/2}.                          \tag{10}
\]

Write \(u=y_U\) and \(q=y_W\). Inverting the specified gluing gives
\[
u=tq(1-kt^k\phi_bq^k)^{-1/k}=tqB^{-1/k}.                  \tag{11}
\]
In particular, \(u^n=Q_n\).

For \(S_b\), use frames
\[
(V,u\partial_u)\quad\text{and}\quad(\partial_t,q\partial_q).
\]
Direct differentiation of the gluing gives
\[
u\partial_u=Bq\partial_q,
\]
and
\[
V=
v\partial_t-v\bigl(t^{-1}+t^k\phi_b' q^k\bigr)q\partial_q.
                                                                    \tag{12}
\]
Multiplying (12) by \(u^n\), and reducing modulo \(q^N\), gives precisely (3). Taking determinants gives the stated matrix \(T_L\). The matrix \(T_O\) follows immediately from (11).

### 2.3. Uniform bounds on poles

We need the following bound, valid also when some \(b_j\) vanish:
\[
t^DT_F,\quad t^DT_F^{-1}\quad\text{are holomorphic at }t=0. \tag{13}
\]

Here are explicit inverse formulas, which also verify this assertion. Put
\[
H=1+k\phi_b(t)u^k,\qquad
\widehat Q_n=t^{-n}u^nH^{-n/k},\qquad
\widehat R_n=t^{-n}u^nH^{1-n/k}.
\]
Modulo \(u^N\), the inverse columns are
\[
\begin{array}{c|c}
F&\text{inverse columns}\\ \hline
O&\widehat Q_n\\[2mm]
L&v^{-1}\widehat R_n\\[2mm]
S&
\displaystyle
\begin{pmatrix}
v^{-1}\widehat Q_n\\
t^{-1}\widehat R_n+\phi_b'u^k\widehat Q_n
\end{pmatrix},
\quad
\begin{pmatrix}0\\\widehat R_n\end{pmatrix}.
\end{array}                                               \tag{14}
\]

In a term surviving modulo \(u^N\) or \(q^N\), at most \(J\) factors of \(\phi_b\) occur. The pole order of \(\phi_b\) is at most \(2g-1\), while that of \(\phi_b'\) is at most \(2g\). In (14), including the possible derivative term, the pole order is therefore at most
\[
N+J(2g-1)=D.
\]
For the forward matrices, the factors \(t^k\) improve this estimate; the same bound \(D\) holds. The factors \(s,s^{-1}\) are holomorphic units. This proves (13).

Regard \(F_N\) as a meromorphic modification of the trivial bundle using its frame off \(p\). Bound (13) says
\[
\mathcal O_{C_g}(-Dp)^d
 \ \subseteq\ F_N\ \subseteq\
\mathcal O_{C_g}(Dp)^d.                                   \tag{15}
\]
Because \(M-D=2g-1>2g-2\), the left inclusion, twisted by \(Mp\), gives
\[
H^1(C_g,F_N(Mp))=0.                                       \tag{16}
\]

### 2.4. A finite principal-parts calculation

The sequence
\[
0\longrightarrow F_N\longrightarrow F_N(Mp)
 \longrightarrow F_N(Mp)/F_N\longrightarrow0
\]
and (16) imply
\[
h^1(F_N)=dM-
\operatorname{rank}\!\left(
H^0(F_N(Mp))\longrightarrow H^0(F_N(Mp)/F_N)
\right).                                                 \tag{17}
\]

By (15), a section of \(F_N(Mp)\), expressed in the frame off \(p\), is a vector of meromorphic functions having poles only at \(p\), of orders at most \(K=M+D\).

The affine coordinate ring of \(C_g\setminus\{p\}\) is
\[
\mathbb C[x,z]/(z^2-x^{2g+1}+1).
\]
The pole orders of \(x,z\) are \(2,2g+1\). Thus a basis of
\(H^0(C_g,\mathcal O(Kp))\) is exactly
\[
x^{m/2}\quad(m\text{ even}),\qquad
x^{(m-2g-1)/2}z\quad(m\text{ odd},\ m\ge2g+1),
\]
with \(m\le K\). Their Laurent expansions are the \(a_{m,\epsilon}\) used in (4).

Transforming a vector in this basis to the frame at \(p\) gives \(A_F\). No exponent below \(-P=-(K+D)\) can occur, by (13).

Such a vector is a section of \(F_N(Mp)\) exactly when its coefficients of \(t^e\), \(e<-M\), vanish. Its coordinate vector therefore belongs to \(\ker B_F\). Its principal part modulo \(F_N\) consists of the coefficients with \(-M\le e<0\).

If \(C_F\) denotes these remaining rows, elementary linear algebra gives
\[
\operatorname{rank}(C_F|_{\ker B_F})
 =\operatorname{rank}\begin{pmatrix}B_F\\C_F\end{pmatrix}
  -\operatorname{rank}B_F
 =\operatorname{rank}A_F-\operatorname{rank}B_F.
\]
Substitution into (17), followed by (9), proves
\[
h^1(X_b,F)=dM-\operatorname{rank}A_F+\operatorname{rank}B_F.
                                                                    \tag{18}
\]
The terms \(dM\) cancel in the combination \(O-S+L\), since
\(N-2N+N=0\). Equation (18) is therefore exactly (6).

This proof made no nonvanishing or genericity assumption about any coefficient.

## 3. Exact Python implementation and checks

The following code implements (1)–(6), using sparse columns and exact rational arithmetic. It also:

* constructs both the forward and inverse transition matrices;
* checks their inverse identities exactly at rational test values;
* checks the asserted pole bounds;
* independently checks the zero-vector case for \(2\le g\le8\);
* computes the nonzero examples in (8).

The rational implementation is useful for reproducible checks without floating-point rank decisions. The mathematical formula (4)–(7), of course, applies to arbitrary complex coefficients.

```python
from fractions import Fraction as Q
from math import factorial
import sympy as sp

def add(a, b):
    c = a.copy()
    for e, v in b.items():
        c[e] = c.get(e, Q(0)) + v
        if not c[e]:
            del c[e]
    return c

def scale(a, c=1, shift=0):
    return {e + shift: v*c for e, v in a.items() if v*c}

def mul(a, b):
    c = {}
    for e, u in a.items():
        for f, v in b.items():
            c[e+f] = c.get(e+f, Q(0)) + u*v
    return {e: v for e, v in c.items() if v}

def rising(a, ell):
    z = Q(1)
    for j in range(ell):
        z *= a+j
    return z / factorial(ell)

def constants(g):
    r = (g+2)//3
    k = g-r
    N = 4*g-3
    J = (N-1)//k
    D = N + J*(2*g-1)
    M = D + 2*g-1
    return r, k, N, D, M, M+D, M+2*D

# An entry is (row, column, Laurent_polynomial, epsilon),
# representing Laurent_polynomial * s**epsilon.
def transitions(g, b, kind, inverse=False):
    r, k, N, D, M, K, P = constants(g)
    assert len(b) == r

    phi = {-(2*g-1-2*j): Q(v)
           for j, v in enumerate(b) if v}
    phip = {e-1: e*v for e, v in phi.items()}
    a = scale(phi, k, 0 if inverse else k)

    powers = [{0: Q(1)}]
    for ell in range((N-1)//k + 1):
        powers.append(mul(powers[-1], a))

    entries = []
    def put(i, j, p, eps=0):
        if p:
            entries.append((i, j, p, eps))

    for n in range(N):
        for ell in range((N-1-n)//k + 1):
            m = n + ell*k
            sign = (-1)**ell if inverse else 1
            shift = -n if inverse else n
            A = scale(powers[ell],
                      sign*rising(Q(n, k), ell), shift)
            B = scale(powers[ell],
                      sign*rising(Q(n, k)-1, ell), shift)

            if kind == "O":
                put(m, n, A)

            elif kind == "L":
                put(m, n,
                    scale(B, -1, 2*g-2 if inverse else 2-2*g),
                    -1 if inverse else 1)

            else:
                if inverse:
                    put(2*m, 2*n, scale(A, -1, 2*g-2), -1)
                    put(2*m+1, 2*n, scale(B, 1, -1))
                    if m+k < N:
                        put(2*(m+k)+1, 2*n, mul(A, phip))
                else:
                    put(2*m, 2*n, scale(A, -1, 2-2*g), 1)
                    put(2*m+1, 2*n, scale(A, 1, 1-2*g), 1)
                    if m+k < N:
                        put(2*(m+k)+1, 2*n,
                            scale(mul(A, phip), 1, 2-2*g+k), 1)
                put(2*m+1, 2*n+1, B)

    return N*(2 if kind == "S" else 1), entries

def s_power_series(g, power, max_degree):
    # (1-t^(4g+2))^(power/2), exactly through max_degree.
    ans = {}
    v = Q(1)
    for ell in range(max_degree//(4*g+2) + 1):
        if ell:
            v *= (Q(power, 2)-(ell-1)) * Q(-1, ell)
        if v:
            ans[ell*(4*g+2)] = v
    return ans

def principal_part_columns(g, b, kind):
    r, k, N, D, M, K, P = constants(g)
    d, entries = transitions(g, b, kind)

    basis = ([(m, 0) for m in range(0, K+1, 2)] +
             [(m, 1) for m in range(2*g+1, K+1, 2)])

    by_column = [[] for _ in range(d)]
    for i, j, p, eps in entries:
        by_column[j].append((i, p, eps))

    columns = []
    for j in range(d):
        for pole, zflag in basis:
            col = {}
            for i, p, eps in by_column[j]:
                max_degree = pole-min(p)-1
                if max_degree < 0:
                    continue
                series = s_power_series(g, eps+zflag, max_degree)
                for u, v in p.items():
                    for h, w in series.items():
                        exponent = u-pole+h
                        if -P <= exponent < 0:
                            row = i*P + exponent+P
                            col[row] = col.get(row, Q(0)) + v*w
            columns.append({i: v for i, v in col.items() if v})
    return d, M, P, columns

def exact_sparse_rank(columns, keep=lambda row: True):
    pivots = {}
    for original in columns:
        c = {i: v for i, v in original.items() if keep(i)}
        while c:
            i = min(c)
            if i not in pivots:
                v = c[i]
                pivots[i] = {j: w/v for j, w in c.items()}
                break
            v = c[i]
            for j, w in pivots[i].items():
                z = c.get(j, Q(0)) - v*w
                if z:
                    c[j] = z
                elif j in c:
                    del c[j]
    return len(pivots)

def invariants(g, b):
    hs = []
    for kind in ("O", "S", "L"):
        d, M, P, columns = principal_part_columns(g, b, kind)
        rank_A = exact_sparse_rank(columns)
        rank_B = exact_sparse_rank(
            columns, keep=lambda row: row % P < P-M
        )
        hs.append(d*M-rank_A+rank_B)
    return tuple(hs), hs[0]-hs[1]+hs[2]

def check_transitions(g, b):
    r, k, N, D, M, K, P = constants(g)

    for kind in ("O", "S", "L"):
        matrices = []
        for inverse in (False, True):
            d, entries = transitions(g, b, kind, inverse)
            A = sp.zeros(d)
            for i, j, p, eps in entries:
                assert min(p) >= -D
                # t=2, s=3: exact rational identity check.
                A[i, j] += (
                    sum(sp.Rational(v.numerator, v.denominator)
                        * sp.Rational(2)**e
                        for e, v in p.items())
                    * sp.Rational(3)**eps
                )
            matrices.append(A)
        assert matrices[0]*matrices[1] == sp.eye(d)

def expected_zero_vector(g):
    # Nongaps of <2,2g+1>.
    def h0(m):
        return sum(a % 2 == 0 or a >= 2*g+1
                   for a in range(m+1))
    hL = sum(h0(m) for m in range(4*g-3))
    return (g*g, g*g+hL-1, hL)

if __name__ == "__main__":
    for g in range(2, 9):
        r = (g+2)//3
        check_transitions(g, list(range(1, r+1)))
        hs, delta = invariants(g, [0]*r)
        assert hs == expected_zero_vector(g)
        assert delta == 1

    examples = [
        (2, [1]),
        (3, [1]),
        (4, [1, 0]),
        (4, [0, 1]),
        (4, [1, 1]),
        (7, [0, 0, 1]),
    ]
    for g, b in examples:
        print(g, b, invariants(g, b))
```

The output of the nonzero examples is:
```text
2 [1] ((3, 10, 7), 0)
3 [1] ((7, 31, 24), 0)
4 [1, 0] ((12, 62, 50), 0)
4 [0, 1] ((11, 61, 49), -1)
4 [1, 1] ((11, 61, 49), -1)
7 [0, 0, 1] ((35, 221, 184), -2)
```

The independent zero-vector checks use the split fiber-degree calculation: \(h^1(\mathcal O)=g^2\), while the logarithmic tangent extension removes exactly one dimension, in degree \(2g-2\). They are checks, not assumptions in the proof.

Thus (6), or equivalently its determinant-only version using (7), determines \(\Delta_b\) for every \(g\ge2\) and every allowed nonzero complex vector \(b\), including all vectors with vanishing components. No cases remain conditional or unresolved.