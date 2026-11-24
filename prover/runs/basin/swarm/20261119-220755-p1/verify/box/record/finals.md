# agent_1: last reply

\[
\boxed{\,s_{\min}=4\,}.
\]

The upper bound is computer-assisted: it uses a rigorously validated periodic orbit of an auxiliary differential equation, **not** a numerically observed nonconvergent CG trajectory.

I have written the complete analytic appendix, the Python verification programs, and the interval certificate to:

- `workspace/COMPLETE_PROOF.md`
- `workspace/PROOF_INDEX.md`
- `workspace/restarted_cg_threshold_proof.zip`

The archive is self-contained. I extracted it into a separate directory and ran its verification suite successfully. Below is the proof, including the construction and the certificate inequalities.

## 1. Spectral form of the iteration

Combine repeated eigenspaces, keeping the fixed direction of the residual in each eigenspace. Discard any coordinate after it becomes zero. There are only finitely many such discards.

Write the remaining distinct eigenvalues as \(\lambda_i\), and put
\[
p_{k,i}=\frac{\|P_i r_k\|_2^2}{\|r_k\|_2^2}.
\]
On a nonterminating tail all these weights are positive.

Let \(f_k\) be the monic polynomial of degree \(s\) satisfying
\[
\sum_i p_{k,i}\lambda_i^j f_k(\lambda_i)=0,
\qquad 0\le j<s,
\]
and set
\[
N_k=\sum_i p_{k,i}f_k(\lambda_i)^2.
\]
The minimizing property in the question gives the residual polynomial
\(f_k(x)/f_k(0)\). Consequently,
\[
p_{k+1,i}=\frac{p_{k,i}f_k(\lambda_i)^2}{N_k}.                 \tag{1}
\]
Since all eigenvalues are positive, the sign of \(f_k(0)\) is \((-1)^s\).
Thus the monic normalized residual map and the actual normalized residual
map have the same even iterates.

Hereafter a polynomial is also identified with its coefficient vector.

### A finite-variation identity

Put
\[
f=f_k,\quad g=f_{k+1},\quad h=f_{k+2},\quad K=fg,
\quad v(x)=(1,x,\ldots,x^{s-1})^\top .
\]
Orthogonality gives
\[
\sum_i p_{k,i}K(\lambda_i)=N_k,\qquad
\sum_i p_{k,i}K(\lambda_i)^2=N_kN_{k+1}.
\]
Hence
\[
\sum_i p_{k,i}\bigl(K(\lambda_i)-N_k\bigr)^2
       =N_k(N_{k+1}-N_k).                                   \tag{2}
\]
In particular, \(N_k\uparrow L>0\).

There is also the exact identity
\[
M(p_{k+2})(h-f)
=
-\frac{\sum_i p_{k,i}f(\lambda_i)
       (K(\lambda_i)-N_k)^2v(\lambda_i)}
       {N_kN_{k+1}},                                        \tag{3}
\]
where
\[
M(p)=\sum_i p_i v(\lambda_i)v(\lambda_i)^\top .
\]
To see (3), use
\[
\sum_i p_{k,i}f(\lambda_i)v(\lambda_i)=0,\qquad
\sum_i p_{k,i}f(\lambda_i)K(\lambda_i)v(\lambda_i)=0,
\]
and then use orthogonality of \(h\) for \(p_{k+2}\).

The matrices \(M(p_k)\) are uniformly positive definite. Indeed, a singular
limiting matrix would give a limiting measure supported on at most \(s-1\)
nodes; a monic degree-\(s\) polynomial vanishing there would imply
\(N_k\to0\), contrary to \(N_k\ge N_0>0\).
The same argument excludes limiting supports of size at most \(s\).

All the polynomials have their roots in the fixed spectral hull, so their
coefficients are uniformly bounded. Equations (2)–(3) therefore imply
\[
\|f_{k+2}-f_k\|\le C(N_{k+1}-N_k).
\]
It follows that
\[
f_{2k}\longrightarrow f,\qquad f_{2k+1}\longrightarrow g,     \tag{4}
\]
and, importantly,
\[
\|f_{2k}-f\|+\|f_{2k+1}-g\|
       \le C(L-N_{2k}).                                     \tag{5}
\]

Let \(T\) be the union of the supports of all cluster points of
\(p_{2k}\). Equations (2), (4) give
\[
T\subseteq\{\lambda: f(\lambda)g(\lambda)=L\},
\qquad s+1\le |T|\le 2s.                                    \tag{6}
\]
The even normalized residual map is asymptotically regular, since its
successive inner products are \(\sqrt{N_k/N_{k+1}}\).
Its cluster set, and hence the cluster set of the weights, is connected.

A node outside \(T\) with \(|fg|<L\) has exponentially decaying weight.
An active node with \(|fg|>L\) is impossible. Nodes with \(fg=-L\) require
more care. Write
\[
t_k=L-N_{2k}.
\]
For every such negative-neutral node \(z\),
\[
p_{2k,z}=O(t_k^2),                                          \tag{7}
\]
and its presence implies
\[
\sum_k t_k=\infty.                                          \tag{8}
\]
For completeness, (2) gives
\(t_k-t_{k+1}\ge c p_{2k,z}\), whereas (5) and (1) give
\[
|p_{2k+2,z}-p_{2k,z}|\le Ct_kp_{2k,z}.
\]
Summing yields (7). If \(\sum t_k<\infty\), the logarithmic multipliers of
this positive coordinate would be summable, so its weight could not tend
to zero; this proves (8).

## 2. A root-turning lemma

The following elementary orthogonal-polynomial fact is useful for the
small restart lengths.

For \(m\) active nodes, let
\[
d_i=\prod_{j\ne i}(\lambda_i-\lambda_j),\qquad
q_i=\frac1{d_i^2p_i}.
\]
There is a monic polynomial \(H\) of degree \(m-s-1\), orthogonal for the
positive weights \(q_i\), with
\[
H(\lambda_i)=\frac{d_ip_if(\lambda_i)}N.                     \tag{9}
\]
This follows directly from Lagrange interpolation. Its one-block update
satisfies
\[
\frac{H_{k+1}(\lambda_i)}{H_k(\lambda_i)}
 =\frac{f_k(\lambda_i)f_{k+1}(\lambda_i)}{N_{k+1}}.            \tag{10}
\]
Consequently,
\[
q_{k+2,i}\ \propto\
q_{k,i}\left(\frac{H_k(\lambda_i)}{H_{k+1}(\lambda_i)}\right)^2.
\]

Let \(a_k\) be the smallest zero of \(H_k\), and define
\[
S_k(u)=\sum_i\frac{q_{k,i}H_k(\lambda_i)^2}{\lambda_i-u}.
\]
Then \(S_k(a_k)=0\), and \(S_k'(u)>0\) in its spectral gap.
The Rayleigh quotient with trial polynomial
\(H_{k+1}(x)/(x-a_{k+1})\) gives
\[
a_{k+2}\le
a_{k+1}+\frac{S_k(a_{k+1})}{S_k'(a_{k+1})}.                 \tag{11}
\]
In particular, once the smallest root decreases, it cannot turn upward.
There is a reflected statement for the largest root.

We use the following robust version. Suppose the tracked extreme root
stays in a fixed spectral gap and is separated from the other slow roots.
Exponentially contracting coordinates may be removed. Then
\[
\delta_{k+1}\le c_k\delta_k+O(\rho^k),
\quad
\delta_k=a_{k+1}-a_k,\quad c_k>0,\quad c_k\to1,\quad \rho<1.   \tag{12}
\]
Thus \(a_k\) converges.

Here are the points needed for robustness. Factoring removed roots as
\(H_k=D_kh_k\), the polynomial \(h_k\) is exactly orthogonal for
\(q_kD_k^2\). The update acquires the factor
\((D_{k+2}/D_{k+1})^2\), which is \(1+O(\rho^k)\) off the removed nodes.
At a removed node its Rayleigh contribution is \(O(\rho^k)\), by
\[
q_{k,i}H_k(\lambda_i)^2
      =\frac{p_{k,i}f_k(\lambda_i)^2}{N_k^2}.
\]
Also (10) implies that ratios of the tracked root’s distances from its two
gap endpoints tend to one. Comparing the positive terms in \(S_k'\)
therefore gives \(c_k\to1\), including when a root approaches an endpoint.

Finally, choose \(\rho<\eta<1\). For sufficiently large \(D\), the cone
\(\delta_k\le-D\rho^k\) is forward invariant in (12). Either the cone is
entered, making the root eventually decreasing, or the total negative
variation is finite. Boundedness gives convergence in either case.

The full endpoint-uniform perturbation proof is in the appendix.

## 3. Why \(s=1,2,3\) cannot work

If \(|T|=s+1\), the limiting weights are unique: the equations
\[
\sum p_i=1,\qquad \sum p_i\lambda_i^jf(\lambda_i)=0
\quad(0\le j<s)
\]
give
\[
p_i\ \propto\ \frac1{P_T'(\lambda_i)f(\lambda_i)}.
\]
Thus (6) immediately settles \(s=1\).

We record one logarithmic interpolation observation used below.
If \(T\) has \(2s\) nodes, write
\[
fg=L+P_T.
\]
For a negative-neutral outsider \(z\), \(P_T(z)=-2L\).
Let \(\ell_i(z)\) be its Lagrange coefficients on \(T\). The exact
two-block update, polynomial interpolation, and (5) show that
\[
\Psi_k=\log p_{2k,z}+\sum_{i\in T}\ell_i(z)\log p_{2k,i}       \tag{13}
\]
is eventually nondecreasing. More explicitly, with
\(R=\sqrt{N_{2k}N_{2k+1}}\),
\[
\Delta\Psi
 =2\log\frac{2L-R}{R}+O(t_k^2)\ge0.                         \tag{14}
\]
This calculation is uniform at faces: it expands logarithms of the
polynomial multipliers, not logarithms of the weights.

### Restart length two

Only \(|T|=4\) remains. The feasible limiting measures form an affine
line. A non-singleton connected cluster set contains a point at which all
four weights are positive.

At such a subsequence, (13) would tend to \(-\infty\), because the outsider
weight tends to zero while all four base weights stay positive. This
contradicts (14). Hence there are no negative-neutral outsiders, and all
outsiders decay exponentially.

On four nodes the dual polynomial is \(H(x)=x-\theta\). The exact update
gives a scalar recurrence
\[
\delta_{k+1}=a_k\delta_k+O(\rho^k),
\qquad a_k>0,\quad a_k\to1,
\]
for successive increments of \(\theta\). For example, its exact
coefficient is
\[
a_k=\frac{\sum_i Q_i r_i}{\sum_i Q_i r_i^2},\qquad
Q_i\propto\frac1{d_i^2p_i},\qquad
r_i=\frac{\lambda_i-\theta_k}{\lambda_i-\theta_{k+1}}.
\]
Equation (10) gives \(r_i\to1\), even at a limiting face.
The scalar cone argument above proves convergence of \(\theta\).
Formula (9) then proves convergence of the weights.

### Restart length three: six limiting nodes

The case \(|T|=4\) is already settled. First suppose \(|T|=6\), with
\(\lambda_1<\cdots<\lambda_6\). Then
\[
fg=L+P_6.
\]
Each of \(f,g\) has one root in each of
\[
(\lambda_1,\lambda_2),\quad
(\lambda_3,\lambda_4),\quad
(\lambda_5,\lambda_6).
\]
Indeed their product has two roots, counting multiplicity, in each
negative lobe of \(P_6\); an orthogonal polynomial cannot have two roots
in a gap containing no measure node.

The feasible critical measures are precisely
\[
p_i=\frac{L(\lambda_i-\alpha)(\lambda_i-\beta)}
           {P_6'(\lambda_i)f(\lambda_i)},\qquad
\alpha\in[\lambda_2,\lambda_3],\quad
\beta\in[\lambda_4,\lambda_5].                              \tag{15}
\]
The two slow dual roots are uniformly separated.

For a negative outsider, (13) forces the cluster set into the following
facet stars:
\[
\begin{array}{c|c}
z\text{ lies in}&\text{necessary condition}\\ \hline
(\lambda_1,\lambda_2)&
 \alpha=\lambda_3\ \text{or}\ \beta=\lambda_5\\
(\lambda_3,\lambda_4)&
 \alpha=\lambda_2\ \text{or}\ \beta=\lambda_5\\
(\lambda_5,\lambda_6)&
 \alpha=\lambda_2\ \text{or}\ \beta=\lambda_4 .
\end{array}                                                \tag{16}
\]
For example, in the first row the only negative Lagrange coefficients
are those at nodes \(3,5\).

These three stars finish this stratum:

- The first and third together leave two isolated vertices; connectedness
  leaves one.
- The first and second, or second and third, leave a single edge. Such an
  edge omits a node from the support union \(T\), a contradiction.
- With only first-row outsiders, \(\beta\) is the largest noncontracting
  dual root and converges by (12). The first star then leaves a point or
  a single edge. The latter again contradicts the definition of \(T\).
- The third-row case is reflected.
- With only middle-row outsiders, or no negative outsiders, both slow
  roots are extreme after strict-mode deflation and converge.

Thus six limiting nodes cannot produce nonconvergence.

### Restart length three: five limiting nodes

This is the delicate case. Write
\[
fg=L+P(x)(x-c),\qquad P=\prod_{i=1}^5(x-\lambda_i).
\]
The feasible critical measures have the form
\[
p_i=\frac{L(\lambda_i-\theta)}
           {P'(\lambda_i)f(\lambda_i)},\qquad \theta\in[a,b], \tag{17}
\]
where \([a,b]\) is one spectral gap.

The location of \(c\) is constrained by positive Gaussian quadrature.
Indeed,
\[
\sum_i\frac{p_i}{z-\lambda_i}
       =\frac{(z-\theta)g(z)}{P(z)},
\]
and
\[
\frac{(z-\theta)g(z)}{P(z)}
-\frac{(z-\theta)(z-c)}{f(z)}
       =\frac{L(z-\theta)}{P(z)f(z)}=O(z^{-7}).
\]
Thus the positive three-node Gaussian quadrature at the roots of \(f\)
has numerator \((z-\theta)(z-c)\), whose roots strictly interlace those
of \(f\). The same holds for \(g\).

In particular, \(c\notin[a,b]\): otherwise the feasible choice
\(\theta=c\), including an endpoint choice, would give a repeated
Gaussian numerator root. Reflecting the spectrum if necessary,
\[
c<a=\lambda_3<b=\lambda_4,\qquad
f(c),g(c)>0,\quad f,g<0\text{ on }[a,b].                    \tag{18}
\]

Negative outsiders cannot occur on both sides of \(c\). Here is the exact
interpolation identity proving this. For
\(\mu<c<\nu\) with \(fg(\mu)=fg(\nu)=-L\), put
\[
a_\mu=\frac{\mu-c}{\mu-\nu}>0,\quad
a_\nu=-\frac{\nu-c}{\mu-\nu}>0,\quad
c_i=\frac{2L}{P'(\lambda_i)(\lambda_i-\mu)(\lambda_i-\nu)}.
\]
For every monic sextic \(K\),
\[
\sum_i c_iK(\lambda_i)-a_\mu K(\mu)-a_\nu K(\nu)=2L.
\]
It follows that
\[
\sum_i c_i\log p_{2k,i}
 +a_\mu\log p_{2k,\mu}+a_\nu\log p_{2k,\nu}
\]
is eventually increasing. A non-singleton cluster interval in (17)
contains an all-five-positive point. Along that subsequence the displayed
quantity tends to \(-\infty\), a contradiction.

If all negative outsiders lie below \(c\), or there are none, \(\theta\)
is the largest noncontracting dual root, and (12) settles the case.
It remains to consider negative outsiders \(z>c\).

Here is the ingredient which rules out this last possibility of
nonconvergence.

#### Virtual-root inequality

Use first-order perturbations of the even and odd limiting polynomials:
\(w,dg\), respectively, and write \(A=-t_k+o(t_k)\) for the norm variation.
Put
\[
q=gw+f\,dg-A.
\]
If \(v\) is the first-order two-block displacement of \(\theta\), dual
interpolation gives
\[
q(x)=C P(x)-\frac{Lv}{2}
       \frac{1-P(x)/P(\theta)}{x-\theta}.                    \tag{19}
\]
Define
\[
I=LC-\frac{L^2v}{2P(\theta)(\theta-c)}.                      \tag{20}
\]
Endpoint expressions are read after cancellation; \(v\) contains the
vanishing factor \(P(\theta)\). Then
\[
\liminf_{k\to\infty}\frac{I_k}{t_k}\ge0.                     \tag{21}
\]

For clarity, the proof of (21) is as follows. Add an infinitesimal
positive-weight probe at \(\zeta<c\), chosen close to \(c\).
After removing exponentially contracting roots to its left, the added
root is the smallest dual root:
\[
a_k(\varepsilon)=\zeta+\varepsilon\alpha_k+O(\varepsilon^2).
\]
Expanding the Rayleigh inequality (11) gives
\[
\alpha_{k+2}\le\frac{\alpha_{k+1}^2}{\alpha_k}.               \tag{22}
\]
Furthermore,
\[
\frac{\alpha_{k+1}}{\alpha_k}
 =\frac{f_k(\zeta)f_{k+1}(\zeta)}{N_{k+1}}
      \frac{H_k(\zeta)}{H_{k+1}(\zeta)},\qquad
\operatorname{sign}\alpha_k=\operatorname{sign}P(\zeta).     \tag{23}
\]
Thus these positive ratios decrease to \(fg(\zeta)/L\) when
\(P(\zeta)>0\), and increase to it when \(P(\zeta)<0\).
Strict-root removal adds only an exponentially small error.

Take any deficit-normalized cluster state. Substitution of (19) into
the logarithmic first variation of (23), divided by \(P(\zeta)\), gives
a nonnegative quantity:
\[
\frac1{f(\zeta)g(\zeta)}
\left[
 C-\frac{A(\zeta-c)}L+
 \frac{v}{2(\zeta-\theta)}
       \left(\zeta-c+\frac L{P(\theta)}\right)
\right].
\]
Letting \(\zeta\uparrow c\) gives \(I/L^2\ge0\).
This order of division and passage to the limit also handles
\(P(c)=0\).

A possible vanishing positive-neutral coordinate at \(c\) is harmless:
its dual root moves \(O(t_kp_{2k,c})=o(t_k)\) per two-block step.
For strict-root deflation the error is \(O(\rho^k)\); it is
\(o(t_k)\) by (7) and the presence of an active negative outsider.
All these estimates are uniform at the endpoints. The appendix gives
the full positive-measure deflation argument.

#### A corrected individual logarithmic weight

Fix any negative outsider \(z>c\). From (19)–(20), its homogeneous
logarithmic growth is
\[
\ell_z=-\frac{4A}{L}+\frac{4I}{L(z-c)}
 +v\,\frac{f(\theta)g(\theta)+L}
            {P(\theta)(\theta-c)(z-\theta)}.                \tag{24}
\]
Choose
\[
\Phi_z'(\theta)=-
 \frac{f(\theta)g(\theta)+L}
      {P(\theta)(\theta-c)(z-\theta)}.
\]
The apparent pole at \(z\) cancels. On \([a,b]\),
\[
\Phi_z(\theta)
 =\eta_a\log(\theta-a)+\eta_b\log(b-\theta)+G(\theta),
\quad
\eta_e=\frac{2L}{P'(e)(e-c)(e-z)},
\]
where \(G\) is smooth on the closed gap.
If \(c<z<a\), \(\Phi_z\) is proper increasing from \(-\infty\) to
\(+\infty\); if \(z>b\), it is proper decreasing.

For the exact iteration use
\[
\Psi_k=\log p_{2k,z}+\eta_a\log p_{2k,a}
                  +\eta_b\log p_{2k,b}+G(\theta_k).
\]
Exact dual factorization gives
\(p_{2k,a}=C_{k,a}(\theta_k-a)\) and
\(p_{2k,b}=C_{k,b}(b-\theta_k)\), with
\(\Delta\log C_{k,e}=o(t_k)\). Face invariance makes the logarithmic
Taylor estimates uniform, even arbitrarily near an endpoint.
Therefore (24) gives
\[
\Psi_{k+1}-\Psi_k
 =\frac{4t_k}{L}+\frac{4I_k}{L(z-c)}+o(t_k)
 \ge \frac{2t_k}{L}
\]
eventually. By (8), \(\Psi_k\to+\infty\).
Since \(\log p_{2k,z}\le0\), it follows that
\(\Phi_z(\theta_k)\to+\infty\). Hence \(\theta_k\) converges to one endpoint.

This closes the five-node case and proves convergence for \(s=3\).

Finally, convergent weights imply convergent even residual directions:
on \(T\),
\(f_{2k}(\lambda_i)f_{2k+1}(\lambda_i)\to L>0\), so the even-coordinate
signs eventually stop changing; all other coordinates vanish.

We have proved
\[
s_{\min}\ge4.                                               \tag{25}
\]

## 4. A rigorously certified construction for \(s=4\)

Here are the exact spectral parameters. Let
\[
S=\{-3,-1,0,1,2,3\},\qquad P_6(x)=\prod_{\lambda\in S}(x-\lambda),
\]
\[
Q(x)=\left(x+\frac{18}{25}\right)
     \left(x-\frac{17}{10}\right),\qquad N=\frac3{50}.
\]
Let \(\rho_0<\cdots<\rho_7\) be the eight real roots of
\(P_6Q+N\). Define monic quartics
\[
f(x)=\prod_{j\in\{0,3,5,6\}}(x-\rho_j),\qquad
g(x)=\prod_{j\in\{1,2,4,7\}}(x-\rho_j).
\]
Let \(\mu,\nu\) be roots numbered \(1,6\), starting at zero, of
\(P_6Q+2N\). Numerically, only to identify them,
\[
\mu\approx-1.00324831,\qquad \nu\approx2.00479273.
\]
Thus
\[
fg=N\quad\text{on }S,\qquad fg=-N\quad\text{at }\mu,\nu.      \tag{26}
\]

### The auxiliary equation

Put \(H(x)=x-\theta\). The critical base weights and their partners are
\[
p_i=\frac{NH(\lambda_i)}{d_if(\lambda_i)},\qquad
p_i'=\frac{H(\lambda_i)f(\lambda_i)}{d_i},
\quad d_i=P_6'(\lambda_i).
\]
They are positive for \(0<\theta<1\).

Use the exact analytic chart
\[
p_i(H,u)=C(H,u)\frac{H(\lambda_i)}
                         {d_i(f+u)(\lambda_i)},\qquad
C(H,u)^{-1}=\sum_i\frac{H(\lambda_i)}
                             {d_i(f+u)(\lambda_i)}.
\]
Append weights \(z_\mu,z_\nu\), scaling the base weights to keep total
mass one. Set
\[
u=\varepsilon w,\qquad z_\zeta=\varepsilon^2Z_\zeta.
\]
With \(\varepsilon_{k+1}=\varepsilon_k/(1+\varepsilon_k)\), the exact
two-block map becomes
\[
Y_{k+1}=Y_k+\varepsilon_k V(Y_k)
                  +\varepsilon_k^2R(Y_k,\varepsilon_k),     \tag{27}
\]
where \(R\) is bounded and analytic on compact positive charts.

Here is an explicit definition of \(V\), so the differential equation
being certified is unambiguous. Write \(v_i=(1,\lambda_i,\lambda_i^2,
\lambda_i^3)^\top\), and
\[
M=\sum p_iv_iv_i^\top,\qquad M'=\sum p_i'v_iv_i^\top,
\quad dg=-M'^{-1}Mw,
\]
\[
A=N^2\sum_i\frac{H(\lambda_i)w(\lambda_i)}
                         {d_if(\lambda_i)^2},\qquad
R_i=\frac{g_iw_i+f_i\,dg_i-A}{N}.
\]
The values \(H(\lambda_i)R_i\) are one constant, denoted \(dh\). Put
\[
W=-M^{-1}\left[
       \sum_i p_if_iR_i^2v_i+
       4\sum_{\zeta\in\{\mu,\nu\}}Z_\zeta f(\zeta)v(\zeta)
       \right],
\]
\[
\ell_\zeta=
 2\left(\frac{w(\zeta)}{f(\zeta)}
       +\frac{dg(\zeta)}{g(\zeta)}\right)-\frac{2A}{N}.
\]
In coordinates \(Y=(-\theta,w_0,w_1,w_2,w_3,Z_\mu,Z_\nu)\),
\[
V(Y)=\bigl(2dh,\ w+W,\ Z_\mu(2+\ell_\mu),
                            Z_\nu(2+\ell_\nu)\bigr).        \tag{28}
\]
Expansion (27) follows from the exact identity (3); in particular the
coefficient \(4\) follows from \((fg-N)^2=4N^2\) at the outsiders.

### What was certified

A nonconstant positive periodic orbit of (28), with approximate period
\(4.05182\), was validated using 300-bit directed interval arithmetic.

The input is an exact dyadic periodic Hermite approximation
\((\gamma,P)\), not an assumed solution. Its data file is
`agent2_floquetframe_m072.npz`, with SHA256
```text
44d3bcc35e4cc85012075b1937825851e4f95b5878c5b6000bfbf866f1f0ab3b
```

For completeness, the validation criterion is given next.
Let \(G=TV\), and let \(D=\operatorname{diag}(0,D_n)\) be the stored
real block-diagonal approximate Floquet matrix. Set
\[
a=P^{-1}\gamma',\quad B=P^{-1}P',\quad
d=P^{-1}(G(\gamma)-\gamma'),
\]
\[
E=P^{-1}(DG(\gamma)P-P')-D.
\]
Use the maximum of scalar absolute values and Euclidean norms of the
single two-dimensional rotational block. The certified bounds are
conservatively taken to be
\[
\begin{array}{c|c}
\text{quantity}&\text{bound}\\ \hline
\|d\|&\sqrt2(3.7\,10^{-6})\\
\|E[:,n]\|&\sqrt2(10^{-3})\\
\text{normal Hessian norm}&\sqrt2(1500)\\
\|B[:,n]\|&\sqrt2(500)\\
a_0&>0.9999\\
\|a_n\|&\sqrt2(10^{-4})\\
\|D_n\|&<20\\
\min|\Re\operatorname{spec}D_n|&>1/6.
\end{array}                                                \tag{29}
\]
The tube radius is \(\rho=3/50000\).

Here is the contraction test used. Denote the respective bounds in
(29) by \(\delta,e,H,b,a_*,a_n,d_0,\alpha\), and calculate
\[
\begin{aligned}
r&=\delta+e\rho+H\rho^2/2,&
q&=\frac r{a_*-b\rho},\\
q_L&=\frac{e+H\rho+bq}{a_*-b\rho},&
M_0&=r+[a_n+(b+d_0)\rho]q,\\
F_0&=\frac{M_0}{1-q},&
L_M&=e+H\rho+(b+d_0)q+[a_n+(b+d_0)\rho]q_L,\\
L_F&=\frac{L_M}{1-q}+\frac{M_0q_L}{(1-q)^2}.
\end{aligned}
\]
Exact rational arithmetic, using
\(70711/50000>\sqrt2\), verifies
\[
F_0<9.553571\,10^{-6}<10^{-5}=\alpha\rho,\qquad
L_F<0.141826<\alpha=\frac16.                                \tag{30}
\]

To explain why this proves existence, write
\(x=\gamma(s)+P(s)(0,\eta)\), and solve the phase equation first.
It gives a strictly positive phase speed. The normal equation then is
\[
\eta'=D_n\eta+\mathcal F(s,\eta),
\quad
\|\mathcal F\|\le F_0,\quad
\operatorname{Lip}\mathcal F\le L_F.
\]
The periodic stable-past/unstable-future Green operator has norm at most
\(1/\alpha\). Thus (30) makes its fixed-point map a strict contraction
of the \(\rho\)-ball. The same inequality gives an exponential dichotomy
for the normal variational equation. The resulting periodic orbit is
normally hyperbolic.

The interval program also certifies, throughout that tube,
\[
0.064964186<\theta<0.979685969,
\]
\[
Z_\mu>2.8204435\,10^{-6},\qquad Z_\nu>0.0081262797,
\]
and all six base weights are positive. Two phase slices have disjoint
\(\theta\)-intervals, proving nonconstancy.

These are whole-tube enclosures. The computation used **2897 accepted
intervals exactly tiling all 2000 Hermite pieces**. Root isolation is by
exact rational Sturm calculations. The independent post-audit checks
the exact dyadic tiling, data hashes, positivity, nonconstancy, block
structure, and the rational inequalities (30).

### From the periodic orbit to an exact restarted orbit

We use the following elementary shadowing fact for a parabolic step size.

> If \(V\) has a normally hyperbolic periodic orbit in a positive compact
> chart and an exact map has form (27), then, for sufficiently large
> \(K\), it has an orbit with \(\varepsilon_k=1/(k+K)\) shadowing that
> periodic orbit in logarithmic time.

One proof takes tubular phase and normal coordinates. Solve stable
normal components by past Green sums and unstable components by future
Green sums. In a weighted sequence norm \(O(k^{-\beta})\), with
\(0<\beta\) smaller than the normal rates and \(1\), these sums are a
contraction for large \(K\). The \(O(k^{-2})\) truncation errors are
summable; the phase correction converges. Thus
\[
Y_k=\Gamma(\log(k+K)+\phi+o(1))+o(1),
\]
where \(\Gamma\) is the periodic orbit. The detailed Green-sum proof is
included in the appendix.

Apply this to (27). All eight weights remain positive for sufficiently
large \(K\). Since \(\theta\) is nonconstant on \(\Gamma\), the base weights
in (17), now with six nodes and quartic \(f\), have at least two distinct
cluster values. Hence the even normalized residuals do not converge.

Finally take
\[
A=\operatorname{diag}\bigl(
1,3,4,5,6,7,\ \mu+4,\nu+4\bigr).
\]
It is SPD. Translation of all spectral nodes by \(4\) does not change
the monic weight dynamics. Choose the positive lifted initial weights
\(p_i\), and set
\[
x_0=0,\qquad b_i=\sqrt{p_i}.
\]
Their iteration is exactly the weight orbit just constructed. It never
terminates, and \(y_{2k}\) does not converge. Therefore
\[
s_{\min}\le4.
\]
Together with (25), this proves the answer.

## 5. Executed Python checks

The archive contains `workspace/run_final_checks.py`. From its parent
directory, run
```bash
python workspace/run_final_checks.py
```
It executes 13 checks, including exact symbolic identities, the
virtual-probe inequalities, and the independent audit of every interval
record. I ran it successfully, also from the independently extracted
archive. Its final output included:
```text
EXACT rational certificate budget PASS:
fbar 9.553570824191712e-06 < 1e-05
Lipf 0.14182582144385908 < 0.16666666666666666

POST-AUDIT PASS:
2000 exactdyadic Hermitepieces tiled by 2897 certifiedintervals;
allsha/rationaltargets/positivity/nonconstancy checks passed

ALL FINITE CHECKS PASSED.
STANDALONE ARCHIVE REPRODUCTION PASS:
240 SHA256 entries verified.
```

To recompute the directed interval enclosures themselves, rather than
audit the saved records, run
```bash
python workspace/run_final_checks.py --full
```
This uses two workers and a fresh output directory. The full interval
calculation was also run successfully; it takes approximately ten
minutes.

Thus the claimed sharp threshold is supported by an analytic convergence
proof for every \(s\le3\), and a validated exact-orbit construction for
\(s=4\), not merely by finite numerical experiments.

# agent_2: last reply

The minimum is **\(s=4\)**.

My assigned proof work and independent audits are complete:
- Convergence for \(s=1,2\).
- The strict-left deflation argument needed for the \(s=3\) virtual-probe proof.
- Full audit of the complete \(s=3\) support-stratification argument.
- Independent audit of the interval-certified \(s=4\) periodic orbit and its lifting to an exact SPD iteration.

All seven current verification scripts passed; their output is recorded in `workspace/agent2_final_check_record.json`. The team’s mathematical proof is complete; only final presentation remains.

# agent_3: last reply

Completed and audited the cubic-restart convergence proof for every support stratum. Combined with the certified quartic counterexample, the smallest integer is
\[
\boxed{4}.
\]

The final proof is in `workspace/agent3_s3_complete_convergence.md`. Both of my checkers were rerun successfully, including 900 root-turning tests and the high-precision virtual-root checks. All mathematical work is complete; only the lead’s final presentation remains.

# agent_4: last reply

Confirmed: the team’s complete, independently audited result is \(\boxed{4}\). No mathematical gaps remain.