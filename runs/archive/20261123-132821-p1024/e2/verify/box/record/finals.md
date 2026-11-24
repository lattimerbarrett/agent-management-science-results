# agent_1: last reply

Put
\[
m=\max\{j:b_j\ne0\}.
\]
We prove that
\[
\boxed{\Delta_b=-m}.
\]

The proof uses a relative divergence operator. It cancels almost all the cohomology calculations, leaving one obstruction map whose matrix is anti-triangular with anti-diagonal \(b_m\).

## 1. Cohomological preliminaries

Write \(C=C_g\), \(\phi=\phi_b\), and
\[
d=2g-2,\qquad \pi:X_b\longrightarrow C.
\]
The projection \(\pi\) exists because the gluing preserves the base.

The Weierstrass semigroup at \(p\) is
\[
\langle 2,2g+1\rangle,
\]
so its gaps are \(1,3,\ldots,2g-1\). Consequently,
\[
H^1(C,\mathcal O_C(np))
=\bigoplus_{\substack{q\in\{1,3,\ldots,2g-1\}\\q>n}}
\mathbb C[t^{-q}].                                      \tag{1}
\]
Also \(dx/z\) has divisor \(dp\), and hence
\[
T_C\simeq\mathcal O_C(-dp).                              \tag{2}
\]

Here are the elementary bounds that will be used:
\[
k<d,\qquad k\ge 2r-2,\qquad 3k\ge d,\qquad 4k>d,          \tag{3}
\]
where \(3k=d\) occurs precisely when \(g\equiv1\pmod3\).

All calculations below can be made on finite infinitesimal neighborhoods of \(E\). Indeed, the associated graded sheaves for the \(E\)-adic filtration are
\[
\begin{array}{c|c}
\mathcal F&\operatorname{gr}_n\mathcal F\\ \hline
\mathcal O_X,\ \Theta_{X/C}(-E)&\mathcal O_C(np)\\
\pi^*T_C,\ L_b&T_C(np).
\end{array}                                             \tag{4}
\]
Thus \(H^1\) of the tails vanishes starting at \(n=d+1\) in the first row and at \(n=2d+1\) in the second.

For completeness, this also justifies passing from the formal calculation to the analytic surface in the question. The contraction is proper over a Stein representative, its higher direct images are supported at \(0\), and formal functions identifies their completions with the inverse limits of the cohomologies of infinitesimal neighborhoods. The exceptional-adic and pulled-back maximal-ideal-adic filtrations are cofinal. By (4), the relevant inverse systems stabilize. Thus the stabilized finite-neighborhood calculations give exactly the analytic \(H^1(X_b,\mathcal F)\).

## 2. The logarithmic tangent sequence

Let
\[
\mathcal A=\Theta_{X/C}(-E),\qquad \mathcal T=\pi^*T_C.
\]
There is an exact sequence
\[
0\longrightarrow\mathcal A\longrightarrow S_b
 \longrightarrow\mathcal T\longrightarrow0,             \tag{5}
\]
and
\[
L_b=\mathcal A\otimes\mathcal T.                         \tag{6}
\]

Set \(u=y_U\), \(v=y_W\), and
\[
A=1-k\phi(t)t^kv^k.
\]
The inverse fiber transformation and the vertical logarithmic frames satisfy
\[
u=tvA^{-1/k},\qquad
u\frac{\partial}{\partial u}
=A\,v\frac{\partial}{\partial v}.                        \tag{7}
\]

We first show that the connecting homomorphism
\[
H^0(X,\mathcal T)\longrightarrow H^1(X,\mathcal A)        \tag{8}
\]
is zero.

By (2), a section of \(\mathcal T\) has \(E\)-order at least \(d\). If its order were exactly \(d\), its leading coefficient would be a nonzero constant in
\[
H^0(C,T_C(dp))=\mathbb C.
\]
The fiber transformation shows that its first obstruction, at order \(d+k\), is that constant times
\[
d[\phi]\in H^1(C,\mathcal O_C(kp)).                       \tag{9}
\]
This class is nonzero: every pole occurring in \(\phi\) is a gap, and the smallest possible one is
\[
2g-1-2(r-1)=2k+1>k.
\]
Thus every global section of \(\mathcal T\) vanishes to order at least \(d+1\). Since
\[
H^1(X,\mathcal A(-(d+1)E))=0,
\]
every such section lifts in (5). Hence (8) is zero, and
\[
h^1(S_b)=h^1(\mathcal A)+h^1(\mathcal T).                 \tag{10}
\]

It remains to prove
\[
h^1(\mathcal O_X)-h^1(\mathcal A)=-m,
\qquad
h^1(L_b)=h^1(\mathcal T).                               \tag{11}
\]

## 3. Relative divergence and cancellation

Consider the relative meromorphic differentials
\[
\alpha_U=\frac{du}{u^{k+1}},\qquad
\alpha_W=\frac{dv}{v^{k+1}}.
\]
Direct differentiation of the gluing gives
\[
\alpha_W=t^k\alpha_U.                                   \tag{12}
\]
Because the multiplier depends only on the base, relative divergence defines a globally well-defined, base-linear operator
\[
D:\mathcal A\longrightarrow\mathcal O_X.
\]
Locally,
\[
D\left(f(u)\,u\frac{\partial}{\partial u}\right)
=u f'(u)-kf(u).                                         \tag{13}
\]
In particular, on degree \(n\), \(D\) is multiplication by \(n-k\).

The action \(u\mapsto\zeta u\), \(\zeta^k=1\), is compatible with the gluing. Decompose into its eigenspaces. On every nontrivial eigenspace, \(n-k\ne0\), so \(D\) is an isomorphism. These eigenspaces therefore cancel in the differences in (11).

We need only the invariant part, with degrees
\[
0,k,2k,\ldots.
\]
All the following decompositions may be performed on finite thickenings, so they are decompositions of coherent \(\mathcal O_C\)-modules.

Let \(Q_1\) be the invariant function tail beginning in degree \(k\), and \(Q_2\) the one beginning in degree \(2k\). Then
\[
(\mathcal O_X)^{\mu_k}=\mathcal O_C\oplus Q_1,\qquad
0\longrightarrow Q_2\longrightarrow Q_1
 \longrightarrow\mathcal O_C(kp)\longrightarrow0.        \tag{14}
\]

For \(\mathcal A\), formula (7) gives the exact identities
\[
e_U=(1-k\phi t^kv^k)e_W,\qquad
u^ke_U=t^kv^ke_W,                                       \tag{15}
\]
where \(e_U=u\partial_u\), \(e_W=v\partial_v\).
Thus degrees \(0,k\) form a rank-two bundle \(B\), and
\[
\mathcal A^{\mu_k}=B\oplus R,\qquad D:R\xrightarrow{\sim}Q_2.
\]
Moreover,
\[
0\longrightarrow\mathcal O_C(kp)\longrightarrow B
 \longrightarrow\mathcal O_C\longrightarrow0             \tag{16}
\]
has extension class \(-k[\phi]\).

That extension class is nonzero, by (1). Therefore its connecting map from \(H^0(\mathcal O_C)=\mathbb C\) has rank one, giving
\[
h^1(B)=h^1(\mathcal O_C)+h^1(\mathcal O_C(kp))-1.         \tag{17}
\]

Let
\[
\rho:H^0(C,\mathcal O_C(kp))\longrightarrow H^1(C,Q_2)
\]
be the connecting map in (14), and put \(R_\rho=\operatorname{rank}\rho\).
The same exact sequence gives
\[
h^1(Q_1)=h^1(Q_2)+h^1(\mathcal O_C(kp))-R_\rho.
\]
Combining this with (17) and the cancellation above,
\[
h^1(\mathcal O_X)-h^1(\mathcal A)=1-R_\rho.              \tag{18}
\]

There is also an immediate consequence after tensoring all these sequences with \(T_C\). Since \(k<d\),
\[
H^0(C,T_C)=H^0(C,T_C(kp))=0.
\]
Both connecting-map ranks then vanish. The same cancellation proves
\[
h^1(\mathcal A\otimes\mathcal T)=h^1(\mathcal T).         \tag{19}
\]

Thus only \(R_\rho\) remains to be calculated.

## 4. The remaining obstruction has rank \(m+1\)

A basis of \(H^0(C,\mathcal O_C(kp))\) is
\[
1,x,\ldots,x^{\lfloor k/2\rfloor}.
\]
The first component of \(\rho\), in degree \(2k\), is a nonzero scalar multiple of
\[
f\longmapsto[\phi f]\in H^1(C,\mathcal O_C(2kp)).        \tag{20}
\]

The gaps greater than \(2k\) are exactly
\[
q_j=2g-1-2j,\qquad 0\le j<r.
\]
For the source vector \(x^a=t^{-2a}\), the coefficient of \(t^{-q_j}\) in \(\phi x^a\) is
\[
M_{j,a}=b_{j+a},                                        \tag{21}
\]
where \(b_\ell=0\) for \(\ell>m\).

Because \(k\ge2r-2\), the matrix contains its first \(m+1\) columns. Its first \((m+1)\)-square block is anti-triangular, with anti-diagonal \(b_m\), so
\[
\det(M_{j,a})_{0\le j,a\le m}
=(-1)^{m(m+1)/2}b_m^{m+1}\ne0.                          \tag{22}
\]
Every column \(a>m\) vanishes. Hence the first obstruction has rank \(m+1\), and its kernel is exactly
\[
\operatorname{span}\{x^a:m<a\le\lfloor k/2\rfloor\}.     \tag{23}
\]

We must check that this kernel has no later obstruction.

For \(a>m\), every term of \(\phi x^a\) has odd pole
\[
2g-1-2j+2a=2g+1+2(a-j-1).
\]
Its principal part is therefore removed by an odd function
\[
z\,x^{a-j-1}.
\]
The difference is holomorphic at \(p\): using
\[
z=t^{-(2g+1)}\bigl(1-t^{4g+2}\bigr)^{1/2},
\]
its first possible exponent is
\[
4g+2-(2g-1-2j+2a)>0.
\]
Thus the first correction can be chosen odd under \(t\mapsto-t\).

The next obstruction, in degree \(3k\), is even: it consists of terms involving either \(\phi^2x^a\) or \(\phi\) times this odd correction. All classes in (1) are odd, so this obstruction vanishes.

Finally, \(3k\ge d\) and \(4k>d\). Therefore:
- if \(3k>d\), even the degree-\(3k\) target has zero \(H^1\);
- if \(3k=d\), the parity argument applies;
- every subsequent target has zero \(H^1\).

Consequently the full connecting map has exactly its first-obstruction rank:
\[
R_\rho=m+1.                                             \tag{24}
\]
Equation (18) now gives
\[
h^1(\mathcal O_X)-h^1(\mathcal A)=-m.
\]
Together with (10) and (19), this proves
\[
\boxed{\Delta_b=-m
=-\max\{j:b_j\ne0\}}.
\]

In particular, no condition on the lower coefficients \(b_0,\ldots,b_{m-1}\) was used.

## 5. Executable exact checks

The following Python checks the divergence intertwining identities, all numerical bounds and gap identifications used above, and the obstruction matrices with **symbolic lower coefficients**. It also checks the principal-part subtraction for every kernel monomial. It uses exact SymPy arithmetic, not floating-point ranks.

```python
import sympy as S

# Transition coefficients in degree n+ell*k:
# O: rising(n/k, ell)/ell!
# A: rising(n/k-1, ell)/ell!
n, k = S.symbols("n k", nonzero=True)
for ell in range(9):
    cO = S.prod(n/k + j for j in range(ell)) / S.factorial(ell)
    cA = S.prod(n/k - 1 + j for j in range(ell)) / S.factorial(ell)
    assert S.cancel((n + ell*k - k)*cA - (n-k)*cO) == 0

cases = 0
for g in range(2, 101):
    r = (g + 2)//3
    K = g-r
    d = 2*g-2

    assert K < d and K >= 2*r-2
    assert 3*K >= d and 4*K > d
    assert (3*K == d) == (g % 3 == 1)

    gaps = list(range(1, 2*g, 2))
    q = [2*g-1-2*j for j in range(r)]
    assert set(h for h in gaps if h > 2*K) == set(q)
    assert min(q) > K

    for m in range(r):
        b = S.symbols("b:" + str(m+1))
        H = S.Matrix(
            r, K//2+1,
            lambda j, a: b[j+a] if j+a <= m else 0
        )

        # Reverse the leading block's columns.
        # It is upper triangular with diagonal b_m.
        J = H[:m+1, :m+1][:, ::-1]
        assert all(J[i, i] == b[m] for i in range(m+1))
        assert all(
            J[i, j] == 0
            for i in range(m+1) for j in range(i)
        )

        # No rows/columns outside this block can increase the rank.
        assert all(
            H[j, a] == 0
            for j in range(r) for a in range(K//2+1)
            if j > m or a > m
        )

        # For every kernel monomial, verify its odd principal part
        # is that of z*x^Q and the remainder is holomorphic.
        for a in range(m+1, K//2+1):
            for j in range(m+1):
                pole = 2*g-1-2*j+2*a
                Q = a-j-1
                assert Q >= 0
                assert pole == 2*g+1+2*Q
                assert 4*g+2-pole > 0

        cases += 1

print("Symbolic divergence identities: 9")
print("All-coefficient symbolic cases:", cases)
```

Executed output:
```text
Symbolic divergence identities: 9
All-coefficient symbolic cases: 1716
```

As an independent check, we also computed the four cohomology dimensions directly from the full nonlinear Čech transitions using exact rational Gaussian elimination for every \(2\le g\le9\), every \(m\), and both sparse and non-sparse coefficient vectors—34 cases in total. Enlarging both the Laurent and fiber cutoffs left all four dimensions unchanged. These computations corroborate, rather than replace, the all-\(g\), all-coefficient proof above.

# agent_2: last reply

Completed the cohomological calculation:
\[
h^1(\mathcal O_{X_b})-h^1(A_b)=-m,
\qquad
h^1(L_b)=h^1(\pi^*T_{C_g}),
\]
where \(A_b\) is the vertical logarithmic tangent sheaf and \(m=\max\{j:b_j\ne0\}\).

The essential obstruction map has rank \(m+1\): its matrix is the Hankel matrix \((b_{a+\ell})\), whose relevant reversed square minor is triangular with diagonal \(b_m\). Higher obstructions vanish by parity and the degree cutoff.

Together with agent_3’s vanishing connecting homomorphism, this proves
\[
\boxed{\Delta_b=-m}.
\]

Exact symbolic checks, valid under arbitrary specialization of the lower coefficients, are saved in `workspace/agent2_resonance_check.py`; they passed all 1,716 pairs \((g,m)\) for \(2\le g\le100\). The complete argument and checks have been communicated to agent_1 for assembly.

# agent_3: last reply

My part is complete.

Set \(A=\Theta_{X_b/C_g}(-E)\) and \(T=\pi^*\Theta_{C_g}\). There is an exact sequence
\[
0\longrightarrow A\longrightarrow S_b\longrightarrow T\longrightarrow0,
\qquad L_b=A\otimes T.
\]
The vertical transition gives
\[
A(-kE)\simeq\pi^*\mathcal O_{C_g}(kp).
\]

For every nonzero \(b\), the connecting map \(H^0(T)\to H^1(A)\) is zero. Indeed, writing \(d=2g-2\), a section of \(T\) must vanish to order at least \(d\) along \(E\). A nonzero leading term of order \(d\) has first obstruction
\[
d[\phi_b]\in H^1(C_g,\mathcal O(kp)),
\]
which is nonzero: the distinct poles \(2g-1-2j\ge 2k+1\) are all Weierstrass gaps. Consequently every section vanishes to order at least \(d+1\), and
\[
H^1(X_b,A(-(d+1)E))=0
\]
makes it lift to \(S_b\). Hence
\[
h^1(S_b)=h^1(A)+h^1(T).
\]

Together with the team’s completed resonance calculation,
\[
h^1(\mathcal O_{X_b})-h^1(A)=-m,
\qquad h^1(L_b)=h^1(T),
\]
this proves \(\Delta_b=-m\).

The analytic justification uses formal functions and the cutoffs \(2g-1\) for \(\mathcal O,A\), and \(4g-3\) for \(T,L_b\). My executable checks are in `workspace/agent3_log_tangent_check.py`; all symbolic transition identities and the stated gap, cutoff, and Hankel checks passed. The full proof and independent exact Čech computations are complete; agent_1 is assembling the final presentation.

# agent_4: last reply

Verification is complete. The team’s proof establishes
\[
\boxed{\Delta_b=-\max\{j:b_j\ne0\}}.
\]

My independent checks include:

- Exact rational, full nonlinear Čech computations for every \(m\) and \(2\le g\le9\), using both sparse and dense coefficient vectors.
- Recomputations with enlarged Laurent and fiber cutoffs, with identical results.
- Universal symbolic Hankel pivot identities, retaining arbitrary lower coefficients.
- Additional finite-field checks through genus \(20\).

Runnable files are in `workspace/agent4_exact_cech.py` and `workspace/agent4_cech.py`. The lead agent is assembling the complete proof and executable verification into the final response.