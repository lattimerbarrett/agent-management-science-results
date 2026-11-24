import sympy as s
from pathlib import Path
J,n=s.symbols('J n'); d=(n-4)/2
R=(2*J**2-n**2/2-n+1)/(n-1)
Ps=[]
for m in range(3):
 c=s.symbols('c0:'+str(m+1))
 P=sum(c[k]*(J-1)**(2*k) for k in range(m+1))
 N=s.together(P*(J+d)**2-P.subs(J,J+2)*(J-d)**2-2*J*R**m)
 equations=s.Poly(s.expand(N*(n-1)**m),J).all_coeffs()
 sol=s.solve(equations,c)
 P=s.factor(P.subs(sol)); Ps.append(P)
 assert s.simplify(P*(J+d)**2-P.subs(J,J+2)*(J-d)**2-2*J*R**m)==0
 print('P',m,'=',P)

# w_j=8 J*a_j/(J+d)^2, so common factor 4 times telescoping P.
# Ratio cancels common factor.
def S(m,nn):
 total=0
 for j in (0,1):
  a=s.gamma(s.Rational(j+3,2))**2/s.gamma(s.Rational(j+nn-1,2))**2
  total+=a*Ps[m].subs({n:nn,J:s.Rational(2*j+nn+2,2)})
 return s.simplify(total)
for nn in (9,10,24,31,32,33,40):
 A,B,C=[S(m,nn) for m in range(3)]
 rat=s.factor(B*B/(A*C))
 print('n',nn,'ratio exact',rat,'numerical',rat.evalf(16),'ratio > 3/4',s.simplify(rat-s.Rational(3,4)).evalf()>0)

# Translation Hessian: reduce the harmonic-cubic and trace-cubic sectors
# to the same quadratic-sector moments, using termwise beta/norm ratios.
j=s.symbols('j',integer=True,nonnegative=True)
alpha2=(n+2)/2; alpha3=(n+4)/2; alpha1=n/2
I0=lambda alpha,ss:2**(2*alpha-ss)*s.gamma(alpha+s.Rational(1,2)-ss)*s.gamma(alpha+s.Rational(1,2))/s.gamma(2*alpha+1-ss)
h=lambda alpha,jj:s.pi*2**(1-2*alpha)*s.gamma(jj+2*alpha)/(s.gamma(jj+1)*(jj+alpha)*s.gamma(alpha)**2)
# m3 coefficients are I0(alpha3,2)*(j+1)*(j+n+3)/(n+3)
I3=I0(alpha3,2)*(j+1)*(j+n+3)/(n+3)
I2=I0(alpha2,1)
ratio3=s.combsimp((I3/I2)**2*h(alpha2,j+1)/h(alpha3,j))
assert s.simplify(ratio3-(j+1)*(j+n+3))==0
# m1 trace coefficients are 2*I0(alpha1,1), for j>=1.
ratiotr=s.combsimp((2*I0(alpha1,1)/I2)**2*h(alpha2,j-1)/h(alpha1,j))
ratiotr=ratiotr.subs(s.gamma(n/2+s.Rational(1,2)),(n-1)/2*s.gamma(n/2-s.Rational(1,2)))
assert s.simplify(ratiotr-4*j*(j+n)/(n-1)**2)==0
print('Exact termwise harmonic/trace cubic reductions checked symbolically arbitrary n,j.')

# At n=32 the scale-discriminant inequality is genuinely exact, not floating-point.
A32,B32,C32=[S(m,32) for m in range(3)]
assert 4*B32**2-3*A32*C32>0
print('n=32 discriminant positive by exact rational arithmetic.')
# Exact translation-coefficient sign at the smaller n=32 scale critical point.
# Normalize quadratic-sector A to 1; q3 and qtrace follow the termwise reductions.
from math import isqrt
nn=32; dd=nn-1
b32=s.cancel(B32/A32); c32=s.cancel(C32/A32)
q3=((nn-1)*b32-(nn+3))/2
qt=2*(1+b32)/(nn-1)
disc=s.cancel(4*b32*b32-3*c32)
scale=10**40; p,q=s.fraction(disc)
m=isqrt(int(p)*scale**2//int(q))
sqrt_lo=s.Rational(m,scale); sqrt_hi=s.Rational(m+1,scale)
assert sqrt_lo**2<disc<sqrt_hi**2
zlo=(2*b32-sqrt_hi)/(3*c32); zhi=(2*b32-sqrt_lo)/(3*c32)
assert 0<zlo<zhi
for ai2 in (0,1):
 T=2
 Hnorm=s.Rational(8*T,dd*(dd+2)*(dd+4))+s.Rational(16*ai2,(dd+2)**2*(dd+4))
 Lnorm=s.Rational(4*(dd+4)**2*ai2,dd*(dd+2)**2)
 base=s.Rational(4*T+16*ai2,dd*(dd+2))
 slope=s.cancel(q3*Hnorm+qt*Lnorm+b32*base)
 assert slope>0
 assert -base+zhi*slope<0
 print('Certified negative translation Q coefficient for a_i^2=',ai2,':',float(((zlo+zhi)/2)*(-base+((zlo+zhi)/2)*slope)))
print('Full scale+translation local minimum of negative-Q at n=32 certified in exact arithmetic.')

# Universal translation sign reduction (all n>9 where the scale minimum exists).
b=s.symbols('b',positive=True)
q3b=((n-1)*b-(n+3))/2; qtb=2*(1+b)/(n-1)
M0=b+2*q3b/(n+3)
M1=b+4*n*q3b/(3*(n+1)*(n+3))+(n+3)**2*qtb/(6*(n+1))
assert s.simplify(M0-(2*(n+1)*b/(n+3)-1))==0
assert s.factor(M1-2*b+(n-9)/(3*(n-1))*(1+4*b/(n+3)))==0
print('All-n translation negativity identities checked symbolically.')
Path('workspace/agent4_mixed_spectral_exact.py').write_text(Path(__file__).read_text())

translation_proof=r'''# Full finite-dimensional quartic-profile minimum for n>=32

This result concerns the exact quadratic shape functional only. It does NOT prove a nonlinear solution or an infinite-gluing counterexample.

Let d=n−1, P2(x)=x1²−x2², P4(x)=|x|²P2(x) on R^d. Transfer a graph h to the equatorial sphere by stereographic projection and its normal-distance conformal factor. Let Q be the positive quadratic form in the shape-Hessian lemma, omitting the universal positive factor α²/2. Define the sector constants A,B,C by

Q(P2,P2)=A ||P2||²_{L²(S^{d−1})},
Q(P2,P4)=B ||P2||²,
Q(P4,P4)=C ||P2||².

Then A,B,C>0, and agent2_quartic_all_dimensions_proof.md proves 4B²−3AC>0 for every n>=32 using exact gamma/telescoping certificates.

Normalize A=1 by dividing Q by A, and replace B,C accordingly. Let f=−P2+P4. At bubble center ξ and scale λ, its effective graph is f(ξ+λx)/λ, modulo affine functions (which are in the gauge kernel). At ξ=0, writing z=λ²,

Q(f(λ·)/λ)=||P2||²(z−2Bz²+Cz³).

The smaller scale critical point is

z−=(2B−sqrt(4B²−3C))/(3C)=1/(2B+sqrt(4B²−3C))>0.

There Q has negative scale second derivative. We prove its full translation Hessian is also negative definite, so −Q has a strict nondegenerate local minimum.

## Cubic constants in terms of A and B

Let q3 and qt be Q constants per angular L² norm on harmonic cubic graphs H3 and trace cubic graphs |x|²H1. Then, before normalizing A,

q3=((n−1)B−(n+3)A)/2,
qt=2(A+B)/(n−1).

Proof: in the Gegenbauer decomposition, the harmonic-cubic mode j has the same total equatorial degree and DtN multiplier as quadratic mode j+1. Their full summands have ratio (j+1)(j+n+3). For trace cubic mode j>=1 the corresponding quadratic mode is j−1, with ratio 4j(j+n)/(n−1)². The j=0 trace mode is gauge. The quadratic-sector coefficient ratio R_k=2(k+1)(k+n+1)/(n−1)−1 therefore converts both sums to the asserted linear combinations of A and B. These termwise ratios were checked symbolically for arbitrary n,j in agent4_mixed_spectral_exact.py.

## Translation Hessian

Write P2=x^T D x, D=diag(1,−1,0,...), T=tr(D²)=2, and a_i=D_ii. At ξ=0,

∂_{ξ_i}[f(ξ+λx)/λ] ≡ λ²∂_iP4,
∂²_{ξ_i}[f(ξ+λx)/λ] ≡ λ∂²_iP4

modulo affine gauge functions. Decompose

∂_iP4=H3_i+|x|²L_i,
H3_i=2x_iP2−4a_i|x|²x_i/(d+2),
L_i=2(d+4)a_i x_i/(d+2).

On the unit S^{d−1}, with normalized angular averages,

average(H3_i²)=8T/[d(d+2)(d+4)]+16a_i²/[(d+2)²(d+4)],
average(L_i²)=4(d+4)²a_i²/[d(d+2)²].

If S_i is the quadratic matrix of ∂²_iP4, then tr(D S_i)=2T+8a_i². Rotational invariance of the quadratic sector gives the coefficient of ξ_i² in Q, divided by |S^{d−1}|A, as

z²{q3 average(H3_i²)+qt average(L_i²)}+(−z+z²B)(4T+16a_i²)/[d(d+2)],

where q3,qt now are normalized by A as well.

For a_i=0 this equals a positive multiple of z(−1+z M0), where

M0=2(n+1)B/(n+3)−1 < 2B.

For a_i²=1 it similarly equals a positive multiple of z(−1+z M1), where

M1−2B=−(n−9)/(3(n−1))*(1+4B/(n+3)) < 0

for n>9. These simplifications are checked symbolically for arbitrary n in the code. At z=z−, both signs are strictly negative because z−=1/(2B+sqrt(4B²−3C)).

The profile is invariant under each coordinate reflection, so the translation Hessian is diagonal and the mixed translation/scale block vanishes. Thus Q has a strict nondegenerate maximum at (ξ,λ)=(0,sqrt(z−)); equivalently the actual negative shape energy has a strict nondegenerate local minimum.

Combining with the exact all-n>=32 discriminant certificate proves this finite-dimensional proposition for every integer n>=32. A separate exact rational enclosure of the n32 square root certifies the two translation signs as an independent check.

Remaining beyond this proposition: uniform nonlinear reduction on shrinking supports, C² control of its reduced-energy remainder, fixed smooth infinite gluing, all required solution bounds, n7 through n31 constructions, and all n3 through n6 compactness.
'''
Path('workspace/agent4_quartic_translation_proof.md').write_text(translation_proof)
print('Saved workspace/agent4_quartic_translation_proof.md')

inverse_proof=r'''# Uniform projected inverse for a concentrating boundary bubble

This standard analytic lemma is proved here because it is a genuine global ingredient absent from the earlier spectral calculations. It does not give quantitative reduced-energy remainders or a scale critical point.

## Set-up

One may conformally normalize so that R_g>0 and H_g=0, but this is not necessary. Work directly in the given metric, which is useful for Euclidean graph domains. Let

Q(v,w)=∫M(∇v·∇w+c_n R_g v w)+2c_n∫∂M H_g v w, H=H¹(M),
a=n(n−2), p=(n+2)/(n−2).

Then Q is an equivalent Hilbert norm on H. Indeed λ1>0 gives λ1||v||²_L2<=Q(v,v), while the bounded curvature and trace interpolation give Q(v,v)>=(1/2)||∇v||²−C||v||²_L2; combining proves coercivity in H¹. Fix a small Fermi radius r0 uniform over boundary centers ξ. Let χ be a smooth radial cutoff, equal to 1 in radius r0/2 and supported in radius r0. Set

U(z)=(1+|z|²)^{−(n−2)/2},
W_{δ,ξ}(F_ξ(δz))=χ(δz)δ^{−(n−2)/2}U(z).

Let Z0=(n−2)U/2+z·∇U and Zj=∂_jU for j=1,...,n−1, and let K^α_{δ,ξ} be the corresponding cut-off rescalings. Let Kδ be their span and Πδ its Q-orthogonal projection. Define Tδ by

Q(Tδv,φ)=pa∫M Wδ^{p−1}vφ,

and Aδ=Πδ^perp(Id−Tδ)|_{Kδ^perp}.

## Theorem

There are δ0>0 and C<∞, independent of ξ∈∂M and 0<δ<δ0, such that Aδ is invertible and ||Aδ^{-1}||<=C.

## Proof

1. The rescaled Fermi metrics tend in C²_loc to the Euclidean halfspace metric, uniformly in ξ. The cut-off kernel Gram matrix converges to the positive definite matrix ∫_{R^n_+}∇Zα·∇Zβ. Also

||(Id−Tδ)K^αδ||_H→0.

Here are explicit cutoff estimates. The slowest Jacobi mode satisfies |Z|<=C(1+|z|)^{2−n}, |∇Z|<=C(1+|z|)^{1−n}. Hence cutting it off at rescaled radius R has D^{1,2} error <=C R^{−(n−2)/2}; the same bound applies to the cutoff-gradient annulus. For any fixed η<r0/2, the Fermi metric differs from Euclidean by O(η) on the physical η-ball. Testing against an H-unit vector and splitting there gives a geometric error <=Cη+C(δ/η)^{(n−2)/2}. The nonlinear-potential cutoff error is bounded by Hölder, using ||U^{p−1}||_{L^{n/2}(|z|>R)}<=C R^{−2}. The interior lower-order term is <=C||Kδ||_L2, with norms O(δ^{1/2}) for n3, O(δ sqrt|logδ|) for n4, O(δ) for n>=5. The boundary curvature term is <=C||Kδ||_{L²(∂M)}, which is O(sqrt(δ|logδ|)) for n3 and O(sqrtδ) for n>=4, by the trace theorem for the test vector. All constants are uniform in ξ. First let δ→0, then η→0. The Gram convergence follows by the same estimates. This proves the stated kernel residual and controls every physical cutoff error.

2. If the estimate failed, choose δ_i→0, ξ_i, v_i∈K_i^perp with ||v_i||_Q=1 and ||A_i v_i||_Q→0. Write (Id−T_i)v_i=r_i+Σ c_iα K_iα, with r_i→0 in H. Testing against K_iβ and using self-adjointness gives

Σ c_iα Q(K_iα,K_iβ)=Q(v_i,(Id−T_i)K_iβ)=o(1).

The Gram limit makes every c_iα→0. Thus the full residual (Id−T_i)v_i tends to zero in H.

3. Passing weakly in H gives v_i⇀v. For a fixed smooth test φ the potential term tends to zero: outside a fixed small boundary ball the weight W_i^{p−1} tends uniformly to zero; inside the ball Hölder bounds it by C||φ||_{L^{2n/(n−2)}(ball)}, which tends to zero with the ball radius. Therefore Q(v,φ)=0, so v=0.

4. Rescale at (ξ_i,δ_i): V_i(z)=δ_i^{(n−2)/2}v_i(F_{ξ_i}(δ_i z)). Local weak compactness gives V_i⇀V in D^{1,2}(R^n_+) and locally strongly in L². Rescaling the weak equation yields

−ΔV=pa U^{p−1}V, ∂νV=0.

Orthogonality against K_iα passes to ∫∇V·∇Zα=0; tails vanish by Cauchy-Schwarz and the finite Dirichlet norms of Zα.

The halfspace linearized kernel is exactly span{Z0,...,Z_{n−1}}. Indeed, divide V by U and use conformal covariance: the resulting equation on a round hemisphere of radius 1/2 is −Δw=4n w with Neumann boundary. The conformal energy identity puts w in H¹; the missing stereographic boundary point has zero H¹ capacity. Even reflection across the equator identifies this eigenspace with the even degree-1 spherical harmonics, precisely n dimensions. Thus the stated orthogonality forces V=0.

5. It follows that the potential energy vanishes. Inside |z|<R this follows from local strong L² convergence. Outside,

∫_{M\B_{Rδ_i}(ξ_i)}W_i^{p−1}v_i² <= C (∫_{|z|>R}U^{2n/(n−2)})^{2/n},

by Hölder and the uniform Sobolev norm of v_i. This bound tends to zero as R→∞. Hence ∫W_i^{p−1}v_i²→0. Testing the full residual against v_i now gives

1−pa∫W_i^{p−1}v_i²=o(1),

a contradiction.

6. For each fixed δ, Tδ is compact on H, because Wδ is smooth bounded and H¹ embeds compactly into L² on the compact manifold. Thus Aδ is self-adjoint Fredholm of index zero on Kδ^perp. The proved lower bound implies bijectivity, completing the proof.

## Consequence: a small projected nonlinear correction

Let S:H*→H be the Q-Riesz solution map. The cut-off bubble residual

rδ=Πδ^perp[Wδ−S(a Wδ^p)]

tends to zero in H, by exactly the same local-rescaling/tail argument. For the nonlinearity (u_+)^p, the Sobolev/Hölder estimates give uniformly

||N(φ)−N(ψ)||_{H*} <= C (||φ||_H+||ψ||_H)^min(1,p−1) ||φ−ψ||_H

on a small H-ball (with the usual harmless bounded-W factor when p>=2). The uniform inverse and contraction mapping therefore give a unique small φδ∈Kδ^perp, ||φδ||_H<=C||rδ||_H, solving the projected nonlinear equation. This does NOT make the kernel residual vanish. It also supplies no sharp rate or C² reduced-energy expansion.

If a parameter choice kills the kernel residual, the resulting actual solution is nonnegative by testing its equation against its negative part and using positivity of Q; the strong maximum principle makes a nonzero solution strictly positive.

## Explicit limits of this lemma

The physical cutoff radius may also shrink: if ρ_i→0 and δ_i/ρ_i→0, compare the fixed-radius and ρ_i-cutoff bubbles and Jacobi modes. Their H¹ difference is <=C(δ_i/ρ_i)^{(n−2)/2}; the potential difference in L^{n/2} is <=C(δ_i/ρ_i)². Gram matrices and kernel projections therefore differ by o(1), and the inverse survives by operator-norm perturbation. Thus the lemma applies to bubbles supported inside individual shrinking gluing patches.

The estimates are uniform over a C²-compact family of smooth metrics on one fixed compact manifold, provided λ1 is uniformly bounded below by a positive number and uniform boundary collar/Fermi radii exist. If uniform inversion failed, take a C²-convergent subsequence of the metrics and repeat the contradiction proof, using the uniformly coercive Q forms. All cutoff estimates above depend only on these common geometric bounds. In particular, for one fixed final C∞ graph-glued domain, moving centers through infinitely many bumps cause no loss whatsoever: the boundary is compact and smooth, so the needed common constants exist. A family of sufficiently small C³ boundary-graph changes pulled back by smooth collar diffeomorphisms is covered whenever its resulting metrics form such a C²-compact family.

The theorem proves a qualitative global inverse and small projected correction on a fixed positive-Yamabe manifold. It does not control the correction sharply relative to an arbitrarily tiny engineered shape-Hessian well; that requires quantitative weighted estimates. It does not prove nonlinear gluing, n>=7 existence, or low-dimensional compactness.
'''
Path('workspace/agent4_uniform_inverse_proof.md').write_text(inverse_proof)
print('Saved workspace/agent4_uniform_inverse_proof.md')
