# agent_1: last reply

Put
\[
a_n=\frac{n(n-2)}{n+2}.
\]
Then the answer is
\[
\boxed{\mathcal E_n=\{\,\beta\in2\mathbb N:\ \beta<a_n\,\}.}
\]
Equivalently,
\[
\boxed{\mathcal E_n
=\left\{2k:1\le k\le
\max\left(1,\left\lfloor\frac{n-4}{2}\right\rfloor\right)\right\}.}
\]
Thus the first few sets are
\[
\begin{array}{c|c}
n&\mathcal E_n\\ \hline
5,6,7&\{2\}\\
8,9&\{2,4\}\\
10,11&\{2,4,6\}\\
12,13&\{2,4,6,8\}.
\end{array}
\]

We prove both directions. The nonexistence argument does not actually require the scalar-curvature assumption. For the other direction, our counterexamples will be flat tori, so they satisfy that assumption.

Throughout, write
\[
p=\frac{2n}{n-2},\qquad q=p-1=\frac{n+2}{n-2},
\qquad h=-f_0.
\]
Thus the equation is
\[
-\Delta_g u=(\lambda-h)u^q. \tag{1}
\]

## 1. Nonexistence when \(\beta<a_n\)

Here \(h\ge0\), its only zero is \(P\), and near \(P\),
\[
h(x)=Q_\beta(x)+O(|x|^{\beta+1}).
\]
Positivity and homogeneity of \(Q_\beta\) give, in a sufficiently small coordinate ball,
\[
c|x|^\beta\le h(x)\le C|x|^\beta,
\qquad x\cdot\nabla h(x)\ge c h(x). \tag{2}
\]
The derivative estimate follows from the smooth Taylor expansion and
\(x\cdot\nabla Q_\beta=\beta Q_\beta\).

Most importantly,
\[
H:=\int_M h^{-q}\,dV_g<\infty
\quad\Longleftrightarrow\quad
\beta q<n.
\]
Our hypothesis \(\beta<a_n=n/q\) therefore implies \(H<\infty\).

Suppose \(u>0\) solves (1). Define
\[
A=\int_M h u^p\,dV_g,\qquad
J=\int_M h u^q\,dV_g.
\]
Integrating (1) gives
\[
J=\lambda\int_M u^q\,dV_g. \tag{3}
\]
In particular, \(J>0\).

All constants below may depend on the fixed data, but not on \(u\) or sufficiently small \(\lambda\).

### 1.1. Uniform estimates away from \(P\)

On any fixed compact subset of \(M\setminus\{P\}\), for sufficiently small \(\lambda\),
\[
\Delta_g u=(h-\lambda)u^q\ge c u^q.
\]
Consequently, \(u\) is uniformly bounded on every smaller compact subset.

For completeness, this is the elementary local Keller–Osserman estimate. In a sufficiently small geodesic ball, take
\[
W(x)=C(R^2-d(x,x_0)^2)^{-2/(q-1)}.
\]
For sufficiently large \(C\),
\(\Delta_g W\le cW^q\), while \(W\to\infty\) at the boundary. An interior positive maximum of \(u-W\) contradicts
\(\Delta_g(u-W)\ge c(u^q-W^q)>0\).
Local elliptic estimates then bound \(\nabla u\) away from \(P\).

### 1.2. A first Pohozaev estimate

Choose a fixed small Euclidean coordinate ball \(B_r\) on which (2) holds. The critical Pohozaev identity is
\[
-\frac1p\int_{B_r}(x\cdot\nabla h)u^p\,dx
=
\int_{\partial B_r}
\left[
r(\partial_\nu u)^2-\frac r2|\nabla u|^2
+\frac{n-2}{2}u\partial_\nu u
+\frac r p(\lambda-h)u^p
\right]d\sigma. \tag{4}
\]
Indeed, it follows by taking the divergence of
\[
(x\cdot\nabla u)\nabla u-\frac{x}{2}|\nabla u|^2
+\frac{n-2}{2}u\nabla u+\frac{x}{p}(\lambda-h)u^p;
\]
the undifferentiated nonlinear terms cancel because \(n/p=(n-2)/2\).

The bounds away from \(P\) control the right side of (4). Using (2), and controlling the integral outside \(B_r\) by the same exterior bound, gives
\[
A\le C. \tag{5}
\]

Weighted Hölder gives
\[
\begin{aligned}
\int_M u^q\,dV_g
&=\int_M (hu^p)^{q/p}h^{-q/p}\,dV_g\\
&\le A^{q/p}H^{1/p}.
\end{aligned} \tag{6}
\]
Together with (3) and (5), this proves
\[
J\le C\lambda. \tag{7}
\]

### 1.3. Sharpening the boundary estimates

On a fixed region away from \(P\), \(u\) is subharmonic. The local mean-value estimate for nonnegative subharmonic functions, together with \(h\ge c>0\) there, gives
\[
u\le C J^{1/q}
\quad\text{away from }P. \tag{8}
\]

We also claim the stronger derivative estimate
\[
|\nabla u|\le CJ
\quad\text{on }\partial B_r. \tag{9}
\]
To prove it, let \(G\) be the normalized Green function of \(-\Delta_g\). From (3),
\[
\int_M |(\lambda-h)u^q|\,dV_g
\le\lambda\int_Mu^q+\int_Mhu^q=2J. \tag{10}
\]
In the Green representation for \(\nabla u(x)\), \(x\in\partial B_r\), split the integration into \(B_{r/2}\) and its complement.

* On \(B_{r/2}\), the kernel is bounded, so (10) gives a bound \(CJ\).
* On the complement, (8) gives
  \(\lvert(\lambda-h)u^q\rvert\le CJ\). The Green-gradient estimate
  \[
  |\nabla_xG(x,y)|\le C\,d_g(x,y)^{1-n}
  \]
  has uniformly bounded integral in \(y\), again giving \(CJ\).

This proves (9).

Apply (8)–(9) in (4). Its boundary terms are bounded by
\[
C\left(J^2+J^{1+1/q}+J^{p/q}\right).
\]
Since \(p=q+1\), and \(1<p/q<2\), (7) allows us to assume \(J\le1\), and hence all these terms are bounded by \(CJ^{p/q}\). Outside \(B_r\), (8) gives the same bound for \(\int hu^p\). We conclude that
\[
A\le CJ^{p/q}. \tag{11}
\]

Finally, (3), (6), and (11) imply
\[
J\le \lambda H^{1/p}A^{q/p}\le C\lambda J.
\]
Since \(J>0\), this is impossible when \(\lambda\) is sufficiently small.

Therefore
\[
\boxed{\beta<a_n\implies\beta\in\mathcal E_n.} \tag{12}
\]

## 2. A variational existence criterion

We will use the following standard critical-exponent minimization argument, including its compactness proof.

Let \(F\in C^\infty(M)\) satisfy
\[
\max_M F=L>0,\qquad \int_M F\,dV_g<0.
\]
Let \(S_n\) be the sharp Euclidean Sobolev constant:
\[
S_n=\inf_{0\ne v\in C_c^\infty(\mathbb R^n)}
\frac{\int_{\mathbb R^n}|\nabla v|^2}
{\left(\int_{\mathbb R^n}|v|^p\right)^{2/p}}.
\]
Define
\[
I_F=\inf_{\int_MF|v|^p>0}
\frac{\int_M|\nabla v|^2\,dV_g}
{\left(\int_MF|v|^p\,dV_g\right)^{2/p}}. \tag{13}
\]

We claim
\[
0<I_F<S_nL^{-2/p}
\quad\Longrightarrow\quad
-\Delta_g u=Fu^q
\text{ has a smooth positive solution}. \tag{14}
\]

Here are the details.

Normalize a nonnegative minimizing sequence by
\(\int Fv_k^p=1\). It is bounded in \(H^1(M)\). Otherwise, since its gradients are bounded, its averages would tend to infinity. Dividing by those averages would give convergence to \(1\) in \(H^1\), hence in \(L^p\), contradicting \(\int F<0\).

The same observation shows \(I_F>0\): if the energies tended to zero, a subsequence would converge in \(H^1\) to a constant, again contradicting the constraint and \(\int F<0\).

After taking a subsequence, write
\[
v_k\rightharpoonup v\quad\text{in }H^1,\qquad
b=\lim_k\int_M|v_k-v|^p.
\]
The local sharp Sobolev inequality and strong \(L^2\) convergence give
\[
I_F\ge \int_M|\nabla v|^2+S_nb^{2/p}. \tag{15}
\]
Set \(D=\int_MFv^p\). The Brezis–Lieb splitting gives
\[
1-D=\lim_k\int_MF|v_k-v|^p\le Lb. \tag{16}
\]

If \(D\le0\), (15)–(16) contradict \(I_F<S_nL^{-2/p}\).

If \(0<D<1\), then
\[
\begin{aligned}
I_F
&\ge I_FD^{2/p}+S_nL^{-2/p}(1-D)^{2/p}\\
&>I_F\bigl(D^{2/p}+(1-D)^{2/p}\bigr)>I_F,
\end{aligned}
\]
another contradiction.

If \(D\ge1\), (15) and
\(\int|\nabla v|^2\ge I_FD^{2/p}\) force \(D=1\) and \(b=0\).
Thus the infimum is attained.

The Euler–Lagrange equation is
\[
-\Delta_g v=I_FFv^q.
\]
Critical elliptic regularity gives a bounded, then smooth, solution; one may obtain the initial higher integrability by the usual truncated-power test, absorbing the tail of
\(Fv^{p-2}\in L^{n/2}\).
The strong maximum principle gives \(v>0\). Finally,
\[
u=I_F^{1/(q-1)}v
\]
solves the required equation. This proves (14).

## 3. Counterexamples when \(\beta>a_n\)

Take a flat \(n\)-torus \(T^n\). Choose a smooth function \(h\) such that
\[
h(x)=|x|^\beta
\quad\text{near }P,\qquad
h>0\quad\text{on }T^n\setminus\{P\}.
\]
Such an \(h\) exists because \(\beta\) is even: \(|x|^\beta\) is a polynomial, and we can smoothly interpolate to a positive constant outside a coordinate ball.

Set \(f_0=-h\). These data satisfy every assumption in the question, with
\[
Q_\beta(x)=(x_1^2+\cdots+x_n^2)^{\beta/2}.
\]

Fix any
\[
0<\lambda<\frac1{\operatorname{Vol}(T^n)}
\int_{T^n}h\,dV.
\]
Then
\[
F=\lambda-h,\qquad \max F=\lambda,\qquad \int F<0.
\]
We will prove
\[
I_F<S_n\lambda^{-2/p}. \tag{17}
\]

### 3.1. Bubble estimates

Put \(s=(n-2)/2\), and take a cutoff \(\chi\), supported where \(h=|x|^\beta\), with \(\chi=1\) near \(P\). Define
\[
v_\delta(x)=\chi(x)
\left(\frac{\delta}{\delta^2+|x|^2}\right)^s.
\]
Let
\[
U(x)=(1+|x|^2)^{-s},\qquad
A_0=\int_{\mathbb R^n}U^p,\qquad
B_0=\int_{\mathbb R^n}U^q,
\]
and
\[
E_0=\int_{\mathbb R^n}|\nabla U|^2.
\]
The sharp Sobolev inequality, attained by \(U\), says
\[
E_0=S_nA_0^{2/p}. \tag{18}
\]

Direct radial integration gives
\[
\int|\nabla v_\delta|^2=E_0+O(\delta^{n-2}), \tag{19}
\]
\[
\int v_\delta^p=A_0+O(\delta^n), \qquad
\int v_\delta^q=B_0\delta^s+O(\delta^{s+2}). \tag{20}
\]
Writing \(b=\min(\beta,n)\), it also gives
\[
\int h v_\delta^p
=O\!\left(\delta^b(1+|\log\delta|)\right), \tag{21}
\]
where the logarithm is needed only if \(\beta=n\).

Since \(\beta>a_n>2\),
\[
\int h v_\delta^q=O(\delta^{s+2}),\qquad
\int h v_\delta^{p-2}=O(\delta^2). \tag{22}
\]
For example, the first estimate in (22) reduces to the integrability near zero of \(r^{\beta-3}\), and the second to that of \(r^{n+\beta-5}\).

Consequently, for our fixed \(\lambda\),
\[
\int Fv_\delta^p
=\lambda A_0-
O\!\left(\delta^b(1+|\log\delta|)\right), \tag{23}
\]
and
\[
\int Fv_\delta^q
=\lambda B_0\delta^s+O(\delta^{s+2}). \tag{24}
\]

### 3.2. Adding a small positive constant

For \(z,t\ge0\) and \(p>2\),
\[
0\le(z+t)^p-z^p-pz^{p-1}t
\le C_p(z^{p-2}t^2+t^p).
\]
Apply the lower inequality to the \(\lambda\)-part of \(F\), and the upper inequality to its \(-h\)-part. Then
\[
\begin{aligned}
\int F(v_\delta+t)^p
\ge{}&\int Fv_\delta^p
+pt\int Fv_\delta^q\\
&-Ct^2\int hv_\delta^{p-2}
-Ct^p. \tag{25}
\end{aligned}
\]

Choose
\[
t=\eta(\lambda\delta^s)^{1/q},
\]
where \(\eta>0\) is a sufficiently small fixed number. The main positive term in (25) is
\[
pB_0\eta(\lambda\delta^s)^{p/q},
\]
whereas \(Ct^p=C\eta^p(\lambda\delta^s)^{p/q}\). Thus the latter is absorbed by choosing \(\eta\) small.

Now
\[
\frac{sp}{q}=\frac{n(n-2)}{n+2}=a_n.
\]
The remaining errors are of smaller order than \(\delta^{a_n}\), because
\[
b>a_n,\qquad n-2>a_n,
\]
and
\[
2+\frac{2s}{q}-a_n
=\frac8{n+2}>0.
\]
Using (22)–(25), for sufficiently small \(\delta\),
\[
\int F(v_\delta+t)^p
\ge \lambda A_0+c_\lambda\delta^{a_n},
\qquad c_\lambda>0. \tag{26}
\]

Adding a constant does not change the energy:
\[
\int|\nabla(v_\delta+t)|^2
=E_0+O(\delta^{n-2}). \tag{27}
\]
Because \(a_n<n-2\), equations (18), (26), and (27) imply
\[
\frac{\int|\nabla(v_\delta+t)|^2}
{\left(\int F(v_\delta+t)^p\right)^{2/p}}
<
\frac{E_0}{(\lambda A_0)^{2/p}}
=S_n\lambda^{-2/p}
\]
for small enough \(\delta\). This is (17).

The criterion in Section 2 now produces a smooth positive solution for every
\[
0<\lambda<\frac{\int h}{\operatorname{Vol}(T^n)}.
\]
In particular, these fixed data have positive solutions for arbitrarily small \(\lambda\). Therefore
\[
\boxed{\beta>a_n\implies\beta\notin\mathcal E_n.} \tag{28}
\]

## 4. There is no even-integer borderline

We have
\[
a_n=n-4+\frac8{n+2}.
\]
If \(a_n\) is an integer, then \(n+2\mid8\). For \(n\ge5\), the only possibility is \(n=6\), giving \(a_6=3\), which is odd.

Thus no allowed \(\beta\) equals \(a_n\). Equations (12) and (28) settle every case.

## 5. Executed Python checks

The proof above is analytic; finite numerical tests cannot replace its universal arguments. The following code checks the symbolic cancellations and exponents used in it, independently evaluates the bubble integrals by quadrature, and checks the stated classification over a substantial range. I executed these checks successfully.

```python
import sympy as sp
import mpmath as mp

n = sp.symbols("n", positive=True)
p = 2*n/(n-2)
q = (n+2)/(n-2)
s = (n-2)/2
a = n*(n-2)/(n+2)

# Symbolic identities used in both halves of the proof.
identities = {
    "p = q+1": p-q-1,
    "Holder threshold": n/q-a,
    "critical Pohozaev cancellation": n/p-(n-2)/2,
    "KO barrier exponent": s*q-s-2,
    "bubble gain exponent": s*p/q-a,
    "cutoff error exponent":
        (n-2-a)-2*(n-2)/(n+2),
    "mixed remainder exponent":
        (2+s*(2-p)/q)-8/(n+2),
    "2 - p/q": (2-p/q)-4/(n+2),
    "integer-borderline identity":
        a-(n-4+8/(n+2)),
}
for name, expression in identities.items():
    assert sp.factor(expression) == 0, name

# a_n > 2 for every n >= 5:
# substitute n=m+5 into the numerator of a_n-2.
m = sp.symbols("m", nonnegative=True)
assert sp.expand(
    (n*n-4*n-4).subs(n, m+5)
) == m*m + 6*m + 1

# Radial powers in the weighted bubble estimates.
beta = sp.symbols("beta", positive=True)
radial_identities = {
    "h*v^q outer power":
        n-1+beta-2*s*q-(beta-3),
    "h*v^(p-2) outer power":
        n-1+beta-2*s*(p-2)-(n+beta-5),
    "v^q inner scaling": n-s*q-s,
    "v^(p-2) numerator power": s*(p-2)-2,
}
for name, expression in radial_identities.items():
    assert sp.factor(expression) == 0, name

print("All symbolic exponent and cancellation checks passed.")

# Independent numerical evaluation of the Euclidean bubble constants.
# Substitute r=tan(theta), so the integrals have finite intervals.
mp.mp.dps = 45
for N in range(5, 16):
    half = mp.mpf(N)/2
    omega = 2*mp.pi**half/mp.gamma(half)
    intervals = [0, mp.pi/4, mp.pi/2]

    A = omega * mp.quad(
        lambda z: mp.sin(z)**(N-1)*mp.cos(z)**(N-1),
        intervals
    )
    B = omega * mp.quad(
        lambda z: mp.sin(z)**(N-1)*mp.cos(z),
        intervals
    )
    E = omega*(N-2)**2 * mp.quad(
        lambda z: mp.sin(z)**(N+1)*mp.cos(z)**(N-3),
        intervals
    )

    A_exact = mp.pi**half * mp.gamma(half)/mp.gamma(N)
    B_exact = mp.pi**half/mp.gamma(mp.mpf(N+2)/2)

    assert abs(A/A_exact-1) < mp.mpf("1e-38")
    assert abs(B/B_exact-1) < mp.mpf("1e-38")
    assert abs(E/(N*(N-2)*A)-1) < mp.mpf("1e-38")

print("Bubble integrals checked independently for n=5,...,15.")

# The only possible integral borderline:
borderlines = []
for d in sp.divisors(8):
    N = d-2
    if N >= 5:
        borderlines.append((N, N-4+8//d))
assert borderlines == [(6, 3)]
assert all(B % 2 != 0 for N, B in borderlines)

# Diagnostic classification checks; the proof covers all n.
for N in range(5, 201):
    Acrit = sp.Rational(N*(N-2), N+2)
    K = max(1, (N-4)//2)

    assert 2 < Acrit < N-2
    for B in range(2, 2*N+1, 2):
        assert (B < Acrit) == (B <= 2*K)
        assert B != Acrit
        if B > Acrit:
            assert B > 2
            assert min(B, N) > Acrit

print("Classification and strict inequalities checked through n=200.")

for N in range(5, 14):
    K = max(1, (N-4)//2)
    print(N, list(range(2, 2*K+1, 2)))
```

The output confirms all assertions and gives the sets displayed at the start.

**What is proved:** the exact set \(\mathcal E_n\), nonexistence for every admissible datum in the listed cases, and explicit admissible counterexample data for every omitted even integer. **Nothing remains unresolved.**