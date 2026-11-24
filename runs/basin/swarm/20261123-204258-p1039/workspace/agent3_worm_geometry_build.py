from pathlib import Path
import mpmath as mp
import sympy as s

note=r'''# An explicit smooth pseudoconvex worm compact with no Stein neighborhood basis

This note proves geometry only. It does **not** claim that the complement is non-Oka.

## 1. The defining function

Put
\[
\chi(s)=\begin{cases}
0,&s\leq0,\\
\displaystyle\int_0^s(s-u)e^{-1/u}\,du,&s>0,
\end{cases}
\qquad
\eta(t)=\chi(-t)+\chi(t-2\pi).
\]
The standard flat function $e^{-1/s}$, extended by zero for $s\leq0$, is smooth. Thus $\chi$ is smooth, convex, flat at zero, strictly increasing for $s>0$, and unbounded. For instance, for $s\geq1$,
\[
\chi(s)\geq \tfrac12e^{-1}(s-1)^2.
\]
Consequently $\eta$ is smooth and convex, vanishes exactly on $[0,2\pi]$, and tends to infinity at both ends. There is a unique $a>0$ with $\chi(a)=1$, and
\[
\{t:\eta(t)<1\}=(-a,2\pi+a).
\]
On $\mathbb C\times\mathbb C^*$ define $t=\log|w|^2$ and
\[
\rho(z,w)=|z-e^{it}|^2-1+\eta(t)
=|z|^2-ze^{-it}-\bar z e^{it}+\eta(t).
\]
Let $\Omega=\{\rho<0\}$ and $K=\overline\Omega$.

## 2. Membership in the class $\mathcal K_2$

Every point of $\Omega$ satisfies
\[
e^{-a/2}<|w|<e^{\pi+a/2},\qquad |z|<2.
\]
Thus the set is bounded and stays away from $w=0$. It is nonempty, since $(z,w)=(1,1)$ has $\rho=-1$. Its base in the $w$ variable is the connected annulus displayed above. Every fiber is the nonempty disc
\[
|z-e^{i\log|w|^2}|<\sqrt{1-\eta(\log|w|^2)}.
\]
Fiberwise recentering and rescaling gives a homeomorphism with the product of this base annulus and the unit disc. In particular, $\Omega$ is connected.

Writing $u=ze^{-it}=x+iy$, direct differentiation gives
\[
\rho_z=\bar z-e^{-it},\qquad
\rho_w=\frac{\eta'(t)-2y}{w}.
\]
If $\rho_z=0$ on the boundary, then $z=e^{it}$ and $\eta(t)=1$. At either such level $\eta'(t)\ne0$, so $\rho_w\ne0$. Hence $d\rho\ne0$ everywhere on $\{\rho=0\}$. All points of this regular zero set are boundary points of $\{\rho<0\}$, so $K=\{\rho\leq0\}$. The preceding compact bounds and regularity prove $K\in\mathcal K_2$.

## 3. Oriented Levi pseudoconvexity

The complex Hessian is
\[
\rho_{z\bar z}=1,\qquad
\rho_{z\bar w}=\frac{i e^{-it}}{\bar w},\qquad
\rho_{w\bar z}=\frac{-i e^{it}}{w},\qquad
\rho_{w\bar w}=\frac{\eta''(t)+2x}{|w|^2}.
\]
The nonzero vector $T=(\rho_w,-\rho_z)$ spans the complex tangent line. Put $d=\eta'-2y$. On the boundary,
\[
x^2+y^2-2x+\eta=0,
\qquad |\rho_z|^2=(x-1)^2+y^2=1-\eta.
\]
A direct calculation gives
\[
\begin{aligned}
|w|^2\mathcal L_\rho(T)
&=d^2+2dy+(\eta''+2x)((x-1)^2+y^2)\\
&=(\eta'-y)^2+(x-\eta)^2
  +\eta(1-\eta)+\eta''(1-\eta)\geq0.
\end{aligned}
\]
Indeed $0\leq\eta\leq1$ on the boundary and $\eta''\geq0$. Thus the boundary is pseudoconvex with precisely the orientation in the problem. The polynomial identity is checked in `agent2_worm_levi.py` and independently in `agent3_worm_identity_check.py`.

## 4. A fixed exterior point belongs to every Stein neighborhood

For $c\in[0,1]$ consider the holomorphic annulus
\[
A_c=\{(c,w):1\leq|w|\leq e^\pi\}.
\]
The initial annulus $A_0$ lies in $K$: its logarithmic radii have $t\in[0,2\pi]$, so $\eta=0$ and $\rho(0,w)=0$. The two boundary circles of every $A_c$ lie in $K$, since at $t=0$ and $t=2\pi$,
\[
\rho(c,w)=c^2-2c\leq0.
\]
However,
\[
p=(1,e^{\pi/2})\in A_1,\qquad \rho(p)=3>0.
\]

Let $U$ be any Stein open neighborhood of $K$, and choose a continuous plurisubharmonic exhaustion $\Phi$ of $U$. Put $M=\max_K\Phi$. The set
\[
J=\{c\in[0,1]:A_c\subset U\}
\]
is relatively open and contains zero. Whenever $c\in J$, the subharmonic maximum principle on the annulus gives $\Phi\leq M$ on $A_c$, because its boundary lies in $K$. Hence all such annuli lie in the fixed compact subset $\{\Phi\leq M\}\Subset U$. If $c_j\in J$ tends to $c$, this compact containment implies $A_c\subset U$, so $J$ is also relatively closed. Connectedness of $[0,1]$ gives $J=[0,1]$. In particular $p\in U$.

Thus every Stein neighborhood of $K$ contains the fixed point $p\notin K$. Taking the neighborhood $\mathbb C^2\setminus\{p\}$ shows that $K$ has no Stein neighborhood basis.

## 5. The same point belongs to the rational hull: a direct argument-principle proof

Let $P$ be a polynomial nonvanishing on $K$. For every $c\in[0,1]$, the polynomial $w\mapsto P(c,w)$ is nonzero on the two boundary circles of the annulus $1\leq|w|\leq e^\pi$. Its number of zeros in the annulus, counted with multiplicity, is the difference of its two boundary winding numbers. This integer is constant in $c$, since neither boundary circle acquires a zero. It is zero at $c=0$, as $A_0\subset K$. Therefore it is zero for all $c$, and in particular $P(p)\ne0$.

Equivalently, every polynomial vanishing at $p$ has a zero on $K$. This is exactly $p\in h_r(K)$, the rational hull of $K$. Hence $K$ is not rationally convex.

## Scope

The note establishes an explicit $K\in\mathcal K_2$ with pseudoconvex boundary and no Stein neighborhood basis, together with a specified exterior rational-hull point. It does not establish any obstruction to the Oka property of $\mathbb C^2\setminus K$. Such an obstruction remains a separate missing theorem in the team's work.
'''
Path('workspace/agent3_worm_geometry.md').write_text(note)
# Independent algebraic checks of the boundary values used in Sections 2 and 4.
c=s.symbols('c',real=True)
assert s.expand((c-1)**2-1-(c*c-2*c))==0
assert (1-(-1))**2-1==3
x,y,eta,e1,e2=s.symbols('x y eta e1 e2',real=True)
d=e1-2*y
numerator=d*d+2*d*y+(e2+2*x)*((x-1)**2+y*y)
positive=(e1-y)**2+(x-eta)**2+eta*(1-eta)+e2*(1-eta)
assert s.rem(s.Poly(s.expand(numerator-positive),x),s.Poly(x*x+y*y-2*x+eta,x)).as_expr()==0
# Numerical illustration only; existence/uniqueness and bounds above are analytic.
mp.mp.dps=35
def chi(v):
    if v<=0:return mp.mpf(0)
    return mp.quad(lambda u:(v-u)*mp.exp(-1/u),[0,v])
a=mp.findroot(lambda v:chi(v)-1,(2,4))
assert abs(chi(a)-1)<mp.mpf('1e-30')
print('Worm geometry note saved; boundary and Levi identities checked.')
print('Illustrative a with chi(a)=1:',a)
print('w radius bounds:',mp.exp(-a/2),mp.exp(mp.pi+a/2))
