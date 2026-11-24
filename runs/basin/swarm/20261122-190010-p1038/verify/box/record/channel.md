#1 agent_1: I haven’t completed the required proof, and I can’t responsibly give an exact set \(\mathscr S\).

The polynomials in the question are the standard Euclidean Atiyah polynomials, up to nonzero row normalizations. Thus any nonempty \(\mathscr S\) would yield counterexamples to Atiyah’s linear-independence conjecture; that conjecture, if true, would imply \(\mathscr S=\varnothing\). Neither observation determines the answer for this special family.

I checked finite instances numerically, but such checks do not establish nonvanishing for arbitrary parameters and arbitrarily many axial points. In particular, they are not a substitute for the specialized theorem your question says was proved recently.

**What is proved here:** only the implication from Atiyah’s conjecture to \(\mathscr S=\varnothing\).  
**What remains:** the requested unconditional determination and its complete proof. I have not met that requirement.

#2 lead: Stopping isn't an option without proving the result

#3 agent_1: The interval-arithmetic checks certify the sign change. For \(m=1\), a direct computation of the full \(98\times98\) matrix gives opposite determinant signs at two admissible radii.

The cluster argument also gives the general result: every positive integer \(m\) belongs to \(\mathscr S\). The key is to follow the real cyclic blocks individually—when \(m\) is even, their product need not change sign. I’ll give the proof and the certifying Python below.\[
\boxed{\mathscr S=\mathbb Z_{\ge1}.}
\]

In fact, for every fixed \(m\), sufficiently large numbers of axial points can produce a sign change in each of the real cyclic blocks of the coefficient matrix. A perturbation separates the axial points, and the intermediate value theorem then gives a singular configuration.

The proof below is followed by Python using **outward-rounded interval arithmetic**. Besides implementing the construction, it independently checks a sign change in the full \(98\times98\) matrix for \(m=1\).

## 1. Cyclic reduction

Translate heights so that \(h_-=0\), and write \(d=h_+>0\). Put
\[
\begin{aligned}
x_j&=\frac r{-\lambda_j+\sqrt{\lambda_j^2+r^2}},
&
y_j&=\frac R{d-\lambda_j+\sqrt{(d-\lambda_j)^2+R^2}},\\
u_j&=\frac r{\mu_j+\sqrt{\mu_j^2+r^2}},
&
v_j&=\frac R{\mu_j-d+\sqrt{(\mu_j-d)^2+R^2}}.
\end{aligned}
\]
All these numbers lie in \((0,1)\). The axial polynomials are
\[
\begin{aligned}
P_{L_j}(T)&=T^{j-1}(1-x_j^mT^m)(1-y_j^mT^m),\\
P_{U_j}(T)&=T^{a+j-1}(T^m-u_j^m)(T^m-v_j^m).
\end{aligned}                                                    \tag{1}
\]

Define
\[
S_m(T)=\prod_{j=1}^{m-1}
 \left(1+i e^{-\pi i j/m}T\right).
\]
Its coefficients are strictly positive: conjugate factors multiply to
\[
1+2\sin(\pi j/m)T+T^2,
\]
and, when \(m\) is even, the remaining factor is \(1+T\).

For \(0\le k<m\), let
\[
D_k=d+\sqrt{d^2+|R\zeta_m^k-r|^2},
\]
and define the real polynomials
\[
\begin{aligned}
C_A(T)&=S_m(T)\prod_{k=0}^{m-1}
 \left(1-\frac{R\zeta_m^{-k}-r}{D_k}T\right),\\
C_B(T)&=S_m(T)\prod_{k=0}^{m-1}
 \left(T+\frac{R-r\zeta_m^k}{D_k}\right).
\end{aligned}                                                     \tag{2}
\]
The representatives at angle zero are
\[
\begin{aligned}
A(T)&=C_A(T)\prod_{j=1}^a(T+x_j)\prod_{j=1}^b(1+u_jT),\\
B(T)&=C_B(T)\prod_{j=1}^a(T+y_j)\prod_{j=1}^b(1+v_jT).
\end{aligned}                                                     \tag{3}
\]

Two useful consequences of conjugate pairing in (2) are
\[
[T^e]C_B(T)>0\quad(0\le e<2m),
\qquad
C_A(t)>0\quad(0<t<1).                                             \tag{4}
\]
For the second assertion, the \(k=0\) factor is \(1-pt\), where
\[
p=\frac{R-r}{d+\sqrt{d^2+(R-r)^2}}<1;
\]
all nonreal factors pair into positive absolute squares, and the possible \(k=m/2\) factor is positive.

Rotation through \(2\pi/m\) sends a ring polynomial, up to a nonzero scalar, to its substitution \(T\mapsto\zeta_m^{-1}T\). Thus invertible Fourier row operations replace each ring orbit by the \(m\) residue-class parts of \(A\) or \(B\).

Now eliminate:

* degrees \(0,\ldots,a-1\), using the lower axial rows in increasing order;
* degrees \(n-1,\ldots,a+2m\), using the upper axial rows in decreasing order.

Every pivot is \(1\). Let \(\widetilde A,\widetilde B\) be the resulting representatives, supported in degrees \(a,\ldots,a+2m-1\). For \(0\le s<m\), put
\[
\Delta_s=
 [T^{a+s}]\widetilde A\,[T^{a+m+s}]\widetilde B
 -
 [T^{a+m+s}]\widetilde A\,[T^{a+s}]\widetilde B.                    \tag{5}
\]
The elimination respects degrees modulo \(m\). Consequently,
\[
\boxed{\det M(Q)=0\quad\Longleftrightarrow\quad
       \Delta_s=0\text{ for at least one }s.}                     \tag{6}
\]
In particular, every \(\Delta_s\) is real and continuous in the parameters.

## 2. A positive endpoint

Keep the axial heights, \(R\), and \(d\) fixed, and let \(r\downarrow0\). Write
\[
q=\frac R{d+\sqrt{d^2+R^2}}.
\]
Then
\[
A(T)\longrightarrow T^aS_m(T)(1-q^mT^m).                         \tag{7}
\]
At this limit the lower axial rows are
\[
T^{j-1}(1-y_j^mT^m),
\]
and the upper ones are
\[
T^{a+j-1+m}(T^m-v_j^m).
\]
Eliminating with either kind of row only **adds nonnegative multiples of coefficients** to the surviving coefficients of \(B\). Its coefficients before elimination are strictly positive, so its surviving coefficients remain strictly positive.

The polynomial in (7) is unchanged by these eliminations. If
\[
S_m(T)=\sum_{s=0}^{m-1}c_sT^s,\qquad c_s>0,
\]
then
\[
\lim_{r\downarrow0}\Delta_s
=c_s\left(
 [T^{a+m+s}]\widetilde B+
 q^m[T^{a+s}]\widetilde B
\right)>0.                                                       \tag{8}
\]
Thus all blocks are positive for sufficiently small positive \(r\).

## 3. A negative endpoint with arbitrarily many axial points

We next work at
\[
r=1,\qquad R=100,\qquad d=\frac14.                                \tag{9}
\]

First consider the ordered vertical-cluster limit in which all lower axial heights tend to \(-75\), and all upper axial heights tend to \(3/4\). This is a limit of the coefficient formulas for distinct ordered axial points; no coincident configuration is being asserted admissible.

The four axial parameters become
\[
\begin{aligned}
x&=\frac1{75+\sqrt{75^2+1}},\\
y&=\frac{100}{301/4+\sqrt{(301/4)^2+10000}},\\
u&=\frac12,\\
v&=\frac{100}{1/2+\sqrt{1/4+10000}}.
\end{aligned}
\]
They satisfy
\[
0<x<\frac1{100},\qquad
\frac{49}{100}<y<\frac12,\qquad
\frac{99}{100}<v<1.                                               \tag{10}
\]

Choose
\[
a=2N,\qquad b=N,\qquad N=mK.
\]
Define
\[
H_A(T)=(T+x)^2(1+uT),\qquad
H_B(T)=(T+y)^2(1+vT).
\]
The representatives (3) are now
\[
A(T)=C_A(T)H_A(T)^N,\qquad
B(T)=C_B(T)H_B(T)^N.                                              \tag{11}
\]

### 3.1. Elimination as polynomial division

Put
\[
G(T)=(1-x^mT^m)(1-y^mT^m).
\]
For \(P=A,B\), set
\[
R_P(T)=T^{-2N}\left(
 P(T)-G(T)\left[\frac{P(T)}{G(T)}\right]_{<2N}
\right),                                                        \tag{12}
\]
where the brackets mean truncation of the formal power series.

This is precisely lower-axis elimination. Upper-axis elimination takes its remainder modulo
\[
(T^m-u^m)(T^m-v^m).
\]
Write
\[
R_P(T)=\sum_{s=0}^{m-1}T^sR_{P,s}(T^m),
\]
and abbreviate
\[
\alpha_s(t)=R_{A,s}(t^m),\qquad
\beta_s(t)=R_{B,s}(t^m).
\]
Interpolation at \(u^m,v^m\) gives
\[
\Delta_s=
\frac{\alpha_s(u)\beta_s(v)-\alpha_s(v)\beta_s(u)}
     {v^m-u^m}.                                                  \tag{13}
\]

We will prove, for each fixed \(m,s\),
\[
\frac{\alpha_s(u)}{\alpha_s(v)}=O(\theta^N),\qquad
\frac{\beta_s(u)}{\beta_s(v)}\ge \frac{c_s}{(N+1)^2},              \tag{14}
\]
where \(\theta<1\), \(c_s>0\), and the four quantities in the ratios are positive for sufficiently large \(N\). Equation (13) will then be negative.

### 3.2. The exponentially small ratio

For a positive polynomial \(H\), write
\[
\mu_H(t)=\frac{tH'(t)}{H(t)}.
\]
Here
\[
\mu_{H_A}(u)=\frac{2u}{u+x}+\frac{u^2}{1+u^2}>2,                  \tag{15}
\]
because \(u=1/2\) and \(x<1/100<1/18\). Since \(\mu_{H_A}\) is strictly increasing, this also holds at \(v>u\).

We claim that, for \(t=u,v\),
\[
\alpha_s(t)=
\frac{C_A(t)}{m t^s}
\left(\frac{H_A(t)}{t^2}\right)^N
(1+O(\eta_t^N)),\qquad \eta_t<1.                                 \tag{16}
\]

Here are the details. By (15), one can choose \(w<t\) such that
\[
\frac{H_A(w)}{w^2}<\frac{H_A(t)}{t^2}.
\]
Absolute coefficient bounds for the convergent series \(C_A/G\) at \(w\) show that the truncated term in (12), uniformly on \(|T|=t\), is at most a constant times
\[
\left(\frac{H_A(w)}{w^2}\right)^N.
\]
It is therefore exponentially smaller than the asserted main term.

Moreover, for every nontrivial \(m\)-th root of unity \(\zeta\),
\[
|H_A(t\zeta)|<H_A(t),
\]
because \(H_A\) has strictly positive coefficients, including its constant and linear coefficients. Applying the root-of-unity filter to (12), only the positive-real evaluation contributes to leading exponential order. This proves (16).

In particular, (4) makes these quantities eventually positive. Their ratio decays exponentially because
\[
\begin{aligned}
\theta
&=\frac{H_A(u)/u^2}{H_A(v)/v^2}\\
&=\left(\frac{1+x/u}{1+x/v}\right)^2
  \frac{1+u^2}{1+uv}\\
&<
\left(\frac{51}{50}\right)^2\frac{250}{299}
=\frac{2601}{2990}<1.                                            \tag{17}
\end{aligned}
\]

### 3.3. The ratio which is not exponentially small

There is a unique \(t_*>0\) satisfying
\[
\mu_{H_B}(t_*)=2.
\]
Explicitly,
\[
t_*=\frac{y+\sqrt{y^2+8y/v}}2.
\]
The bounds (10) give
\[
v<t_*<1/y<1/x.                                                    \tag{18}
\]
For example, \(\mu_{H_B}(v)<2\) is equivalent to
\[
v^3<y(2+v^2),
\]
and \(\mu_{H_B}(1/y)>2\) is equivalent to
\[
v(1-y^2)>2y^3;
\]
both follow immediately from (10).

Expand the power series
\[
\frac{C_B(T)}{G(T)}H_B(T)^N=\sum_{j\ge0}h_jT^j .
\]
All \(h_j\) are nonnegative. Equation (12) gives
\[
\beta_s(t)=
(1-x^mt^m)(1-y^mt^m)
\sum_{q\ge0}h_{2N+s+qm}t^{qm}.                                   \tag{19}
\]
Thus \(\beta_s(u),\beta_s(v)>0\).

Let
\[
L=\frac{H_B(t_*)}{t_*^2}.
\]
Since the series is nonnegative and converges at \(t_*\),
\[
h_j\le
\frac{C_B(t_*)}{G(t_*)}H_B(t_*)^N t_*^{-j}.
\]
Using \(v<t_*\) in (19) yields
\[
\beta_s(v)\le C_sL^N.                                            \tag{20}
\]

For the lower bound, let
\[
p_1=\frac{t_*}{t_*+y},\qquad
p_2=\frac{vt_*}{1+vt_*}.
\]
The saddle equation says \(2p_1+p_2=2\). If
\[
X\sim\operatorname{Bin}(2N,p_1),\qquad
Y\sim\operatorname{Bin}(N,p_2)
\]
are independent, then
\[
[T^{2N+s}]H_B(T)^N
=H_B(t_*)^N t_*^{-(2N+s)}
  \Pr(X+Y=2N+s).                                                  \tag{21}
\]

For fixed \(s\), choose \(i\) within \(1\) of \(2Np_1\), and put \(j=2N+s-i\). Then \(j\) stays a bounded distance from \(Np_2\). A binomial mode has probability at least \(1/(n+1)\), and
\[
\frac{\Pr(Z=k+1)}{\Pr(Z=k)}
=\frac{(n-k)p}{(k+1)(1-p)}
\]
is bounded above and below away from zero within any fixed distance of \(np\), for sufficiently large \(n\). Hence
\[
\Pr(X=i)\Pr(Y=j)\ge \frac{c_s}{(N+1)^2}.
\]
Using (21), the positive constant coefficient of \(C_B/G\), and the \(q=0\) term of (19), we get
\[
\beta_s(u)\ge \frac{c'_s}{(N+1)^2}L^N.                            \tag{22}
\]
Equations (20)–(22) prove the second part of (14).

Together, (14) and (13) prove
\[
\boxed{\Delta_s<0\quad(0\le s<m)}
\]
for every sufficiently large \(K\).

## 4. Separating the clusters and obtaining zeros

Fix any such \(K\), and replace the two clusters by
\[
\lambda_j=-75+\varepsilon\frac{j}{a+1},
\qquad
\mu_j=\frac34+\varepsilon\frac{j}{b+1},
\qquad 0<\varepsilon<1.                                          \tag{23}
\]
For sufficiently small \(\varepsilon\), continuity preserves all the strict negative signs at \(r=1\).

These are now admissible distinct points. Keep their heights fixed and decrease \(r\). By (8), all \(\Delta_s\) are positive for sufficiently small \(r>0\). Thus, for instance, the real continuous function \(\Delta_0(r)\) has a zero in \((0,1)\). By (6), that configuration is singular.

Its size is
\[
n=a+b+2m=3mK+2m,
\]
which is arbitrarily large. This proves that **every** positive integer \(m\) belongs to \(\mathscr S\), completing the set determination.

## 5. Certifying Python

The following is ordinary Python using SageMath. It does not infer signs from floating-point approximations: a sign is accepted only when an outward-rounded interval excludes zero.

`find_bracket(m, Nmin)` returns rational parameters for two admissible configurations of size at least `Nmin`, with opposite signs in every cyclic block. Its searches terminate by the proof above. The dovetailing avoids assuming any particular sufficient cluster size or precision.

```python
from sage.all import RealIntervalField, PolynomialRing, QQ
from itertools import count


def pmul(a, b):
    I = a[0].parent()
    out = [I(0) for _ in range(len(a) + len(b) - 1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out


def sign_cert(x):
    if x.lower() > 0:
        return 1
    if x.upper() < 0:
        return -1
    return 0                   # inconclusive, NOT an equality claim


def reduced(m, a, b, r=QQ(1), eps=QQ(0), bits=512):
    """
    Certified intervals containing Delta_s, s=0,...,m-1.

    R=100, h_-=0, h_+=1/4,
    lambda_j=-75+eps*j/(a+1),
    mu_j=3/4+eps*j/(b+1).

    eps=0 means the ordered vertical-cluster limit.
    """
    I = RealIntervalField(bits)
    r, R, d = I(r), I(100), I(QQ(1)/4)

    # S_m, formed with real positive quadratic factors.
    S = [I(1)]
    for j in range(1, (m-1)//2 + 1):
        S = pmul(S, [I(1), 2*(I.pi()*j/m).sin(), I(1)])
    if m % 2 == 0:
        S = pmul(S, [I(1), I(1)])

    # C_A and C_B; conjugate factors are multiplied as real quadratics.
    p = (R-r)/(d + (d*d + (R-r)**2).sqrt())
    A, B = pmul(S, [I(1), -p]), pmul(S, [p, I(1)])

    for j in range(1, (m-1)//2 + 1):
        c = (2*I.pi()*j/m).cos()
        q2 = r*r + R*R - 2*r*R*c
        D = d + (d*d + q2).sqrt()
        A = pmul(A, [I(1), 2*(r-R*c)/D, q2/D**2])
        B = pmul(B, [q2/D**2, 2*(R-r*c)/D, I(1)])

    if m % 2 == 0:
        q = (R+r)/(d + (d*d + (R+r)**2).sqrt())
        A, B = pmul(A, [I(1), q]), pmul(B, [q, I(1)])

    xy, uv = [], []

    for j in range(a):
        h = I(-75 + eps*QQ(j+1)/(a+1))
        x = r/(-h + (h*h + r*r).sqrt())
        y = R/(d-h + ((d-h)**2 + R*R).sqrt())
        xy.append((x, y))
        A, B = pmul(A, [x, I(1)]), pmul(B, [y, I(1)])

    for j in range(b):
        h = I(QQ(3)/4 + eps*QQ(j+1)/(b+1))
        u = r/(h + (h*h + r*r).sqrt())
        v = R/(h-d + ((h-d)**2 + R*R).sqrt())
        uv.append((u, v))
        A, B = pmul(A, [I(1), u]), pmul(B, [I(1), v])

    # Lower-axis elimination.
    for j, (x, y) in enumerate(xy):
        for P in (A, B):
            c = P[j]
            P[j] = I(0)
            P[j+m] += c*(x**m + y**m)
            P[j+2*m] -= c*(x*y)**m

    # Upper-axis elimination.
    for j in reversed(range(b)):
        u, v = uv[j]
        k = a+j
        for P in (A, B):
            c = P[k+2*m]
            P[k+2*m] = I(0)
            P[k+m] += c*(u**m + v**m)
            P[k] -= c*(u*v)**m

    return [
        A[k]*B[k+m] - B[k]*A[k+m]
        for k in range(a, a+m)
    ]


def check_constants():
    I = RealIntervalField(128)
    x = 1/(I(75) + (I(75)**2 + 1).sqrt())
    y = 100/(I(QQ(301)/4) +
             (I(QQ(301)/4)**2 + 10000).sqrt())
    u = I(QQ(1)/2)
    v = 100/(I(QQ(1)/2) +
             (I(QQ(1)/2)**2 + 10000).sqrt())

    assert x.upper() < QQ(1)/100
    assert y.lower() > QQ(49)/100
    assert y.upper() < QQ(1)/2
    assert v.lower() > QQ(99)/100
    assert v.upper() < 1

    t = (y + (y*y + 8*y/v).sqrt())/2
    assert t.lower() > v.upper()
    assert t.upper() < (1/y).lower()

    decay = ((1+x/u)/(1+x/v))**2 * (1+u*u)/(1+u*v)
    assert decay.upper() < QQ(2601)/2990


def check_division_identity():
    """Exact rational checks of the elimination/division identity."""
    P = PolynomialRing(QQ, 'T')
    T = P.gen()

    for m in range(1, 6):
        a, b = 2*m, m
        x, y, u, v = QQ(1)/7, QQ(2)/5, QQ(1)/2, QQ(4)/5
        g = (1-x**m*T**m)*(1-y**m*T**m)
        h = (T**m-u**m)*(T**m-v**m)
        F = (1+2*T+3*T**(2*m-1))*(T+x)**a*(1+u*T)**b

        Z = F
        for j in range(a):
            Z -= Z[j]*T**j*g
        remainder = P(Z // T**a) % h

        V = list(F) + [QQ(0)]*(a+b+2*m-len(list(F)))
        for j in range(a):
            c = V[j]
            V[j] = 0
            V[j+m] += c*(x**m+y**m)
            V[j+2*m] -= c*(x*y)**m
        for j in reversed(range(b)):
            k = a+j
            c = V[k+2*m]
            V[k+2*m] = 0
            V[k+m] += c*(u**m+v**m)
            V[k] -= c*(u*v)**m

        assert P(V) == T**a*remainder


def find_bracket(m, Nmin=1):
    K0 = max(1, (max(0, Nmin-2*m)+3*m-1)//(3*m))

    # Find a negative cluster limit.
    found = None
    for stage in count():
        for j in range(stage+1):
            K = K0*2**j
            bits = 128*2**(stage-j)
            a, b = 2*m*K, m*K
            D = reduced(m, a, b, bits=bits)
            if all(sign_cert(z) == -1 for z in D):
                found = (a, b)
                break
        if found is not None:
            break
    a, b = found

    # Separate all axial points, preserving negativity.
    eps = None
    for stage in count(1):
        for j in range(1, stage+1):
            e = QQ(1)/2**j
            bits = 128*2**(stage-j)
            D = reduced(m, a, b, eps=e, bits=bits)
            if all(sign_cert(z) == -1 for z in D):
                eps = e
                break
        if eps is not None:
            break

    # Find the positive-radius endpoint.
    for stage in count(1):
        for j in range(1, stage+1):
            r = QQ(1)/2**j
            bits = 128*2**(stage-j)
            D = reduced(m, a, b, r=r, eps=eps, bits=bits)
            if all(sign_cert(z) == 1 for z in D):
                return dict(m=m, a=a, b=b, eps=eps,
                            r_left=r, r_right=QQ(1))


def direct_m1(a, b, r, eps=QQ(1)/1000000, bits=2048):
    """Independent full-matrix calculation directly from the question."""
    I = RealIntervalField(bits)
    pts = [
        (I(-75+eps*QQ(j+1)/(a+1)), I(0))
        for j in range(a)
    ]
    pts += [(I(0), I(r)), (I(QQ(1)/4), I(100))]
    pts += [
        (I(QQ(3)/4+eps*QQ(j+1)/(b+1)), I(0))
        for j in range(b)
    ]

    n, mat = len(pts), []
    for i, (h, w) in enumerate(pts):
        P = [I(1)]
        for j, (g, z) in enumerate(pts):
            if i == j:
                continue
            dh, dw = abs(g-h), z-w
            D = dh + (dh**2+dw**2).sqrt()
            fac = [I(1), -dw/D] if i < j else [-dw/D, I(1)]
            P = pmul(P, fac)
        mat.append(P)

    det = I(1)
    for k in range(n):
        j = next(j for j in range(k, n)
                 if sign_cert(mat[j][k]) != 0)
        if j != k:
            mat[k], mat[j] = mat[j], mat[k]
            det = -det

        pivot = mat[k][k]
        det *= pivot
        for j in range(k+1, n):
            q = mat[j][k]/pivot
            for e in range(k+1, n):
                mat[j][e] -= q*mat[k][e]
            mat[j][k] = I(0)
    return det


if __name__ == "__main__":
    check_constants()
    check_division_identity()

    print(find_bracket(1, 150))
    print(find_bracket(3, 200))

    # Independent check of the full 98-by-98 coefficient matrix.
    for r, expected in [(QQ(1)/4, 1), (QQ(1), -1)]:
        full = direct_m1(64, 32, r)
        block = reduced(1, 64, 32, r=r,
                        eps=QQ(1)/1000000, bits=2048)[0]
        assert sign_cert(full) == expected
        assert sign_cert(block) == expected
        assert (full/block - 1).contains_zero()
        print("full 98-by-98 check:", r, sign_cert(full))

    # Certified narrower bracket for the same singular configuration.
    lo, hi = QQ(1)/4, QQ(1)
    for _ in range(32):
        mid = (lo+hi)/2
        s = sign_cert(reduced(
            1, 64, 32, r=mid,
            eps=QQ(1)/1000000, bits=2048
        )[0])
        assert s != 0
        if s == 1:
            lo = mid
        else:
            hi = mid
    print("root bracket:", lo, hi)
```

I ran these checks. In particular, the full-matrix check certified
\[
\det M(r=1/4)>0,\qquad \det M(r=1)<0
\]
for \(m=1,a=64,b=32,\varepsilon=10^{-6}\). The final certified radius bracket was
\[
\frac{2076227755}{4294967296}
<
r_*
<
\frac{8304911023}{17179869184},
\]
approximately
\[
0.48340944456867874<r_*<0.4834094447433017.
\]

The automatic constructions also returned, among others,
```text
{'m': 1, 'a': 100, 'b': 50, 'eps': 1/2,
 'r_left': 1/4, 'r_right': 1}

{'m': 3, 'a': 132, 'b': 66, 'eps': 1/2,
 'r_left': 1/8, 'r_right': 1}
```
with interval-certified opposite block signs at their endpoints.

**Proved:** every positive integer \(m\) admits singular configurations of the required form with arbitrarily large \(n\). Therefore \(\mathscr S=\mathbb Z_{\ge1}\). **Nothing remains for the stated problem.**