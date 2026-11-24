# Conditional isolated-simple boundary-bubble estimates

These estimates assume (rather than prove) an isolated-simple bubble, its standard
pointwise/gradient decay, valid modulation orthogonality, and existence of linear
Jacobi profiles with the indicated weighted tails. They are not a compactness theorem.

Let eps = M^(-2/(n-2)), R=r/eps, d=floor(n/2), and
F(eps*y)/eps = sum_{k=2}^d a_k F_k(y) + remainder,
where a_k includes eps^(k-1), and the F_k have bounded normalized coefficients.
Remove the constant/linear/quadratic radial conformal graph gauges. Set
eta^2 = sum_{k<n/2}|a_k|^2 + 1_{n even}|a_d|^2 log R.

1. Linear boundary source.
The degree-k Robin source is bounded by C(1+|y|)^(k-n).
For k<n/2 it belongs uniformly to the trace dual L^(2(n-1)/n), hence to (D^1,2)*.
For k=n/2, its H^(-1/2) norm squared is O(log R): decompose into dyadic shells.
The same-shell squared norm is O(1), while shell separation h has interaction
O(2^(-h(n-2)/2)) from the kernel |x-z|^(2-n). Summing gives O(log R).
Thus the total jet-source dual norm is O(eta).

2. Taylor remainder.
F_rem=O(|x|^(d+1)) produces source
C eps^d(1+|y|)^(d+1-n), up to R. Its trace-dual Lq norm is at most
C eps^d R^(d+1-n/2) = C eps^((n-2)/2) r^theta,
where theta=d+1-n/2 is 1 or 1/2.

3. Conditional projected inverse estimate.
Assume v<=C(1+s)^(2-n), |grad v|<=C(1+s)^(1-n), and local v->U.
Then cutoff(v-U)->0 strongly in critical Lq by dominated convergence.
The cutoff-annulus residual has D* norm O(R^(-(n-2)/2)).
On the complement of the n bubble Jacobi modes, the flat Jacobi inverse is bounded
by its hemisphere spectral decomposition. The flattened graph form is an O(r)
operator perturbation: |Df_eps|<=C eps(1+s)<=Cr, and its Robin curvature term
is controlled by the trace Hardy inequality. Choose r small to retain invertibility.
The nonlinear residual is o(||w||_D), by strong critical-Lq convergence.
Absorption gives
||w||_D <= C[eta + eps^((n-2)/2) r^(-(n-2)/2)].

4. Regular outer matching and source cross.
Suppose Jacobi profiles satisfy psi_k=O((1+s)^(k+1-n)), with corresponding
first derivative bounds. On the outer sphere R, a_k psi_k(R)=O_r(eps^(n-2));
the same holds for v and U by simple decay. Solve a regular mixed harmonic
extension h of the mismatch, with homogeneous Robin data on the graph bottom.
For small r the mixed problem has a maximum principle (Dirichlet Poincare
absorbs the bounded physical Robin coefficient), giving |h|<=C_r eps^(n-2).
This uses no expansion G=|x|^(2-n)+A and permits intermediate geometric singularities.

Then, directly,
|<a_k S_k,h>| <= C_r |a_k| eps^(n-2) R^(k-1)
 = C_r |a_k| eps^((n-2)/2) eps^(n/2-k).
For k<n/2 the extra eps power tends to zero. For k=n/2 the eta normalization
has sqrt(log R), so this cross is also o_r(eta eps^((n-2)/2)).
Thus the total cross is o_r(eta^2+eps^(n-2)).
The bulk-potential cross is smaller, since V=O(s^-4) and
integral V psi_k scales as integral_1^R s^(k-4) ds.
Gradient cross terms reduce by integration by parts to these terms and an outer
sphere term bounded by the same source-cross estimate.

What is NOT established here:
- existence and uniform weighted estimates for every required Jacobi profile;
- the full second-order localized Pohozaev identity and invariant mass extraction;
- isolated/simple blowup or exclusion of clusters;
- a complete compactness theorem.
