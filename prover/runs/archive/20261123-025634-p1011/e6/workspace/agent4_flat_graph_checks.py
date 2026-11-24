from pathlib import Path
proof=r'''# Exact flat-graph energy/residual lemma

**Scope:** this is an analytic estimate for the local graph perturbation, not
an existence theorem or the missing n=18 construction.

Put m=n-1, c=(n-2)/(4(n-1)), U(x,t)=(1+|x|^2+t^2)^(-(n-2)/2).
Let h be smooth and compactly supported in R^m and Ω_h={t>h(x)}. Assume, for
j=0,1,2, |D^j h(x)|<=C0 a(1+r)^(d-j), on its support, and that
 a(1+r)^(d-1)<=b there, where r=|x|, a>0, b>0. Norms are Euclidean.
Assume n>2d. Constants below depend only on n,d,C0.

Let
 J_Ω(v)=1/2 int_Ω |Dv|^2+c int_boundaryΩ H v^2
           -(n-2)^2/2 int_Ω v^(2n/(n-2)).
Then
 |J_Ωh(U)-J_Ω0(U)| <= C b a^2.
Let T_h(x) be the boundary residual density, so J'_Ωh(U)[v]=
 int_Rm T_h(x) v(x,h(x))dx. Then
 T_h=S_h+E_h,
 S_h=(n-2)(h-x.Dh)(1+r^2)^(-n/2)
          +2c Delta h (1+r^2)^(-(n-2)/2),
 |E_h(x)|<=C b^2 a(1+r)^(d-n),
 ||T_h-S_h||_Lq <= C b^2 a, q=2(n-1)/n.
Consequently the residual norm in the dual of homogeneous D^{1,2}(Ω_h) is
O(a), uniformly when b is sufficiently small, by the trace inequality on
uniformly Lipschitz graph domains.

## Proof: exact geometry

The outward unit normal is (Dh,-1)/sqrt(1+|Dh|^2). Direct differentiation gives
 H dS=K_h dx,
 K_h=Delta h-(Dh)^T D^2h Dh/(1+|Dh|^2).
Write V(x,t)=U(x,t)^2 and
 e(x,t)=(n-2)^2/2*(r^2+t^2-1)/(1+r^2+t^2)^n.
The difference of the volume integrals is an integral from0 to h, so exactly
 J_Ωh(U)-J_Ω0(U)=-int_Rm int_0^h e(x,t)dt dx+c int_Rm K_h V(x,h)dx.
The exact radial identity c Delta_x V(x,0)=e(x,0) shows its linear part is0,
by integration by parts (h is compactly supported). The functions e,V are even
in t and K_h is odd in h; in particular its second variation is identically0.
More quantitatively, differentiating with respect to t^2 gives, for all t,
 |e(x,t)-e(x,0)|<=C t^2(1+r)^(-2n),
 |V(x,t)-V(x,0)|<=C t^2(1+r)^(-2n+2),
 0<V(x,t)<=(1+r^2)^(-(n-2)).
Subtracting the zero linear part therefore bounds the absolute energy
difference by C times the integral of
 |h|^3(1+r)^(-2n)
 +|D^2h||h|^2(1+r)^(-2n+2)
 +|Dh|^2|D^2h|(1+r)^(-2n+4).
Each term is <=C a^3(1+r)^(3d-2n), and hence
 <=C b a^2(1+r)^(2d-2n+1).
The radial integral is omega_(n-2)*B(n-1,n-2d), finite exactly when n>2d.
This proves the energy bound.

Since U is an exact interior solution, integration by parts yields the exact
boundary residual density
 T_h=(n-2)(h-x.Dh)(1+r^2+h^2)^(-n/2)
       +2c K_h(1+r^2+h^2)^(-(n-2)/2).
The mean-value theorem in h^2 and the expression for K_h bound T_h-S_h by
 C[(|h|+r|Dh|)|h|^2(1+r)^(-n-2)
   +|D^2h||h|^2(1+r)^(-n)
   +|Dh|^2|D^2h|(1+r)^(-n+2)]
 <=C a^3(1+r)^(3d-n-2)<=C b^2 a(1+r)^(d-n).
The envelope (1+r)^(d-n) is in Lq(R^(n-1)) iff
 (n-d)q>n-1, equivalently n>2d. Its q-th power integral is the finite beta
integral B(n-1,(n-d)q-(n-1)). This proves the residual estimate.

## Polynomial-core consequence

Take a fixed polynomial P of degree<=d, smooth cutoff chi supported |x|<=2
and identically1 on |x|<=1, and h_R=a P(x)chi(x/R), R->infinity.
Then the derivative hypotheses hold uniformly, with b=C a(1+2R)^(d-1).
If b->0, then J_ΩhR(U)=J_Ω0(U)+o(a^2) and T_hR/a converges in Lq to S_P,
by dominated convergence and the displayed envelope. In physical parameters
h_phys=mu lambda^d P(x/lambda)chi(x/rho), one has
 a=mu lambda^(d-1), R=rho/lambda, b=O(mu rho^(d-1)).
Thus for n>2d the desired local residual and direct-action estimates hold
without any formal Taylor truncation of a divergent integral.

To obtain reduced energy -1/2 a^2 Q(z,z), one must additionally identify the
rescaled linear correction and prove other-bump/global errors are o(a) in
residual and o(a^2) in energy. The present lemma does NOT silently assert
these additional matching estimates.
'''
if not Path('workspace/agent4_flat_graph_estimates.md').exists():
 Path('workspace/agent4_flat_graph_estimates.md').write_text(proof)
# Exact, dimension-symbolic identities used above.
import sympy as s
n,r2,t=s.symbols('n r2 t',positive=True)
c=(n-2)/(4*(n-1));V=(1+r2+t*t)**(-(n-2))
e=(n-2)**2/2*(r2+t*t-1)/(1+r2+t*t)**n
lapV0=4*r2*s.diff(V.subs(t,0),r2,2)+2*(n-1)*s.diff(V.subs(t,0),r2)
assert s.simplify(c*lapV0-e.subs(t,0))==0
assert s.simplify(e.subs(t,-t)-e)==0
assert s.simplify(V.subs(t,-t)-V)==0
x,y=s.symbols('x y',real=True);h=s.Function('h',real=True)(x,y)
g=s.Matrix([s.diff(h,x),s.diff(h,y)]);D2=s.hessian(h,(x,y));w=s.sqrt(1+g.dot(g))
H=s.diff(g[0]/w,x)+s.diff(g[1]/w,y)
K=s.trace(D2)-(g.T*D2*g)[0]/(1+g.dot(g))
assert s.simplify(H*w-K)==0
U=(1+x*x+y*y+t*t)**(-(n-2)/2)
normalder=(g[0]*s.diff(U,x)+g[1]*s.diff(U,y)-s.diff(U,t))/w
actual=s.simplify((normalder+2*c*H*U).subs(t,h)*w)
expected=(n-2)*(h-x*g[0]-y*g[1])*(1+x*x+y*y+h*h)**(-n/2)+2*c*K*(1+x*x+y*y+h*h)**(-(n-2)/2)
assert s.simplify(actual-expected)==0
d=s.symbols('d');q=2*(n-1)/n
assert s.simplify((n-d)*q-(n-1)-(n-1)*(n-2*d)/n)==0
print('PASS exact graph curvature density, first-action cancellation, parity, residual, integrability exponent')
Path('workspace/agent4_flat_graph_checks.py').write_text(Path(__file__).read_text())
