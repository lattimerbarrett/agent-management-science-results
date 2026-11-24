# agent_1: last reply

\[
\boxed{\mathcal D=\{n\in\mathbb Z:n\ge19\}.}
\]

The proof has two distinct ingredients: a sharp boundary-shape calculation, and an analytic argument connecting that calculation to solutions. In particular, the sign change of a finite matrix alone would not prove the result.

The code and detailed proof modules produced in the calculation are collected in

```text
workspace/boundary_yamabe_verified.zip
```

with SHA-256
```text
e6b43ce3122edafd5fbe7177da8492c18f785603f347202c9c4a1efe1368fb7d
```

The consolidated command is

```bash
python workspace/boundary_yamabe_verified/verify_all.py
```

It was executed successfully: **25 scripts passed**, including the exact low-dimensional positivity certificates, the high-dimensional critical-point certificates, and the conformal, Pohozaev, cutoff, and mass-flux identities. The verifier also checks that no source file changes during execution. Floating-point calculations are not used to certify any sign needed below.

I use the standard classification of positive entire critical solutions on \(\mathbb R^n\), its Neumann half-space consequence by reflection, standard Sobolev/elliptic/implicit-function results, Malcev’s residual-finiteness theorem, and the spin positive-mass theorem for asymptotically flat metrics, including minimal-boundary doubling. None of these inputs is the sharp compactness theorem at issue here.

## 1. Normalizations

Put
\[
a=\frac{n-2}{2},\qquad
A=n(n-2),\qquad
p=\frac{n+2}{n-2},\qquad
q=p+1=\frac{2n}{n-2},\qquad b=2c_n.
\]
The conformal quadratic form is
\[
Q_g(v)=\int_M\bigl(|\nabla v|^2+c_nR_gv^2\bigr)
       +b\int_{\partial M}H_gv^2.
\]
Thus positive Yamabe type is precisely positivity of the first eigenvalue of this form.

For \(\widehat g=u^{4/(n-2)}g\), conformal covariance gives
\[
L_{\widehat g}\phi=u^{-p}L_g(u\phi),\qquad
B_{\widehat g}\phi=u^{-n/(n-2)}B_g(u\phi).
\]
Consequently, a solution in the question gives
\[
R_{\widehat g}=4n(n-1),\qquad H_{\widehat g}=0.                 \tag{1}
\]
The factor \(4\) is important with the coefficient used in the question.

The Euclidean Neumann bubble is
\[
U_{\varepsilon,\xi}(x)=
\left(\frac{\varepsilon}
{\varepsilon^2+|x'-\xi|^2+x_n^2}\right)^a.
\]
It satisfies
\[
\Delta U_{\varepsilon,\xi}+A U_{\varepsilon,\xi}^{p}=0,
\qquad \partial_nU_{\varepsilon,\xi}=0.
\]

These identities, with the stated trace convention for \(H\), are checked symbolically in the bundle.

## 2. The exact boundary-shape form

Write a flat boundary chart as an epigraph
\[
\Omega_h=\{x_n>h(x')\}.
\]
Flatten it by \(T(y)=(y',y_n+h(y'))\). Its Jacobian is one, and the action becomes exactly
\[
\begin{aligned}
I_h(v)={}&\frac12\int_{\mathbb R^n_+}
 \left(|\nabla v|^2-2h_av_av_n+|Dh|^2v_n^2\right)\\
&+c_n\int_{\mathbb R^{n-1}}b_hv^2
-\frac A q\int_{\mathbb R^n_+}(v_+)^q,                         \tag{2}\\
b_h={}&\Delta h-\frac{h_ah_bh_{ab}}{1+|Dh|^2}.
\end{aligned}
\]
Indeed \(H_h\,dS=b_h\,dy'\).

At \(U=U_{1,0}\), the linear graph residual is
\[
R_f(v)=
-\int f_a(U_av_n+U_nv_a)+b\int_{\partial\mathbb R^n_+}\Delta f\,Uv. \tag{3}
\]
There is no first-order direct energy term:
\[
-\int f_aU_aU_n+c_n\int\Delta f\,U^2=0.                       \tag{4}
\]
After integration in \(y_n\), this follows from the pointwise boundary identity
\[
\frac A qU^q-\frac12|D'U|^2+c_n\Delta'(U^2)=0.
\]
Differentiating (4) in bubble parameters shows that \(R_f\) annihilates all translation and dilation kernel functions.

Here is the second-order form, including its sign. Conformally transform to the unit hemisphere, where the bubble becomes the constant
\[
k=2^{-a}.
\]
The linearized equation is \((\Delta_{\mathbb S^n}+n)V=0\). For a boundary spherical harmonic of degree \(L\ge2\), its Dirichlet-to-Neumann eigenvalue is
\[
\mu_L=
\frac{2\Gamma((L+n+1)/2)\Gamma(L/2)}
{\Gamma((L-1)/2)\Gamma((L+n)/2)}>0.                           \tag{5}
\]
For a normal displacement \(\rho\), the first correction has Neumann datum
\[
2c_nk(\Delta_{\mathbb S^{n-1}}+n-1)\rho.
\]
The direct second shape variation is zero: the volume increment and integrated outward mean curvature are odd under reflection across the equator. Eliminating \(V\) therefore gives
\[
-2c_n^2k^2\,\mathcal Q(\rho),\qquad
\mathcal Q(\rho)=
\sum_{L\ge2}\frac{(L-1)^2(L+n-1)^2}{\mu_L}\|\rho_L\|^2.       \tag{6}
\]
The degree-one source vanishes. Degree zero contributes zero because the corresponding Neumann solution has zero boundary value.

The flat and spherical computations agree. A change of first-order base by \(W\) changes the quadratic data by
\[
B\mapsto B+R(W)+\tfrac12\mathscr A(W,W),\qquad
R\mapsto R+\mathscr AW,
\]
so that
\[
B-\tfrac12\langle R,\mathscr A^{-1}R\rangle                  \tag{7}
\]
is unchanged. Here \(\mathscr A=I_0''(U)\) is inverted off its kernel. Kernel components are absorbed by bubble reparametrization.

For a polynomial flat graph \(f\), its spherical normal displacement is
\[
\rho(x')=\frac{2f(x')}{1+|x'|^2}.
\]

## 3. Exact dimensional algebra

Decompose homogeneous graph polynomials into
\[
P_\ell(x')|x'|^{2j},
\]
with \(P_\ell\) harmonic. Under bubble dilation their weights are
\(\lambda^{\ell+2j-1}\). Hence the scale-derivative matrix in each harmonic sector is
\[
M_{\ell,jk}=(\ell-1+j+k)Q_{\ell,jk}.                         \tag{8}
\]

The exact calculations give:

* For \(3\le n\le18\), every finite-integral nongauge block with graph degrees \(d<n/2\) is positive definite.
* At even-dimensional degree \(d=n/2\), the leading logarithmic form is strictly positive on nongauge modes.
* For every \(n\ge19\), there is
  \[
  f=P_2(x')F(|x'|^2),\qquad \deg F\le3,
  \]
  for which the full scale-and-translation shape function has a strict local maximum.

Here is how the finite calculations are certified, rather than inferred numerically.

Set
\[
\alpha=\frac{n+2}{2},\quad
W_m=(m+\alpha)
 \left[\frac{\Gamma((m+1)/2)}{\Gamma((m+n+3)/2)}\right]^2,
\]
and
\[
E_r(X)=\prod_{h=0}^{r-1}[X-(\alpha-1-2h)^2].
\]
For \(n>2r\),
\[
\begin{aligned}
\sum_{m\ge0}W_mE_r((m+\alpha)^2)
=\frac{4^r}{\alpha-r-1}\bigg[
&\frac{\Gamma(r+\tfrac12)\Gamma(\tfrac12)}
 {\Gamma(\alpha-r-\tfrac12)\Gamma(\alpha-\tfrac12)}\\
+&\frac{\Gamma(r+1)}
 {\Gamma(\alpha-r)\Gamma(\alpha)}
\bigg].                                                     \tag{9}
\end{aligned}
\]
This is an elementary telescoping identity. Split \(m=2k+s\), put \(B=(s+1)/2\), and use the difference of
\[
G_k=
\frac{\Gamma(k+B+r)\Gamma(k+B)}
{(\alpha-r-1)\Gamma(k+B+\alpha-r-1)\Gamma(k+B+\alpha-1)}.
\]
The identity needed is
\[
(x+\alpha-r-1)(x+\alpha-1)-x(x+r)
=(\alpha-r-1)(2x+\alpha-1).
\]
Also \(G_k\to0\) precisely under the asserted convergence condition.

Gegenbauer integration converts every required spectral sum into (9). For example, if \(\beta=(n+1)/2\),
\[
\begin{aligned}
&\int_{-1}^1(1-z^2)^\beta(1-z)^{-(r+1)}
 C_m^{(n+2)/2}(z)\,dz\\
&\quad=
\frac{2^{n+1-r}\Gamma(\beta+1)\Gamma(\beta-r)}{\Gamma(n+2)}
(m+n+2-r)_r\frac{(r+1)_m}{m!}.                              \tag{10}
\end{aligned}
\]
Thus there are no truncated infinite sums in the certificates.

The low-dimensional check consists of **142 exact positive leading principal minors**. Signs involving \(\pi\) are bounded using rational alternating-series bounds in Machin’s formula. Ninety independent beta-integral checks verify the moment formulas, including the \(\ell=0,1\) sectors after their genuine conformal gauge modes are removed.

For the logarithmic terms, let \(n=2d\). The homogeneous corrector is
\[
V=r^{1-d}\phi,\qquad
(\Delta_{\mathbb S^{n-1}}-(d-1)^2)\phi=0.
\]
Its boundary source in sector \(\ell+2j=d\) has coefficient proportional to
\[
1-d+\frac{j(4d-2j-3)}{2d-1}.
\]
This is nonzero except for the radial quadratic gauge. Consequently its leading energy is
\[
\log R\int_{\mathbb S^{n-1}_+}
\bigl(|D\phi|^2+(d-1)^2\phi^2\bigr)>0.                       \tag{11}
\]

For the high-dimensional calculation, in dimension \(19\) one may use
\[
F(s)=1-\frac5{12}s+\frac{11}{240}s^2-\frac1{960}s^3.
\]
Exact interval arithmetic isolates a scale critical point in
\[
1.00254797<\lambda^2<1.00254798
\]
and proves strict negativity of both the scale and translation Hessians. Fixed rational witnesses and root intervals similarly certify every \(20\le n\le39\).

For all \(n\ge40\), a degree-four graph suffices. Writing \(q_{ij}=Q_{2,ij}\), \(i,j=0,1\), the exact certificate proves
\[
3q_{00}q_{11}-4q_{01}^2<0,\qquad q_{01}>0.
\]
At the smaller root \(x>0\) of
\[
q_{00}-4q_{01}x+3q_{11}x^2=0,
\]
the scale Hessian is negative. If \(d=n-1\) and
\(t_e=e^TA^2e/\operatorname{tr}(A^2)\in[0,1]\), the translation Hessian has sign
\[
x^2\left[
-(2+8t_e)(2q_{01}-3q_{11}x)
+\left(-2+\frac{32t_e}{d}\right)
 \left(q_{00}+\frac{4q_{01}}{d+4}\right)
\right]<0.                                                  \tag{12}
\]
This proves the required full-parameter strict maximum, not merely scale indefiniteness.

## 4. The local compactness calculation

This is the step that connects the preceding algebra to arbitrary blowing-up solutions.

Choose a flat conformal boundary chart and make a uniformly controlled Möbius normalization so that
\[
h_i(0)=Dh_i(0)=\Delta h_i(0)=0.
\]
This removes the trace of the quadratic graph, not its tracefree part; no umbilicity assumption has been introduced. Modulation can be performed using the center-dependent osculating-sphere family. If its signed curvature is \(\kappa=H/(n-1)\), the adapted bubble center has normal displacement
\[
t=\frac{\kappa\varepsilon^2}
 {1+\sqrt{1-\kappa^2\varepsilon^2}}.
\]
The identity \(\varepsilon^2=2t/\kappa-t^2\) makes its Robin condition exact on the osculating sphere.

Suppose an isolated peak has height \(M_i\), scale
\(\varepsilon_i=M_i^{-1/a}\), bubble convergence, and the sharp bound
\[
u_i(x)\le C M_i^{-1}|x|^{2-n}
\quad(C\varepsilon_i\le |x|\le\rho_0).                       \tag{13}
\]
We prove that, for \(n\le18\), its limiting normalized Green function has nonnegative **compensated** Pohozaev flux.

Choose the cutoff in physical radius before flattening, and put
\(R=\rho/\varepsilon_i\). The cutoff rescaled solution tends strongly to \(U\) in \(D^{1,2}\); Caccioppoli and (13) give
\[
\int_{|y|>L}|Dv_i|^2\le CL^{2-n}.
\]
Its cutoff force \(F_i\) is supported where \(|y|\asymp R\), with bulk density \(O(R^{-n})\), divergence and boundary densities \(O(R^{1-n})\), and
\[
\|F_i\|_{H^*}+\|\partial_{\rm par}F_i\|_{H^*}\le CR^{-a}.     \tag{14}
\]

### The forced Schur expansion

After conformal trivialization of bubble parameters, the unperturbed action is parameter-independent. On the orthogonal complement of its kernel, let
\(\mathscr A=I_0''(U)\), \(E\) be the metric quadratic perturbation, \(e=PEU\), and \(f=PF_i\). The projected implicit-function theorem gives
\[
\begin{aligned}
j={}&I_0(U)+\tfrac12E(U,U)-F_i(U)\\
&-\tfrac12\langle e-f,(\mathscr A+E)^{-1}(e-f)\rangle
+\operatorname{Rem},                                       \tag{15}\\
|\operatorname{Rem}|+|D_{\rm par}\operatorname{Rem}|
&\le C\zeta^\gamma,\qquad \gamma=\min(3,q)>2.
\end{aligned}
\]
Here \(\zeta\) is an upper bound for the residual and its parameter derivatives. This differentiated estimate is legitimate because the parameter dependence has been moved entirely into the quadratic form and forcing; the implicit correction and its parameter derivative are both \(O(\zeta)\).

Set \(D=\lfloor n/2\rfloor\), and expand the normalized graph into homogeneous terms. Define
\[
X_i^2=
\sum_{d<n/2}\varepsilon_i^{2d-2}|h_{i,d}|^2
+\mathbf1_{2\mid n}\,
 \varepsilon_i^{n-2}\log(\rho/\varepsilon_i)|h_{i,n/2}|^2.    \tag{16}
\]
The Taylor remainder contributes squared residual at most
\[
C\varepsilon_i^{n-2}\rho^{\,2D+2-n}.                        \tag{17}
\]
Indeed the degree-\(d\) bulk weight is \(r^{d-n}\), whose squared radial integral is \(\int r^{2d-n-1}\,dr\).

At the borderline, a crude trace-Hölder estimate would lose a logarithmic power. Instead use the explicit corrector in (11): its energy is \(O(\log R)\), and its equation represents the residual as \(\mathscr A V\) plus bounded cutoff terms. This gives the required \(O(\sqrt{\log R})\) dual norm.

The negative graph-only scale derivative in (15) is precisely the positive form (8), together with (11). For a fixed sufficiently small \(\rho\), the remaining terms satisfy
\[
\eta X_i^2+C_\eta(\rho)\varepsilon_i^{n-2}
+O(\rho)X_i^2+o(X_i^2+\varepsilon_i^{n-2}).
\]
Absorption therefore yields
\[
X_i^2\le C(\rho)\varepsilon_i^{n-2}.                         \tag{18}
\]
In particular,
\[
|h_{i,d}|^2\le C\varepsilon_i^{n-2d}\quad(d<n/2),\qquad
|h_{i,n/2}|^2\le\frac C{\log(1/\varepsilon_i)}.               \tag{19}
\]
The limiting graph thus begins in degree \(d_0>n/2\).

### Compensation and the outer terms

The compensation cannot be omitted. Put
\[
P(r,G)=\int_{S_r\cap\Omega}
\left(aGG_r-\frac r2|DG|^2+rG_r^2\right),
\]
\[
\mathcal H(r)=\int_{\mathbb S^{n-2}}h(r\theta)\,d\theta,\qquad
L_h(r)=ab\,r^{-(n-2)}
 \left(\frac{2\mathcal H(r)}r-\mathcal H'(r)\right).           \tag{20}
\]
Bare \(P(r,G)\) can diverge even after (19).

For the first harmonic correction to \(z=r^{2-n}\),
\[
\partial_\nu V=-(n-2)r^{-n}
 \left[h-rh_r+\frac{r^2\Delta h}{2(n-1)}\right],
\]
angular averaging gives the exact identity
\[
P_{\rm lin}'(r)=L_h'(r).                                    \tag{21}
\]
The radius-independent quantity is \(P_{\rm lin}-L_h\).

There is no hidden cutoff constant. With
\(C_\chi=\int\chi' L_h\), the cutoff commutator gives
\[
F_i(Z_0)=-P_{\rm aug}+C_\chi+o(\varepsilon_i^{n-2}),
\qquad P_{\rm aug}=P-L_h.
\]
The localized lateral Noether term is \(+C_\chi\), so it cancels the
\(-C_\chi\) coming from \(-F_i(Z_0)\). The physical regular constant remains.

For clarity, the identities behind this bookkeeping are
\[
\operatorname{div}\!\left[
(x\!\cdot\!Du)Du-\frac{|Du|^2}{2}x+\frac A q u^q x+a\,uDu
\right]=0
\]
and the exact cutoff force
\[
-2D\chi\!\cdot\!Du-u\Delta\chi+A(\chi-\chi^p)u^p,
\qquad (\partial_\nu\chi)u
\]
on the boundary. The nonlinear tail pairs with \(Z_0\) at \(O(R^{-n})\).
The Robin cutoff term cancels in the Green identity. Also
\[
Z_0=a r^{2-n}+O(r^{-n}),
\]
so replacing the kernel by its fundamental tail has the same negligible error. These statements account for physical-cap, flattening, and cutoff terms together.

The inverse kernel off the bubble kernel has, for fixed inner \(x\) and annular \(y\),
\[
|\partial_x^\alpha K(x,y)|\le C_\alpha R^{2-n}.
\]
Thus the inner response to (14) is \(O(R^{2-n})\), not merely \(O(R^{-a})\). Its potential energy is
\[
O(R^{-2})\ (n=3),\quad O(R^{-4}\log R)\ (n=4),\quad
O(R^{-n})\ (n\ge5),
\]
all \(o(R^{2-n})\).

After (19), the remaining normalized outer errors have bounds
\[
C\rho^{2d_0-n},\qquad C\rho^{d_0-n/2},\qquad
C\rho^{d_0-1},\qquad C\rho^{2D+2-n}.                        \tag{22}
\]
They come respectively from \(E^2f^2\), \(Eef\), \(Ee^2\), and the Taylor remainder in (15). All tend to zero.

The Green asymptotics established below give
\(G-z=O(r^{2-n+\tau})\) for some \(\tau>(n-2)/2\). The remaining linear-geometry cross term is
\[
O(\rho^{d_0+\tau+1-n})=o(1).
\]
The scale equation from (15), with (8), now implies
\[
\lim_{r\downarrow0}\bigl(P(r,G)-L_h(r)\bigr)\ge0.             \tag{23}
\]
This argument is scale-uniform. For \(n=3\) there are no retained jets and (17) is \(O(\varepsilon_i\rho)\); for \(n=4\), (11) handles the tracefree quadratic term. Thus no low-dimensional case is missing.

## 5. Selection, simplicity, and exclusion of clusters

Here are the blow-up reductions needed to apply the local calculation.

A maximal bubble-selection argument gives centers \(x_{ij}\), scales \(\varepsilon_{ij}\), standard profiles, large mutual separation in both bubble scales, and
\[
u_i(x)\operatorname{dist}(x,\{x_{ij}\})^a\le C.              \tag{24}
\]
To prove maximality gives (24), point-pick a point violating it by maximizing distance-to-the-artificial-boundary times \(u^{1/a}\). Its rescaled neighborhood has bounded height and radius tending to infinity. Entire-solution classification produces another standard bubble, separated from all previous centers, a contradiction. This argument includes interior and boundary centers and uses no energy bound.

Before a second critical radius of \(r^a\overline u_i(r)\), the sharp estimate (13) holds. One way to see this is to conformally normalize locally to scalar-flat, minimal boundary and use Fermi coordinates. Annular Harnack and Schauder estimates give
\[
w_{tt}\ge a^2w-Cw^p-Crw,\qquad w=r^a\overline u,\quad t=\log r.
\]
Past the first bubble maximum, \(w\) is small and decreasing. Comparison with \(z''=(a-\eta)^2z\) gives
\[
u_i\le C\varepsilon_i^{a-\eta}r^{2-n+\eta}.
\]
Choosing \(p\eta<2\) yields
\[
\int u_i^p\le C\varepsilon_i^a.
\]
The exact scalar-flat Neumann flux identity, together with radial monotonicity, then improves this to (13).

If a second critical radius tends to zero, rescale there and normalize by the peak height. The limit is
\[
h=A_0r^{2-n}+B(y),\qquad A_0>0,
\]
harmonic with Neumann boundary data. The second-critical-radius condition gives \(B(0)=A_0\). But
\[
\lim_{r\downarrow0}P(r,h)
=-\frac{(n-2)^2|\mathbb S^{n-1}|}{4}A_0B(0)<0,
\]
contradicting (23). Thus isolated blow-ups are simple.

If selected centers cluster, rescale their minimum distance. If all rescaled heights stay bounded, classification gives one bubble despite two surviving maxima. Otherwise the sharp estimate and Harnack chains show that all nearby selected heights diverge. Normalize by the larger endpoint height of a closest pair. The harmonic limit has two strictly positive pole coefficients; positivity and comparison with Green functions give a strictly positive regular part at the first pole. The same negative \(AB\) flux is again a contradiction.

Interior clusters have the identical argument using the exact flat interior Pohozaev identity. An interior peak approaching the boundary is excluded by its positive Neumann image contribution after rescaling by its boundary distance.

Consequently there are uniformly finitely many separated, isolated-simple blow-ups. Normalizing by one boundary peak height gives, away from their limiting points,
\[
M_i u_i\longrightarrow G=\sum_j\alpha_jG_{p_j},\qquad
\alpha_j\ge0,
\]
with a positive coefficient at that boundary point. Positive Yamabe type supplies the positive Green functions and excludes an additional homogeneous term.

## 6. Mass and the low-dimensional contradiction

By (19), a boundary pole has graph order \(d_0>n/2\). After Kelvin inversion its boundary is
\[
y_n=F(y'),\qquad F=O(R^{2-d_0}).
\]
The Kelvin Green factor \(w\to1\) is harmonic and has Robin source
\(O(R^{-d_0})\). Exterior barriers
\[
R^{-\tau}(C-y_n/R)
\]
give, for any suitable
\[
\frac{n-2}{2}<\tau<\min(d_0-1,n-2),
\]
\[
w-1=O(R^{-\tau})
\]
with derivative bounds by scaled Robin Schauder estimates. Thus the Green metric \(G^{4/(n-2)}g\) is asymptotically flat. It has scalar curvature zero and minimal boundary.

The compensated flux is exactly the mass flux. To see the required boundary correction explicitly, flatten the Kelvin graph. To first order,
\[
g_{ij}=\delta_{ij}+\frac4{n-2}(w-1)\delta_{ij}
 +F_i\delta_{jn}+F_j\delta_{in}+O(R^{-2\tau}).
\]
The unnormalized boundary mass is
\[
-\frac{4(n-1)}{n-2}\int_{S_R^+}\partial_Rw
+2\int_{\partial S_R^+}\partial_RF+o(1).
\]
The two graph edge contributions have the same sign. Since
\[
\frac{4(n-1)}{n-2}\,b=2,
\]
Kelvin inversion and (20) give
\[
m=-C_n\lim_{r\downarrow0}\bigl(P(r,G)-L_h(r)\bigr),
\qquad C_n>0.                                               \tag{25}
\]
Quadratic errors vanish because \(2\tau>n-2\). By (23), \(m\le0\).

For completeness, no spin hypothesis on \(M\) is needed. First take its orientation cover. The developing holonomy is a finitely generated linear group
\(\Gamma\subset SO^+(n+1,1)\). Its inverse image in
\(\operatorname{Spin}^+(n+1,1)\) is finitely generated and linear. Residual finiteness gives a finite-index subgroup avoiding the central element \(-1\). Its projection lifts to Spin and supplies a finite spin cover of \(M\).

Lift the Green metric and double in a Fermi collar across its minimal boundary. The double is complete, spin, asymptotically flat, and Lipschitz across the seam; its scalar curvature is nonnegative distributionally because the mean-curvature jump is zero. The spin positive-mass theorem gives nonnegative mass, with Euclidean rigidity at zero mass.

Together with (25), equality holds. Rigidity forces one Euclidean end. Therefore there was exactly one boundary pole, no interior pole, and the finite cover has degree one. The doubling reflection is reflection in a Euclidean hyperplane, so the undoubled Green metric is Euclidean half-space. Its smooth conformal compactification is the round hemisphere. Liouville’s theorem extends the conformal identification across the removed point.

This contradicts the excluded hemisphere. Hence, for every fixed admissible metric and every \(3\le n\le18\), boundary maxima are bounded.

## 7. A fixed metric with blow-up for every \(n\ge19\)

Fix the strict-maximum profile \(f\) from Section 3. Let
\[
p_k=2^{-k}e_1,\quad r_k=2^{-k-3},\quad
\mu_k=\tau2^{-k^2},\quad \varepsilon_k=2^{-k^4},
\]
discarding finitely many initial indices. With a fixed cutoff \(\chi\), define
\[
h_k(x')=\mu_k\varepsilon_k^8
 f\!\left(\frac{x'-p_k}{\varepsilon_k}\right)
 \chi\!\left(\frac{x'-p_k}{r_k}\right),\qquad h=\sum_kh_k.
\]
The supports are disjoint, and
\[
\|D^mh_k\|_\infty\le C_m\mu_kr_k^{8-m}.
\]
Thus \(h\) is one fixed smooth compactly supported graph, flat at its accumulation point.

Take \(\tau\) sufficiently small. The trace inequality applied to (2) makes its quadratic form coercive. The projected bubble linearization is uniformly invertible off the \(n\) kernel modes, by the hemisphere spectrum and small quadratic-form perturbation.

At patch \(k\), put \(\delta_k=\mu_k\varepsilon_k^7\). The local graph is
\(\delta_kf\), cut off at \(R_k=r_k/\varepsilon_k\). For degree at most eight,
\[
|Df\,DU|=O(r^{8-n}),\qquad
\int_R^\infty r^{15-n}\,dr<\infty\quad(n>16).
\]
Hence the projected correction is
\[
w_k=-\delta_k\mathscr A^{-1}R_f+o(\delta_k).
\]
The direct cubic boundary error is at most
\[
C\delta_k^3\left(1+\int_1^{R_k}r^{22-n}\,dr\right)
=o(\delta_k^2).
\]
Other patches contribute residual and energy bounded respectively by
\[
C2^{Ck}\varepsilon_k^{(n-2)/2},\qquad
C2^{Ck}\varepsilon_k^{n-2}.
\]
They are \(o(\delta_k)\) and \(o(\delta_k^2)\), since
\[
\frac{\varepsilon_k^{n-16}}{\mu_k^2}\longrightarrow0.
\]
Uniformly on a fixed small parameter neighborhood,
\[
I_h(U_{\lambda,\xi}+w_k)
=I_0(U)-C_n\delta_k^2\mathcal Q_f(\lambda,\xi)
+o(\delta_k^2).
\]
The strict model maximum therefore gives an interior minimum of the reduced action. Parametric implicit-function theory makes it an exact critical point. Only uniform \(C^0\) energy asymptotics are needed here.

Testing against its negative part and using coercivity gives a nonnegative solution; regularity and the maximum principle make it smooth and positive. Rescaled boundary trace convergence to \(U\) yields
\[
\max_{\partial\Omega_h}u_k
\ge c\varepsilon_k^{-a}\longrightarrow\infty.                \tag{26}
\]

Finally compactify infinity with
\[
g=\frac4{(1+|x|^2)^2}\delta.
\]
Because \(h=0\) outside a compact set, the compactification is smooth with smooth boundary. Finite-energy solutions extend across the compactifying boundary point: it has zero \(H^1\)-capacity, followed by local critical-potential iteration and elliptic regularity.

This metric is locally conformally flat. Coercivity gives positive Yamabe type. At \(p_k\), the tracefree Hessian is a nonzero multiple of
\(\mu_k\varepsilon_k^6D^2P_2\), so the boundary is nonumbilic somewhere. Since tracefree second fundamental form is conformally covariant, the manifold cannot be conformally equivalent to the hemisphere. The compactifying conformal factor is bounded above and below near \(p_k\), so (26) remains true for \(g\).

Thus every \(n\ge19\) belongs to \(\mathcal D\), while Sections 4–6 exclude every \(3\le n\le18\). Therefore
\[
\boxed{\mathcal D=\{19,20,21,\ldots\}.}
\]

# agent_2: last reply

The reproducibility failure is fixed. All six required agent_2 scripts were reconstructed without self-copy operations, rerun successfully, and checked byte-for-byte to remain unchanged after execution.

The finite certificates again rigorously verified every dimension \(19\le n\le39\); the translation, gauge, Schur-complement, and flattening identities also passed. The restored files are ready for the consolidated bundle.

# agent_3: last reply

The agent3 proof files and checking scripts are finalized and frozen. No additional gap was identified after the independent audits. The lead is assembling the complete proof and running the consolidated verification bundle.

# agent_4: last reply

All assigned pieces are complete and connected to the team’s proof.

- Exact dimension-threshold and translation certificates pass.
- The Green-metric mass identification and hemisphere rigidity reduction are written, including virtual spin covers and mixed ends.
- Both the high-dimensional construction and finalized low-dimensional Pohozaev bridge have been independently audited.
- All six agent_4 computational suites were rerun successfully; every exact assertion passed.

The lead is assembling the unified proof and sanitized reproducibility bundle.