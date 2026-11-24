# agent_1: last reply

Put
\[
m=\max\{j:b_j\ne0\}.
\]
Then the answer is
\[
\boxed{\Delta_b=-m.}
\]
Thus the answer depends on the last nonzero component, not on the first nonzero component. In particular, it can be negative.

We prove this for every complex coefficient vector in the question. We also give an exact-arithmetic program which computes the cohomology directly from the full transition functions, independently of the final formula.

## 1. Some notation and the individual cohomology dimensions

Write
\[
d=2g-2,\qquad N=d-k=g+r-2,
\]
and set
\[
R=(m+1)(g+r-1-2m)-1.
\]
In fact, we will prove the stronger formulas
\[
\begin{aligned}
h^1(X_b,\mathcal O_{X_b})&=g^2-R,\\
h^1(X_b,S_b)&=6g^2-7g+2-2R+m,\\
h^1(X_b,L_b)&=5g^2-7g+2-R.
\end{aligned}                                                    \tag{1}
\]
Their alternating sum is \(-m\).

Hereafter all sheaves on a sufficiently small neighborhood of \(E\) can equivalently be considered on its formal completion. We justify the finite truncation used below.

## 2. Reduction to a finite cohomology calculation

Let \(\pi:X_b\to C_g\) be the projection preserved by the gluing. Along \(E\),
\[
\mathcal I_E^n/\mathcal I_E^{n+1}\simeq\mathcal O_{C_g}(np).
\]
There is an exact sequence
\[
0\longrightarrow\mathcal O_{C_g}
\longrightarrow S_b|_E
\longrightarrow\Theta_{C_g}
\longrightarrow0,
\]
and \(L_b|_E\simeq\Theta_{C_g}\).

The differential \(dx/z\) has divisor \(dp\). Consequently,
\[
\Theta_{C_g}\simeq\mathcal O_{C_g}(-dp).
\]
It follows that, for each of \(\mathcal O_{X_b},S_b,L_b\),
\[
H^1\!\left(E,\mathcal I_E^n\mathcal F/
                      \mathcal I_E^{n+1}\mathcal F\right)=0
\quad(n>2d).
\]
Indeed, this follows from Serre duality for the two line bundles
\(\mathcal O(np)\) and \(\mathcal O((n-d)p)\).

Thus the cohomology of the successive infinitesimal neighborhoods stabilizes at
\[
M=2d+1=4g-3.
\]
The theorem on formal functions, applied to the proper resolution over the Stein representative, gives
\[
H^1(X_b,\mathcal F)
 \simeq H^1\!\left(E,\mathcal F/\mathcal I_E^M\mathcal F\right).       \tag{2}
\]
Here the higher direct image is supported at the contracted point, so its completion is the same finite-dimensional vector space. This proves that the calculation below is finite and computes the analytic cohomology specified in the question.

## 3. Scalar Čech reduction on \(C_g\)

Set
\[
h(t)=(1-t^{4g+2})^{1/2},\qquad
A=\mathbb C[x,z]/(z^2-x^{2g+1}+1).
\]
The functions regular away from \(p\) have the basis
\[
x^a=t^{-2a},\qquad
zx^a=t^{-(2g+1+2a)}h(t).
\]
Thus the gap sequence at \(p\) is
\[
1,3,\ldots,2g-1.                                                   \tag{3}
\]

For the line bundle \(\mathcal O(\lambda p)\), a convenient basis for its first cohomology is
\[
\left\{t^{-(2i-1)}:1\le i\le g,\ 2i-1>\lambda\right\}
\ \cup\
\left\{t,t^2,\ldots,t^{-\lambda-1}\right\},                          \tag{4}
\]
where the second set is empty when \(\lambda\ge-1\).

Explicitly, any Laurent series can be reduced modulo
\[
A+t^{-\lambda}\mathbb C[[t]]
\]
to the span in (4): eliminate nongap poles using the displayed basis of \(A\), and then remove the part in \(t^{-\lambda}\mathbb C[[t]]\). This reduction can be chosen to preserve parity under \(t\mapsto-t\).

We use the following elementary consequence of this reduction. Suppose a vector bundle has a triangular transition matrix whose diagonal entries are \(t^{-\lambda_i}\). Eliminating the scalar Čech coboundaries gives a finite complex
\[
\bigoplus_i H^0\bigl(\mathcal O(\lambda_i p)\bigr)
 \xrightarrow{D}
\bigoplus_i H^1\bigl(\mathcal O(\lambda_i p)\bigr),                   \tag{5}
\]
and
\[
h^1=\sum_i h^1\bigl(\mathcal O(\lambda_i p)\bigr)-\operatorname{rank}D.
                                                                    \tag{6}
\]
This is ordinary block Gaussian elimination of the Čech differential. To construct a column of \(D\), begin with a diagonal global section, apply the off-diagonal transition terms, and repeatedly perform the scalar reduction above in increasing triangular order. This also describes the algorithm used in the code below.

## 4. The actual transition matrices

Abbreviate \(u=y_U\), \(v=y_W\), \(\phi=\phi_b\), and put
\[
P=1+k\phi u^k.
\]
Then
\[
v=t^{-1}uP^{-1/k}.
\]

On the \(U\)-chart let
\[
\epsilon_U=u\partial_u,\qquad
\delta_U(x)=z,\quad
\delta_U(z)=\frac{2g+1}{2}x^{2g},
\]
with \(\delta_U(u)=0\). On the \(W\)-chart let
\[
\epsilon_W=v\partial_v,\qquad
\eta_W=-\frac{h(t)}2\partial_t,
\]
where \(\partial_t\) holds \(v\) fixed. Since
\[
\delta_U(t)=-\frac12t^{-d}h(t),
\]
direct differentiation gives
\[
\begin{aligned}
\epsilon_W&=P\epsilon_U,\\
\eta_W&=t^d\delta_U
-\frac h2\left(\frac1t+
       \left(\frac{k\phi}{t}+\phi'\right)u^k\right)\epsilon_U,\\
\eta_W\wedge\epsilon_W&=t^dP\,\delta_U\wedge\epsilon_U.
\end{aligned}                                                       \tag{7}
\]

Let \(\mathcal T\) denote the vertical logarithmic tangent line bundle, and let
\(\mathcal Q=\pi^*\Theta_{C_g}\). There is an exact sequence
\[
0\longrightarrow\mathcal T\longrightarrow S_b
 \longrightarrow\mathcal Q\longrightarrow0.                        \tag{8}
\]

For each of the four line bundles
\(\mathcal O,\mathcal T,\mathcal Q,L_b\), its transition on the fiber-degree-\(n\) basis vector has the scalar form
\[
u^n t^{e-n}P^{\,c-n/k},                                             \tag{9}
\]
with the following values:
\[
\begin{array}{c|cc}
 &e&c\\ \hline
\mathcal O&0&0\\
\mathcal T&0&1\\
\mathcal Q&d&0\\
L_b&d&1.
\end{array}                                                        \tag{10}
\]
The diagonal summand in degree \(n\) is therefore
\(\mathcal O((n-e)p)\).

## 5. Why only the first nonlinear block affects the rank

Consider one of the scalar transitions (9). Put \(s=n-e\). A diagonal global section relevant to a nonlinear obstruction has
\[
0\le s\le N=d-k.
\]
Its basis consists only of \(1,x,\ldots,x^{\lfloor s/2\rfloor}\), since \(s<2g+1\).

The first nonlinear obstruction, from degree \(n\) to \(n+k\), is
\[
(kc-n)\,[\phi f]\in H^1\bigl(\mathcal O((s+k)p)\bigr).               \tag{11}
\]
All later terms increase fiber degree by multiples of \(k\).

We claim that the rank in (5) is the sum of the ranks of the first blocks (11). Here are the details that rule out hidden higher obstructions.

* Each multiplication by \(\phi\) reverses \(t\)-parity.
* The scalar reductions preserve parity.
* All obstruction targets reached from a global section have
  \(\lambda=s+ak>0\); their \(H^1\)-bases consist only of odd negative powers.
* Hence every second-order block is zero.
* From the definition of \(r\),
  \[
  d\le3k.
  \]
  Thus an odd block of order at least three can occur only when
  \(d=3k\), at order three, and from \(s=0\).

The last possible block cannot increase the rank. Its source is one-dimensional. For \(\mathcal O\) that source is the global constant and its entire column is zero. In the other three cases its first block is nonzero, and no other source contributes to that first target degree. It is already an isolated pivot column; any third-order entry in that column can be removed without changing the rank.

This proves the claim, including the borderline case \(d=3k\).

## 6. The first blocks are truncated Hankel matrices

For \(0\le s\le N\), let \(a_s\) be the rank of
\[
H^0(\mathcal O(sp))
 \xrightarrow{\ f\mapsto[\phi f]\ }
H^1(\mathcal O((s+k)p)).
\]
The source has dimension \(\lfloor s/2\rfloor+1\), and the target has dimension
\(\lfloor(N-s)/2\rfloor+1\). In the bases above, its matrix is
\[
(b_{i+\ell})_{\substack{0\le i<\lfloor(N-s)/2\rfloor+1\\
                       0\le\ell<\lfloor s/2\rfloor+1}},             \tag{12}
\]
with \(b_j=0\) for \(j>m\).

There are no additional contributions to (12) from eliminating nongap poles: the poles of \(\phi x^\ell\) have order less than \(4g+2\), so the \(h(t)-1\) correction produces only positive powers, which vanish in these targets.

We have
\[
N\ge4(r-1)\ge4m.
\]
Consequently at least one dimension of the rectangle (12) is at least \(m+1\). The last nonzero antidiagonal is \(b_m\). The appropriate square minor of size
\[
q=\min\left(\left\lfloor\frac s2\right\rfloor+1,\
             \left\lfloor\frac{N-s}2\right\rfloor+1,\
             m+1\right)
\]
has determinant
\[
(-1)^{q(q-1)/2}b_m^q\ne0.
\]
All larger minors vanish. Hence, uniformly for every allowed vector,
\[
a_s=
\min\left(\left\lfloor\frac s2\right\rfloor+1,\
          \left\lfloor\frac{N-s}2\right\rfloor+1,\
          m+1\right).                                             \tag{13}
\]
In particular,
\[
a_0=1,\qquad a_k=m+1.                                              \tag{14}
\]

Define \(R=\sum_{s=1}^N a_s\). Summing the two symmetric tails of (13) gives
\[
R=(m+1)(N+1-2m)-1
 =(m+1)(g+r-1-2m)-1,                                               \tag{15}
\]
as asserted earlier.

The coefficients \(kc-n\) in (11) now give the ranks of the reduced differentials:
\[
\begin{array}{c|c}
\text{line bundle}&\operatorname{rank}D\\ \hline
\mathcal O&R\\
\mathcal T&R+1-a_k=R-m\\
\mathcal Q&R+1\\
L_b&R+1.
\end{array}                                                        \tag{16}
\]
Indeed, \(\mathcal O\) omits \(s=0\), \(\mathcal T\) omits \(s=k\), and neither \(\mathcal Q\) nor \(L_b\) has a zero coefficient.

## 7. The extension defining \(S_b\)

One must still check that simply adding the two line-bundle ranks in (16) correctly handles (8).

After the same scalar Čech reductions, the differential for \(S_b\), with horizontal and vertical parts separated, has the form
\[
D_S=
\begin{pmatrix}
D_{\mathcal Q}&0\\
C&D_{\mathcal T}
\end{pmatrix}.                                                     \tag{17}
\]
A horizontal diagonal global section can start only in degree \(n\ge d\). The cross term in (7) never decreases fiber degree. Meanwhile vertical \(H^1\) vanishes in degrees greater than \(d\). Thus \(C\) is supported only on the single horizontal source in degree \(d\), and the single vertical target in degree \(d\).

The first horizontal obstruction from that source is
\[
-d[\phi]\in H^1(\mathcal O(kp)),
\]
which is nonzero: every term of \(\phi\) is a gap pole of order greater than \(k\). No other horizontal source contributes to this first target degree. Therefore every vector in \(\ker D_{\mathcal Q}\) has zero coefficient at that source, so
\[
C(\ker D_{\mathcal Q})=0.
\]
Linear algebra applied to (17) now yields
\[
\operatorname{rank}D_S
 =\operatorname{rank}D_{\mathcal Q}
  +\operatorname{rank}D_{\mathcal T}
 =2R+1-m.                                                        \tag{18}
\]

This argument is the point where it is important not to assume that the logarithmic tangent sequence splits.

## 8. Finishing the cohomology calculation

From the gap sequence,
\[
\sum_{n\ge0}h^1(\mathcal O(np))=1+3+\cdots+(2g-1)=g^2.
\]
Also,
\[
\begin{aligned}
\sum_{n\ge0}h^1(\Theta_{C_g}(np))
 &=\sum_{\lambda=-d}^{d}h^1(\mathcal O(\lambda p))\\
 &=g^2+\sum_{j=1}^d(g-1+j)\\
 &=5g^2-7g+3.
\end{aligned}
\]
Equations (6), (16), and (18) give exactly (1). Therefore
\[
\Delta_b
=(g^2-R)
 -(6g^2-7g+2-2R+m)
 +(5g^2-7g+2-R)
=-m.
\]

## 9. Exact computational verification

The following program uses rational arithmetic throughout. In particular, it does **not** substitute the final answer into a purported cohomology computation.

It constructs the full transition matrices modulo \(u^{4g-3}\), including every nonlinear term and the exact square root. Laurent expressions are represented as
\[
P(t)+Q(t)h(t),\qquad h(t)^2=1-t^{4g+2},
\]
so no numerical or power-series approximation is involved. It then performs the Čech elimination described in Section 3 and computes the resulting matrix ranks.

The checks include symbolic pivot determinants, the rank sums, regularity after every Čech reduction, and independent full-transition computations for vectors with zero, negative, and rational components.

```python
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
import sympy as sp

# Pairs (P,Q) represent P(t)+Q(t)*h(t), h^2=1-t^H.
def pa(a, b, c=1):
    z = a.copy()
    for i, v in b.items():
        z[i] = z.get(i, 0) + c*v
        if not z[i]:
            del z[i]
    return z

def pm(a, b):
    z = {}
    for i, v in a.items():
        for j, w in b.items():
            z[i+j] = z.get(i+j, 0) + v*w
    return {i: v for i, v in z.items() if v}

def add(a, b, c=1):
    return pa(a[0], b[0], c), pa(a[1], b[1], c)

def sc(a, c):
    return tuple({i: v*c for i, v in p.items() if v*c} for p in a)

def sh(a, n):
    return tuple({i+n: v for i, v in p.items()} for p in a)

def mon(n, c=1):
    return ({n: Q(c)} if c else {}, {})

def mul(a, b):
    q = pm(a[1], b[1])
    even = pa(pa(pm(a[0], b[0]), q),
              {i+H: v for i, v in q.items()}, -1)
    odd = pa(pm(a[0], b[1]), pm(a[1], b[0]))
    return even, odd

@lru_cache(None)
def hc(n):
    return Q(1) if n == 0 else hc(n-1)*Q(2*n-3, 2*n)

def coeff(a, n):
    return a[0].get(n, 0) + sum(
        v*hc((n-i)//H) for i, v in a[1].items()
        if n >= i and (n-i) % H == 0
    )

def af(s):
    # The function in A with leading pole t^(-s).
    return mon(-s) if s % 2 == 0 else ({}, {-s: Q(1)})

def split(a, lam):
    # a = f + eta + t^(-lam)*w, with f in A and w regular.
    a = (a[0].copy(), a[1].copy())
    eta = {}
    for n in range(min([0] + list(a[0]) + list(a[1])), -lam):
        c = coeff(a, n)
        if not c:
            continue
        s = -n
        if (s >= 0 and s % 2 == 0) or s >= 2*g+1:
            a = add(a, sc(af(s), c), -1)
        else:
            eta[n] = c
            a = add(a, mon(n, c), -1)
    w = sh(a, lam)
    # Check actual regularity, allowing cancellation between P and Qh.
    for n in range(min([0] + list(w[0]) + list(w[1])), 0):
        assert coeff(w, n) == 0
    return eta, w

def rank(cols):
    piv = {}
    for c in cols:
        c = {i: Q(v) for i, v in c.items() if v}
        while c:
            i = min(c)
            v = c[i]
            if i in piv:
                c = pa(c, piv[i], -v)
            else:
                piv[i] = {j: w/v for j, w in c.items()}
                break
    return len(piv)

def cech(gg, b, kind):
    global g, H
    g = gg
    H = 4*g+2
    d = 2*g-2
    k = g-(g+2)//3
    M = 2*d+1

    phi = ({-(2*g-1-2*j): Q(v)
            for j, v in enumerate(b) if v}, {})
    phip = ({e-1: e*v for e, v in phi[0].items()}, {})
    kp = sc(phi, k)
    powers = [mon(0)]
    for a in range((M-1)//k):
        powers.append(mul(powers[-1], kp))

    def power(alpha, a):
        c = Q(1)
        for j in range(a):
            c *= Q(alpha-j, j+1)
        return sc(powers[a], c)

    if kind == 'S':
        inds = [(n, c) for n in range(M) for c in ('h', 'v')]
    else:
        inds = [(n, kind) for n in range(M)]

    lam = [n-d if c in ('h', 'L') else n for n, c in inds]
    R = [{} for _ in inds]

    # Full W-to-U transition matrix, not just its first nonlinear term.
    for j, (n, c) in enumerate(inds):
        alpha = -Q(n, k)
        for a in range((M-1-n)//k+1):
            m = n+a*k
            if kind != 'S':
                R[j][m] = sh(
                    power(alpha+(kind == 'L'), a),
                    -n+(d if kind == 'L' else 0)
                )
            elif c == 'v':
                R[j][2*m+1] = sh(power(alpha+1, a), -n)
            else:
                R[j][2*m] = sh(power(alpha, a), d-n)
                v = sh(power(alpha, a), -n-1)
                if a:
                    v = add(v, sh(mul(
                        power(alpha, a-1),
                        add(sh(kp, -1), phip)
                    ), -n))
                R[j][2*m+1] = sc(
                    mul(v, ({}, {0: Q(1)})), -Q(1, 2)
                )

    rows = {}
    h0 = []
    for i, l in enumerate(lam):
        exps = ([-s for s in range(1, 2*g, 2) if s > l]
                + list(range(1, max(1, -l))))
        for e in exps:
            rows[i, e] = len(rows)
        for s in range(max(-1, l)+1):
            if s % 2 == 0 or s >= 2*g+1:
                h0.append((i, s))

    cols = []
    for j, s in h0:
        w = sh(af(s), lam[j])
        v = {i: mul(p, w) for i, p in R[j].items() if i != j}
        col = {}
        for i in range(j+1, len(inds)):
            if i not in v:
                continue
            eta, w = split(v[i], lam[i])
            for e, c in eta.items():
                col[rows[i, e]] = c
            for ell, p in R[i].items():
                if ell != i:
                    v[ell] = add(
                        v.get(ell, ({}, {})), mul(p, w), -1
                    )
        cols.append(col)

    rk = rank(cols)
    return len(rows)-rk, rk

def checks():
    # Check the inverse differential transition symbolically.
    t, u, k, F, Fp = sp.symbols('t u k F Fp', nonzero=True)
    B = 1+k*F*u**k
    logv_t = -1/t-Fp*u**k/B
    logv_e = 1/B
    inv_e = sp.simplify(-logv_t/logv_e)
    assert sp.simplify(
        inv_e-(1/t+(k*F/t+Fp)*u**k)
    ) == 0
    assert sp.simplify(logv_e*B) == 1

    # Symbolic antitriangular pivot determinants.
    for m in range(6):
        bs = sp.symbols('b:'+str(m+1))
        for a in range(1, m+5):
            for q in range(1, m+5):
                if max(a, q) < m+1:
                    continue
                s = min(a, q, m+1)
                start = m-s+1
                mat = sp.Matrix(
                    s, s,
                    lambda i, j:
                    bs[start+i+j] if start+i+j <= m else 0
                )
                expected = (-1)**(s*(s-1)//2)*bs[m]**s
                assert sp.expand(
                    mat.det(method='domain-ge')-expected
                ) == 0

    # Integer inequalities and the closed rank sum.
    for g in range(2, 101):
        r = (g+2)//3
        k = g-r
        d = 2*g-2
        N = d-k
        assert d <= 3*k and N >= 4*(r-1)
        for m in range(r):
            aa = [
                min(n//2+1, (N-n)//2+1, m+1)
                for n in range(N+1)
            ]
            assert sum(aa[1:]) == (m+1)*(g+r-1-2*m)-1
            assert aa[k] == m+1

    # Independent, full-transition exact-rational computations.
    count = 0
    for gg in range(2, 13):
        r = (gg+2)//3
        vectors = (list(product((-1, 0, 1), repeat=r))
                   if r <= 3 else [])
        vectors += [
            tuple(int(i == j) for i in range(r))
            for j in range(r)
        ]
        vectors += [tuple(Q((-2)**i, i+1) for i in range(r))]
        for b in vectors:
            if not any(b):
                continue
            m = max(i for i, v in enumerate(b) if v)
            R = (m+1)*(gg+r-1-2*m)-1
            vals = [cech(gg, b, c) for c in ('O', 'S', 'L')]
            expected = [
                (gg*gg-R, R),
                (6*gg*gg-7*gg+2-2*R+m, 2*R+1-m),
                (5*gg*gg-7*gg+2-R, R+1)
            ]
            assert vals == expected, (gg, b, vals, expected)
            assert vals[0][0]-vals[1][0]+vals[2][0] == -m
            count += 1

    print("All exact checks passed;",
          count, "full-transition examples.")

if __name__ == '__main__':
    checks()
```

I ran this program; its output was:
```text
All exact checks passed; 146 full-transition examples.
```

The proof, rather than these finite tests, establishes uniformity over all \(g\) and all complex coefficients. **What is proved:** the three formulas (1), and hence \(\Delta_b=-\max\{j:b_j\ne0\}\), for every vector allowed in the question. **What is left:** nothing.