# Geometric lemmas established independently (agent 1)

These lemmas do NOT prove the requested sharp compactness/noncompactness theorem.

## 1. Conformal covariance and normalizations
Let a=(n-2)/2 and b=(n-2)/(2(n-1)). If ghat=phi^(4/(n-2))g,
then

L_ghat(v)=phi^(-(n+2)/(n-2)) L_g(phi v),
B_ghat(v)=phi^(-n/(n-2)) B_g(phi v).

Indeed nuhat=phi^(-2/(n-2))nu and
Hhat=phi^(-n/(n-2)) [H phi+2(n-1)/(n-2) nu(phi)],
while
Rhat=phi^(-(n+2)/(n-2)) [R phi-4(n-1)/(n-2) Delta(phi)].
Substitution and the product rule give both identities with the exact constants
in the question. Consequently the solution equation is invariant under u=phi v.
Since a fixed positive smooth phi on a compact manifold has positive minimum
and finite maximum, boundary blow-up is preserved.

The quadratic form
Q_g(v)=int_M(|grad v|^2+c_n R v^2)+b int_boundary H v^2
satisfies Q_ghat(v)=Q_g(phi v), by integration by parts and covariance.
Positivity of the first Robin eigenvalue is therefore conformally invariant:
positivity is equivalently Q_g(v)>=C||v||_L2(g)^2, and the fixed weights in the
conformal change are uniformly comparable.

The trace-free second fundamental form transforms as
IIhat^circ=phi^(2/(n-2)) II^circ.
Thus any nonumbilic boundary point rules out conformal equivalence to the round
hemisphere, whose boundary is totally geodesic.

## 2. Strictly mean-convex flat domains have positive Yamabe type
Let Omega be bounded, smooth, connected, and Euclidean, with H>0. Then R=0 and
Q(v)=int_Omega |grad v|^2+b int_boundary H v^2>=0.
The first Robin eigenvalue is attained by standard compact-resolvent elliptic
spectral theory. If it were zero, its eigenfunction would have zero gradient,
so would be constant. Its boundary term would then force that constant to be
zero, contradicting normalization. Hence lambda_1>0. The same proof works for
H>=0 and H>0 on a nonempty relatively open boundary subset.

A sufficiently small C2 perturbation of the unit sphere remains strictly mean
convex. A perturbation with nonzero trace-free II is therefore automatically an
admissible metric as far as LCF, positivity, and non-hemisphere conditions go.
It does NOT automatically admit any blowing-up solutions.

## 3. Exact hemisphere bubbles
For eps>0 and xi in R^n set U=(eps/(eps^2+|x-xi|^2))^a. Radial differentiation
gives Delta U/U=-n(n-2)eps^2/(eps^2+|x-xi|^2)^2=-n(n-2)U^(4/(n-2)).
On |x|=1, nu=x and H=n-1, so

B U/U=a (eps^2+|xi|^2-1)/(eps^2+1+|xi|^2-2 x.xi).

Thus eps^2+|xi|^2=1 yields exact positive solutions on the ball. Taking eps->0
and xi->boundary gives boundary blow-up, but this example is excluded because
the ball is conformally equivalent to the hemisphere. These identities are
checked for symbolic n by workspace/agent1_checks.py.

## 4. Smooth assembly of polynomial graph perturbations
Fix a polynomial F on R^(n-1) of degree d and a smooth cutoff chi supported in
the unit ball. Let p_k=2^(-k)e_1, rho_k=2^(-k-4),
mu_k=exp(-rho_k^(-2)), and 0<lambda_k<=rho_k. Define

h_k(x)=mu_k lambda_k^d F((x-p_k)/lambda_k) chi((x-p_k)/rho_k).

The supports are pairwise disjoint and avoid 0. For every multi-index beta,
Leibniz's rule, expanded monomial by monomial in F, yields

sup |partial^beta h_k| <= C_beta mu_k rho_k^(d-|beta|).

For a monomial of degree j<=d this follows from lambda^(d-j)<=rho^(d-j),
and differentiating the monomial and cutoff contributes total rho-power
j-|beta|. Terms differentiated more often than their degree vanish. Since
mu_k tends to zero faster than every power of rho_k, h=sum h_k extends smoothly
across 0 with all derivatives zero there. This follows inductively from the
displayed derivative bounds and |p_k|=16 rho_k. Multiplication by an additional
small fixed constant makes all prescribed finite C^m norms small.

The Cayley map
C(x,t)=(2x/D, (|x|^2+t^2-1)/D), D=|x|^2+(t+1)^2,
satisfies |C(x,t)|^2=1-4t/D. It maps t>0 conformally to the unit ball and maps
t=0 to the unit sphere minus one point. A sufficiently small compactly supported
graph t=h(x) therefore gives a smooth bounded-domain perturbation of the ball,
unchanged near the missing compactification point. Small C2 norm preserves
strict mean convexity. If h creates a nonumbilic point, Lemmas 1 and 2 verify
all required background geometric hypotheses.

This argument constructs the background geometry only. It does NOT construct
solutions or prove the existence of a suitable reduced-energy seed.

## 5. Scale inequality for a hypothetical degree-d seed
If a Lyapunov-Schmidt reduction has a local effect of order
mu_k^2 lambda_k^(2d-2) and a fixed-background error O(lambda_k^(n-2)), then the
latter is lower order when lambda_k=mu_k^K and

K(n-2d)>2.

Indeed the ratio is mu_k^(K(n-2d)-2)->0. This choice is possible if n>2d.
This is a scale calculation, not an assertion that the requisite reduction or
seed exists. In particular it cannot by itself prove the endpoint n=18.
