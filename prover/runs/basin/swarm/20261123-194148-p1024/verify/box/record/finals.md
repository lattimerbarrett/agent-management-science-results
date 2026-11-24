# agent_1: last reply

Put
\[
j(b)=\max\{j:b_j\ne0\}.
\]
Then the answer is
\[
\boxed{\displaystyle \Delta_b=-j(b).}
\]
Thus the answer depends on the position of the **last nonzero component**, not on how many components are nonzero. In particular, it is \(0\) when only \(b_0\) is nonzero.

We give a proof covering all coefficient vectors, followed by exact-arithmetic Python that computes the three cohomology dimensions from finite Čech matrices.

## 1. The relevant bundles and transitions

Write
\[
d=2g-2,\qquad \mathcal F=\ker(S_b\longrightarrow\pi^*\Theta_{C_g}),
\qquad \mathcal P=\pi^*\Theta_{C_g},
\]
where \(\pi:X_b\to C_g\) is the projection. The local generator of \(\mathcal F\) is the logarithmic vertical vector field \(y\partial_y\). Consequently,
\[
0\longrightarrow\mathcal F\longrightarrow S_b
 \longrightarrow\mathcal P\longrightarrow0,
\qquad
L_b=\mathcal F\otimes\mathcal P.                                      \tag{1}
\]

Set \(u=y_U,\ v=y_W\), and introduce
\[
\psi=t^k\phi_b,\qquad B=1-k\psi v^k.
\]
The inverse fiber-coordinate change is
\[
u=tvB^{-1/k}.                                                        \tag{2}
\]
In particular,
\[
u\partial_u=B\,v\partial_v.                                         \tag{3}
\]

The differential \(dx/z\) has divisor \(dp\). Its dual vector field
\[
e=z\partial_x+\frac{2g+1}{2}x^{2g}\partial_z
\]
is a nowhere-zero frame of \(\Theta_{C_g}\) away from \(p\). In the \(t\)-coordinate,
\[
e=q(t)\partial_t,\qquad
q(t)=-\frac12t^{-d}(1-t^{4g+2})^{1/2}.                               \tag{4}
\]

Let \(\mathcal I=\mathcal I_E\). The associated graded bundles are
\[
\begin{aligned}
\mathcal I^n\mathcal O/\mathcal I^{n+1}\mathcal O
 &\simeq\mathcal O_{C_g}(np),\\
\mathcal I^n\mathcal F/\mathcal I^{n+1}\mathcal F
 &\simeq\mathcal O_{C_g}(np),\\
\mathcal I^n\mathcal P/\mathcal I^{n+1}\mathcal P
 &\simeq\mathcal O_{C_g}((n-d)p),\\
\mathcal I^nL_b/\mathcal I^{n+1}L_b
 &\simeq\mathcal O_{C_g}((n-d)p).
\end{aligned}                                                       \tag{5}
\]

These filtrations can be used to compute the actual analytic cohomology. Indeed, the first cohomology of the graded terms vanishes for \(n\ge2g-1\) in the first two cases, and for \(n\ge4g-3\) in the last two. The same latter bound applies to \(S_b\), by (1). Formal functions, together with cohomological dimension at most one for a resolution over a sufficiently small Stein representative, therefore gives
\[
H^1(X_b,\mathcal G)
 \simeq H^1(X_b,\mathcal G/\mathcal I^{\,4g-3}\mathcal G)              \tag{6}
\]
for every sheaf used below. It also gives
\[
H^1(X_b,\mathcal I^{d+1}\mathcal F)=0.                               \tag{7}
\]
For clarity, the vanishing assertion follows by first applying the graded vanishing to every finite thickening. Formal functions makes the completion of the corresponding \(R^1f_*\) zero; coherence and Nakayama then make \(R^1f_*\) itself zero.

## 2. Scalar obstruction maps

The Weierstrass semigroup at \(p\) is
\[
\langle2,2g+1\rangle.
\]
Its gaps are \(1,3,\ldots,2g-1\). Thus, for \(m\ge0\),
\[
H^1(C_g,\mathcal O(mp))
 =
\left\langle[t^{-\ell}]:
 \ell\ \text{odd},\ m<\ell\le2g-1\right\rangle.                      \tag{8}
\]
In particular, this cohomology has only odd principal-part parity. For \(0\le m\le d\),
\[
H^0(C_g,\mathcal O(mp))
 =\langle1,x,\ldots,x^{\lfloor m/2\rfloor}\rangle,                    \tag{9}
\]
so its elements have even parity.

After removing the even holomorphic unit in (4), the four scalar transitions in fiber degree \(n\) have the following form:
\[
\begin{array}{c|c|c}
\text{sheaf}&\text{graded bundle}&\text{factor involving }B\\ \hline
\mathcal O&\mathcal O(np)&B^{-n/k}\\
\mathcal F&\mathcal O(np)&B^{1-n/k}\\
\mathcal P&\mathcal O((n-d)p)&B^{-n/k}\\
L_b&\mathcal O((n-d)p)&B^{1-n/k}.
\end{array}                                                        \tag{10}
\]

Expanding \(B^\alpha\) shows that the first possible obstruction raises fiber degree by \(k\). On the corresponding graded cohomology it is multiplication by \(\phi_b\), with scalar coefficient
\[
n\quad\text{for }\mathcal O,\mathcal P,
\qquad
n-k\quad\text{for }\mathcal F,L_b.                                  \tag{11}
\]
Signs do not matter for its rank.

### Why there are no further rank losses

Here are the details needed to rule out hidden higher obstructions.

The transitions preserve fiber degree modulo \(k\), so subsequent obstructions can only raise degree by \(2k,3k,\ldots\). Reindex a possible source by \(m=n\) for \(\mathcal O,\mathcal F\), and by \(m=n-d\) for \(\mathcal P,L_b\). A source capable of reaching nonzero \(H^1\) has \(m\ge0\), and its leading coefficient is even by (9).

The function \(\phi_b\) is odd. If the first obstruction vanishes, its correcting cochains can be chosen odd: the ordinary line-bundle Čech decomposition respects the involution \(t\mapsto-t\). The obstruction at the next step, of size \(2k\), is consequently even. It vanishes by (8).

Moreover,
\[
3k\ge d.                                                          \tag{12}
\]
Indeed \(g\in\{3r-2,3r-1,3r\}\), and \(3k-d=g-3r+2\in\{0,1,2\}\).
Thus an obstruction of size \(3k\) is possible only when \(3k=d\) and \(m=0\).

For \(\mathcal F,\mathcal P,L_b\), that unique source is already killed by the first obstruction. Its scalar coefficient is respectively \(-k,d,d-k\), all nonzero, and
\[
[\phi_b]\ne0\quad\text{in }H^1(C_g,\mathcal O(kp)).                   \tag{13}
\]
To see (13), every monomial of \(\phi_b\) is an odd gap principal part, with pole order at least
\[
2g-1-2(r-1)=2k+1>k.
\]
For \(\mathcal O\), the \(m=0\) source is the constant function, which lifts exactly. No larger obstruction is possible.

Finally, the exceptional first coefficient \(n-k=0\) for \(\mathcal F\) causes no later obstruction: in that degree the factor in (10) is exactly \(B^0=1\).

Therefore all four scalar cohomologies are obtained from their graded cohomologies by subtracting precisely the ranks of the first maps (11).

## 3. Comparing the scalar cohomologies

For \(m\ge0\), denote by
\[
R_m=\operatorname{rank}\left(
H^0(C_g,\mathcal O(mp))
 \xrightarrow{\ \phi_b\ }
H^1(C_g,\mathcal O((m+k)p))
\right).                                                          \tag{14}
\]

The sheaves \(\mathcal O\) and \(\mathcal F\) have identical graded bundles. Their first-map ranks agree except in degrees \(0\) and \(k\). Equation (11) therefore gives
\[
h^1(\mathcal F)-h^1(\mathcal O)=R_k-R_0.                             \tag{15}
\]
By (13), \(R_0=1\).

Put
\[
s=j(b)+1.
\]
We claim \(R_k=s\). In the bases (8)–(9), the matrix in (14) for \(m=k\) is
\[
H=(b_{\ell+a})_{\substack{0\le\ell\le r-1\\
                          0\le a\le\lfloor k/2\rfloor}},
\qquad b_j=0\quad(j\ge r).                                         \tag{16}
\]
There are at least \(r\) columns, since \(\lfloor k/2\rfloor+1\ge r\).
All entries with \(\ell+a\ge s\) vanish, while the leading \(s\times s\)
block is anti-triangular with anti-diagonal \(b_{s-1}\ne0\). Its determinant is
\[
\pm b_{s-1}^{\,s}.
\]
All rows and columns beyond that block are zero. Hence \(R_k=s\), proving
\[
h^1(\mathcal F)=h^1(\mathcal O)+s-1.                                \tag{17}
\]

Likewise, \(\mathcal P\) and \(L_b\) have identical graded bundles. Every possible \(H^0\) source has fiber degree \(n\ge d\), and both coefficients \(n\) and \(n-k\) in (11) are nonzero. Their first-map ranks, and hence their cohomology dimensions, agree:
\[
h^1(\mathcal P)=h^1(L_b).                                          \tag{18}
\]

## 4. The connecting homomorphism is zero

It remains important not to discard the connecting homomorphism in (1).

Every global section of \(\mathcal P\) has fiber order at least \(d\), because its lower graded bundles have negative degree. A section with a nonzero symbol in degree \(d\) would have first obstruction
\[
d[\phi_b]\in H^1(C_g,\mathcal O(kp)),
\]
which is nonzero by (13). Consequently every global section actually belongs to
\[
H^0(X_b,\mathcal I^{d+1}\mathcal P).
\]
By (7) and the sequence (1) tensored with \(\mathcal I^{d+1}\), every such section lifts to \(S_b\). Thus the connecting map
\[
H^0(X_b,\mathcal P)\longrightarrow H^1(X_b,\mathcal F)
\]
is zero. Since \(H^2(X_b,\mathcal F)=0\), we obtain
\[
h^1(S_b)=h^1(\mathcal F)+h^1(\mathcal P).                            \tag{19}
\]

Combining (17)–(19),
\[
\begin{aligned}
\Delta_b
 &=h^1(\mathcal O)-h^1(S_b)+h^1(L_b)\\
 &=h^1(\mathcal O)-h^1(\mathcal F)\\
 &=1-s=-j(b),
\end{aligned}
\]
as asserted. The anti-triangular argument explicitly includes all patterns of vanishing components.

## 5. Exact computational verification

The following standalone Python uses only rational arithmetic. It **does not compute the cohomology by substituting the answer**: it constructs finite Čech matrices for \(\mathcal O,S_b,L_b\) from the given gluing and computes their ranks.

For completeness, the horizontal logarithmic transition used in the code is
\[
e_U=q\partial_t+
q\left(-\frac1t-\phi_b't^kv^k\right)v\partial_v,                    \tag{20}
\]
together with (2)–(4).

Here is why its Laurent cutoffs are certified. Set \(N=4g-3\) and
\[
R_n=3n+4g.
\]
Retain the negative Laurent rows \(t^ev^n\) with \(-R_n\le e<0\); for the vertical component of \(S_b\), retain one additional row. A basis of functions regular away from \(p\), indexed by pole order, is
\[
a_D=
\begin{cases}
x^{D/2},&D\text{ even},\\
x^{(D-2g-1)/2}z,&D\text{ odd},\ D\ge2g+1.
\end{cases}
\]
The respective source cutoffs in degree \(n\) are
\[
D\le4n+4g,\qquad
D\le4n+2g+2,\qquad
D\le4n+4g+1
\]
for \(\mathcal O\), for \(L_b\) or the horizontal component, and for the vertical component.

Each jump by \(k\) lowers the \(t\)-exponent by at most \(2g-1-k\le3k\); (20) requires precisely the extra vertical row. Thus retained columns remain in the retained rows. Every omitted target monomial corresponds to a nongap pole order and can be eliminated by an omitted source. Conversely, in a relation landing in the retained window, the least fiber degree and most negative leading term exclude every omitted source. For \(S_b\), apply this first to the horizontal component, then to the vertical component. Hence these finite matrix cokernels are exactly the required cohomologies. Analytic rather than polynomial source functions introduce no extra relations: a source whose boundary has finite principal parts extends meromorphically at \(p\), degree by degree.

```python
from fractions import Fraction as Q

def choose(a, j):
    v = Q(1)
    for i in range(j):
        v *= (a-i)/(i+1)
    return v

def mul(a, b):
    c = {}
    for i, x in a.items():
        for j, y in b.items():
            c[i+j] = c.get(i+j, 0) + x*y
    return {i: x for i, x in c.items() if x}

def cech_matrix(g, b, kind):
    r = (g+2)//3
    k, N, M = g-r, 4*g-3, 4*g+2
    types = ('h', 'v') if kind == 'S' else ('f',)

    rows = {}
    for n in range(N):
        for typ in types:
            for e in range(-3*n-4*g-(typ == 'v'), 0):
                rows[n, typ, e] = len(rows)

    psi = {k-2*g+1+2*j: Q(x)
           for j, x in enumerate(b) if x}
    # phi'(t) t^k
    deriv = {e-1: (e-k)*x for e, x in psi.items()}
    powers = [{0: Q(1)}]
    for j in range((N-1)//k):
        powers.append(mul(powers[-1], psi))

    columns = []
    for n in range(N):
        for typ in types:
            horizontal = (kind == 'L' or typ == 'h')
            limit = 4*n + (
                2*g+2 if horizontal else 4*g+(typ == 'v')
            )
            alpha = (
                Q(1) if kind == 'L' or typ == 'v' else Q(0)
            ) - Q(n, k)

            for D in range(limit+1):
                if D % 2 and D < 2*g+1:
                    continue
                col = {}

                for j in range((N-1-n)//k+1):
                    factor = choose(alpha, j)*(-k)**j
                    if horizontal:
                        factor *= -Q(1, 2)
                    p = {e: factor*x for e, x in powers[j].items()}
                    terms = [(n+j*k, typ, p, 0)]

                    if typ == 'h':
                        terms = [
                            (n+j*k, 'h', p, 0),
                            (n+j*k, 'v',
                             {e: -x for e, x in p.items()}, -1)
                        ]
                        if n+(j+1)*k < N:
                            terms.append((
                                n+(j+1)*k, 'v',
                                {e: -x for e, x
                                 in mul(p, deriv).items()}, 0
                            ))

                    for m, tp, p, shift in terms:
                        for e, x in p.items():
                            base = (
                                n-D+(2-2*g if horizontal else 0)
                                +e+shift
                            )
                            # Expansion of
                            # (1-t^M)^((D%2+horizontal)/2)
                            for a in range(
                                max(0, (-1-base)//M+1)
                            ):
                                exponent = base+M*a
                                value = (
                                    x*choose(
                                        Q(D % 2+horizontal, 2), a
                                    )*(-1)**a
                                )
                                if value:
                                    key = (m, tp, exponent)
                                    assert key in rows
                                    i = rows[key]
                                    col[i] = col.get(i, 0)+value

                columns.append({
                    i: x for i, x in col.items() if x
                })

    return len(rows), columns

def exact_rank(columns):
    pivots = {}
    for col in columns:
        col = dict(col)
        while col:
            i = min(col)
            x = col[i]
            if i not in pivots:
                pivots[i] = {
                    j: y/x for j, y in col.items()
                }
                break
            for j, y in pivots[i].items():
                col[j] = col.get(j, 0)-x*y
                if not col[j]:
                    del col[j]
    return len(pivots)

def cohomology(g, b):
    answer = []
    for kind in ('O', 'S', 'L'):
        nr, columns = cech_matrix(g, b, kind)
        answer.append(nr-exact_rank(columns))
    return tuple(answer)

if __name__ == '__main__':
    import random
    random.seed(2)
    checked = 0

    for g in range(2, 9):
        r = (g+2)//3
        cases = [[0]*r]
        cases += [
            [int(i == j) for i in range(r)]
            for j in range(r)
        ]
        cases += [
            [random.randint(-2, 2) for _ in range(r)]
            for _ in range(3)
        ]

        for b in cases:
            hO, hS, hL = cohomology(g, b)
            s = max(
                (j+1 for j, x in enumerate(b) if x),
                default=0
            )
            assert hO-hS+hL == 1-s, (
                g, b, (hO, hS, hL)
            )

            if s:
                assert hL-hO == 4*g*g-7*g+2
            else:
                # Auxiliary undeformed consistency check.
                assert (hO, hS, hL) == (
                    g*g,
                    6*g*g-7*g+2,
                    5*g*g-7*g+3
                )
            checked += 1

    print(checked, "exact Cech-matrix checks passed")
```

Executing this code produced:

```text
42 exact Cech-matrix checks passed
```

For example, when \(g=7\), the exact computed triples
\((h^1(\mathcal O),h^1(S_b),h^1(L_b))\) for \(b=(1,0,0),(0,1,0),(0,0,1)\) are respectively
\[
(41,231,190),\qquad(36,222,185),\qquad(35,221,184),
\]
giving \(\Delta_b=0,-1,-2\), as the formula requires.

# agent_2: last reply

Let
\[
s=1+\max\{j:b_j\ne0\}.
\]
Then
\[
\boxed{\Delta_b=1-s=-\max\{j:b_j\ne0\}.}
\]

My part of the proof is complete:

- Writing \(F\) for the vertical logarithmic tangent line bundle gives
  \[
  0\longrightarrow F\longrightarrow S_b\longrightarrow\pi^*T_{C_g}\longrightarrow0,
  \qquad L_b=F\otimes\pi^*T_{C_g}.
  \]
- Explicit transition calculations and the fiber-order filtration give
  \[
  h^1(F)=h^1(\mathcal O_{X_b})+s-1,
  \qquad
  h^1(\pi^*T_{C_g})=h^1(L_b).
  \]
  The first identities reduce to multiplication by \(\phi_b\); higher obstructions vanish by parity and \(3k\ge2g-2\). The exceptional multiplication matrix has rank \(s\), by its nonzero anti-diagonal \(b_{s-1}\).
- The connecting map
  \[
  H^0(\pi^*T_{C_g})\longrightarrow H^1(F)
  \]
  vanishes. Indeed, the unique possible leading horizontal symbol of fiber order \(2g-2\) has nonzero first obstruction proportional to \([\phi_b]\). Thus every actual horizontal section has order at least \(2g-1\), where \(H^1(F\mathcal I_E^{2g-1})=0\).
- Consequently,
  \[
  h^1(S_b)=h^1(F)+h^1(\pi^*T_{C_g}),
  \]
  yielding the boxed answer.

Independent exact-rank checks agree with the formula. Additional cutoff and Hankel-rank verification code is saved in `workspace/agent2_checks.py`; the team’s full Laurent-transition computation is in `workspace/agent4_laurent_matrix.py`.

# agent_3: last reply

Proved the scalar cohomology comparisons needed for the closed answer. Writing
\[
s=1+\max\{j:b_j\ne0\},
\]
they are
\[
h^1(X_b,F)=h^1(X_b,\mathcal O_{X_b})-1+s,
\qquad
h^1(X_b,\pi^*T_{C_g})=h^1(X_b,L_b),
\]
where \(F=\ker(S_b\to\pi^*T_{C_g})\).

Together with the team’s proof that the connecting homomorphism
\[
H^0(X_b,\pi^*T_{C_g})\longrightarrow H^1(X_b,F)
\]
vanishes, these give
\[
\boxed{\Delta_b=1-s=-\max\{j:b_j\ne0\}.}
\]

The scalar proof includes the vanishing of all higher filtration differentials and analytic/formal truncation justification. Independent exact Hankel computations are saved in `workspace/agent3_O.py`; 843 coefficient vectors were checked against the derived closed formula. All results and proof details have been posted to the team.

# agent_4: last reply

Put
\[
s=1+\max\{j:b_j\ne0\}.
\]
Then the answer is
\[
\boxed{\Delta_b=1-s=-\max\{j:b_j\ne0\}.}
\]

The coefficient dependence is therefore determined by the **last**, not the first, nonzero component.

My contribution is complete:

- Established finite Laurent Čech matrices with rigorous safe pole bounds.
- Implemented actual transition expansions and exact rational sparse rank computations in `workspace/agent4_laurent_matrix.py`.
- Checked all three cohomology dimensions against the resulting closed formulas for 23 coefficient vectors through genus \(7\), with additional modular computations through genus \(16\).
- Verified the scalar comparison
  \[
  h^1(V)=h^1(\mathcal O)-1+s,\qquad
  h^1(\pi^*T_C)=h^1(L),
  \]
  including the parity argument excluding higher differentials.
- Together with the proved vanishing of the connecting homomorphism for
  \[
  0\to V\to S\to\pi^*T_C\to0,
  \]
  these identities yield \(\Delta_b=1-s\).

No remaining proof gap identified.