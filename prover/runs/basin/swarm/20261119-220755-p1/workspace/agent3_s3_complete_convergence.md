# Cubic restart convergence: complete stratum reduction (agent 3)

This note uses the already-proved spectral dynamics, polynomial total
variation, negative-neutral weight bound, and virtual-probe inequality.
It records ALL support strata; it does not assume an interior omega point.

Let f_(2k)->f, f_(2k+1)->g, N_k->L>0. Set T to the UNION of supports of
all omega points. Then T is contained in {fg=L}, so |T|<=6. All coordinates
outside T tend zero. Coordinates with |fg|<L decay exponentially; |fg|>L
cannot remain active. The remaining neutral outsiders satisfy fg=+L or fg=-L. Positive-neutral
outsiders are extra roots of fg-L outside T; they too have vanishing weights
by the definition of T. In the five-node stratum the only possible such
extra is c, explicitly retained below as a possible positive guard.
An annihilated coordinate is discarded once and for all.

The omega set is compact and connected, by asymptotic regularity. At every
omega point p, f is its monic cubic OP, and g is the partner OP. Feasibility
is linear in p (normalization and orthogonality of f). Averaging finitely
many omega points, one positive on each member of T, gives a FEASIBLE measure
positive on ALL T, even when no omega point is positive on all T. Its partner
has the same g since fg=L on T. This is used only to establish structure.

## A. Robust extreme-root turning

For exact dual dynamics, if a_k is the smallest Gauss root, a_(k+1) is in the
same spectral gap, the Rayleigh trial gives

 a_(k+2) <= a_(k+1) + S_k(a_(k+1))/S'_k(a_(k+1)),
 S_k(z)=sum q_(k,i) H_k(lambda_i)^2/(lambda_i-z), S_k(a_k)=0.

Consequently

 delta_(k+1) <= c_k delta_k,  c_k>0,

with c_k=S'_k(xi_k)/S'_k(a_(k+1)) for a point xi between the two roots.
The reflected inequality holds for the largest root.

We need the following uniform late-tail version. Suppose the tracked root
stays in one fixed spectral gap, remains uniformly separated from all other
dual roots, and the ratios H_(k+1)(lambda_i)/H_k(lambda_i) tend 1 on the
positive base nodes at the two gap endpoints. All other root factors vary
o(1) and are bounded away from zero there. Thus the ratios of the distances
from the tracked root to either gap endpoint tend 1. The same is automatic
for all other spectral nodes, whose distances stay bounded below. For any
xi between a_k,a_(k+1), all ratios

 (lambda_i-xi)/(lambda_i-a_(k+1)) -> 1

uniformly in i. Hence c_k->1 independently of possibly unbounded q weights.

If strictly contracting dual roots beyond the tracked extreme have to be
removed, factor them D_k. The remaining polynomial is EXACTLY an OP under
q_k D_k^2, by testing original orthogonality with D_k times a lower polynomial.
The two-step Christoffel update acquires a factor
(D_(k+2)/D_(k+1))^2=1+O(rho^k) away from the removed nodes. At a removed node,
its contribution to the Rayleigh numerator/denominator is O(rho^k), by
q_k H_k^2=p_k f_k^2/N_k^2 and separation of the tracked gap from that node.
The denominator has a uniform positive lower bound relative to the norm.
Thus the same argument yields

 delta_(k+1) <= c_k delta_k+O(rho^k), c_k->1,                       (A1)

or its reflection for the largest root. The detailed positive-measure
perturbation argument is the simpler, non-infinitesimal version of
agent2_strict_left_deflation.md.

A bounded scalar sequence satisfying (A1) converges. Choose rho<eta<1 and
c_k>=eta eventually. For sufficiently large D, delta_k<=-D rho^k implies
 delta_(k+1)<=-D rho^(k+1), so this negative cone is forward invariant. Either
the cone is entered and every subsequent increment is negative, or all late
negative increments are summable. In either case boundedness gives convergence.
The reflected assertion holds for a largest root.

## B. At most four omega-support nodes

A positive-norm cubic requires |T|>=4. If |T|=4, normalization plus cubic
orthogonality uniquely determine p: its entries are proportional to
1/[P_T'(lambda_i) f(lambda_i)], with the positive normalization fixed.
Hence the omega set is a singleton, and the even residual directions converge.

## C. Six omega-support nodes

Write P6=prod_T(x-lambda_i), lambda_1<...<lambda_6. Since fg-L is monic
of degree 6, fg=L+P6. Both f and g have three simple real roots. Their product
has no roots where P6>=0. Since P6 has a unique critical minimum in
each negative lobe, P6+L has at most two roots COUNTING MULTIPLICITY in each
such lobe; all six product roots are real, so there are exactly two in each
lobe (lambda_1,lambda_2), (lambda_3,lambda_4), (lambda_5,lambda_6).
Each OP has at most one zero in any spectral-node gap: two roots in an empty
gap contradict orthogonality against the OP divided by those factors.
Thus EACH of f,g has one zero in EACH of the three negative lobes.
Their signs on T are therefore (-,+,+,-,-,+).

Every feasible critical weight vector has the exact representation

 p_i=L H(lambda_i)/[P6'(lambda_i) f(lambda_i)],
 H(x)=(x-alpha)(x-beta),
 alpha in [lambda_2,lambda_3], beta in [lambda_4,lambda_5].

Conversely every such pair gives a feasible critical vector (normalization
follows by leading-coefficient interpolation of H*g). Thus the critical
polytope is a quadrilateral parametrized by this rectangle, with FOUR faces
alpha=lambda_2, alpha=lambda_3, beta=lambda_4, beta=lambda_5. The two slow
roots are uniformly separated by lambda_4-lambda_3>0.

The eventual actual dual polynomial has one root near each outsider and two
slow roots in these same fixed gaps. This follows from exact dual
interpolation H_k(lambda_i)=d_i p_(k,i) f_k(lambda_i)/N_k and positive
base-node product ratios tending 1. The slow roots are uniformly separated
from every outsider root and from one another.

For a negative-neutral outsider mu, P6(mu)=-2L. Let ell_i(mu) be its degree-5
Lagrange interpolation coefficients on T. The previously-proved monomial

 log p_mu+sum_i ell_i(mu) log p_i

is eventually increasing. At an omega point it tends -infinity if every
vanishing base coordinate has nonnegative ell_i. Hence omega must lie in
at least one face whose ell_i<0. Direct signs give:

 mu in (lambda_1,lambda_2): faces {3,5}, i.e.
       alpha=lambda_3 OR beta=lambda_5;                     (L)
 mu in (lambda_3,lambda_4): faces {2,5}, i.e.
       alpha=lambda_2 OR beta=lambda_5;                     (C)
 mu in (lambda_5,lambda_6): faces {2,4}, i.e.
       alpha=lambda_2 OR beta=lambda_4.                     (R)

These are the only possible mu intervals because P6(mu)<0. Let a category
be present if an active outsider lies in it.

* L and R together restrict omega to two isolated opposite rectangle
  vertices. Connectedness makes omega a singleton.
* L and C restrict omega to the single edge beta=lambda_5.
* C and R restrict omega to the single edge alpha=lambda_2.
* Only L present: beta is the GLOBAL LARGEST noncontracting dual root;
  all negative outsiders lie below alpha. Part A (deflating exponentially
  contracting roots beyond beta) gives convergence of beta. The L-star then
  makes omega either a point, or a subset of beta=lambda_5.
* Only R: similarly alpha converges, giving a point or alpha=lambda_2.
* Only C: alpha and beta are both global noncontracting extremes, and both
  converge by A.
* No negative outsiders: both slow roots converge after strict deflation.

In every non-singleton case omega would be contained in one FACE, so its
support UNION would omit one member of T. This contradicts |T|=6. Therefore
this stratum cannot contain a nonconvergent even subsequence.

## D. Five omega-support nodes

Write P=P5, so fg=L+P(x)(x-c) with a real c. Feasible critical weights have

 p_i=L(lambda_i-theta)/[P'(lambda_i) f(lambda_i)]

for theta in a single closed gap [a,b] of T. A non-singleton connected omega
set contains an interior point of this gap, hence an all-five-positive
omega point.

The cubic Gaussian quadrature of this positive measure has Stieltjes
numerator (x-c)(x-theta): indeed

 sum_i p_i/(z-lambda_i)=(z-theta)g(z)/P(z),
 (z-theta)g/P - (z-theta)(z-c)/f = L(z-theta)/(P f)=O(z^-7).

The first six moments agree, so the positive three-node Gaussian measure
at the f roots has numerator (z-c)(z-theta). Thus its two numerator roots
strictly interlace f; the same holds for g. Consequently c lies strictly
OUTSIDE [a,b]: otherwise take the feasible theta=c, including endpoints
where there are still four positive spectral weights. Its positive cubic
Gaussian measure would have a double numerator root, impossible by strict
interlacing. Reflect the spectrum if necessary, and assume c<a.
Then, for every theta in [a,b], both f and g have root placement

 zeta_1<c<zeta_2<a<=theta<=b<zeta_3.

In particular f(c),g(c)>0 and f,g<0 on [a,b]. Since d_a f(a)<0 from positive
endpoint weights, d_a>0, so a has odd index in T. The first gap is impossible
because the two OP roots below a would be below the smallest spectral node.
Hence necessarily a=lambda_3, b=lambda_4, d_a>0,d_b<0.

If active negative-neutral outsiders occur on opposite sides of c, the
five-node TWO-outsider monomial of agent2_s3_logmoment.md has positive
coefficients on both outsider logarithms. Along an all-five-positive omega
subsequence its value tends -infinity, contradicting eventual increase.
Thus all active negative-neutral outsiders are on the SAME side of c.

If there are no negative outsiders, or all lie below c, theta is the global
largest noncontracting dual root (a possible positive-neutral outsider at
c also lies below it). Part A gives convergence of theta, contradiction.

The only remaining case has all negative-neutral outsiders z>c. The virtual
probe lemma, including strict-left deflation and the degenerate c case,
proves liminf I_k/t_k>=0; see agent3_virtual_root_lemma.md,
agent2_strict_left_deflation.md, agent4_virtual_probe_degenerate.md.
The exact single-negative corrected log-weight argument in
agent3_single_negative_edge_closure.md then forces theta to one endpoint,
again contradiction to a non-singleton omega set.

Thus ALL s=3 nonterminating orbits have convergent even normalized residual
DIRECTIONS. Indeed convergent weights on T and vanishing outsiders give
convergent magnitudes; on T, f_k(lambda_i)f_(k+1)(lambda_i)>0 eventually,
so every even-coordinate sign is eventually fixed. Repeated eigenspaces
were combined at the start, and their original residual directions are
fixed under polynomial multiplication. Euclidean convergence follows.
