# Uniform near-balanced cycle estimate and bounded imbalance (r>=3)

Fix r>=3, q=(r-1)/r, K=r/(r-2). All constants below may depend on r
and a fixed bound D on internal degrees. Let a_i=n/r+delta_i with
sum delta_i=0 and max|delta_i|=o(n). Put Q=sum delta_i^2 and d=||delta||.
The choice of Euclidean or max norm only changes constants.

## 1. A uniform complete-partite coefficient estimate

Let A(z)_{ij}=1_{i!=j} z_j and let lambda(z) be its Perron eigenvalue for
positive z. Write phi(t)=log lambda(exp t). Adding a constant to all t_i
adds the same constant to phi. Fix the gauge t_r=0. Near p_i=1/r there
is a unique analytic t=t(p) with gradient phi=p in the first r-1
coordinates. This follows from the positive Hessian computed below.
Set

psi(p)=phi(t(p))-t(p).p,
rho_i(p)=exp(t_i(p))/lambda(exp t(p)).

Let W(n,a) count indexed cyclic proper r-color words with counts a. Then

W(n,a)=[z^a] tr(A(z)^n)
      = n^{-(r-1)/2} b(p) exp(n psi(p)) (1+O_r(1/n)),       (1)

uniformly on a fixed sufficiently small neighborhood of p=(1/r,...,1/r),
where b(p)>0 is analytic.

Here is a self-contained justification of the required uniformity.
Use coefficient Fourier inversion at z=exp(t(p)). By the triangle
inequality, the spectral radius of A(exp(t+i theta)) is at most lambda.
Equality in the Perron triangle inequality forces
exp(i theta_j)=exp(i alpha) h_i/h_j for all i!=j. Since r>=3, choosing a
third index shows all h_i equal, hence all theta_i equal. In the gauge
theta_r=0 this is only theta=0 modulo 2pi. Thus, outside any fixed
neighborhood of zero, there is a uniform strict spectral gap, on a
compact real saddle neighborhood. Near zero the simple Perron branch is
analytic and

phi(t+i theta)-phi(t)-i theta.p
 = -theta^T Sigma(t) theta/2 + O(||theta||^3).

The Hessian Sigma is uniformly positive definite in the chosen gauge.
Integrate on ||theta||<=n^(-2/5); outside this ball the Gaussian bound is
exponentially small. Expand to fourth order inside the ball. The odd
cubic contribution integrates to zero, and the quartic and squared-cubic
errors have relative integral O(1/n); all higher terms are smaller.
All derivative bounds are uniform on the compact saddle neighborhood.
This proves (1), with b the analytic Gaussian determinant prefactor.
The other eigenvalues contribute an exponentially small error, since
A is primitive (its directed cycles have lengths two and three).

At the uniform saddle t=0 the transition matrix is (J-I)/(r-1), whose
nonconstant eigenvalue is -1/(r-1). Summing the geometric occupation
covariances gives, on the zero-sum subspace,

Sigma(0)=(r-2)/r^2 * I.

Therefore the Hessian of psi on that subspace is
-r^2/(r-2)*I. The labelled Hamilton-cycle count is

h(a)=prod_i(a_i!)*W(n,a)/(2n).

Uniform Stirling and (1) show its exponential rate is
f(p)=sum_i p_i log p_i+psi(p), whose Hessian at uniform p is

r I-r^2/(r-2) I = -2K I.

The analytic Gaussian/Stirling prefactors change by O(d/n), and the
uniform relative errors are O(1/n). Thus, for a balanced vector a^0,

log(h(a)/h(a^0))
 = -K Q/n + O_r(d^3/n^2+(1+d)/n).                         (2)

## 2. All cycles versus Hamilton cycles, uniformly

If b_i vertices of part i are omitted, let s=sum b_i. Exact labelling
cancellation gives

binom(a,b) h(a-b)/h(a)
 = n/(n-s) * W(n-s,a-b)/W(n,a) / prod_i b_i!.

For s<=log^2 n, (1) and the homogeneous rate Taylor expansion give

W(n-s,a-b)/W(n,a)
 = prod_i rho_i(p)^{b_i} * (1+O_r((s+1)^2/n)).

The tail is uniformly factorially small, even when d grows with n.
Indeed positivity of coefficients gives

W(n-s,a-b) <= r lambda^{n-s} exp(-t.(a-b)),

whereas (1) bounds W(n,a) below by a constant times
n^{-(r-1)/2}lambda^n exp(-t.a). Hence every omitted-vector term is at most

C n^{(r+1)/2} prod_i rho_i(p)^{b_i}/b_i!.

The rho_i remain bounded on the saddle neighborhood; sum over s>log^2 n
is smaller than every inverse power of n. Summing the local estimate,

c(T_a)/h(a)=exp(sum_i rho_i(p))*(1+O_r(1/n)).              (3)

In particular the extra logarithmic factor in (3) changes by O(d/n)
from balanced p. Thus (2) holds with c(T_a) in place of h(a).
At uniform p, rho_i=1/(r-1), recovering exp(1/q).

## 3. Bounded-degree internal edges

Let J be an internal graph of maximum degree D in ONE part A, with M
edges. For a selected internal path forest P with j edges and p path
components, contraction lowers a_A by j and contributes orientation
weight 2^p. From (1), uniformly for j<=log^2 n,

h(a-j e_A)/h(a)
 = [z_A(p)/n]^j*(1+O_r((j+1)^2/n)),

where z_A(p)=rho_A(p)/p_A is analytic and
z_A(p)=1/q+O_r(d/n).

Let S_j be the sum of 2^p over all selected j-edge path forests. The
explicit uniform forest bound in agent2_endpoint_wedge_lemma.md gives
S_j=2^j binom(M,j)+an error whose sum at z=O(1/n) is O_D(1/n).
Consequently summing the contraction formula gives

h(T_a+J)/h(T_a)=exp(2M z_A(p)/n)*(1+O_{r,D}(1/n)).

The contraction tail is uniform: the Perron coefficient upper bound
above and (a_A)_j >= (a_A/e)^j bound every term by n^C C^j/j!.
Thus j>log^2 n is negligible. For all cycles, the contracted path blocks
must be present, but omitting any of the p specified blocks has relative
probability O(p/n), by the factorial omission calculation. Applying (3)
to the contracted part vector yields the same formula:

log[c(T_a+J)/c(T_a)] = 2M z_A(p)/n+O_{r,D}(1/n).           (4)

Wholly internal cycles and cycles contracting to fewer than three
vertices have at most n^C D^n descriptions and are factorially negligible.

A fixed number of internal edges in other parts changes (4) by O(1/n).
A fixed number of missing cross edges also changes it by O(1/n). To see
the latter, condition on the selected path forest. If a specified
endpoint is in a selected internal path this costs O_D(1/n); otherwise
labels are exchangeable within its contracted part, and a fixed cross
edge occurs in at most n/(a_i a_j)=O(1/n) of the normalized cycles.
The omitted-vertex tail is harmless. A union bound handles finitely many
such edges. This also proves the claim for finite exceptional gadgets.

## 4. The imbalance lemma used in the lower bound

Consider a finite-template phase: one active bounded-degree tree bulk,
fixed finite exceptions/holes, and all other parts internally bounded.
Let G have part deviations delta=o(n). There is an H-free graph G0 in
the SAME phase with balanced part sizes, and its internal edge count
M0 differs from M by O_H(1+d): keep the finite context, alter the number
of copies of one abundant maximum tree, and use a connected subtree of
each required leftover order. This changes only O_H(1+d) bulk vertices.
The remapping argument defining the phase certifies H-freeness.

Combining (2)--(4), and using M=O(n), M-M0=O_H(1+d), gives

log(c(G)/c(G0))
 = -K Q/n + O_H(d^3/n^2+(1+d)/n).                        (5)

If G maximizes cycles, its left side is nonnegative. Since d=o(n),
the cubic term is o(Q/n). Multiplying (5) by n gives

K Q <= o(Q)+O_H(1+d).

But Q is comparable to d^2. Hence d=O_H(1). Thus every cycle-maximizing
finite-template graph in the low-linear-excess regime has bounded
part imbalance. No fixed-delta expansion was applied outside its range.

## Coefficient normalization

The coefficient in (2) is K=r/(r-2), NOT K/2. The weaker negative
constant would also suffice for bounded imbalance, but this value agrees
with the fixed-part contraction expansion and the exact covariance.

## Joint omission/contraction tail (explicit uniform bound)

For completeness, the separate tails in sections 2--3 can be controlled
simultaneously, without applying a near-balanced saddle to a heavily
contracted or heavily omitted vector. Keep the ORIGINAL saddle t(p).
If b_i vertices are omitted and j_i internal path edges are contracted,
positivity and the original denominator saddle lower bound give

 W(n-s-j,a-b-j)/W(n,a) <= C n^C prod_i rho_i(p)^(b_i+j_i).

Exact label cancellation contributes
 prod_i 1/[b_i! (a_i-b_i)_(j_i)].
The total orientation-weighted j_i-edge path forests in the induced
remaining internal graph are at most
 [D(a_i-b_i)]^j_i / j_i!. Since
 (a_i-b_i)_(j_i) >= ((a_i-b_i)/e)^j_i
for every valid j_i, the joint normalized contribution is bounded by

 C n^C prod_i [rho_i^b_i/b_i!] [(D e rho_i)^j_i/j_i!].

The harmless all-cycle normalization n/(n-s-j) is absorbed into n^C.
Requiring selected blocks to be present can only decrease this bound.
Consequently either s>log^2 n or j>log^2 n gives a tail smaller than
every inverse power of n, uniformly in delta=o(n). This proves that
all local saddle substitutions in sections 2--3 are made only in their
valid compact analytic neighborhood.
