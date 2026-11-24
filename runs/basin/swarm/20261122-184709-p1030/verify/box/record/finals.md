# agent_1: last reply

Put
\[
E=\frac{(1+4h^2)s(s+1)-2hs+h(h-1)}2.
\]
Then the answer is the single monomial
\[
\boxed{\displaystyle Q_{h,s}(t)=t^E.}
\]
In particular, its coefficient is the integer \(1\). More precisely,
\[
L=E,\qquad m_E=1,\qquad m_{E-j}=0\quad(1\le j<\min(h,s+1)).
\]

We prove these assertions, including the gap below the largest elementary divisor. Python checks are given after the proof.

## 1. The Heegaard Floer path model

We use the standard graded-root computation for negative-definite Seifert plumbings with at most one bad vertex. Here is the particular form needed.

For a Seifert integral homology sphere with normalized data
\[
\left(-1;(p,p-1),(q,1),(r,1)\right),
\]
define
\[
\Delta(n)=1+\left\lfloor\frac np\right\rfloor
-\left\lceil\frac nq\right\rceil
-\left\lceil\frac nr\right\rceil,\qquad
\tau(n)=\sum_{j=0}^{n-1}\Delta(j).
\]
The finite bars of the sublevel-set persistence of the path with vertex heights \(\tau(n)\) give the \(U\)-torsion elementary-divisor lengths. A finite bar of length \(e\) gives one copy of \(\mathbb F[U]/(U^e)\).

This is the usual Ozsváth–Szabó/Némethi graded-root computation, expressed as persistence of a weighted path. Absolute gradings are unnecessary here. Changing orientation or passing between the corresponding plus and minus computations dualizes the finite modules and does not change their lengths.

In our case,
\[
pq+pr-qr=-1.
\]
Thus the displayed Seifert data have rational Euler number \(-1/(pqr)\), and the associated plumbing is negative definite. Its central vertex has weight \(-1\), its three legs have continued fractions
\[
\frac p{p-1}=[2,\ldots,2],\qquad q=[q],\qquad r=[r].
\]
Only the central vertex is bad. The relation above also proves pairwise coprimality.

Write
\[
C=qr,\qquad b=q+r.
\]
Then
\[
C=pb+1,\qquad
N=pqr-pq-pr-qr=(p-2)C+1.
\]
We can truncate the path at
\[
M=N+1=(p-2)C+2.
\]
Indeed, direct floor arithmetic gives
\[
\Delta(N-n)=-\Delta(n).
\]
Also, for \(k>0\),
\[
\Delta(-k)=1-\left\lceil\frac kp\right\rceil
+\left\lfloor\frac kq\right\rfloor+\left\lfloor\frac kr\right\rfloor\le0,
\]
because \(1/q+1/r<1/p\). Consequently \(\Delta(n)\ge0\) for \(n>N\), so extending the path adds no finite bars. We also have
\[
\tau(n)=\tau(M-n).
\tag{1}
\]

For later use, throughout \(0\le n\le N\),
\[
\Delta(n)\in\{-1,0,1\}.
\tag{2}
\]

## 2. Two integral vectors

Set
\[
u=(2h,1),\qquad v=(4hs-1,2s).
\]
These satisfy
\[
\det(u,v)=1,\qquad
\|u\|^2=a,\qquad u\cdot v=p,\qquad \|v\|^2=r-p.
\]
Let
\[
V=u+v=(x,y),
\quad x=2h(2s+1)-1,\quad y=2s+1.
\]
Then
\[
\|V\|^2=b,\qquad u\cdot V=q,\qquad v\cdot V=r.
\tag{3}
\]
In particular,
\[
b=x^2+y^2,\qquad b-4p=\|v-u\|^2\ge0.
\tag{4}
\]

Both \(x,y\) are odd, so \(b\equiv2\pmod8\). Thus
\[
E=\frac{b-2}{8}
=\frac{x^2-1}{8}+\frac{y^2-1}{8}.
\tag{5}
\]
Expanding (5) gives the exponent in the answer.

Put
\[
c=\frac M2,\qquad H=\tau(c)-E.
\]

## 3. A quadratic formula for the minima

For an integer \(n\) divisible by \(p\), put \(z=n-c\) and define
\[
A=2\left\lfloor\frac zq\right\rfloor+1,\qquad
B=2\left\lfloor\frac zr\right\rfloor+1,
\]
\[
W=\frac{2z}{p}-A-B,\qquad
X=2hA-(4hs-1)B,\qquad Y=A-2sB.
\]
All of \(W,X,Y\) are odd. The key identity is
\[
\boxed{\quad
8\bigl(\tau(n)-H\bigr)
=p(W^2-1)+X^2+Y^2-2.
\quad}
\tag{6}
\]
Moreover,
\[
W=2\Delta(n)-1.
\tag{7}
\]

Here are direct ways to verify the identities, rather than treating them as additional topological input. For any integer \(n\), define
\[
F_k(n)=k\frac{m(m-1)}2+mr,\qquad n=km+r,\quad 0\le r<k.
\]
Then
\[
\tau(n)=2-n+F_p(n)-F_q(n-1)-F_r(n-1).
\tag{8}
\]
This includes \(n=0\). Substitute
\[
F_k(n)=\frac{n^2}{2k}-\frac n2+\frac{r(k-r)}{2k}
\]
in (8), use \(qr=p(q+r)+1\), and complete squares. The final integral square completion is
\[
aA^2-2pAB+(r-p)B^2
=\bigl(2hA-(4hs-1)B\bigr)^2+(A-2sB)^2.
\]
This gives (6); (7) follows directly from the definitions.

A minimum plateau of \(\tau\) has a representative divisible by \(p\): the slope can increase only at such a point. The endpoints also are divisible by \(p\). Since the right side of (6) is nonnegative,
\[
\tau(n)\ge H\qquad(0\le n\le M).
\tag{9}
\]

Equality really occurs on both sides of \(c\). For \(X,Y\in\{-1,1\}\), choose \(W=1\) and
\[
n=c+\frac p2(1+yX-xY).
\tag{10}
\]
The inverse formulas are
\[
A=2sX-(4hs-1)Y,\qquad B=X-2hY.
\]
They give the required floors: the relevant centered remainders are
\[
p-2hX-Y,\qquad p+(4hs-1)X+2sY,
\]
whose absolute values are respectively less than \(q\) and \(r\). The points (10) lie strictly between \(0\) and \(M\). Since \(x>y+1\), those with \(Y=1\) lie to the left of \(c\), and those with \(Y=-1\) lie to its right. By (6), all have height \(H\).

Thus \(H\) is the global minimum, attained on both sides of the central vertex.

## 4. An arithmetic gap lemma

Define the integral linear form
\[
T(Z)=yZ_1-xZ_2.
\]

**Lemma.** Let \(Z\in\mathbb Z^2\setminus\{0\}\) satisfy
\[
T(Z)<0,\qquad |u\cdot Z|\le p/2,\qquad |v\cdot Z|\le p/2.
\]
If \(D=(D_1,D_2)\) has odd coordinates and \(T(D)\ge2\), then, with
\(d=\min(h,s+1)\),
\[
\boxed{\quad
\|D\|^2-4Z\cdot D+4|V\cdot Z|-2\ge8d.
\quad}
\tag{11}
\]

### Proof

Let the left side of (11) be \(G\), and write
\[
m=V\cdot Z,\qquad i=u\cdot Z,\qquad J=T(D).
\]
We have
\[
|m|\le p\le b/4,\qquad T(Z)=bi-qm.
\tag{12}
\]
Orthogonal decomposition along \(V\) and \((y,-x)\), using \(T(Z)<0<J\), gives
\[
\|D\|^2-4Z\cdot D\ge-\frac{4m^2}{b}.
\]
Therefore
\[
G\ge3|m|-2.
\tag{13}
\]
Also \(G\) is divisible by \(8\).

Suppose, for contradiction, that \(G<8d\). From (13),
\[
|m|\le\frac{8d-6}{3}
\le\frac{4y-2}{3}<2y.
\tag{14}
\]
Since \(T(Z)=bi-qm<0\),
\[
i\le i_0:=\left\lfloor\frac{qm-1}{b}\right\rfloor.
\]
For fixed \(m,D\), the expression
\[
G=\|D\|^2-4iJ+4m(D_1-2hD_2)+4|m|-2
\tag{15}
\]
decreases as \(i\) increases. It suffices to use \(i=i_0\).

The identity \(qy=b+x\) gives
\[
\frac qb=\frac1y+\frac{x}{by}.
\]
For \(0<k<2y\), the correction \(xk/(by)\) is less than \(1/y\), because
\(2xy<b=x^2+y^2\). Hence
\[
\begin{array}{c|ccccc}
m&0&0<m<y&y\le m<2y&-y<m<0&-2y<m\le-y\\ \hline
i_0&-1&0&1&-1&-2.
\end{array}
\tag{16}
\]

Put \(e=D_1-2hD_2\), an odd integer. Since
\[
J=ye+D_2\ge2,
\tag{17}
\]
if \(e=-k<0\), then
\[
D_2\ge yk+2,\qquad
D_1\ge(2hy-1)k+4h\ge hyk+4h.
\]
In each case of (16), expression (15) has the form
\[
\|D\|^2+4\rho e+4\gamma D_2+4|m|-2,
\qquad 0\le\rho\le y,\quad \gamma\ge-1.
\]
Consequently
\[
G\ge (hyk+4h)^2-4yk-6
\ge16h^2-6\ge8h\ge8d,
\]
a contradiction.

It remains to take \(e\ge1\). Elementary odd-integer inequalities give
\[
\begin{aligned}
\|D\|^2+4e+2&\ge8h,\\
\|D\|^2-4D_2&\ge6,\\
\|D\|^2+4D_2+4(e-1)&\ge6,\\
\|D\|^2+8D_2+4(e-1)&\ge2.
\end{aligned}
\tag{18}
\]
For completeness, split according to the sign of \(D_2\). If \(D_2\ge1\), then
\(D_1=2hD_2+e\ge2hD_2+1\), and all four bounds follow immediately. If
\(D_2\le-1\), use
\[
D_1^2+4D_1\ge-3
\]
and \(h\ge2\); the respective bounds follow by setting \(-D_2\ge1\).

Substitute (18) in the five cases of (16). For \(0<m<y\), the first inequality gives \(G\ge8h\). For \(y\le m<2y\), put \(n=m-y\ge0\) and write
\[
G=\|D\|^2-4D_2+4n(e+1)+4y-2\ge4y+4.
\]
For \(m=-k\), \(0<k<y\), put \(n=y-k\ge1\):
\[
G=\|D\|^2+4D_2+4n(e-1)+4y-2\ge4y+4.
\]
For \(y\le k<2y\), put \(n=2y-k\ge1\):
\[
G=\|D\|^2+8D_2+4n(e-1)+8y-2\ge8y.
\]
Finally, \(m=0\) gives
\[
G=\bigl(\|D\|^2+4D_2+4(e-1)\bigr)+4(y-1)e+2
\ge4y+4.
\]
Because \(4y+4=8(s+1)\), every case gives \(G\ge8d\), completing the contradiction and the proof. ∎

## 5. Every noncentral maximum has a shorter bar

We now describe the maxima of \(\tau\). On a cell
\[
[n_0,n_0+p],\qquad p\mid n_0,
\]
the slope can decrease only at points \(qj+1\) and \(rk+1\). Since \(q,r>p\), there is at most one event of each kind in the cell.

Every genuine maximum plateau has a representative of the following form:

* \(\Delta(n_0)=1\);
* both next negative events occur in the closed cell;
* their distances from \(n_0\) are \(\alpha,\beta\in(0,p]\);
* the height of the plateau is \(\tau(n_0)+\min(\alpha,\beta)\).

Here is why this also handles coincidences at cell boundaries. Start with the positive segment immediately preceding a maximum plateau. Its first negative event lowers the slope from \(1\) to \(0\). Before the next \(p\)-boundary there must be another negative event, possibly at that boundary; otherwise the boundary raises the slope back to \(1\), contradicting that the intervening plateau is a maximum. Thus one can choose the asserted cell.

By (7), \(W=1\) at \(n_0\). Write the odd vector \((X,Y)\) from Section 3 as
\[
(X,Y)=v-u+2Z.
\]
The distances to the next two negative events are
\[
\alpha=\frac p2+u\cdot Z,\qquad
\beta=\frac p2-v\cdot Z.
\tag{19}
\]
Thus
\[
|u\cdot Z|,\ |v\cdot Z|\le p/2.
\]
Equations (6) and (19) give the maximum height
\[
\boxed{\quad
\tau_{\rm peak}
=H+E+\frac{\|Z\|^2-|V\cdot Z|}{2}.
\quad}
\tag{20}
\]
Also,
\[
n_0-c=p\left(T(Z)-\frac12\right).
\tag{21}
\]

The central maximum corresponds to \(Z=0\): both events occur at \(c\), and its height is \(H+E=\tau(c)\). For a maximum to the left of \(c\), (19)–(21) imply \(T(Z)<0\). Indeed, \(T(Z)=0\) would force \(Z\) to be an integral multiple of the primitive vector \(V\), and the strip bounds force that multiple to be zero.

Consider a left-hand maximum, and choose a prefix minimum before it. It can be represented at a point \(n_b\le n_0\) divisible by \(p\) with \(\Delta(n_b)=1\). Let its odd vector from Section 3 be \(B_0\). Then
\[
\tau(n_b)=H+\frac{\|B_0\|^2-2}{8}.
\]
The ordering \(n_b\le n_0\), together with (21), implies
\[
T(B_0)\le2T(Z)-2.
\]
Therefore
\[
D=2Z-B_0
\]
has odd coordinates and \(T(D)\ge2\). Subtracting the birth height from (20),
\[
8\bigl(\tau_{\rm peak}-\tau(n_b)\bigr)
=8E-\left(\|D\|^2-4Z\cdot D+4|V\cdot Z|-2\right).
\]
The arithmetic lemma proves
\[
\tau_{\rm peak}-\min_{n\le n_{\rm peak}}\tau(n)\le E-d.
\tag{22}
\]
By reflection (1), the corresponding suffix-minimum bound holds for every right-hand maximum.

At a maximum of a weighted path, the two merging components lie on opposite sides of that maximum. Their birth heights are at least the respective prefix and suffix minima. Thus every finite bar dying at a noncentral maximum has length at most \(E-d\), by (22).

Finally, take one of the global minima from (10) on each side of \(c\). For every noncentral maximum between the left one and \(c\), its prefix minimum is \(H\); hence (22) places its height strictly below \(\tau(c)\). The reflected statement holds on the right. Therefore, at height \(\tau(c)\), the central vertex joins two components both born at height \(H\). It produces exactly one bar of length
\[
\tau(c)-H=E.
\]
Every other finite bar has length at most \(E-d\).

This proves the claimed largest length, multiplicity, and gap.

## 6. Executable checks

The following Python computes the path and its persistence bars, checks the quadratic identity at **every** \(p\)-grid point, checks **every** possible cell roof, and checks the resulting top multiplicities. For two cases it independently verifies the entire delta sequence using the Brieskorn semigroup.

The argument above is uniform in \(h,s\); these are additional exact checks, not an extrapolation from numerical examples.

```python
import numpy as np
from collections import Counter

def parameters(h, s):
    a = 1 + 4*h*h
    p = 2*a*s - 2*h
    q = p + a
    r = p + (p*p + 1)//a
    return a, p, q, r

def F(n, k):
    m, z = np.divmod(n, k)
    return k*(m*(m-1)//2) + m*z

def tau(n, p, q, r):
    return 2-n + F(n, p) - F(n-1, q) - F(n-1, r)

def delta(n, p, q, r):
    return 1+n//p-(n+q-1)//q-(n+r-1)//r

def persistence(weights):
    """Exact sublevel persistence of a path; return finite bar lengths."""
    size = len(weights)
    parent = np.full(size, -1, dtype=np.int64)
    birth = np.zeros(size, dtype=np.int64)
    bars = []

    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i in np.argsort(weights, kind="stable"):
        parent[i] = i
        birth[i] = weights[i]
        for j in (i-1, i+1):
            if 0 <= j < size and parent[j] >= 0:
                u, v = root(i), root(j)
                if u == v:
                    continue
                if birth[u] > birth[v]:
                    u, v = v, u
                length = int(weights[i] - birth[v])
                if length:
                    bars.append(length)
                parent[v] = u
    return Counter(bars)

def check_case(h, s, full=False):
    a, p, q, r = parameters(h, s)
    b = q+r
    M = (p-2)*q*r + 2
    c = M//2
    v1 = 4*h*s-1
    x, y = v1+2*h, 2*s+1
    E, d = (b-2)//8, min(h, s+1)

    assert a*(r-p) == p*p+1
    assert q*r == p*b+1
    assert x*x+y*y == b
    assert b % 8 == 2 and p % 2 == 0
    assert 4*p <= b

    H = int(tau(c, p, q, r)) - E

    # All p-grid points, not a sample.
    grid = np.arange(0, M+1, p, dtype=np.int64)
    z = grid-c
    A = 2*(z//q)+1
    B = 2*(z//r)+1
    W = 2*z//p-A-B
    X = 2*h*A-v1*B
    Y = A-2*s*B
    tg = tau(grid, p, q, r)

    assert np.all((W % 2 == 1) & (X % 2 == 1) & (Y % 2 == 1))
    assert np.array_equal(
        8*(tg-H), p*(W*W-1)+X*X+Y*Y-2
    )
    assert np.all(W == 2*delta(grid, p, q, r)-1)
    assert np.min(tg) == H

    explicit_minima = []
    for XX in (-1, 1):
        for YY in (-1, 1):
            n = c+p*(1+y*XX-x*YY)//2
            assert 0 < n < M and n % p == 0
            assert tau(n, p, q, r) == H
            explicit_minima.append(n)
    assert min(explicit_minima) < c < max(explicit_minima)

    prefix = np.minimum.accumulate(tg)
    roofs = []

    for k, n in enumerate(grid[:-1]):
        if delta(n, p, q, r) != 1:
            continue
        alpha = q-(n-1) % q
        beta = r-(n-1) % r
        if alpha > p or beta > p:
            continue

        Z1 = (int(X[k])-(v1-2*h))//2
        Z2 = (int(Y[k])-(2*s-1))//2
        m = x*Z1+y*Z2
        T = y*Z1-x*Z2

        assert alpha == p//2+2*h*Z1+Z2
        assert beta == p//2-v1*Z1-2*s*Z2

        peak = n+min(alpha, beta)
        height = int(tau(peak, p, q, r))
        assert height == H+E+(Z1*Z1+Z2*Z2-abs(m))//2
        roofs.append((peak, height))

        if peak < c:
            assert T < 0
            assert max(abs(2*h*Z1+Z2),
                       abs(v1*Z1+2*s*Z2)) <= p//2

            # Find an actual prefix minimum with W=1.
            choices = np.flatnonzero(
                (tg[:k+1] == prefix[k]) & (W[:k+1] == 1)
            )
            assert len(choices)
            j = int(choices[-1])
            D1 = 2*Z1-int(X[j])
            D2 = 2*Z2-int(Y[j])
            assert D1 % 2 == D2 % 2 == 1
            assert y*D1-x*D2 >= 2

            G = (D1*D1+D2*D2
                 -4*(Z1*D1+Z2*D2)+4*abs(m)-2)
            assert G % 8 == 0 and G >= 8*d
            assert height-prefix[k] <= E-d

    # Every point where the slope can change.
    events = np.unique(np.r_[
        grid,
        np.arange(1, M, q, dtype=np.int64),
        np.arange(1, M, r, dtype=np.int64),
        M
    ])
    weights = tau(events, p, q, r)
    assert np.all(weights >= H)
    assert np.array_equal(weights, tau(M-events, p, q, r))

    # Collapse constant runs, retaining their full plateau ranges.
    change = np.r_[True, weights[1:] != weights[:-1]]
    starts = np.flatnonzero(change)
    ends = np.r_[starts[1:]-1, len(events)-1]
    ww = weights[change]

    rp = np.array([z[0] for z in roofs])
    rh = np.array([z[1] for z in roofs])
    for j in range(1, len(ww)-1):
        if ww[j] > ww[j-1] and ww[j] > ww[j+1]:
            lo, hi = events[starts[j]], events[ends[j]]
            k = np.searchsorted(rp, lo)
            assert k < len(roofs)
            assert rp[k] <= hi and rh[k] == ww[j]

    # Removing monotone interior vertices preserves the finite bars.
    signs = np.sign(np.diff(ww))
    keep = np.r_[True, signs[:-1] != signs[1:], True]
    bars = persistence(ww[keep])

    assert max(bars) == E
    assert bars[E] == 1
    assert all(bars.get(j, 0) == 0 for j in range(E-d+1, E))

    if full:
        ns = np.arange(M, dtype=np.int64)
        dd = delta(ns, p, q, r)
        assert np.all(np.abs(dd) <= 1)
        assert np.array_equal(dd, -dd[::-1])

        entire_tau = np.r_[0, np.cumsum(dd)]
        assert np.array_equal(
            entire_tau, tau(np.arange(M+1), p, q, r)
        )
        assert np.array_equal(entire_tau[events], weights)

        # Independent semigroup check at every integer 0 <= n <= N.
        N = M-1
        S = np.zeros(M, dtype=np.int8)
        aa, bb, cc = p*q, p*r, q*r
        for i in range(N//aa+1):
            for j in range((N-i*aa)//bb+1):
                S[i*aa+j*bb:N+1:cc] = 1
        assert np.array_equal(dd, S-S[::-1])

    top = [(j, bars.get(j, 0)) for j in range(E, E-d, -1)]
    print((h, s), "grid points:", len(grid), "top:", top)

for h, s in [
    (2, 1), (2, 2), (2, 3), (3, 1),
    (3, 2), (4, 1), (4, 2), (4, 3)
]:
    check_case(h, s, full=(h, s) in [(2, 1), (3, 1)])
```

These checks give:
```text
(2, 1) grid points: 3642    top: [(16, 1), (15, 0)]
(2, 2) grid points: 23934   top: [(48, 1), (47, 0)]
(2, 3) grid points: 74690   top: [(97, 1), (96, 0)]
(3, 1) grid points: 19670   top: [(37, 1), (36, 0)]
(3, 2) grid points: 121242  top: [(108, 1), (107, 0), (106, 0)]
(4, 1) grid points: 64562   top: [(67, 1), (66, 0)]
(4, 2) grid points: 386502  top: [(193, 1), (192, 0), (191, 0)]
(4, 3) grid points: 1168122 top: [(384, 1), (383, 0), (382, 0), (381, 0)]
```

**Proved:** for every \(h\ge2\), \(s\ge1\), the largest torsion length is \(E\), it occurs exactly once, and the next \(d-1\) degree positions have multiplicity zero. Hence \(Q_{h,s}(t)=t^E\). Nothing remains to be determined for the question asked.